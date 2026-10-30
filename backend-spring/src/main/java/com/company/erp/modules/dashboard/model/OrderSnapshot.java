package com.company.erp.modules.dashboard.model;

import com.company.erp.modules.catalog.model.ProductType;
import jakarta.persistence.*;
import lombok.Data;

import java.time.LocalDate;

@Entity
@Table(name="order_snapshots")
@Data
public class OrderSnapshot {

    @Id
    @Column(name="id", length =50)
    private String id;

    @ManyToOne
    @JoinColumn(name="product_type_id")
    private ProductType productType;


    @Column(name="quantity", nullable =false)
    private Integer quantity;

    @Column(name= "testiq_status")
    private Integer tesdiqStatus;

    @Column(name = "is_hypothetical")
    private Boolean isHypothetical;

    @Column(name= "current_phase")
    private String currentPhase;

    @Column(name = "order_date")
    private LocalDate  orderDate;

    @Column(name = "deadline")
    private LocalDate deadline;

    @Column(name ="planned_start_date")
    private LocalDate plannedStartDate;

    @Column(name = "project_completion_date")
    private LocalDate projectCompletionDate;

    @Column(name="status", length =50)
    private String status;

    @Column(name="efficiency_percent")
    private Double efficiencyPercent;

    @Column(name= "estimated_days")
    private Double estimatedDays;

    @Column(name = "design_days")
    private Double designDays;

    @Column(name = "sourcing_days")
    private Double sourcingDays;

    @Column(name = "conveyor_line", length = 50)
    private String conveyorLine;

    @Column(name = "assigned_workers")
    private Integer assignedWorkers;

    @Column(name = "difficulty", length = 20)
    private String difficulty;

    @Column(name = "queue_position")
    private Integer queuePosition;

    @Column(name = "cutting_days")
    private Double cuttingDays;

    @Column(name = "sewing_days")
    private Double sewingDays;

    @Column(name = "extra_workers_needed")
    private Integer extraWorkersNeeded;

    @Column(name = "delay_days")
    private Long delayDays;

    @Column(name = "material_shortage")
    private Boolean materialShortage;

    @Column(name = "shortage_details", length = 500)
    private String shortageDetails;

    @Column(name = "customer_name", length = 150)
    private String customerName;

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

    @Column(name = "material_readiness_pct")
    private Integer materialReadinessPct;

    @Column(name = "is_reservation_active")
    private Boolean isReservationActive = true;

    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL, fetch = FetchType.EAGER, orphanRemoval = true)
    @OrderBy("lineNum ASC")
    @com.fasterxml.jackson.annotation.JsonManagedReference
    private java.util.List<OrderSubItem> subItems = new java.util.ArrayList<>();
}
