package com.company.erp.modules.inventory.model;
import jakarta.persistence.*;
import lombok.Data;
import com.company.erp.modules.catalog.model.Material;
import java.time.LocalDateTime;

@Entity
@Table(name="inventory_balances")
@Data

public class InventoryBalance{

    @Id
    @GeneratedValue (strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name="material_id")
    private Material material;

    @Column(name= "available_quantity")
    private Double availableQuantity;

    @Column(name="warehouse_code" , length =50)
    private String warehouseCode;

    @Column(name = "last_updated")
    private LocalDateTime lastUpdate;
}