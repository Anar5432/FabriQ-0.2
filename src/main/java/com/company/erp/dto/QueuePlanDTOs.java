package com.company.erp.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDate;
import java.util.List;
import java.util.Map;

public class QueuePlanDTOs {

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    public static class QueueSimulationRequest {
        private String conveyorLine; // "ALL", "Workwear", "Underwear-boxer", "Socks"
        private Integer defaultWorkers;
        private String difficulty; // "EASY", "HARD"
        private Map<String, OrderOverrideDTO> orderOverrides;
    }

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    public static class OrderOverrideDTO {
        private Integer workers;
        private String difficulty;
    }

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    public static class QueuePlanItemDTO {
        private String orderId;
        private String productTypeId;
        private String productName;
        private String category;
        private String conveyorLine;
        private Integer quantity;
        private Integer queuePosition;
        private Integer workers;
        private String difficulty;
        private Double dailyCuttingRate;
        private Double dailySewingRate;
        private Double cuttingDays;
        private Double sewingDays;
        private Double totalManufacturingDays;
        private LocalDate orderDate;
        private LocalDate plannedStartDate;
        private LocalDate projectCompletionDate;
        private LocalDate deadline;
        private Long delayDays;
        private Integer extraWorkersNeeded;
        private Boolean materialShortage;
        private String shortageDetails;
        private String status;
    }

    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Builder
    public static class ApplyQueueRequest {
        private String conveyorLine;
        private Integer defaultWorkers;
        private String difficulty;
        private List<QueuePlanItemDTO> plans;
    }
}
