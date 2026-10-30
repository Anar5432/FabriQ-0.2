package com.company.erp.controller;

import com.company.erp.modules.catalog.model.ProductType;
import com.company.erp.modules.dashboard.model.OrderSnapshot;
import com.company.erp.modules.planning.model.ProductionBaseline;
import com.company.erp.modules.planning.model.WorkerTeam;
import com.company.erp.repository.OrderSnapshotRepository;
import com.company.erp.repository.ProductionBaselineRepository;
import com.company.erp.repository.ProductTypeRepository;
import com.company.erp.repository.WorkerTeamRepository;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDate;
import java.util.*;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/settings")
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
public class SettingsController {

    private final OrderSnapshotRepository orderRepo;
    private final ProductionBaselineRepository baselineRepo;
    private final WorkerTeamRepository teamRepo;
    private final ProductTypeRepository productTypeRepo;

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class OrderSettingDTO {
        private String orderId;
        private String customerName;
        private String productName;
        private String category;
        private Integer quantity;
        private Integer deliveredQuantity;
        private Boolean isReservationActive;
        private String status;
        private String currentPhase;
        private LocalDate orderDate;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class BaselineSettingDTO {
        private String productTypeId;
        private String productName;
        private String category;
        private Integer dailyTargetEasy;
        private Integer dailyTargetHard;
        private String teamName;
        private Integer workerCount;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class SettingsOverviewDTO {
        private List<OrderSettingDTO> orders;
        private List<BaselineSettingDTO> baselines;
        private List<WorkerTeam> teams;
        private Integer totalOrders;
        private Integer activeReservationCount;
        private Integer syncIntervalSeconds;
    }

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class BulkToggleRequest {
        private List<String> orderIds;
        private Boolean active;
    }

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class BaselineUpdateRequest {
        private String productTypeId;
        private Integer dailyTargetEasy;
        private Integer dailyTargetHard;
    }

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    public static class TeamUpdateRequest {
        private Long teamId;
        private Integer workerCount;
    }

    @GetMapping("/overview")
    public SettingsOverviewDTO getOverview() {
        List<OrderSnapshot> allOrders = orderRepo.findAll();

        // Filter out ghost orders (missing customer or empty product)
        List<OrderSettingDTO> orderDTOs = allOrders.stream()
                .filter(o -> o.getId() != null && !o.getId().isBlank())
                .sorted((a, b) -> {
                    LocalDate d1 = a.getOrderDate() != null ? a.getOrderDate() : LocalDate.MIN;
                    LocalDate d2 = b.getOrderDate() != null ? b.getOrderDate() : LocalDate.MIN;
                    return d2.compareTo(d1); // Newest first
                })
                .map(o -> OrderSettingDTO.builder()
                        .orderId(o.getId())
                        .customerName(o.getCustomerName() != null ? o.getCustomerName() : "Müştəri")
                        .productName(o.getProductType() != null ? o.getProductType().getName() : "Standart Məhsul")
                        .category(o.getProductType() != null ? o.getProductType().getCategory() : (o.getConveyorLine() != null ? o.getConveyorLine() : "Workwear"))
                        .quantity(o.getQuantity() != null ? o.getQuantity() : 0)
                        .deliveredQuantity(o.getDeliveredQuantity() != null ? o.getDeliveredQuantity() : 0)
                        .isReservationActive(Boolean.TRUE.equals(o.getIsReservationActive()))
                        .status(o.getStatus() != null ? o.getStatus() : "IN_PROGRESS")
                        .currentPhase(o.getCurrentPhase() != null ? o.getCurrentPhase() : "İstehsalat")
                        .orderDate(o.getOrderDate())
                        .build())
                .collect(Collectors.toList());

        List<ProductionBaseline> baselines = baselineRepo.findAll();
        List<BaselineSettingDTO> baselineDTOs = baselines.stream()
                .map(b -> BaselineSettingDTO.builder()
                        .productTypeId(b.getProductType() != null ? b.getProductType().getId() : "")
                        .productName(b.getProductType() != null ? b.getProductType().getName() : "")
                        .category(b.getProductType() != null ? b.getProductType().getCategory() : "")
                        .dailyTargetEasy(b.getDailyTargetPieces() != null ? b.getDailyTargetPieces() : 150)
                        .dailyTargetHard(b.getDailyTargetPiecesHard() != null ? b.getDailyTargetPiecesHard() : 100)
                        .teamName(b.getWorkerTeam() != null ? b.getWorkerTeam().getDepartmentName() : "Əsas Briqada")
                        .workerCount(b.getWorkerTeam() != null ? b.getWorkerTeam().getWorkerCount() : 10)
                        .build())
                .sorted(Comparator.comparing(BaselineSettingDTO::getCategory).thenComparing(BaselineSettingDTO::getProductName))
                .collect(Collectors.toList());

        List<WorkerTeam> teams = teamRepo.findAll();

        long activeCount = orderDTOs.stream().filter(OrderSettingDTO::getIsReservationActive).count();

        return SettingsOverviewDTO.builder()
                .orders(orderDTOs)
                .baselines(baselineDTOs)
                .teams(teams)
                .totalOrders(orderDTOs.size())
                .activeReservationCount((int) activeCount)
                .syncIntervalSeconds(5)
                .build();
    }

    @PostMapping("/orders/toggle/{orderId}")
    public OrderSnapshot toggleOrderReservation(@PathVariable String orderId) {
        OrderSnapshot order = orderRepo.findById(orderId).orElseThrow(() -> new RuntimeException("Sifariş tapılmadı: " + orderId));
        boolean current = Boolean.TRUE.equals(order.getIsReservationActive());
        order.setIsReservationActive(!current);
        return orderRepo.save(order);
    }

    @PostMapping("/orders/bulk-toggle")
    public Map<String, Object> bulkToggleOrders(@RequestBody BulkToggleRequest req) {
        if (req.getOrderIds() == null || req.getOrderIds().isEmpty()) {
            return Map.of("success", true, "updatedCount", 0);
        }
        boolean activeState = Boolean.TRUE.equals(req.getActive());
        List<OrderSnapshot> orders = orderRepo.findAllById(req.getOrderIds());
        for (OrderSnapshot o : orders) {
            o.setIsReservationActive(activeState);
        }
        orderRepo.saveAll(orders);
        return Map.of("success", true, "updatedCount", orders.size(), "activeState", activeState);
    }

    @PutMapping("/baselines")
    public Map<String, Object> updateBaselines(@RequestBody List<BaselineUpdateRequest> updates) {
        int updated = 0;
        for (BaselineUpdateRequest u : updates) {
            Optional<ProductType> ptOpt = productTypeRepo.findById(u.getProductTypeId());
            if (ptOpt.isPresent()) {
                ProductionBaseline pb = baselineRepo.findByProductType(ptOpt.get());
                if (pb != null) {
                    if (u.getDailyTargetEasy() != null && u.getDailyTargetEasy() > 0) {
                        pb.setDailyTargetPieces(u.getDailyTargetEasy());
                    }
                    if (u.getDailyTargetHard() != null && u.getDailyTargetHard() > 0) {
                        pb.setDailyTargetPiecesHard(u.getDailyTargetHard());
                    }
                    baselineRepo.save(pb);
                    updated++;
                }
            }
        }
        return Map.of("success", true, "updatedBaselinesCount", updated);
    }

    @PutMapping("/teams")
    public Map<String, Object> updateTeams(@RequestBody List<TeamUpdateRequest> updates) {
        int updated = 0;
        for (TeamUpdateRequest u : updates) {
            if (u.getTeamId() != null) {
                Optional<WorkerTeam> teamOpt = teamRepo.findById(u.getTeamId());
                if (teamOpt.isPresent()) {
                    WorkerTeam t = teamOpt.get();
                    if (u.getWorkerCount() != null && u.getWorkerCount() > 0) {
                        t.setWorkerCount(u.getWorkerCount());
                        teamRepo.save(t);
                        updated++;
                    }
                }
            }
        }
        return Map.of("success", true, "updatedTeamsCount", updated);
    }
}
