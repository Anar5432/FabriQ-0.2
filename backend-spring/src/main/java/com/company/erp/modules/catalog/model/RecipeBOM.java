package com.company.erp.modules.catalog.model;
import jakarta.persistence.*;
import lombok.Data;

@Entity
@Table(name="recipe_bom")
@Data

public class RecipeBOM {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "product_type_id")
    private ProductType productType;

    @ManyToOne
    @JoinColumn(name = "product_part_id")
    private ProductPart productPart;

    @ManyToOne
    @JoinColumn(name = "material_id")
    private Material material;

    @Column(name = "quantity")
    private Double quantityPerUnit;


}
