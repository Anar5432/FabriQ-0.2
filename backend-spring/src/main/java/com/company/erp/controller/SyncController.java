package com.company.erp.controller;

import com.company.erp.repository.OrderSnapshotRepository;
import com.company.erp.service.LegacyService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
public class SyncController {

    private final LegacyService legacyService;
    private final OrderSnapshotRepository orderRepo;

    @GetMapping("/api/sync")
    public ResponseEntity<Map<String, Object>> triggerSync() {
        legacyService.syncOrdersFromLegacy();
        long total = orderRepo.count();
        Map<String, Object> res = new HashMap<>();
        res.put("status", "SUCCESS");
        res.put("totalOrders", total);
        res.put("message", "MS SQL serverindən sifarişlər uğurla yeniləndi (Cəmi: " + total + " sifariş).");
        return ResponseEntity.ok(res);
    }

    @GetMapping("/api/sync/status")
    public ResponseEntity<Map<String, Object>> getSyncStatus() {
        Map<String, Object> map = new HashMap<>();
        map.put("version", legacyService.getDataVersion());
        map.put("lastSyncTime", legacyService.getLastSyncTime().toString());
        map.put("totalOrders", orderRepo.count());
        return ResponseEntity.ok(map);
    }

    @GetMapping("/api/sync/inventory")
    public String syncInventory() {
        legacyService.syncInventoryFromLegacy();
        return "Inventory sync completed successfully!";
    }
}
