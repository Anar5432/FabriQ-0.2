package com.company.erp.config;

import com.company.erp.modules.catalog.model.Material;
import com.company.erp.modules.catalog.model.ProductType;
import com.company.erp.modules.catalog.model.RecipeBOM;
import com.company.erp.modules.dashboard.model.OrderSnapshot;
import com.company.erp.modules.inventory.model.InventoryBalance;
import com.company.erp.modules.planning.model.ProductionBaseline;
import com.company.erp.modules.planning.model.WorkerTeam;
import com.company.erp.repository.*;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.List;

@Component
@RequiredArgsConstructor
public class DataInitializer implements CommandLineRunner {

    private final ProductTypeRepository productTypeRepo;
    private final WorkerTeamRepository teamRepo;
    private final ProductionBaselineRepository baselineRepo;
    private final MaterialRepository materialRepo;
    private final RecipeBOMRepository recipeRepo;
    private final InventoryBalanceRepository inventoryRepo;
    private final OrderSnapshotRepository orderRepo;

    @Override
    public void run(String... args) throws Exception {
        System.out.println("=== Ensuring Factory Master Data and Categories ===");

        // ── 1. Worker Teams / Bants ───────────────────────────────────────────
        WorkerTeam workwear = teamRepo.findAll().stream()
                .filter(t -> t.getDepartmentName() != null && t.getDepartmentName().contains("Workwear"))
                .findFirst().orElse(new WorkerTeam());
        workwear.setDepartmentName("Workwear (İş Geyimi)");
        workwear.setWorkerCount(10);
        teamRepo.save(workwear);

        WorkerTeam underwear = teamRepo.findAll().stream()
                .filter(t -> t.getDepartmentName() != null && t.getDepartmentName().contains("Underwear"))
                .findFirst().orElse(new WorkerTeam());
        underwear.setDepartmentName("Underwear-boxer (Alt Geyim)");
        underwear.setWorkerCount(7);
        teamRepo.save(underwear);

        WorkerTeam socks = teamRepo.findAll().stream()
                .filter(t -> t.getDepartmentName() != null && t.getDepartmentName().contains("Socks"))
                .findFirst().orElse(new WorkerTeam());
        socks.setDepartmentName("Socks (Corab)");
        socks.setWorkerCount(10);
        teamRepo.save(socks);

        // ── 2. Product Types & Daily Targets ─────────────────────────────────
        // Workwear (Bant 1)
        ProductType kitel = createProduct("kitel", "Kitel / Tunic", "Workwear");
        createBaseline(kitel, workwear, 150, 100);
        ProductType salvar = createProduct("salvar", "Şalvar / Trousers", "Workwear");
        createBaseline(salvar, workwear, 200, 150);
        ProductType godekce = createProduct("godekce", "Gödəkcə / Jacket", "Workwear");
        createBaseline(godekce, workwear, 120, 80);
        ProductType polar = createProduct("polar_godekce", "Polar Gödəkcə", "Workwear");
        createBaseline(polar, workwear, 250, 170);
        ProductType qisaqol = createProduct("qisaqol_godekce", "Qısaqol Gödəkcə", "Workwear");
        createBaseline(qisaqol, workwear, 200, 150);
        ProductType xalat = createProduct("xalat", "Xalat / Robe", "Workwear");
        createBaseline(xalat, workwear, 250, 200);
        ProductType salvarMed = createProduct("salvar_medical", "Şalvar Medical", "Workwear");
        createBaseline(salvarMed, workwear, 300, 250);
        ProductType yagmurluq = createProduct("yagmurluq", "Yağmurluq / Raincoat", "Workwear");
        createBaseline(yagmurluq, workwear, 300, 250);
        ProductType jilet = createProduct("ixare_jileti", "İxarə Jileti / Vest", "Workwear");
        createBaseline(jilet, workwear, 600, 300);
        ProductType onluk = createProduct("onluk", "Önlük / Apron", "Workwear");
        createBaseline(onluk, workwear, 1000, 1000);
        ProductType polo = createProduct("polo", "Polo T-Shirt", "Workwear");
        createBaseline(polo, workwear, 400, 300);
        ProductType papaq = createProduct("papaq", "Papaq / Cap", "Workwear");
        createBaseline(papaq, workwear, 1000, 500);

        // Underwear-boxer (Bant 2)
        ProductType boxer = createProduct("boxer", "Boxer", "Underwear-boxer");
        createBaseline(boxer, underwear, 1200, 1000);
        ProductType mayka = createProduct("mayka", "Mayka / T-shirt", "Underwear-boxer");
        createBaseline(mayka, underwear, 2400, 2000);
        ProductType kulot = createProduct("kulot", "Külot", "Underwear-boxer");
        createBaseline(kulot, underwear, 2000, 1800);

        // Socks (Bant 3)
        ProductType qisCorab = createProduct("qis_corabi", "Qış Corabı (Qalın)", "Socks");
        createBaseline(qisCorab, socks, 300, 200);
        ProductType idmanCorab = createProduct("idman_corabi", "İkili İdman Corabı", "Socks");
        createBaseline(idmanCorab, socks, 400, 300);
        ProductType qadinCorab = createProduct("qadin_corabi", "Qadın Corabı", "Socks");
        createBaseline(qadinCorab, socks, 500, 400);
        ProductType kosakCorab = createProduct("kosak_corabi", "Kişi Kosak Corabı", "Socks");
        createBaseline(kosakCorab, socks, 350, 250);

        // ── IDEMPOTENCY GUARD ─────────────────────────────────────────────────
        // If BOM rows already exist, skip all material/BOM/inventory seeding.
        // This prevents duplicate rows on every server restart.
        if (recipeRepo.count() > 0) {
            System.out.println("=== BOM already seeded (" + recipeRepo.count() + " rows). Skipping. ===");
            seedSampleOrdersIfNeeded();
            return;
        }
        System.out.println("=== First run: seeding Materials, BOMs, and Inventory ===");

        // ── 3. Materials ──────────────────────────────────────────────────────
        // Workwear
        Material qabardin    = saveMaterial("MAT-QABARDIN",       "Qabardin Parça 16x12",     "METR",  "Boz / Qara");
        Material astar        = saveMaterial("MAT-ASTAR",          "Astar (Ciblik)",            "METR",  "Bej");
        Material duyume       = saveMaterial("MAT-DUYUME",         "Metal Düymə",               "ƏDƏD",  "Gümüşü");
        Material fermuar      = saveMaterial("MAT-FERMUAR",        "Fermuar (Zipper)",          "ƏDƏD",  "Qara");
        Material workwearSap  = saveMaterial("MAT-SAP-WORKWEAR",   "Polyester Sap (Bobin)",     "BOBIN", "Rəngsiz");
        // Underwear
        Material suprem       = saveMaterial("MAT-SUPREM",         "Süprəm Likralı Parça",     "METR",  "Müxtəlif");
        Material belRezin     = saveMaterial("MAT-BEL-REZIN",      "Elastik Bel Rezini",        "METR",  "Ağ");
        Material underwearSap = saveMaterial("MAT-SAP-UNDERWEAR",  "Overlok Sap (Bobin)",       "BOBIN", "Rəngsiz");
        // Socks — ALWAYS KQ (weight), NEVER meters
        Material pambuqIplik  = saveMaterial("MAT-IPLIK-PAMBUQ",   "Pambıq İplik 20/1",        "KQ",    "Müxtəlif");
        Material elastan      = saveMaterial("MAT-ELASTAN",        "Elastan / Likra",           "KQ",    "Ağ");
        Material poliamid     = saveMaterial("MAT-POLIAMID",       "Poliamid İpliyi",           "KQ",    "Qara");
        Material qablasdirma  = saveMaterial("MAT-QABLASDIRMA",    "Qablaşdırma Kartonu",       "ƏDƏD",  "Rəngsiz");

        // ── 4. Recipe BOM (Category-Aware) ───────────────────────────────────
        // WORKWEAR (qabardin + astar + düymə/fermuar + sap — in meters)
        saveBOM(kitel,     qabardin, 1.99); saveBOM(kitel,    astar, 0.40); saveBOM(kitel,    duyume, 4.0); saveBOM(kitel,    workwearSap, 0.025);
        saveBOM(salvar,    qabardin, 1.20); saveBOM(salvar,   fermuar, 1.0); saveBOM(salvar,   workwearSap, 0.020);
        saveBOM(godekce,   qabardin, 2.50); saveBOM(godekce,  astar, 0.80); saveBOM(godekce,  fermuar, 1.0); saveBOM(godekce,  duyume, 3.0); saveBOM(godekce, workwearSap, 0.030);
        saveBOM(polar,     qabardin, 2.30); saveBOM(polar,    astar, 0.60); saveBOM(polar,    fermuar, 1.0); saveBOM(polar,    workwearSap, 0.025);
        saveBOM(qisaqol,   qabardin, 1.80); saveBOM(qisaqol,  astar, 0.50); saveBOM(qisaqol,  fermuar, 1.0); saveBOM(qisaqol,  workwearSap, 0.020);
        saveBOM(xalat,     qabardin, 2.80); saveBOM(xalat,    duyume, 4.0); saveBOM(xalat,    workwearSap, 0.030);
        saveBOM(salvarMed, qabardin, 1.10); saveBOM(salvarMed, fermuar, 1.0); saveBOM(salvarMed, workwearSap, 0.018);
        saveBOM(yagmurluq, qabardin, 2.20); saveBOM(yagmurluq, astar, 0.70); saveBOM(yagmurluq, fermuar, 1.0); saveBOM(yagmurluq, workwearSap, 0.025);
        saveBOM(jilet,     qabardin, 0.80); saveBOM(jilet,    duyume, 5.0); saveBOM(jilet,    workwearSap, 0.015);
        saveBOM(onluk,     qabardin, 0.60); saveBOM(onluk,    workwearSap, 0.010);
        saveBOM(polo,      suprem,   0.50); saveBOM(polo,     underwearSap, 0.015);  // polo is jersey knit
        saveBOM(papaq,     qabardin, 0.15); saveBOM(papaq,    workwearSap, 0.005);

        // UNDERWEAR (süprəm + bel rezini + overlok sap — in meters/bobins)
        saveBOM(boxer, suprem, 0.30); saveBOM(boxer, belRezin, 0.40); saveBOM(boxer, underwearSap, 0.012);
        saveBOM(mayka, suprem, 0.40); saveBOM(mayka, underwearSap, 0.018);
        saveBOM(kulot, suprem, 0.25); saveBOM(kulot, belRezin, 0.30); saveBOM(kulot, underwearSap, 0.010);

        // SOCKS (iplik in KQ — never meters of fabric!)
        saveBOM(qisCorab,   pambuqIplik, 0.120); saveBOM(qisCorab,   elastan, 0.010); saveBOM(qisCorab,   qablasdirma, 1.0);
        saveBOM(idmanCorab, pambuqIplik, 0.085); saveBOM(idmanCorab, elastan, 0.008); saveBOM(idmanCorab, poliamid, 0.015); saveBOM(idmanCorab, qablasdirma, 1.0);
        saveBOM(qadinCorab, pambuqIplik, 0.060); saveBOM(qadinCorab, elastan, 0.012); saveBOM(qadinCorab, qablasdirma, 1.0);
        saveBOM(kosakCorab, pambuqIplik, 0.095); saveBOM(kosakCorab, elastan, 0.009); saveBOM(kosakCorab, qablasdirma, 1.0);

        // ── 5. Warehouse Inventory ────────────────────────────────────────────
        saveInventory(qabardin,    4500.0,  "WH-WORKWEAR");
        saveInventory(astar,       1200.0,  "WH-WORKWEAR");
        saveInventory(duyume,     50000.0,  "WH-WORKWEAR");
        saveInventory(fermuar,     8000.0,  "WH-WORKWEAR");
        saveInventory(workwearSap,  120.0,  "WH-WORKWEAR");
        saveInventory(suprem,       800.0,  "WH-UNDERWEAR");
        saveInventory(belRezin,     600.0,  "WH-UNDERWEAR");
        saveInventory(underwearSap,  80.0,  "WH-UNDERWEAR");
        saveInventory(pambuqIplik,  350.0,  "WH-SOCKS");   // 350 KQ cotton yarn
        saveInventory(elastan,       25.0,  "WH-SOCKS");
        saveInventory(poliamid,      40.0,  "WH-SOCKS");
        saveInventory(qablasdirma, 20000.0, "WH-SOCKS");

        System.out.println("=== BOM Seeding Complete: " + recipeRepo.count() + " recipe rows ===");
        seedSampleOrdersIfNeeded();
        System.out.println("=== Factory Master Data Seeding Complete ===");
    }

    /**
     * Seeds realistic active production orders (5 per category / 15 total) with current
     * dates (August/September 2026) and future deadlines (October/November 2026).
     * Automatically purges legacy remnants older than 90 days so they never pollute the
     * active planning engine or planning studio.
     */
    private void seedSampleOrdersIfNeeded() {
        // 1. Purge legacy remnants older than 90 days from order snapshots
        List<OrderSnapshot> allOrders = orderRepo.findAll();
        for (OrderSnapshot ord : allOrders) {
            if (ord.getOrderDate() != null && ord.getOrderDate().isBefore(LocalDate.now().minusDays(90))) {
                orderRepo.delete(ord);
            }
        }

        // 2. Workwear Orders (Bant 1)
        seedOrderIfNotExists("ORD-WW-01", "kitel", "Workwear", "SOCAR (Neft Emalı Zavodu)", 450, 150, "Tikiş", "APPROVED_IN_PRODUCTION", 10, 20);
        seedOrderIfNotExists("ORD-WW-02", "salvar", "Workwear", "Paşa Holdinq (Tikinti Qrupu)", 800, 200, "Kəsim", "APPROVED_IN_PRODUCTION", 8, 25);
        seedOrderIfNotExists("ORD-WW-03", "godekce", "Workwear", "Azərsu ASC (Su Kanal İdarəsi)", 350, 0, "Material Təchizatı", "MATERIAL_GATHERING", 5, 30);
        seedOrderIfNotExists("ORD-WW-04", "polo", "Workwear", "Baku Steel Company ASC", 1200, 0, "Dizayn & Sifariş", "DRAFT_QUOTATION", 3, 35);
        seedOrderIfNotExists("ORD-WW-05", "polar_godekce", "Workwear", "Norm Sement Zavodu", 600, 600, "Hazır Məhsul", "TAMAMLANDI", 25, 5);

        // 3. Underwear-boxer Orders (Bant 2)
        seedOrderIfNotExists("ORD-UW-01", "boxer", "Underwear-boxer", "Bravo Supermarketlər Şəbəkəsi", 2500, 1000, "Tikiş", "APPROVED_IN_PRODUCTION", 7, 20);
        seedOrderIfNotExists("ORD-UW-02", "mayka", "Underwear-boxer", "Rahat Supermarketlər", 3000, 500, "Kəsim", "APPROVED_IN_PRODUCTION", 5, 25);
        seedOrderIfNotExists("ORD-UW-03", "kulot", "Underwear-boxer", "Bazarstore MMC", 1500, 0, "Material Təchizatı", "MATERIAL_GATHERING", 3, 28);
        seedOrderIfNotExists("ORD-UW-04", "boxer", "Underwear-boxer", "Araz Supermarket Qrupu", 4000, 0, "Dizayn & Sifariş", "DRAFT_QUOTATION", 2, 40);
        seedOrderIfNotExists("ORD-UW-05", "mayka", "Underwear-boxer", "Al Marketlər Şəbəkəsi", 1800, 1800, "Hazır Məhsul", "TAMAMLANDI", 20, 10);

        // 4. Socks Orders (Bant 3)
        seedOrderIfNotExists("ORD-SK-01", "idman_corabi", "Socks", "Silk Way West Airlines", 5000, 2000, "Hörgü (Knitting)", "APPROVED_IN_PRODUCTION", 12, 25);
        seedOrderIfNotExists("ORD-SK-02", "qis_corabi", "Socks", "Azərbaycan Dəmir Yolları QSC", 3500, 1000, "Tikiş (Toe-closing)", "APPROVED_IN_PRODUCTION", 10, 22);
        seedOrderIfNotExists("ORD-SK-03", "qadin_corabi", "Socks", "Azercell Telekom MMC", 2000, 0, "Forma (Boarding)", "APPROVED_IN_PRODUCTION", 6, 18);
        seedOrderIfNotExists("ORD-SK-04", "kosak_corabi", "Socks", "Bakı Metropoliteni QSC", 4000, 0, "Material Təchizatı", "MATERIAL_GATHERING", 4, 30);
        seedOrderIfNotExists("ORD-SK-05", "idman_corabi", "Socks", "Neftçi PFK İdman Klubu", 2500, 2500, "Paket & Anbar", "TAMAMLANDI", 18, 12);
    }

    private void seedOrderIfNotExists(String id, String prodId, String category, String client,
                                      int qty, int deliveredQty, String stage, String status,
                                      int daysAgo, int daysAhead) {
        ProductType pt = productTypeRepo.findById(prodId).orElse(null);
        if (pt == null) return;
        OrderSnapshot ord = orderRepo.findById(id).orElse(new OrderSnapshot());
        ord.setId(id);
        ord.setProductType(pt);
        ord.setConveyorLine(category);
        ord.setCustomerName(client);
        ord.setQuantity(qty);
        ord.setDeliveredQuantity(deliveredQty);
        ord.setCurrentPhase(stage);
        ord.setStatus(status);
        ord.setTesdiqStatus("DRAFT_QUOTATION".equals(status) ? 0 : 1);
        ord.setIsHypothetical(false);
        ord.setOrderDate(LocalDate.now().minusDays(daysAgo));
        ord.setDeadline(LocalDate.now().plusDays(daysAhead));
        ord.setDesignDays(stage.contains("Dizayn") ? 1.0 : 0.0);
        ord.setSourcingDays(stage.contains("Material") ? 2.0 : 0.0);
        ord.setMaterialReadinessPct(deliveredQty > 0 || stage.contains("Tikiş") || stage.contains("Hörgü") ? 100 : 80);
        ord.setMaterialShortage(ord.getMaterialReadinessPct() < 100);
        ord.setShortageDetails(ord.getMaterialShortage() ? "Xammal ehtiyatı çatışmır" : "");
        orderRepo.save(ord);
    }

    private Material saveMaterial(String id, String name, String unit, String color) {
        Material m = materialRepo.findById(id).orElse(new Material());
        m.setId(id); m.setName(name); m.setUnit(unit); m.setColor(color);
        return materialRepo.save(m);
    }

    private void saveBOM(ProductType pt, Material mat, double qty) {
        RecipeBOM bom = new RecipeBOM();
        bom.setProductType(pt); bom.setMaterial(mat); bom.setQuantityPerUnit(qty);
        recipeRepo.save(bom);
    }

    private void saveInventory(Material mat, double qty, String warehouseCode) {
        InventoryBalance inv = new InventoryBalance();
        inv.setMaterial(mat); inv.setAvailableQuantity(qty);
        inv.setWarehouseCode(warehouseCode); inv.setLastUpdate(LocalDateTime.now());
        inventoryRepo.save(inv);
    }

    private ProductType createProduct(String id, String name, String category) {
        ProductType pt = productTypeRepo.findById(id).orElse(new ProductType());
        pt.setId(id); pt.setName(name); pt.setCategory(category);
        return productTypeRepo.save(pt);
    }

    private void createBaseline(ProductType pt, WorkerTeam team, int easy, int hard) {
        ProductionBaseline pb = baselineRepo.findByProductType(pt);
        if (pb == null) pb = new ProductionBaseline();
        pb.setProductType(pt); pb.setWorkerTeam(team);
        pb.setDailyTargetPieces(easy); pb.setDailyTargetPiecesHard(hard);
        baselineRepo.save(pb);
    }
}
