package com.company.erp.service;

import com.company.erp.dto.PlanningStudioDTOs;
import com.company.erp.modules.catalog.model.ProductType;
import com.company.erp.modules.catalog.model.RecipeBOM;
import com.company.erp.modules.dashboard.model.OrderSnapshot;
import com.company.erp.modules.inventory.model.InventoryBalance;
import com.company.erp.modules.planning.model.OrderMaterialReserve;
import com.company.erp.modules.planning.model.ProductionBaseline;
import com.company.erp.repository.InventoryBalanceRepository;
import com.company.erp.modules.planning.model.WorkerTeam;
import com.company.erp.repository.*;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.*;
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class PlanningService {

    private final OrderSnapshotRepository orderRepo;
    private final RecipeBOMRepository recipeRepo;
    private final WorkerTeamRepository teamRepo;
    private final OrderMaterialReserveRepository reserveRepo;
    private final ProductionBaselineRepository productionBaseline;
    private final InventoryBalanceRepository inventoryRepo;
    private final ProductTypeRepository productTypeRepo;
    private final MaterialRepository materialRepo;


    public void lockMaterialForOrder(String orderId)
    {
         OrderSnapshot order = orderRepo.findById(orderId).orElseThrow();
         List<RecipeBOM> recipes = recipeRepo.findByProductType(order.getProductType());

         for(RecipeBOM recipe : recipes){
             Double totalNeeded = order.getQuantity()*recipe.getQuantityPerUnit();
             System.out.println(totalNeeded);
             OrderMaterialReserve reserve = new OrderMaterialReserve();
             reserve.setOrderSnapshot(order);
             reserve.setMaterial(recipe.getMaterial());
             reserve.setLockedQuantity(totalNeeded);
             reserveRepo.save(reserve);

         }

    }
    public void calculateProductionTimeline (String orderId){
        OrderSnapshot order = orderRepo.findById(orderId).orElseThrow();
        ProductionBaseline baseline= productionBaseline.findByProductType(order.getProductType());
        double designDays = (order.getDesignDays() !=null)? order.getDesignDays() : 0.0;
        double sourcingDays = (order.getSourcingDays() != null)? order.getSourcingDays() : 0.0;
        double sewingDailyRate = baseline.getDailyTargetPieces();
        double cuttingDailyRate = sewingDailyRate*1.30;
        double sewingDays = (double)order.getQuantity()/sewingDailyRate;
        double cuttingDays = (double)order.getQuantity()/cuttingDailyRate;
        double totalManufacturingDays = cuttingDays   + sewingDays;
        LocalDate today = LocalDate.now();
        LocalDate plannedStartDate = today.plusDays((long)Math.ceil(designDays+sourcingDays));
        LocalDate projectCompletionDate = plannedStartDate.plusDays((long)Math.ceil(totalManufacturingDays));


        order.setEstimatedDays(totalManufacturingDays);
        order.setPlannedStartDate(plannedStartDate);
        order.setProjectCompletionDate(projectCompletionDate);
        orderRepo.save(order);

    }
    public boolean checkOrderReadiness(String orderId){
        OrderSnapshot order = orderRepo.findById(orderId).orElseThrow();
       List<OrderMaterialReserve> reserves = reserveRepo.findByOrderSnapshot(order);
       boolean hasShortage = false;
       for (OrderMaterialReserve reserve : reserves) {
           Double avail = inventoryRepo.getTotalAvailableQuantityByMaterial(reserve.getMaterial());
           if (avail == null || avail < reserve.getLockedQuantity()) {
               hasShortage = true;
           }
       }
           if(hasShortage == true) {order.setStatus("MATERIAL_SHORTAGE") ;

       }else {
               order.setStatus("READY_FOR_PRODUCTION");
           }
        orderRepo.save(order);
       return !hasShortage;
    }

    public void calculateBackwardRequirements(String orderId) {
        calculateProductionTimeline(orderId);
        OrderSnapshot order = orderRepo.findById(orderId).orElseThrow();
        if (order.getDeadline() == null) return;
        ProductionBaseline baseline = productionBaseline.findByProductType(order.getProductType());
        WorkerTeam team = baseline.getWorkerTeam();
        LocalDate today = LocalDate.now();
        double designDays = order.getDesignDays() != null ? order.getDesignDays() : 0.0;
        double sourcingDays = order.getSourcingDays() != null ? order.getSourcingDays() : 0.0;
        double totalManufacturingDays = order.getEstimatedDays() != null ? order.getEstimatedDays() : 0.0;

        long totalDaysUntilDeadline = ChronoUnit.DAYS.between(today, order.getDeadline());
        double availableShopFloorDays = (double) totalDaysUntilDeadline - (designDays + sourcingDays);
        if (availableShopFloorDays <= 0) {
            order.setStatus("DEADLINE_IMPOSSIBLE_BEFORE_PRODUCTION_STARTS");
        } else if(totalManufacturingDays <= availableShopFloorDays) {
            order.setStatus("DEADLINE_FEASIBLE");
        }else{
            double accelerationFactor = totalManufacturingDays / availableShopFloorDays;
            int currentWorkers = team != null ? team.getWorkerCount() : 10;
            int extraWorkersNeed = (int) Math.ceil((accelerationFactor - 1.0) * currentWorkers);
            System.out.println(order.getProjectCompletionDate());

            order.setStatus("CAPACITY_BOTTLENECK_NEED_" + extraWorkersNeed + "_EXTRA_WORKERS");
        }
        orderRepo.save(order);
    }

    public List<com.company.erp.dto.QueuePlanDTOs.QueuePlanItemDTO> simulateQueuePlanning(com.company.erp.dto.QueuePlanDTOs.QueueSimulationRequest request) {
        if (request == null) {
            request = new com.company.erp.dto.QueuePlanDTOs.QueueSimulationRequest();
        }
        String filterLine = request.getConveyorLine();
        String defaultDiff = (request.getDifficulty() != null && !request.getDifficulty().isBlank()) ? request.getDifficulty().toUpperCase() : "EASY";
        int defaultWorkers = (request.getDefaultWorkers() != null && request.getDefaultWorkers() > 0) ? request.getDefaultWorkers() : 10;

        List<OrderSnapshot> orders = orderRepo.findAll();
        orders.sort(java.util.Comparator.comparing(OrderSnapshot::getOrderDate, java.util.Comparator.nullsLast(java.util.Comparator.naturalOrder()))
                .thenComparing(OrderSnapshot::getId));

        // Virtual FIFO Inventory
        java.util.Map<String, Double> virtualStock = new java.util.HashMap<>();
        for (InventoryBalance bal : inventoryRepo.findAll()) {
            if (bal.getMaterial() != null) {
                virtualStock.put(bal.getMaterial().getId(), bal.getAvailableQuantity() != null ? bal.getAvailableQuantity() : 0.0);
            }
        }

        java.util.Map<String, LocalDate> lineCalendar = new java.util.HashMap<>();
        java.util.Map<String, Integer> linePositions = new java.util.HashMap<>();
        List<com.company.erp.dto.QueuePlanDTOs.QueuePlanItemDTO> results = new java.util.ArrayList<>();

        for (OrderSnapshot order : orders) {
            String line = order.getConveyorLine();
            if (line == null && order.getProductType() != null) {
                line = order.getProductType().getCategory();
            }
            if (line == null || line.isBlank()) {
                line = "Workwear";
            }

            if (filterLine != null && !filterLine.isBlank() && !"ALL".equalsIgnoreCase(filterLine) && !line.equalsIgnoreCase(filterLine)) {
                continue;
            }

            int queuePos = linePositions.getOrDefault(line, 0) + 1;
            linePositions.put(line, queuePos);

            int workers = defaultWorkers;
            String diff = defaultDiff;
            if (request.getOrderOverrides() != null && request.getOrderOverrides().containsKey(order.getId())) {
                com.company.erp.dto.QueuePlanDTOs.OrderOverrideDTO override = request.getOrderOverrides().get(order.getId());
                if (override.getWorkers() != null && override.getWorkers() > 0) workers = override.getWorkers();
                if (override.getDifficulty() != null && !override.getDifficulty().isBlank()) diff = override.getDifficulty().toUpperCase();
            }

            ProductionBaseline baseline = order.getProductType() != null ? productionBaseline.findByProductType(order.getProductType()) : null;
            WorkerTeam team = baseline != null ? baseline.getWorkerTeam() : null;
            int teamBaseWorkers = (team != null && team.getWorkerCount() != null && team.getWorkerCount() > 0) ? team.getWorkerCount() : 10;

            int targetDailyPieces = 150;
            if (baseline != null) {
                if ("HARD".equalsIgnoreCase(diff) && baseline.getDailyTargetPiecesHard() != null) {
                    targetDailyPieces = baseline.getDailyTargetPiecesHard();
                } else if (baseline.getDailyTargetPieces() != null) {
                    targetDailyPieces = baseline.getDailyTargetPieces();
                }
            }

            double dailySewingRate = ((double) targetDailyPieces / (double) teamBaseWorkers) * workers;
            if (dailySewingRate <= 0) dailySewingRate = 1.0;
            double dailyCuttingRate = dailySewingRate * 1.30;

            int orderQty = order.getQuantity() != null && order.getQuantity() > 0 ? order.getQuantity() : 500;
            double cuttingDays = (double) orderQty / dailyCuttingRate;
            double sewingDays = (double) orderQty / dailySewingRate;
            double totalMfgDays = cuttingDays + sewingDays;

            // FIFO Stock check
            boolean hasShortage = false;
            StringBuilder shortageDetails = new StringBuilder();
            if (order.getProductType() != null) {
                List<RecipeBOM> recipes = recipeRepo.findByProductType(order.getProductType());
                for (RecipeBOM recipe : recipes) {
                    if (recipe.getMaterial() == null) continue;
                    double needed = (double) orderQty * (recipe.getQuantityPerUnit() != null ? recipe.getQuantityPerUnit() : 1.0);
                    String matId = recipe.getMaterial().getId();
                    double stock = virtualStock.getOrDefault(matId, 0.0);
                    if (stock < needed) {
                        hasShortage = true;
                        double missing = needed - stock;
                        virtualStock.put(matId, 0.0);
                        if (shortageDetails.length() > 0) shortageDetails.append(", ");
                        shortageDetails.append(recipe.getMaterial().getName())
                                .append(" (-")
                                .append(String.format("%.0f", missing))
                                .append(" ")
                                .append(recipe.getMaterial().getUnit() != null ? recipe.getMaterial().getUnit() : "")
                                .append(")");
                    } else {
                        virtualStock.put(matId, stock - needed);
                    }
                }
            }

            double designDays = order.getDesignDays() != null ? order.getDesignDays() : 0.0;
            double sourcingDays = order.getSourcingDays() != null ? order.getSourcingDays() : (hasShortage ? 5.0 : 0.0);

            LocalDate lineAvail = lineCalendar.getOrDefault(line, LocalDate.now());
            LocalDate orderBaseDate = order.getOrderDate() != null ? order.getOrderDate() : LocalDate.now();
            LocalDate orderPrepReady = orderBaseDate.plusDays((long) Math.ceil(designDays + sourcingDays));
            LocalDate plannedStart = lineAvail.isAfter(orderPrepReady) ? lineAvail : orderPrepReady;
            LocalDate projectCompletion = plannedStart.plusDays((long) Math.ceil(totalMfgDays));
            lineCalendar.put(line, projectCompletion);

            LocalDate deadline = order.getDeadline();
            Long delayDays = null;
            Integer extraWorkersNeeded = null;
            String status = hasShortage ? "MATERIAL_SHORTAGE" : "READY_FOR_PRODUCTION";

            if (deadline != null) {
                if (projectCompletion.isAfter(deadline)) {
                    delayDays = ChronoUnit.DAYS.between(deadline, projectCompletion);
                    long availableDays = ChronoUnit.DAYS.between(plannedStart, deadline);
                    if (availableDays <= 0) {
                        status = "DEADLINE_IMPOSSIBLE_QUEUE_DELAY";
                    } else {
                        double acceleration = totalMfgDays / (double) availableDays;
                        extraWorkersNeeded = (int) Math.ceil((acceleration - 1.0) * workers);
                        if (extraWorkersNeeded < 1) extraWorkersNeeded = 1;
                        status = "CAPACITY_BOTTLENECK_NEED_" + extraWorkersNeeded + "_EXTRA_WORKERS";
                    }
                } else {
                    if (!hasShortage) status = "DEADLINE_FEASIBLE";
                }
            }

            com.company.erp.dto.QueuePlanDTOs.QueuePlanItemDTO item = com.company.erp.dto.QueuePlanDTOs.QueuePlanItemDTO.builder()
                    .orderId(order.getId())
                    .productTypeId(order.getProductType() != null ? order.getProductType().getId() : "unknown")
                    .productName(order.getProductType() != null ? order.getProductType().getName() : "Standart Məhsul")
                    .category(order.getProductType() != null ? order.getProductType().getCategory() : line)
                    .conveyorLine(line)
                    .quantity(orderQty)
                    .queuePosition(queuePos)
                    .workers(workers)
                    .difficulty(diff)
                    .dailyCuttingRate(dailyCuttingRate)
                    .dailySewingRate(dailySewingRate)
                    .cuttingDays(cuttingDays)
                    .sewingDays(sewingDays)
                    .totalManufacturingDays(totalMfgDays)
                    .orderDate(orderBaseDate)
                    .plannedStartDate(plannedStart)
                    .projectCompletionDate(projectCompletion)
                    .deadline(deadline)
                    .delayDays(delayDays)
                    .extraWorkersNeeded(extraWorkersNeeded)
                    .materialShortage(hasShortage)
                    .shortageDetails(shortageDetails.toString())
                    .status(status)
                    .build();

            results.add(item);
        }

        return results;
    }

    public List<OrderSnapshot> applyQueuePlanning(com.company.erp.dto.QueuePlanDTOs.ApplyQueueRequest request) {
        List<com.company.erp.dto.QueuePlanDTOs.QueuePlanItemDTO> plans = request != null ? request.getPlans() : null;
        if (plans == null || plans.isEmpty()) {
            com.company.erp.dto.QueuePlanDTOs.QueueSimulationRequest simReq = new com.company.erp.dto.QueuePlanDTOs.QueueSimulationRequest();
            if (request != null) {
                simReq.setConveyorLine(request.getConveyorLine());
                simReq.setDefaultWorkers(request.getDefaultWorkers());
                simReq.setDifficulty(request.getDifficulty());
            }
            plans = simulateQueuePlanning(simReq);
        }

        List<OrderSnapshot> updatedOrders = new java.util.ArrayList<>();
        for (com.company.erp.dto.QueuePlanDTOs.QueuePlanItemDTO plan : plans) {
            Optional<OrderSnapshot> opt = orderRepo.findById(plan.getOrderId());
            if (opt.isPresent()) {
                OrderSnapshot order = opt.get();
                order.setPlannedStartDate(plan.getPlannedStartDate());
                order.setProjectCompletionDate(plan.getProjectCompletionDate());
                order.setConveyorLine(plan.getConveyorLine());
                order.setAssignedWorkers(plan.getWorkers());
                order.setDifficulty(plan.getDifficulty());
                order.setQueuePosition(plan.getQueuePosition());
                order.setCuttingDays(plan.getCuttingDays());
                order.setSewingDays(plan.getSewingDays());
                order.setEstimatedDays(plan.getTotalManufacturingDays());
                order.setExtraWorkersNeeded(plan.getExtraWorkersNeeded());
                order.setDelayDays(plan.getDelayDays());
                order.setMaterialShortage(plan.getMaterialShortage());
                order.setShortageDetails(plan.getShortageDetails());
                order.setStatus(plan.getStatus());
                orderRepo.save(order);
                updatedOrders.add(order);
            }
        }
        return updatedOrders;
    }

    // ══════════════════════════════════════════════════════════════
    // PLANNING STUDIO: MATERIAL CHECK GATE
    // ══════════════════════════════════════════════════════════════
    public PlanningStudioDTOs.MaterialCheckResult checkMaterialAvailability(PlanningStudioDTOs.MaterialCheckRequest req) {
        String ptId = req.getProductTypeId() != null ? req.getProductTypeId() : "kitel";
        int qty = req.getQuantity() != null && req.getQuantity() > 0 ? req.getQuantity() : 500;
        ProductType pt = productTypeRepo.findById(ptId).orElse(productTypeRepo.findById("kitel").orElse(null));

        List<RecipeBOM> recipes = pt != null ? recipeRepo.findByProductType(pt) : new ArrayList<>();
        List<PlanningStudioDTOs.MaterialCheckItem> items = new ArrayList<>();
        boolean allSufficient = true;

        if (recipes.isEmpty()) {
            String category = pt != null ? pt.getCategory() : (req.getConveyorLine() != null ? req.getConveyorLine() : "Workwear");
            String matId;
            String matName;
            String unit;
            double needed;

            if ("Socks".equalsIgnoreCase(category)) {
                matId = "MAT-IPLIK-PAMBUQ";
                matName = "Pambıq İplik 20/1";
                unit = "KQ";
                needed = qty * 0.085; // 85g per pair
            } else if ("Underwear-boxer".equalsIgnoreCase(category)) {
                matId = "MAT-SUPREM";
                matName = "Süprəm Likralı Parça";
                unit = "METR";
                needed = qty * 0.30;
            } else {
                matId = "MAT-QABARDIN";
                matName = "Qabardin Parça 16x12";
                unit = "METR";
                needed = qty * 1.80;
            }

            Optional<com.company.erp.modules.catalog.model.Material> mOpt = materialRepo.findById(matId);
            Double availVal = mOpt.map(inventoryRepo::getTotalAvailableQuantityByMaterial).orElse(0.0);
            double avail = (availVal != null && availVal > 0) ? availVal : 5000.0;
            boolean suff = avail >= needed;
            if (!suff) allSufficient = false;

            items.add(PlanningStudioDTOs.MaterialCheckItem.builder()
                    .materialId(matId)
                    .materialName(matName)
                    .unit(unit)
                    .neededQuantity(needed)
                    .availableQuantity(avail)
                    .missingQuantity(suff ? 0.0 : needed - avail)
                    .isSufficient(suff)
                    .build());
        } else {
            java.util.Set<String> seenMaterials = new java.util.HashSet<>();
            for (RecipeBOM r : recipes) {
                String matId = r.getMaterial().getId();
                if (seenMaterials.contains(matId)) continue;
                seenMaterials.add(matId);

                double needed = qty * r.getQuantityPerUnit();
                Double availVal = inventoryRepo.getTotalAvailableQuantityByMaterial(r.getMaterial());
                double avail = availVal != null ? availVal : 0.0;
                boolean suff = avail >= needed;
                if (!suff) allSufficient = false;
                items.add(PlanningStudioDTOs.MaterialCheckItem.builder()
                        .materialId(r.getMaterial().getId())
                        .materialName(r.getMaterial().getName())
                        .unit(r.getMaterial().getUnit())
                        .neededQuantity(needed)
                        .availableQuantity(avail)
                        .missingQuantity(suff ? 0.0 : needed - avail)
                        .isSufficient(suff)
                        .build());
            }
        }

        return PlanningStudioDTOs.MaterialCheckResult.builder()
                .productTypeId(pt != null ? pt.getId() : ptId)
                .productName(pt != null ? pt.getName() : "Standart Məhsul")
                .quantity(qty)
                .allMaterialsSufficient(allSufficient)
                .materials(items)
                .recommendedLeadTimeDays(allSufficient ? 0 : 5)
                .build();
    }

    // ══════════════════════════════════════════════════════════════
    // PLANNING STUDIO: OPTION 1 (FORWARD PLANNING - RESOURCES IN HAND -> DELIVERY DATE)
    // ══════════════════════════════════════════════════════════════
    public PlanningStudioDTOs.ForwardPlanningResult executeForwardPlanning(PlanningStudioDTOs.ForwardPlanningRequest req) {
        String ptId = req.getProductTypeId() != null ? req.getProductTypeId() : "kitel";
        int qty = req.getQuantity() != null && req.getQuantity() > 0 ? req.getQuantity() : 500;
        ProductType pt = productTypeRepo.findById(ptId).orElse(productTypeRepo.findById("kitel").orElse(null));

        ProductionBaseline pb = pt != null ? productionBaseline.findByProductType(pt) : null;
        int baseWorkers = pb != null && pb.getWorkerTeam() != null ? pb.getWorkerTeam().getWorkerCount() : 10;
        int workers = req.getWorkers() != null && req.getWorkers() > 0 ? req.getWorkers() : baseWorkers;
        String diff = "HARD".equalsIgnoreCase(req.getDifficulty()) ? "HARD" : "EASY";

        double baseDailyRate = "HARD".equalsIgnoreCase(diff) && pb != null && pb.getDailyTargetPiecesHard() != null
                ? pb.getDailyTargetPiecesHard()
                : (pb != null ? pb.getDailyTargetPieces() : 150);

        double dailySewingRate = (baseDailyRate / (double) baseWorkers) * (double) workers;
        double dailyCuttingRate = dailySewingRate * 1.30; // +30% cutting speed rule

        double cuttingDays = Math.max(0.1, (double) qty / dailyCuttingRate);
        double sewingDays = Math.max(0.1, (double) qty / dailySewingRate);
        double totalMfgDays = cuttingDays + sewingDays;

        double designDays = req.getDesignDays() != null && req.getDesignDays() > 0 ? req.getDesignDays() : 0.0;
        double sourcingDays = req.getSourcingDays() != null && req.getSourcingDays() > 0 ? req.getSourcingDays() : 0.0;

        LocalDate start = req.getStartDate() != null ? req.getStartDate() : LocalDate.now();
        LocalDate cursor = start;

        List<PlanningStudioDTOs.StageTimelineItem> stageItems = new ArrayList<>();

        if (designDays > 0) {
            LocalDate dEnd = cursor.plusDays((long) Math.ceil(designDays));
            stageItems.add(PlanningStudioDTOs.StageTimelineItem.builder()
                    .stageId("dizayn")
                    .stageName("Dizayn və Nümunə Hazırlığı")
                    .days(designDays)
                    .startDate(cursor)
                    .endDate(dEnd)
                    .status("LEAD_TIME")
                    .details("Kalıp və lekal hazırlanması")
                    .build());
            cursor = dEnd;
        }

        if (sourcingDays > 0) {
            LocalDate sEnd = cursor.plusDays((long) Math.ceil(sourcingDays));
            stageItems.add(PlanningStudioDTOs.StageTimelineItem.builder()
                    .stageId("material")
                    .stageName("Xammal Təchizatı və Çatdırılma")
                    .days(sourcingDays)
                    .startDate(cursor)
                    .endDate(sEnd)
                    .status("SOURCING_BUFFER")
                    .details("Təchizatçıdan parçanın gətirilməsi və yoxlanılması")
                    .build());
            cursor = sEnd;
        }

        boolean isSocks = pt != null && "Socks".equalsIgnoreCase(pt.getCategory());
        String stage1Id = isSocks ? "horgu" : "kesim";
        String stage1Name = isSocks ? "Hörgü Şöbəsi (Knitting)" : "Kəsim Şöbəsi (+30% Sürət)";
        String stage2Id = isSocks ? "tikis_forma" : "tikis";
        String stage2Name = isSocks ? "Tikiş və Forma (Toe-closing & Boarding)" : "Tikiş Şöbəsi (Əsas İstehsalat)";

        LocalDate cuttingStart = cursor;
        LocalDate cuttingEnd = cuttingStart.plusDays((long) Math.ceil(cuttingDays));
        stageItems.add(PlanningStudioDTOs.StageTimelineItem.builder()
                .stageId(stage1Id)
                .stageName(stage1Name)
                .days(cuttingDays)
                .startDate(cuttingStart)
                .endDate(cuttingEnd)
                .status("MANUFACTURING")
                .details(String.format("Norma: %.0f ədəd/gün", dailyCuttingRate))
                .build());

        LocalDate sewingStart = cuttingEnd;
        LocalDate sewingEnd = sewingStart.plusDays((long) Math.ceil(sewingDays));
        stageItems.add(PlanningStudioDTOs.StageTimelineItem.builder()
                .stageId(stage2Id)
                .stageName(stage2Name)
                .days(sewingDays)
                .startDate(sewingStart)
                .endDate(sewingEnd)
                .status("MANUFACTURING")
                .details(String.format("%d işçi, norma: %.0f ədəd/gün (%s)", workers, dailySewingRate, "HARD".equals(diff) ? "Çətin" : "Asan"))
                .build());

        LocalDate deliveryDate = sewingEnd;

        return PlanningStudioDTOs.ForwardPlanningResult.builder()
                .productTypeId(pt != null ? pt.getId() : ptId)
                .productName(pt != null ? pt.getName() : "Standart Məhsul")
                .quantity(qty)
                .conveyorLine(pt != null ? pt.getCategory() : (req.getConveyorLine() != null ? req.getConveyorLine() : "Workwear"))
                .workers(workers)
                .difficulty(diff)
                .dailySewingRate(dailySewingRate)
                .dailyCuttingRate(dailyCuttingRate)
                .cuttingDays(cuttingDays)
                .sewingDays(sewingDays)
                .totalManufacturingDays(totalMfgDays)
                .designDays(designDays)
                .sourcingDays(sourcingDays)
                .startDate(start)
                .cuttingEndDate(cuttingEnd)
                .sewingEndDate(sewingEnd)
                .deliveryDate(deliveryDate)
                .stages(stageItems)
                .status("PLAN_CALCULATED")
                .build();
    }

    // ══════════════════════════════════════════════════════════════
    // PLANNING STUDIO: OPTION 2 (BACKWARD PLANNING - TARGET DEADLINE -> REQUIRED RESOURCES)
    // ══════════════════════════════════════════════════════════════
    public PlanningStudioDTOs.BackwardPlanningResult executeBackwardPlanning(PlanningStudioDTOs.BackwardPlanningRequest req) {
        String ptId = req.getProductTypeId() != null ? req.getProductTypeId() : "kitel";
        int qty = req.getQuantity() != null && req.getQuantity() > 0 ? req.getQuantity() : 500;
        ProductType pt = productTypeRepo.findById(ptId).orElse(productTypeRepo.findById("kitel").orElse(null));

        ProductionBaseline pb = pt != null ? productionBaseline.findByProductType(pt) : null;
        int baseWorkers = pb != null && pb.getWorkerTeam() != null ? pb.getWorkerTeam().getWorkerCount() : 10;
        if (req.getBaseWorkers() != null && req.getBaseWorkers() > 0) {
            baseWorkers = req.getBaseWorkers();
        }
        String diff = "HARD".equalsIgnoreCase(req.getDifficulty()) ? "HARD" : "EASY";

        double baseDailyRate = "HARD".equalsIgnoreCase(diff) && pb != null && pb.getDailyTargetPiecesHard() != null
                ? pb.getDailyTargetPiecesHard()
                : (pb != null ? pb.getDailyTargetPieces() : 150);

        double stdSewingRate = baseDailyRate;
        double stdCuttingRate = stdSewingRate * 1.30;
        double stdCuttingDays = Math.max(0.1, (double) qty / stdCuttingRate);
        double stdSewingDays = Math.max(0.1, (double) qty / stdSewingRate);
        double stdTotalDuration = stdCuttingDays + stdSewingDays;

        double designDays = req.getDesignDays() != null && req.getDesignDays() > 0 ? req.getDesignDays() : 0.0;
        double sourcingDays = req.getSourcingDays() != null && req.getSourcingDays() > 0 ? req.getSourcingDays() : 0.0;

        LocalDate start = req.getStartDate() != null ? req.getStartDate() : LocalDate.now();
        LocalDate deadline = req.getCustomerDeadline() != null ? req.getCustomerDeadline() : start.plusDays(20);

        if (deadline.isBefore(start)) {
            return PlanningStudioDTOs.BackwardPlanningResult.builder()
                    .productTypeId(pt != null ? pt.getId() : ptId)
                    .productName(pt != null ? pt.getName() : "Standart Məhsul")
                    .quantity(qty)
                    .customerDeadline(deadline)
                    .startDate(start)
                    .designDays(designDays)
                    .sourcingDays(sourcingDays)
                    .grossCalendarDays(0L)
                    .netManufacturingDays(0L)
                    .standardDurationDays(stdTotalDuration)
                    .isFeasible(false)
                    .accelerationFactor(0.0)
                    .baseWorkers(baseWorkers)
                    .requiredWorkers(baseWorkers)
                    .extraWorkersNeeded(0)
                    .status("INVALID_DEADLINE_IN_PAST")
                    .recommendation(String.format("Xəta: Müştəri hədəf tarixi (%s) başlama tarixindən (%s) əvvəldir. İstehsalat planlaması üçün zəhmət olmasa gələcək tarix təyin edin.",
                            deadline, start))
                    .stages(new ArrayList<>())
                    .build();
        }

        long grossDays = ChronoUnit.DAYS.between(start, deadline);
        long netDays = Math.max(0, grossDays - (long) Math.ceil(designDays + sourcingDays));

        boolean isFeasible;
        double accel = 1.0;
        int requiredWorkers = baseWorkers;
        int extraWorkers = 0;
        double reqDailySewingRate = stdSewingRate;
        double reqDailyCuttingRate = stdCuttingRate;
        String status;
        String recommendation;

        if (netDays <= 0) {
            isFeasible = false;
            status = "IMPOSSIBLE_LEAD_TIME_EXCEEDS_DEADLINE";
            accel = 0.0;
            requiredWorkers = baseWorkers * 3;
            extraWorkers = requiredWorkers - baseWorkers;
            recommendation = String.format("Qeyri-mümkündür: Təchizat və dizayn müddəti (%.0f gün) müştəri son tarixini (%s) aşır. Tarix ən azı %.0f gün uzadılmalıdır.",
                    (designDays + sourcingDays), deadline, stdTotalDuration + designDays + sourcingDays);
        } else {
            accel = stdTotalDuration / (double) netDays;
            if (accel <= 1.0) {
                isFeasible = true;
                status = "FEASIBLE";
                requiredWorkers = baseWorkers;
                extraWorkers = 0;
                recommendation = String.format("Mövcud standart resurslar (%d işçi) ilə sifariş vaxtında çatdırıla bilər. Net istehsalat müddəti: %d gün.",
                        baseWorkers, netDays);
            } else {
                isFeasible = false;
                status = "BOTTLENECK_EXTRA_RESOURCES_REQUIRED";
                requiredWorkers = (int) Math.ceil(baseWorkers * accel);
                extraWorkers = Math.max(1, requiredWorkers - baseWorkers);
                reqDailySewingRate = (double) qty / ((double) netDays * 0.565);
                reqDailyCuttingRate = reqDailySewingRate * 1.30;
                recommendation = String.format("Gecikmə riski: Hədəf tarixə çatdırmaq üçün +%d əlavə işçi (cəmi %d işçi) cəlb edilməli və ya 2-ci növbə / overtime tətbiq olunmalıdır.",
                        extraWorkers, requiredWorkers);
            }
        }

        List<PlanningStudioDTOs.StageTimelineItem> stageItems = new ArrayList<>();
        LocalDate cursor = start;
        if (designDays > 0) {
            LocalDate dEnd = cursor.plusDays((long) Math.ceil(designDays));
            stageItems.add(PlanningStudioDTOs.StageTimelineItem.builder()
                    .stageId("dizayn").stageName("Dizayn").days(designDays).startDate(cursor).endDate(dEnd).status("LEAD_TIME").build());
            cursor = dEnd;
        }
        if (sourcingDays > 0) {
            LocalDate sEnd = cursor.plusDays((long) Math.ceil(sourcingDays));
            stageItems.add(PlanningStudioDTOs.StageTimelineItem.builder()
                    .stageId("material").stageName("Təchizat").days(sourcingDays).startDate(cursor).endDate(sEnd).status("SOURCING").build());
            cursor = sEnd;
        }

        boolean isSocks = pt != null && "Socks".equalsIgnoreCase(pt.getCategory());
        String bStage1Id = isSocks ? "horgu" : "kesim";
        String bStage1Name = isSocks ? "Hörgü" : "Kəsim";
        String bStage2Id = isSocks ? "tikis_forma" : "tikis";
        String bStage2Name = isSocks ? "Tikiş və Forma" : "Tikiş";

        double allocatedCuttingDays;
        double allocatedSewingDays;
        LocalDate cutEnd;
        LocalDate sewEnd;

        if (isFeasible) {
            allocatedCuttingDays = stdCuttingDays;
            allocatedSewingDays = stdSewingDays;
            cutEnd = cursor.plusDays((long) Math.ceil(allocatedCuttingDays));
            sewEnd = cutEnd.plusDays((long) Math.ceil(allocatedSewingDays));
        } else {
            allocatedCuttingDays = Math.max(0.1, netDays * 0.435);
            allocatedSewingDays = Math.max(0.1, netDays * 0.565);
            cutEnd = cursor.plusDays((long) Math.ceil(allocatedCuttingDays));
            sewEnd = deadline;
        }

        stageItems.add(PlanningStudioDTOs.StageTimelineItem.builder()
                .stageId(bStage1Id).stageName(bStage1Name).days(allocatedCuttingDays).startDate(cursor).endDate(cutEnd).status(isFeasible ? "ON_TRACK" : "ACCELERATED").build());

        stageItems.add(PlanningStudioDTOs.StageTimelineItem.builder()
                .stageId(bStage2Id).stageName(bStage2Name).days(allocatedSewingDays).startDate(cutEnd).endDate(sewEnd).status(isFeasible ? "ON_TRACK" : "ACCELERATED").build());

        return PlanningStudioDTOs.BackwardPlanningResult.builder()
                .productTypeId(pt != null ? pt.getId() : ptId)
                .productName(pt != null ? pt.getName() : "Standart Məhsul")
                .quantity(qty)
                .customerDeadline(deadline)
                .startDate(start)
                .designDays(designDays)
                .sourcingDays(sourcingDays)
                .grossCalendarDays(grossDays)
                .netManufacturingDays(netDays)
                .standardDurationDays(stdTotalDuration)
                .isFeasible(isFeasible)
                .accelerationFactor(accel)
                .baseWorkers(baseWorkers)
                .requiredWorkers(requiredWorkers)
                .extraWorkersNeeded(extraWorkers)
                .requiredDailyCuttingRate(reqDailyCuttingRate)
                .requiredDailySewingRate(reqDailySewingRate)
                .status(status)
                .recommendation(recommendation)
                .stages(stageItems)
                .build();
    }
}

