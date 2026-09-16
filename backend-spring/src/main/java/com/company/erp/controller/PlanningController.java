package com.company.erp.controller;

import com.company.erp.modules.dashboard.model.OrderSnapshot;
import com.company.erp.repository.OrderSnapshotRepository;
import com.company.erp.service.PlanningService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

@RequiredArgsConstructor
@RestController
@RequestMapping("/api/planning")
@CrossOrigin(origins = "*")
public class PlanningController {

    private final PlanningService planningService;
    private final OrderSnapshotRepository orderRepo;

    @RequestMapping(value = "/timeline/{orderId}", method = {RequestMethod.GET, RequestMethod.POST})
    public OrderSnapshot calculateTimeline(@PathVariable String orderId) {
        planningService.calculateProductionTimeline(orderId);
        return orderRepo.findById(orderId).orElseThrow();
    }

    @RequestMapping(value = "/check-readiness/{orderId}", method = {RequestMethod.GET, RequestMethod.POST})
    public OrderSnapshot checkReadiness(@PathVariable String orderId) {
        planningService.checkOrderReadiness(orderId);
        return orderRepo.findById(orderId).orElseThrow();
    }

    @RequestMapping(value = "/backward/{orderId}", method = {RequestMethod.GET, RequestMethod.POST})
    public OrderSnapshot calculateBackward(@PathVariable String orderId) {
        planningService.calculateBackwardRequirements(orderId);
        return orderRepo.findById(orderId).orElseThrow();
    }

    @RequestMapping(value = "/lock-material/{orderId}", method = {RequestMethod.GET, RequestMethod.POST})
    public OrderSnapshot lockMaterial(@PathVariable String orderId) {
        planningService.lockMaterialForOrder(orderId);
        return orderRepo.findById(orderId).orElseThrow();
    }

    @PostMapping("/simulate-queue")
    public java.util.List<com.company.erp.dto.QueuePlanDTOs.QueuePlanItemDTO> simulateQueue(
            @RequestBody(required = false) com.company.erp.dto.QueuePlanDTOs.QueueSimulationRequest request) {
        return planningService.simulateQueuePlanning(request);
    }

    @PostMapping("/apply-queue")
    public java.util.List<OrderSnapshot> applyQueue(
            @RequestBody(required = false) com.company.erp.dto.QueuePlanDTOs.ApplyQueueRequest request) {
        return planningService.applyQueuePlanning(request);
    }

    @PostMapping("/check-materials")
    public com.company.erp.dto.PlanningStudioDTOs.MaterialCheckResult checkMaterials(
            @RequestBody com.company.erp.dto.PlanningStudioDTOs.MaterialCheckRequest request) {
        return planningService.checkMaterialAvailability(request);
    }

    @PostMapping("/forward")
    public com.company.erp.dto.PlanningStudioDTOs.ForwardPlanningResult forwardPlanning(
            @RequestBody com.company.erp.dto.PlanningStudioDTOs.ForwardPlanningRequest request) {
        return planningService.executeForwardPlanning(request);
    }

    @PostMapping("/backward")
    public com.company.erp.dto.PlanningStudioDTOs.BackwardPlanningResult backwardPlanning(
            @RequestBody com.company.erp.dto.PlanningStudioDTOs.BackwardPlanningRequest request) {
        return planningService.executeBackwardPlanning(request);
    }
}
