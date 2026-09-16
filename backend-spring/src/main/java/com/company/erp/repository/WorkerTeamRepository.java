package com.company.erp.repository;

import com.company.erp.modules.planning.model.WorkerTeam;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.*;

@Repository
public interface WorkerTeamRepository extends JpaRepository<WorkerTeam, Long> {


}
