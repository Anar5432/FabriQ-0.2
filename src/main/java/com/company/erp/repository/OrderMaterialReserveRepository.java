package com.company.erp.repository;

import com.company.erp.modules.planning.model.OrderMaterialReserve;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.*;
import com.company.erp.modules.dashboard.model.OrderSnapshot;
import  java.util.List;

@Repository
public interface OrderMaterialReserveRepository extends JpaRepository<OrderMaterialReserve,Long> {
   List<OrderMaterialReserve> findByOrderSnapshot( OrderSnapshot orderSnapshot);
}
