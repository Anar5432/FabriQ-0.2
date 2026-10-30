package com.company.erp.service;

import com.company.erp.modules.catalog.model.Material;
import com.company.erp.modules.catalog.model.ProductType;
import com.company.erp.modules.dashboard.model.OrderSnapshot;
import com.company.erp.modules.dashboard.model.OrderSubItem;
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
import java.time.Instant;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.atomic.AtomicLong;

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

    private final AtomicLong dataVersion = new AtomicLong(1);
    private volatile Instant lastSyncTime = Instant.now();
    private volatile String lastSeenFingerprint = "";

    public long getDataVersion() {
        return dataVersion.get();
    }

    public Instant getLastSyncTime() {
        return lastSyncTime;
    }

    @EventListener(ApplicationReadyEvent.class)
    public void onStartup() {
        log.info("Application started: Triggering initial ERP synchronization from MS SQL (81.17.85.185)...");
        try {
            syncOrdersFromLegacy();
        } catch (Exception e) {
            log.warn("Initial sync encountered an issue: {}", e.getMessage());
        }
    }

    @Scheduled(initialDelay = 120000, fixedRate = 300000) // Periodic backup full refresh every 5 minutes
    public void scheduledSync() {
        log.info("Running periodic background ERP synchronization check...");
        try {
            syncOrdersFromLegacy();
        } catch (Throwable t) {
            log.warn("Scheduled sync error: {}", t.getMessage());
        }
    }

    private String getDbFingerprint(String dbUrl) {
        String sql = """
            SELECT
                (SELECT ISNULL(MAX(idn), 0) FROM sm_sif_sened WITH (NOLOCK)) AS max_sened,
                (SELECT ISNULL(MAX(idn), 0) FROM sm_sifaris_form WITH (NOLOCK)) AS max_form,
                (SELECT ISNULL(CHECKSUM_AGG(BINARY_CHECKSUM(idn, tes)), 0)
                 FROM (SELECT TOP 250 idn, tes FROM sm_sifaris_form WITH (NOLOCK) ORDER BY idn DESC) f) AS chk_form,
                (SELECT ISNULL(CHECKSUM_AGG(BINARY_CHECKSUM(idn, ISNULL(sat_miq, 0), miqdar)), 0)
                 FROM (SELECT TOP 500 idn, sat_miq, miqdar FROM sm_sif_sened_el WITH (NOLOCK) ORDER BY idn DESC) el) AS chk_el
        """;
        try (Connection conn = getResilientConnection(dbUrl);
             PreparedStatement stmt = conn.prepareStatement(sql);
             ResultSet rs = stmt.executeQuery()) {
            if (rs.next()) {
                return rs.getLong("max_sened") + ":" + rs.getLong("max_form") + ":" + rs.getLong("chk_form") + ":" + rs.getLong("chk_el");
            }
        } catch (Throwable t) {
            log.debug("Fingerprint check query failed for {}: {}", dbUrl, t.getMessage());
        }
        return "0:0:0:0";
    }

    // Live Heartbeat: checks every 10 seconds across BOTH databases (Workwear & Socks) for ANY new order or update!
    @Scheduled(initialDelay = 10000, fixedDelay = 5000) // ⚡ Real-time 5-second Live Heartbeat
    public void liveHeartbeatSync() {
        try {
            String fpWorkwear = getDbFingerprint(legacyUrl);
            String fpSocks = getDbFingerprint(corabaUrl);
            String currentFingerprint = fpWorkwear + "|" + fpSocks;

            if (!lastSeenFingerprint.isEmpty() && !currentFingerprint.equals(lastSeenFingerprint)) {
                log.info("⚡ Real-time update detected in ERP MS SQL database! (Fingerprint changed: {} -> {}). Triggering instant live sync...",
                        lastSeenFingerprint, currentFingerprint);
                syncOrdersFromLegacy();
            }
            lastSeenFingerprint = currentFingerprint;
        } catch (Throwable e) {
            log.debug("Live heartbeat error: {}", e.getMessage());
        }
    }

    private Connection getResilientConnection(String primaryUrl) throws Exception {
        try {
            return DriverManager.getConnection(primaryUrl, legacyUsername, legacyPassword);
        } catch (Exception e1) {
            String altUrl;
            if (primaryUrl.contains("81.17.85.185")) {
                altUrl = primaryUrl.replace("81.17.85.185", "192.168.100.1");
            } else if (primaryUrl.contains("192.168.100.1")) {
                altUrl = primaryUrl.replace("192.168.100.1", "81.17.85.185");
            } else {
                throw e1;
            }
            log.info("Primary URL connection failed, attempting alternative: {}", altUrl);
            return DriverManager.getConnection(altUrl, legacyUsername, legacyPassword);
        }
    }

    public synchronized void syncOrdersFromLegacy() {
        log.info("Starting ERP Order Synchronization from MS SQL (81.17.85.185)...");

        // 1. Sync Workwear and Underwear from BTFERPDB
        syncFromDatabase(legacyUrl, "BTFERPDB (Workwear & Underwear)", false);

        // 2. Sync Socks from BTFERPDB_CORABA
        syncFromDatabase(corabaUrl, "BTFERPDB_CORABA (Socks Factory)", true);

        long newVersion = dataVersion.incrementAndGet();
        lastSyncTime = Instant.now();
        log.info("ERP Order Synchronization complete. Data Version: {}, Total orders in DB: {}", newVersion, orderRepo.count());
    }

        private void syncFromDatabase(String dbUrl, String dbLabel, boolean isSocksDb) {
        log.info("Connecting to legacy database: {}", dbLabel);
        
        // Pre-fetch BOM normalized cut map for apparel garments
        java.util.Map<Integer, Integer> bomCutMap = new java.util.HashMap<>();
        if (!isSocksDb) {
            String bomSql = """
                SELECT sub.sifaris, ISNULL(SUM(sub.max_cut), 0) AS bom_cut
                FROM (
                    SELECT f.sifaris, el.esas_mal, MAX(e.miqdar) AS max_cut
                    FROM sm_good_ist i WITH (NOLOCK)
                    JOIN sm_good_ist_el e WITH (NOLOCK) ON i.idn = e.es_no
                    JOIN sm_sifaris_form f WITH (NOLOCK) ON i.sif_no = f.idn
                    JOIN sm_sifaris_form_el el WITH (NOLOCK) ON f.idn = el.es_no AND e.mal = el.mal
                    WHERE e.son_faza = 4 AND i.tarix >= DATEADD(MONTH, -6, GETDATE())
                    GROUP BY f.sifaris, f.idn, el.esas_mal
                ) sub
                GROUP BY sub.sifaris
            """;
            try (Connection bConn = getResilientConnection(dbUrl);
                 PreparedStatement bStmt = bConn.prepareStatement(bomSql);
                 ResultSet bRs = bStmt.executeQuery()) {
                while (bRs.next()) {
                    bomCutMap.put(bRs.getInt("sifaris"), bRs.getInt("bom_cut"));
                }
            } catch (Exception bEx) {
                log.debug("BOM cut map fetch notice for {}: {}", dbLabel, bEx.getMessage());
            }
        }

        String sql = """
            WITH OrderCategoryBreakdown AS (
                SELECT
                    s.idn AS order_id,
                    COALESCE(s.sen_no, CAST(s.idn AS VARCHAR)) AS sen_no,
                    s.tarix AS order_date,
                    s.status AS erp_status,
                    ISNULL(COALESCE(c.name, s.kontra_name), N'B2B Sifarişçi') AS customer_name,
                    SUM(e.miqdar) AS total_ordered,
                    
                    SUM(CASE 
                        WHEN g.class = 20 OR g.name LIKE '%BOXER%' OR g.name LIKE '%MAYKA%' OR g.name LIKE '%KULOT%' 
                             OR g.name LIKE '%SLIP%' OR g.name LIKE '%POLO CLUB%' THEN e.miqdar 
                        ELSE 0 
                    END) AS qty_underwear,
                    
                    SUM(CASE 
                        WHEN g.class IN (21, 29, 30) OR g.name LIKE '%CORAB%' THEN e.miqdar 
                        ELSE 0 
                    END) AS qty_socks,
                    
                    SUM(CASE 
                        WHEN (g.class NOT IN (20, 21, 29, 30) OR g.class IS NULL)
                             AND g.name NOT LIKE '%BOXER%' AND g.name NOT LIKE '%MAYKA%' AND g.name NOT LIKE '%KULOT%' 
                             AND g.name NOT LIKE '%SLIP%' AND g.name NOT LIKE '%POLO CLUB%' AND g.name NOT LIKE '%CORAB%' 
                        THEN e.miqdar 
                        ELSE 0 
                    END) AS qty_workwear,
                    
                    (SELECT TOP 1 g2.name 
                     FROM sm_sif_sened_el e2 WITH (NOLOCK)
                     JOIN sm_goods g2 WITH (NOLOCK) ON e2.mal = g2.idn 
                     WHERE e2.es_no = s.idn 
                     ORDER BY e2.miqdar DESC) AS top_product_name,
                     
                    ISNULL((SELECT SUM(ks_el.miqdar) 
                            FROM sm_kontr_sat ks WITH (NOLOCK)
                            JOIN sm_kontr_sat_el ks_el WITH (NOLOCK) ON ks.idn = ks_el.es_no 
                            WHERE ks.sif_sen = s.idn), 0) AS waybill_delivered,

                    ISNULL((SELECT SUM(tel.miqdar)
                            FROM sm_sob_trans t WITH (NOLOCK)
                            JOIN sm_sob_trans_el tel WITH (NOLOCK) ON t.idn = tel.es_no 
                            WHERE t.el_sif = s.idn AND t.sobe2 IN (1, 6, 15) AND t.tarix >= s.tarix), 0) AS wh_arrived,

                    ISNULL((SELECT SUM(ge.miqdar)
                            FROM sm_good_ist gi WITH (NOLOCK)
                            JOIN sm_good_ist_el ge WITH (NOLOCK) ON gi.idn = ge.es_no 
                            WHERE (gi.el_sif = s.idn OR gi.sif_no IN (SELECT idn FROM sm_sifaris_form WITH (NOLOCK) WHERE sifaris = s.idn))
                              AND ge.son_faza = 5 AND gi.tarix >= s.tarix), 0) AS sewn_qty,

                    ISNULL((SELECT SUM(ge.miqdar)
                            FROM sm_good_ist gi WITH (NOLOCK)
                            JOIN sm_good_ist_el ge WITH (NOLOCK) ON gi.idn = ge.es_no 
                            WHERE (gi.el_sif = s.idn OR gi.sif_no IN (SELECT idn FROM sm_sifaris_form WITH (NOLOCK) WHERE sifaris = s.idn))
                              AND ge.son_faza = 4 AND gi.tarix >= s.tarix), 0) AS cut_qty_raw

                FROM sm_sif_sened s WITH (NOLOCK)
                JOIN sm_sif_sened_el e WITH (NOLOCK) ON s.idn = e.es_no
                LEFT JOIN sm_kontra c WITH (NOLOCK) ON s.kontra = c.idn
                JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn
                WHERE s.tarix >= DATEADD(MONTH, -6, GETDATE())
                GROUP BY s.idn, s.sen_no, s.tarix, s.status, c.name, s.kontra_name
            )
            SELECT TOP 250
                order_id,
                sen_no,
                order_date,
                erp_status,
                customer_name,
                total_ordered,
                waybill_delivered,
                wh_arrived,
                sewn_qty,
                cut_qty_raw,
                top_product_name,
                CASE 
                    WHEN ? = 1 THEN 'Socks'
                    WHEN qty_underwear >= qty_socks AND qty_underwear >= qty_workwear AND qty_underwear > 0 THEN 'Underwear-boxer'
                    WHEN qty_socks > qty_underwear AND qty_socks >= qty_workwear THEN 'Socks'
                    ELSE 'Workwear'
                END AS dominant_category
            FROM OrderCategoryBreakdown
            ORDER BY order_date DESC, sen_no DESC;
        """;

        try (Connection conn = getResilientConnection(dbUrl);
             PreparedStatement stmt = conn.prepareStatement(sql)) {

            stmt.setInt(1, isSocksDb ? 1 : 0);

            try (ResultSet rs = stmt.executeQuery()) {
                int count = 0;
                while (rs.next()) {
                    String senNo = rs.getString("sen_no");
                    if (senNo == null || senNo.isBlank()) continue;

                    int orderId = rs.getInt("order_id");
                    double totalQty = rs.getDouble("total_ordered");
                    int erpStatus = rs.getInt("erp_status");
                    java.sql.Date legacyDate = rs.getDate("order_date");
                    String companyName = rs.getString("customer_name");
                    String sampleProd = rs.getString("top_product_name");
                    String dominantCat = rs.getString("dominant_category");
                    double waybillDelivered = rs.getDouble("waybill_delivered");
                    double whArrived = rs.getDouble("wh_arrived");
                    double sewnQty = rs.getDouble("sewn_qty");
                    double cutQtyRaw = rs.getDouble("cut_qty_raw");

                    int totalOrdered = totalQty > 0 ? (int) Math.round(totalQty) : 100;
                    int bomCut = bomCutMap.getOrDefault(orderId, 0);
                    int effCut = bomCut > 0 ? bomCut : (int) Math.round(cutQtyRaw);

                    OrderSnapshot order = orderRepo.findById(senNo).orElse(new OrderSnapshot());
                    order.setId(senNo);
                    order.setQuantity(totalOrdered);
                    order.setTesdiqStatus(erpStatus);
                    order.setIsHypothetical(false);
                    order.setCustomerName(companyName != null && !companyName.isBlank() ? companyName.trim() : "B2B Sifarişçi");

                    // Determine Category and Product Type
                    String category = (dominantCat != null && !dominantCat.isBlank()) ? dominantCat : resolveCategory(sampleProd, 0, isSocksDb);
                    ProductType pt = resolveProductType(sampleProd, 0, category);
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

                    // 5-Stage Precise Physical Quantities Calculation
                    int D = Math.min(totalOrdered, (int) Math.round(waybillDelivered));
                    int W = Math.max(0, Math.min(totalOrdered - D, (int) Math.round(whArrived) - D));
                    int S = Math.max(0, Math.min(totalOrdered - D - W, (int) Math.round(sewnQty) - (int) Math.round(whArrived)));
                    int C;
                    if (isSocksDb || "Socks".equals(category)) {
                        C = 0;
                    } else {
                        C = Math.max(0, Math.min(totalOrdered - D - W - S, effCut - (int) Math.round(sewnQty)));
                    }
                    int P = Math.max(0, totalOrdered - (D + W + S + C));

                    order.setDeliveredQuantity(D);
                    order.setWarehouseQuantity(W);
                    order.setSewingQuantity(S);
                    order.setCuttingQuantity(C);
                    order.setQueueQuantity(P);

                    // Stage & Status Mapping
                    if (D >= totalOrdered && totalOrdered > 0) {
                        order.setCurrentPhase("Çatdırılıb");
                        order.setStatus("TAMAMLANDI");
                    } else if (W > 0 && S == 0 && C == 0) {
                        order.setCurrentPhase("Anbarda (Hazır)");
                        order.setStatus("WAREHOUSE_READY");
                    } else if (S > 0) {
                        order.setCurrentPhase((isSocksDb || "Socks".equals(category)) ? "Tikiş (Toe-closing)" : "Tikiş");
                        order.setStatus("APPROVED_IN_PRODUCTION");
                    } else if (C > 0) {
                        order.setCurrentPhase((isSocksDb || "Socks".equals(category)) ? "Hörgü (Knitting)" : "Kəsim");
                        order.setStatus("APPROVED_IN_PRODUCTION");
                    } else if (W > 0) {
                        order.setCurrentPhase("Anbarda (Hazır)");
                        order.setStatus("APPROVED_IN_PRODUCTION");
                    } else if (erpStatus == 0) {
                        order.setCurrentPhase("Dizayn & Sifariş");
                        order.setStatus("DRAFT_QUOTATION");
                    } else {
                        order.setCurrentPhase((isSocksDb || "Socks".equals(category)) ? "Hörgü (Knitting)" : "İstehsalat Növbəsində");
                        order.setStatus("APPROVED_IN_PRODUCTION");
                    }

                    order.setMaterialReadinessPct(100);
                    order.setMaterialShortage(false);
                    if (order.getIsReservationActive() == null) {
                        order.setIsReservationActive(!"TAMAMLANDI".equals(order.getStatus()) && !"Çatdırılıb".equals(order.getCurrentPhase()));
                    }
                    order.setShortageDetails("");

                    // Synchronize granular sub-items from child lines
                    order.getSubItems().clear();

                    // Pre-fetch delivered quantities from waybills for this specific order lines
                    java.util.Map<Integer, Integer> waybillDelivMap = new java.util.HashMap<>();
                    String wbSql = "SELECT ks_el.mal, CAST(SUM(ks_el.miqdar) AS INT) AS deliv_qty FROM sm_kontr_sat ks WITH (NOLOCK) JOIN sm_kontr_sat_el ks_el WITH (NOLOCK) ON ks_el.es_no = ks.idn WHERE ks.sif_sen = ? GROUP BY ks_el.mal";
                    try (PreparedStatement wbStmt = conn.prepareStatement(wbSql)) {
                        wbStmt.setInt(1, orderId);
                        try (ResultSet wbRs = wbStmt.executeQuery()) {
                            while (wbRs.next()) {
                                waybillDelivMap.put(wbRs.getInt("mal"), wbRs.getInt("deliv_qty"));
                            }
                        }
                    } catch (Exception wbEx) {
                        // ignore if waybills table does not support the column in this DB
                    }

                    String itemsSql = "SELECT e.idn AS line_id, e.num AS line_num, e.mal, g.name AS product_name, g.serial AS product_code, e.miqdar AS qty_ordered, ISNULL(e.sat_miq, 0) AS qty_delivered FROM sm_sif_sened_el e WITH (NOLOCK) JOIN sm_goods g WITH (NOLOCK) ON e.mal = g.idn WHERE e.es_no = ? ORDER BY e.num ASC";

                    try (PreparedStatement itemStmt = conn.prepareStatement(itemsSql)) {
                        itemStmt.setInt(1, orderId);
                        try (ResultSet itemRs = itemStmt.executeQuery()) {
                            int idx = 1;
                            while (itemRs.next()) {
                                OrderSubItem subItem = new OrderSubItem();
                                subItem.setOrder(order);
                                int lineNum = itemRs.getInt("line_num");
                                subItem.setLineNum(lineNum > 0 ? lineNum : idx++);
                                subItem.setProductCode(itemRs.getString("product_code"));
                                String pName = itemRs.getString("product_name");
                                subItem.setProductName(pName != null && !pName.isBlank() ? pName.trim() : "Standart Məhsul");
                                double qOrdered = itemRs.getDouble("qty_ordered");
                                double qDeliv = itemRs.getDouble("qty_delivered");
                                int malId = itemRs.getInt("mal");
                                int waybillDeliv = waybillDelivMap.getOrDefault(malId, 0);
                                int effectiveDeliv = (int) Math.round(Math.max(qDeliv, waybillDeliv));

                                int lineOrdered = (int) Math.round(qOrdered);
                                int lineDeliv = Math.min(lineOrdered, effectiveDeliv);
                                double ratio = totalOrdered > 0 ? ((double) lineOrdered / totalOrdered) : 0;
                                int lineW = Math.max(0, Math.min(lineOrdered - lineDeliv, (int) Math.round(W * ratio)));
                                int lineS = Math.max(0, Math.min(lineOrdered - lineDeliv - lineW, (int) Math.round(S * ratio)));
                                int lineC = Math.max(0, Math.min(lineOrdered - lineDeliv - lineW - lineS, (int) Math.round(C * ratio)));
                                int lineP = Math.max(0, lineOrdered - (lineDeliv + lineW + lineS + lineC));

                                subItem.setQuantity(lineOrdered);
                                subItem.setDeliveredQuantity(lineDeliv);
                                subItem.setWarehouseQuantity(lineW);
                                subItem.setSewingQuantity(lineS);
                                subItem.setCuttingQuantity(lineC);
                                subItem.setQueueQuantity(lineP);

                                subItem.setVariantDetails("Standart");

                                if (subItem.getDeliveredQuantity() >= subItem.getQuantity() && subItem.getQuantity() > 0) {
                                    subItem.setCurrentPhase("Çatdırılıb");
                                    subItem.setStatus("TAMAMLANDI");
                                    subItem.setMaterialStatus("READY");
                                    subItem.setMaterialReadinessPct(100);
                                    subItem.setMaterialDetails("Bütün materiallar təmin edilib");
                                } else if ("APPROVED_IN_PRODUCTION".equals(order.getStatus())) {
                                    subItem.setCurrentPhase(order.getCurrentPhase());
                                    subItem.setStatus("APPROVED_IN_PRODUCTION");
                                    subItem.setMaterialStatus("READY");
                                    subItem.setMaterialReadinessPct(100);
                                    subItem.setMaterialDetails("Bütün materiallar anbarda mövcuddur");
                                } else {
                                    subItem.setCurrentPhase("Dizayn & Sifariş");
                                    subItem.setStatus("DRAFT_QUOTATION");
                                    subItem.setMaterialStatus(subItem.getLineNum() % 2 == 0 ? "SOURCING_REQUIRED" : "READY");
                                    subItem.setMaterialReadinessPct(subItem.getLineNum() % 2 == 0 ? 50 : 100);
                                    subItem.setMaterialDetails(subItem.getLineNum() % 2 == 0 ? "Əsas parça / xammal təchizat gözləyir" : "Bütün materiallar anbarda mövcuddur");
                                }

                                order.getSubItems().add(subItem);
                            }
                        }
                    } catch (Exception itemEx) {
                        log.debug("Sub-items fetch notice for order {}: {}", senNo, itemEx.getMessage());
                    }

                    orderRepo.save(order);
                    count++;
                }
                log.info("Successfully synchronized {} aggregated orders from {}", count, dbLabel);
            }
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
        if (prodClass == 20 || p.contains("BOXER") || p.contains("MAYKA") || p.contains("KÜLOT") || p.contains("KULOT") || p.contains("SLİP") || p.contains("SLIP") || p.contains("PENYE") || p.contains("POLO CLUB")) {
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
