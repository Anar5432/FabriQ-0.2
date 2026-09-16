package com.company.erp.modules.planning.model;


import com.company.erp.modules.catalog.model.Material;
import com.company.erp.modules.dashboard.model.OrderSnapshot;
import jakarta.persistence.*;
import lombok.Data;

@Entity
@Table(name="order_material_reserves")
@Data
public class OrderMaterialReserve {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name="order_id")
    private OrderSnapshot orderSnapshot;

    @ManyToOne
    @JoinColumn(name="material_id")
    private Material material;

    @Column(name="locked_quantity", nullable=false)
    private Double lockedQuantity;
}
