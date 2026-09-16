package com.company.erp.modules.planning.model;

import com.company.erp.modules.catalog.model.ProductType;
import jakarta.persistence.*;
import lombok.Data;

@Entity
@Table(name="production_baselines")
@Data
public class ProductionBaseline {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name="team_id")
    private WorkerTeam workerTeam;

    @ManyToOne
    @JoinColumn(name="product_type_id")
    private ProductType productType;

    @Column(name="daily_target", nullable = false)
    private Integer dailyTargetPieces;

    @Column(name="daily_target_hard")
    private Integer dailyTargetPiecesHard;
}
