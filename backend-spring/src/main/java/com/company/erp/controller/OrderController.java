package com.company.erp.controller;

import com.company.erp.modules.dashboard.model.OrderSnapshot;
import com.company.erp.modules.dashboard.model.OrderSubItem;
import com.company.erp.repository.OrderSubItemRepository;
import org.springframework.web.bind.annotation.PathVariable;
import com.company.erp.repository.OrderSnapshotRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequiredArgsConstructor
@CrossOrigin(origins = "*")
public class OrderController {

    private final OrderSnapshotRepository orderRepo;
    private final OrderSubItemRepository subItemRepo;

    @GetMapping("/api/orders")
    public List<OrderSnapshot> getOrders() {
        return orderRepo.findAllByOrderByOrderDateDescIdDesc();
    }

    @GetMapping("/api/orders/{id}")
    public ResponseEntity<OrderSnapshot> getOrderById(@PathVariable String id) {
        return orderRepo.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/api/orders/{id}/items")
    public List<OrderSubItem> getOrderItems(@PathVariable String id) {
        return subItemRepo.findByOrder_IdOrderByLineNumAsc(id);
    }

    @GetMapping("/api/orders/batch")
    public ResponseEntity<Map<String, Object>> getOrdersBatch(
            @RequestParam(required = false) String category,
            @RequestParam(required = false) String search,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "50") int size
    ) {
        String cleanSearch = (search != null && !search.isBlank()) ? search.trim().toLowerCase().replace("\u0307", "") : null;
        String unpadded = (cleanSearch != null) ? cleanSearch.replaceFirst("^0+", "") : "";
        if (unpadded.isEmpty() && cleanSearch != null) {
            unpadded = cleanSearch;
        }

        String searchUpper = (search != null && !search.isBlank())
                ? search.trim().toUpperCase()
                        .replace("\u0307", "")
                        .replace("İ", "I")
                        .replace("ı", "I")
                        .replace("Ə", "E")
                        .replace("ə", "E")
                        .replace("Ö", "O")
                        .replace("ö", "O")
                        .replace("Ü", "U")
                        .replace("ü", "U")
                        .replace("Ş", "S")
                        .replace("ş", "S")
                        .replace("Ç", "C")
                        .replace("ç", "C")
                        .replace("Ğ", "G")
                        .replace("ğ", "G")
                        .trim()
                : "";

        String catType = "ALL";
        if (category != null && !category.isBlank() && !"ALL".equalsIgnoreCase(category)) {
            String c = category.trim().toLowerCase();
            if (c.contains("under")) catType = "UNDERWEAR";
            else if (c.contains("sock")) catType = "SOCKS";
            else if (c.contains("work")) catType = "WORKWEAR";
            else catType = c.toUpperCase();
        }

        Pageable pageable = PageRequest.of(Math.max(0, page), Math.min(100, Math.max(1, size)));
        Page<OrderSnapshot> resultPage;

        if (cleanSearch != null) {
            switch (catType) {
                case "WORKWEAR":
                    resultPage = orderRepo.findWorkwearWithSearch(cleanSearch, unpadded, searchUpper, pageable);
                    break;
                case "UNDERWEAR":
                    resultPage = orderRepo.findUnderwearWithSearch(cleanSearch, unpadded, searchUpper, pageable);
                    break;
                case "SOCKS":
                    resultPage = orderRepo.findSocksWithSearch(cleanSearch, unpadded, searchUpper, pageable);
                    break;
                default:
                    resultPage = orderRepo.findAllWithSearch(cleanSearch, unpadded, searchUpper, pageable);
                    break;
            }
        } else {
            switch (catType) {
                case "WORKWEAR":
                    resultPage = orderRepo.findWorkwearOrders(pageable);
                    break;
                case "UNDERWEAR":
                    resultPage = orderRepo.findUnderwearOrders(pageable);
                    break;
                case "SOCKS":
                    resultPage = orderRepo.findSocksOrders(pageable);
                    break;
                default:
                    resultPage = orderRepo.findAllOrdersPaged(pageable);
                    break;
            }
        }

        Map<String, Object> response = new HashMap<>();
        response.put("orders", resultPage.getContent());
        response.put("currentPage", resultPage.getNumber());
        response.put("totalItems", resultPage.getTotalElements());
        response.put("totalPages", resultPage.getTotalPages());
        response.put("hasNext", resultPage.hasNext());

        return ResponseEntity.ok(response);
    }
}
