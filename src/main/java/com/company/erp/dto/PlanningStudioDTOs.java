package com.company.erp.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;
import java.util.List;

public class PlanningStudioDTOs {

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class MaterialCheckRequest {
        private String productTypeId;
        private Integer quantity;
        private String conveyorLine;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class MaterialCheckItem {
        private String materialId;
        private String materialName;
        private String unit;
        private Double neededQuantity;
        private Double availableQuantity;
        private Double missingQuantity;
        private Boolean isSufficient;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class MaterialCheckResult {
        private String productTypeId;
        private String productName;
        private Integer quantity;
        private Boolean allMaterialsSufficient;
        private List<MaterialCheckItem> materials;
        private Integer recommendedLeadTimeDays;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class StageTimelineItem {
        private String stageId;
        private String stageName;
        private Double days;
        private LocalDate startDate;
        private LocalDate endDate;
        private String status;
        private String details;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class ForwardPlanningRequest {
        private String productTypeId;
        private Integer quantity;
        private String conveyorLine;
        private Integer workers;
        private String difficulty; // EASY, HARD
        private LocalDate startDate;
        private Double designDays;
        private Double sourcingDays;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class ForwardPlanningResult {
        private String productTypeId;
        private String productName;
        private Integer quantity;
        private String conveyorLine;
        private Integer workers;
        private String difficulty;
        private Double dailySewingRate;
        private Double dailyCuttingRate;
        private Double cuttingDays;
        private Double sewingDays;
        private Double totalManufacturingDays;
        private Double designDays;
        private Double sourcingDays;
        private LocalDate startDate;
        private LocalDate cuttingEndDate;
        private LocalDate sewingEndDate;
        private LocalDate deliveryDate;
        private List<StageTimelineItem> stages;
        private String status;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class BackwardPlanningRequest {
        private String productTypeId;
        private Integer quantity;
        private LocalDate customerDeadline;
        private LocalDate startDate;
        private String conveyorLine;
        private Integer baseWorkers;
        private String difficulty; // EASY, HARD
        private Double designDays;
        private Double sourcingDays;
    }

    @Data
    @Builder
    @NoArgsConstructor
    @AllArgsConstructor
    public static class BackwardPlanningResult {
        private String productTypeId;
        private String productName;
        private Integer quantity;
        private LocalDate customerDeadline;
        private LocalDate startDate;
        private Double designDays;
        private Double sourcingDays;
        private Long grossCalendarDays;
        private Long netManufacturingDays;
        private Double standardDurationDays;
        private Boolean isFeasible;
        private Double accelerationFactor;
        private Integer baseWorkers;
        private Integer requiredWorkers;
        private Integer extraWorkersNeeded;
        private Double requiredDailyCuttingRate;
        private Double requiredDailySewingRate;
        private String status;
        private String recommendation;
        private List<StageTimelineItem> stages;
    }
}
