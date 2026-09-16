package com.company.erp.modules.planning.model;

import jakarta.persistence.*;
import lombok.Data;

@Entity
@Table(name="worker_teams")
@Data
public class WorkerTeam {

    @Id
    @GeneratedValue(strategy= GenerationType.IDENTITY)
    private Long id;

    @Column(name="department_name", length =50, nullable =false)
    private String departmentName;

    @Column(name="worker_count", nullable=false)
    private Integer workerCount;
}
