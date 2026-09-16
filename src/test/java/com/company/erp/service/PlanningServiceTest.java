package com.company.erp.service;

import com.company.erp.dto.PlanningStudioDTOs;
import com.company.erp.modules.catalog.model.Material;
import com.company.erp.modules.catalog.model.ProductType;
import com.company.erp.modules.catalog.model.RecipeBOM;
import com.company.erp.modules.planning.model.ProductionBaseline;
import com.company.erp.modules.planning.model.WorkerTeam;
import com.company.erp.repository.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDate;
import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class PlanningServiceTest {

    @Mock
    private OrderSnapshotRepository orderRepo;
    @Mock
    private RecipeBOMRepository recipeRepo;
    @Mock
    private WorkerTeamRepository teamRepo;
    @Mock
    private OrderMaterialReserveRepository reserveRepo;
    @Mock
    private ProductionBaselineRepository productionBaseline;
    @Mock
    private InventoryBalanceRepository inventoryRepo;
    @Mock
    private ProductTypeRepository productTypeRepo;
    @Mock
    private MaterialRepository materialRepo;

    @InjectMocks
    private PlanningService planningService;

    private ProductType kitelProduct;
    private ProductType socksProduct;
    private ProductionBaseline kitelBaseline;
    private ProductionBaseline socksBaseline;
    private WorkerTeam defaultTeam;

    @BeforeEach
    void setUp() {
        defaultTeam = new WorkerTeam();
        defaultTeam.setId(1L);
        defaultTeam.setDepartmentName("Tikiş Şöbəsi");
        defaultTeam.setWorkerCount(10);

        kitelProduct = new ProductType();
        kitelProduct.setId("kitel");
        kitelProduct.setName("Kitel / Tunic");
        kitelProduct.setCategory("Workwear");

        socksProduct = new ProductType();
        socksProduct.setId("qis_corabi");
        socksProduct.setName("Qış Corabı");
        socksProduct.setCategory("Socks");

        kitelBaseline = new ProductionBaseline();
        kitelBaseline.setId(1L);
        kitelBaseline.setProductType(kitelProduct);
        kitelBaseline.setWorkerTeam(defaultTeam);
        kitelBaseline.setDailyTargetPieces(150);
        kitelBaseline.setDailyTargetPiecesHard(100);

        socksBaseline = new ProductionBaseline();
        socksBaseline.setId(2L);
        socksBaseline.setProductType(socksProduct);
        socksBaseline.setWorkerTeam(defaultTeam);
        socksBaseline.setDailyTargetPieces(300);
        socksBaseline.setDailyTargetPiecesHard(200);
    }

    @Test
    @DisplayName("Forward Planning: Kəsim sürəti tikiş sürətindən dəqiq +30% çox olmalıdır")
    void testCuttingRateIs30PercentFasterThanSewingRate() {
        when(productTypeRepo.findById("kitel")).thenReturn(Optional.of(kitelProduct));
        when(productionBaseline.findByProductType(kitelProduct)).thenReturn(kitelBaseline);

        PlanningStudioDTOs.ForwardPlanningRequest req = PlanningStudioDTOs.ForwardPlanningRequest.builder()
                .productTypeId("kitel")
                .quantity(1000)
                .workers(10)
                .difficulty("EASY")
                .startDate(LocalDate.of(2026, 9, 1))
                .build();

        PlanningStudioDTOs.ForwardPlanningResult result = planningService.executeForwardPlanning(req);

        assertThat(result.getDailySewingRate()).isEqualTo(150.0);
        assertThat(result.getDailyCuttingRate()).isEqualTo(150.0 * 1.30);
        assertThat(result.getCuttingDays()).isLessThan(result.getSewingDays());
    }

    @Test
    @DisplayName("Forward Planning: Sifariş müddəti və mərhələlər düzgün hesablanmalıdır")
    void testForwardPlanningCalculation() {
        when(productTypeRepo.findById("kitel")).thenReturn(Optional.of(kitelProduct));
        when(productionBaseline.findByProductType(kitelProduct)).thenReturn(kitelBaseline);

        LocalDate startDate = LocalDate.of(2026, 9, 1);
        PlanningStudioDTOs.ForwardPlanningRequest req = PlanningStudioDTOs.ForwardPlanningRequest.builder()
                .productTypeId("kitel")
                .quantity(300)
                .workers(10)
                .difficulty("EASY")
                .startDate(startDate)
                .designDays(1.0)
                .sourcingDays(2.0)
                .build();

        PlanningStudioDTOs.ForwardPlanningResult result = planningService.executeForwardPlanning(req);

        assertThat(result).isNotNull();
        assertThat(result.getQuantity()).isEqualTo(300);
        assertThat(result.getDesignDays()).isEqualTo(1.0);
        assertThat(result.getSourcingDays()).isEqualTo(2.0);
        assertThat(result.getDeliveryDate()).isAfter(startDate);
        assertThat(result.getStages()).hasSizeGreaterThanOrEqualTo(4); // Dizayn, Təchizat, Kəsim, Tikiş
    }

    @Test
    @DisplayName("Backward Planning: Keçmiş deadline tarixi rədd edilməli, mənfi gün və ya 99x verilməməlidir")
    void testBackwardPlanningWithPastDeadlineRejected() {
        when(productTypeRepo.findById("kitel")).thenReturn(Optional.of(kitelProduct));
        when(productionBaseline.findByProductType(kitelProduct)).thenReturn(kitelBaseline);

        LocalDate startDate = LocalDate.of(2026, 9, 1);
        LocalDate pastDeadline = LocalDate.of(2019, 4, 23); // Old date

        PlanningStudioDTOs.BackwardPlanningRequest req = PlanningStudioDTOs.BackwardPlanningRequest.builder()
                .productTypeId("kitel")
                .quantity(500)
                .startDate(startDate)
                .customerDeadline(pastDeadline)
                .baseWorkers(10)
                .difficulty("EASY")
                .build();

        PlanningStudioDTOs.BackwardPlanningResult result = planningService.executeBackwardPlanning(req);

        assertThat(result.getStatus()).isEqualTo("INVALID_DEADLINE_IN_PAST");
        assertThat(result.getIsFeasible()).isFalse();
        assertThat(result.getNetManufacturingDays()).isZero();
        assertThat(result.getAccelerationFactor()).isEqualTo(0.0);
        assertThat(result.getRecommendation()).contains("Xəta: Müştəri hədəf tarixi");
    }

    @Test
    @DisplayName("Backward Planning: Əlçatan gələcək deadline olduqda FEASIBLE olmalıdır")
    void testBackwardPlanningFeasibleSchedule() {
        when(productTypeRepo.findById("kitel")).thenReturn(Optional.of(kitelProduct));
        when(productionBaseline.findByProductType(kitelProduct)).thenReturn(kitelBaseline);

        LocalDate startDate = LocalDate.of(2026, 9, 1);
        LocalDate comfortableDeadline = LocalDate.of(2026, 10, 15); // 44 days away

        PlanningStudioDTOs.BackwardPlanningRequest req = PlanningStudioDTOs.BackwardPlanningRequest.builder()
                .productTypeId("kitel")
                .quantity(500)
                .startDate(startDate)
                .customerDeadline(comfortableDeadline)
                .baseWorkers(10)
                .difficulty("EASY")
                .build();

        PlanningStudioDTOs.BackwardPlanningResult result = planningService.executeBackwardPlanning(req);

        assertThat(result.getIsFeasible()).isTrue();
        assertThat(result.getStatus()).isEqualTo("FEASIBLE");
        assertThat(result.getExtraWorkersNeeded()).isZero();
        assertThat(result.getAccelerationFactor()).isLessThanOrEqualTo(1.0);
        assertThat(result.getNetManufacturingDays()).isGreaterThan(0);
    }

    @Test
    @DisplayName("Backward Planning: Tələsik deadline olduqda əlavə işçi və sürətləndirmə tələb olunmalıdır")
    void testBackwardPlanningTightDeadlineRequiresExtraWorkers() {
        when(productTypeRepo.findById("kitel")).thenReturn(Optional.of(kitelProduct));
        when(productionBaseline.findByProductType(kitelProduct)).thenReturn(kitelBaseline);

        LocalDate startDate = LocalDate.of(2026, 9, 1);
        LocalDate tightDeadline = LocalDate.of(2026, 9, 3); // only 2 days away for 1000 items

        PlanningStudioDTOs.BackwardPlanningRequest req = PlanningStudioDTOs.BackwardPlanningRequest.builder()
                .productTypeId("kitel")
                .quantity(1000)
                .startDate(startDate)
                .customerDeadline(tightDeadline)
                .baseWorkers(10)
                .difficulty("EASY")
                .build();

        PlanningStudioDTOs.BackwardPlanningResult result = planningService.executeBackwardPlanning(req);

        assertThat(result.getIsFeasible()).isFalse();
        assertThat(result.getStatus()).isEqualTo("BOTTLENECK_EXTRA_RESOURCES_REQUIRED");
        assertThat(result.getExtraWorkersNeeded()).isGreaterThan(0);
        assertThat(result.getAccelerationFactor()).isGreaterThan(1.0);
    }

    @Test
    @DisplayName("Corab Bantı (Socks): Mərhələlər Hörgü və Tikiş və Forma olmalıdır (Kəsim olmamalıdır)")
    void testSocksStageNamesAreKnittingAndClosing() {
        when(productTypeRepo.findById("qis_corabi")).thenReturn(Optional.of(socksProduct));
        when(productionBaseline.findByProductType(socksProduct)).thenReturn(socksBaseline);

        LocalDate startDate = LocalDate.of(2026, 9, 1);
        LocalDate deadline = LocalDate.of(2026, 9, 25);

        PlanningStudioDTOs.BackwardPlanningRequest req = PlanningStudioDTOs.BackwardPlanningRequest.builder()
                .productTypeId("qis_corabi")
                .quantity(600)
                .startDate(startDate)
                .customerDeadline(deadline)
                .baseWorkers(10)
                .build();

        PlanningStudioDTOs.BackwardPlanningResult result = planningService.executeBackwardPlanning(req);

        List<PlanningStudioDTOs.StageTimelineItem> stages = result.getStages();
        assertThat(stages).isNotEmpty();
        // Check stage names: must contain Hörgü and Tikiş və Forma, NEVER Kəsim
        List<String> stageNames = stages.stream().map(PlanningStudioDTOs.StageTimelineItem::getStageName).toList();
        assertThat(stageNames).contains("Hörgü");
        assertThat(stageNames).contains("Tikiş və Forma");
        assertThat(stageNames).doesNotContain("Kəsim");
    }

    @Test
    @DisplayName("Xammal Yoxlanışı (BOM Gate): Anbarda çatışmayan material olduqda çatışmazlıq qeydə alınmalıdır")
    void testCheckMaterialsDetectsShortage() {
        when(productTypeRepo.findById("kitel")).thenReturn(Optional.of(kitelProduct));

        Material fabric = new Material();
        fabric.setId("MAT-FAB-001");
        fabric.setName("Kitel Parçası (Pambıq)");
        fabric.setUnit("METR");

        RecipeBOM bom = new RecipeBOM();
        bom.setMaterial(fabric);
        bom.setProductType(kitelProduct);
        bom.setQuantityPerUnit(2.5); // 2.5m per item -> for 100 items needs 250m

        when(recipeRepo.findByProductType(kitelProduct)).thenReturn(List.of(bom));
        when(inventoryRepo.getTotalAvailableQuantityByMaterial(fabric)).thenReturn(100.0); // Only 100m available

        PlanningStudioDTOs.MaterialCheckRequest req = PlanningStudioDTOs.MaterialCheckRequest.builder()
                .productTypeId("kitel")
                .quantity(100)
                .build();

        PlanningStudioDTOs.MaterialCheckResult result = planningService.checkMaterialAvailability(req);

        assertThat(result.getAllMaterialsSufficient()).isFalse();
        assertThat(result.getMaterials()).hasSize(1);
        assertThat(result.getMaterials().get(0).getIsSufficient()).isFalse();
        assertThat(result.getMaterials().get(0).getNeededQuantity()).isEqualTo(250.0);
        assertThat(result.getMaterials().get(0).getAvailableQuantity()).isEqualTo(100.0);
        assertThat(result.getMaterials().get(0).getMissingQuantity()).isEqualTo(150.0);
    }
}
