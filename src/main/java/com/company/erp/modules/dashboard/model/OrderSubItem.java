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

    @Column(name = "current_phase", length = 50)
    private String currentPhase;

    @Column(name = "status", length = 50)
    private String status;
}
