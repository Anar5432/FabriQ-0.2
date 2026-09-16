package com.company.erp.modules.catalog.model;
import jakarta.persistence.*;
import lombok.Data;

@Entity
@Table(name = "materials")
@Data
public class Material {

    @Id
    @Column(name = "id" , length = 50)
    private String id ;

    @Column(name = "name" , nullable = false)
    private String name;

    @Column(name = "unit", nullable = false, length = 20)
    private String unit;

    @Column(name = "color")
    private String color;
}
