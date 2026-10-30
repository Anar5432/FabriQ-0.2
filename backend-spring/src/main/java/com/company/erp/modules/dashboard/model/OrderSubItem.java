package com.company.erp.modules.dashboard.model;

import com.fasterxml.jackson.annotation.JsonBackReference;
import jakarta.persistence.*;
import lombok.Data;
import lombok.ToString;

@Entity
@Table(name = "order_sub_items")
@Data
public class OrderSubItem {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "order_id", nullable = false)
    @JsonBackReference
    @ToString.Exclude
    private OrderSnapshot order;

    @Column(name = "line_num")
    private Integer lineNum;

    @Column(name = "product_code", length = 100)
    private String productCode;

    @Column(name = "product_name", length = 250, nullable = false)
    private String productName;

    @Column(name = "variant_details", length = 100)
    private String variantDetails;

    @Column(name = "quantity", nullable = false)
    private Integer quantity;

    @Column(name = "delivered_quantity")
    private Integer deliveredQuantity;

    @Column(name = "cutting_quantity")
    private Integer cuttingQuantity;

    @Column(name = "sewing_quantity")
    private Integer sewingQuantity;

    @Column(name = "warehouse_quantity")
    private Integer warehouseQuantity;

    @Column(name = "queue_quantity")
    private Integer queueQuantity;

    @Column(name = "current_phase", length = 50)
    private String currentPhase;

    @Column(name = "status", length = 50)
    private String status;

    @Column(name = "material_status", length = 50)
    private String materialStatus;

    @Column(name = "material_details", length = 250)
    private String materialDetails;

    @Column(name = "material_readiness_pct")
    private Integer materialReadinessPct;

    @Column(name = "lead_time_days")
    private Integer leadTimeDays;

    @Column(name = "fabric_specs", length = 150)
    private String fabricSpecs;

    @Column(name = "required_material_qty")
    private Double requiredMaterialQty;

    @Column(name = "available_material_qty")
    private Double availableMaterialQty;

    @Column(name = "material_unit", length = 20)
    private String materialUnit;
}
