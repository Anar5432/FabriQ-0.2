package com.company.erp.modules.catalog.model;
import jakarta.persistence.*;
import lombok.Data;

@Entity
@Table(name= "product_types")
@Data
public class ProductType {



    @Id
    @Column(name = "id", length=50)
    private String id;


    @Column(name = "name", nullable = false)
    private String name;

    @Column(name = "category" , nullable = false)
    private String category;






}
