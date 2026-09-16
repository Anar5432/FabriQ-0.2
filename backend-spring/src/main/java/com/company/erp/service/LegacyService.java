package com.company.erp.service;

import com.company.erp.modules.catalog.model.Material;
import com.company.erp.modules.catalog.model.ProductType;
import com.company.erp.modules.dashboard.model.OrderSnapshot;
import com.company.erp.modules.inventory.model.InventoryBalance;
import com.company.erp.repository.InventoryBalanceRepository;
import com.company.erp.repository.MaterialRepository;
import com.company.erp.repository.OrderSnapshotRepository;
import com.company.erp.repository.ProductTypeRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.context.event.ApplicationReadyEvent;
import org.springframework.context.event.EventListener;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
@Slf4j
public class LegacyService {

    private final OrderSnapshotRepository orderRepo;
    private final InventoryBalanceRepository inventoryRepo;
    private final MaterialRepository materialRepo;
    private final ProductTypeRepository productTypeRepo;

    @Value("${spring.legacy-db.url}")
    String legacyUrl;

    @Value("${spring.legacy-db.coraba-url:${spring.legacy-db.url}}")
    String corabaUrl;

    @Value("${spring.legacy-db.username}")
    String legacyUsername;

    @Value("${spring.legacy-db.password}")
    String legacyPassword;

    @EventListener(ApplicationReadyEvent.class)
    public void onStartup() {
        log.info("Application started: Triggering initial ERP synchronization...");
        try {
            syncOrdersFromLegacy();
        } catch (Exception e) {
            log.warn("Initial sync encountered an issue: {}", e.getMessage());
        }
    }

    @Scheduled(fixedRate = 600000) // Every 10 minutes
    public void scheduledSync() {
        log.info("Running scheduled ERP synchronization...");
        syncOrdersFromLegacy();
    }

    private Connection getResilientConnection(String primaryUrl) throws Exception {
        // Try primary URL first
        try {
            return DriverManager.getConnection(primaryUrl, legacyUsername, legacyPassword);
        } catch (Exception e1) {
            // If primary failed, try alternative IP (192.168.100.1 <-> 81.17.87.85)
            String altUrl;
            if (primaryUrl.contains("192.168.100.1")) {
                altUrl = primaryUrl.replace("192.168.100.1", "81.17.87.85");
            } else if (primaryUrl.contains("81.17.87.85")) {
                altUrl = primaryUrl.replace("81.17.87.85", "192.168.100.1");
            } else {
                throw e1;
            }
            log.info("Primary URL connection failed, attempting alternative: {}", altUrl);
            return DriverManager.getConnection(altUrl, legacyUsername, legacyPassword);
        }
    }

    public synchronized void syncOrdersFromLegacy() {
        log.info("Starting ERP Order Synchronization...");

        // 1. Sync Workwear and Underwear from BTFERPDB
        syncFromDatabase(legacyUrl, "BTFERPDB (Workwear & Underwear)", false);

        // 2. Sync Socks from BTFERPDB_CORABA
        syncFromDatabase(corabaUrl, "BTFERPDB_CORABA (Socks Factory)", true);

        log.info("ERP Order Synchronization complete. Total orders in DB: {}", orderRepo.count());
    }

    private void syncFromDatabase(String dbUrl, String dbLabel, boolean isSocksDb) {
        log.info("Connecting to legacy database: {}", dbLabel);
        String sql = """
            WITH AllOrderLines AS (
                SELECT
                    COALESCE(s.sen_no, CAST(s.idn AS VARCHAR)) AS sen_no,
                    s.idn AS legacy_id,
                    ISNULL(c.name, N'B2B Sifarişçi') AS customer_name,
                    g.name AS product_name,
                    g.class AS product_class,
                    e.miqdar AS qty,
                    s.tarix AS order_date,
                    s.tes AS tesdiq,
                    'sm_sifaris_form' AS src
                FROM sm_sifaris_form s WITH (NOLOCK)
                JOIN sm_sifaris_form_el e WITH (NOLOCK) ON e.es_no = s.idn
                LEFT JOIN sm_kontra c WITH (NOLOCK) ON s.kontra = c.idn
                JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
                WHERE s.tarix >= DATEADD(MONTH, -6, GETDATE())

                UNION ALL

                SELECT
                    COALESCE(s.sen_no, CAST(s.idn AS VARCHAR)) AS sen_no,
                    s.idn AS legacy_id,
                    ISNULL(COALESCE(c.name, s.kontra_name), N'B2B Sifarişçi') AS customer_name,
                    g.name AS product_name,
                    g.class AS product_class,
                    e.miqdar AS qty,
                    s.tarix AS order_date,
                    0 AS tesdiq,
                    'sm_sif_sened' AS src
                FROM sm_sif_sened s WITH (NOLOCK)
                JOIN sm_sif_sened_el e WITH (NOLOCK) ON e.es_no = s.idn
                LEFT JOIN sm_kontra c WITH (NOLOCK) ON s.kontra = c.idn
                JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
                WHERE s.tarix >= DATEADD(MONTH, -6, GETDATE())
                  AND NOT EXISTS (SELECT 1 FROM sm_sifaris_form sf WITH (NOLOCK) WHERE sf.sifaris = s.idn)
            )
            SELECT TOP 250
                sen_no,
                MAX(legacy_id) AS legacy_id,
                MAX(customer_name) AS customer_name,
                MAX(product_name) AS sample_product,
                MAX(product_class) AS sample_class,
                COUNT(*) AS item_count,
                SUM(qty) AS total_qty,
                MAX(order_date) AS order_date,
                MAX(tesdiq) AS tesdiq,
                MAX(src) AS src
            FROM AllOrderLines
            GROUP BY sen_no
            ORDER BY MAX(order_date) DESC, sen_no DESC
        """;

        try (Connection conn = getResilientConnection(dbUrl);
             PreparedStatement stmt = conn.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {

            int count = 0;
            while (rs.next()) {
                String senNo = rs.getString("sen_no");
                if (senNo == null || senNo.isBlank()) continue;

                double totalQty = rs.getDouble("total_qty");
                int tesdiq = rs.getInt("tesdiq");
                java.sql.Date legacyDate = rs.getDate("order_date");
                String companyName = rs.getString("customer_name");
                String sampleProd = rs.getString("sample_product");
                int prodClass = rs.getInt("sample_class");
                String src = rs.getString("src");

                OrderSnapshot order = orderRepo.findById(senNo).orElse(new OrderSnapshot());
                order.setId(senNo);
                order.setQuantity(totalQty > 0 ? (int) Math.round(totalQty) : 100);
                order.setTesdiqStatus(tesdiq);
                order.setIsHypothetical(false);
                order.setCustomerName(companyName != null && !companyName.isBlank() ? companyName.trim() : "B2B Sifarişçi");

                // Determine Category and Product Type
                String category = resolveCategory(sampleProd, prodClass, isSocksDb);
                ProductType pt = resolveProductType(sampleProd, prodClass, category);
                order.setProductType(pt);
                order.setConveyorLine(category);

                if (legacyDate != null) {
                    order.setOrderDate(legacyDate.toLocalDate());
                } else {
                    order.setOrderDate(LocalDate.now());
                }

                if (order.getDeadline() == null) {
                    order.setDeadline(order.getOrderDate().plusDays(25));
                }

                // Stage and Status mapping
                if ("sm_sifaris_form".equals(src) || tesdiq == 1) {
                    order.setStatus("APPROVED_IN_PRODUCTION");
                    if ("Socks".equals(category)) {
                        order.setCurrentPhase("Hörgü (Knitting)");
                    } else {
                        order.setCurrentPhase("Tikiş");
                    }
                    order.setDeliveredQuantity((int) (order.getQuantity() * 0.25));
                } else {
                    order.setStatus("DRAFT_QUOTATION");
                    order.setCurrentPhase("Dizayn & Sifariş");
                    order.setDeliveredQuantity(0);
                }

                order.setMaterialReadinessPct(100);
                order.setMaterialShortage(false);
                order.setShortageDetails("");

                orderRepo.save(order);
                count++;
            }
            log.info("Successfully synchronized {} aggregated orders from {}", count, dbLabel);

        } catch (Exception e) {
            log.warn("Could not connect to {}: {}. (Remote server may be currently offline or behind firewall; using existing snapshots)",
                    dbLabel, e.getMessage());
        }
    }

    public String resolveCategory(String prodName, int prodClass, boolean isSocksDb) {
        if (isSocksDb || prodClass == 1 || prodClass == 2 || prodClass == 3 || prodClass == 21 || prodClass == 29 || prodClass == 30) {
            return "Socks";
        }
        String p = prodName != null ? prodName.toUpperCase() : "";
        if (p.contains("CORAB") || p.contains("SOCKS")) {
            return "Socks";
        }
        if (prodClass == 20 || p.contains("BOXER") || p.contains("MAYKA") || p.contains("KÜLOT") || p.contains("KULOT") || p.contains("SLİP") || p.contains("SLIP") || p.contains("PENYE")) {
            return "Underwear-boxer";
        }
        return "Workwear";
    }

    private ProductType resolveProductType(String prodName, int prodClass, String category) {
        String p = prodName != null ? prodName.toUpperCase() : "";

        if ("Socks".equals(category)) {
            if (p.contains("QADIN")) return getProduct("qadin_corabi", "idman_corabi");
            if (p.contains("QIŞ") || p.contains("QALIN")) return getProduct("qis_corabi", "idman_corabi");
            if (p.contains("KOSAK")) return getProduct("kosak_corabi", "idman_corabi");
            return getProduct("idman_corabi", "qis_corabi");
        }

        if ("Underwear-boxer".equals(category)) {
            if (p.contains("MAYKA") || p.contains("T-SH")) return getProduct("mayka", "boxer");
            if (p.contains("KÜLOT") || p.contains("KULOT") || p.contains("SLİP")) return getProduct("kulot", "boxer");
            return getProduct("boxer", "mayka");
        }

        // Workwear
        if (p.contains("HUDİ") || p.contains("HUDI") || p.contains("PAPAQLI")) return getProduct("polar_godekce", "godekce");
        if (p.contains("OVERSİZE") || p.contains("OVERSIZE") || p.contains("TOMMY")) return getProduct("polo", "kitel");
        if (p.contains("ŞALVAR") || p.contains("SALVAR")) return getProduct("salvar", "kitel");
        if (p.contains("GÖDƏKCƏ") || p.contains("GODEKCE") || p.contains("JAKET")) return getProduct("godekce", "kitel");
        if (p.contains("POLAR")) return getProduct("polar_godekce", "kitel");
        if (p.contains("POLO")) return getProduct("polo", "kitel");
        if (p.contains("ÖNLÜK") || p.contains("ONLUK")) return getProduct("onluk", "kitel");
        if (p.contains("PAPAQ")) return getProduct("papaq", "kitel");
        if (p.contains("XALAT")) return getProduct("xalat", "kitel");
        if (p.contains("JİLET") || p.contains("JILET")) return getProduct("ixare_jileti", "kitel");
        if (p.contains("YAĞMURLUQ") || p.contains("YAGMURLUQ")) return getProduct("yagmurluq", "kitel");
        return getProduct("kitel", "salvar");
    }

    private ProductType getProduct(String primaryId, String fallbackId) {
        return productTypeRepo.findById(primaryId)
                .orElseGet(() -> productTypeRepo.findById(fallbackId)
                        .orElseGet(() -> productTypeRepo.findAll().stream().findFirst().orElse(null)));
    }

    public void syncInventoryFromLegacy() {
        log.info("Starting legacy inventory synchronization...");
        try (Connection conn = getResilientConnection(legacyUrl);
             PreparedStatement stmt = conn.prepareStatement("SELECT TOP 50 idn, say FROM sm_mal_say");
             ResultSet rs = stmt.executeQuery()) {

            int count = 0;
            while (rs.next()) {
                String legacyMaterialId = rs.getString("idn");
                Double legacyQuantity = rs.getDouble("say");
                Optional<Material> materialOpt = materialRepo.findById(legacyMaterialId);
                if (materialOpt.isPresent()) {
                    Material material = materialOpt.get();
                    List<InventoryBalance> balances = inventoryRepo.findAllByMaterial(material);
                    InventoryBalance balance = balances.isEmpty() ? new InventoryBalance() : balances.get(0);

                    balance.setMaterial(material);
                    balance.setAvailableQuantity(legacyQuantity);
                    balance.setWarehouseCode("MAIN_WH");
                    balance.setLastUpdate(LocalDateTime.now());
                    inventoryRepo.save(balance);
                    count++;
                }
            }
            log.info("Inventory sync complete: {} items updated", count);
        } catch (Exception e) {
            log.warn("Legacy inventory sync error: {}", e.getMessage());
        }
    }
}
