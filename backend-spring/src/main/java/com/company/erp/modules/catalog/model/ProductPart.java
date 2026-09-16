package com.company.erp.modules.catalog.model;
import jakarta.persistence.*;
import lombok.Data;

@Entity
@Table(name="product_parts")
@Data

public class ProductPart {

    @Id
    @Column(name="id" , length = 50)
    private String id;

    @Column(name="name" , nullable = false)
    private String name;
}
