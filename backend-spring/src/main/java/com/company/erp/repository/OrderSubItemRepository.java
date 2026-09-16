package com.company.erp.repository;

import com.company.erp.modules.dashboard.model.OrderSubItem;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface OrderSubItemRepository extends JpaRepository<OrderSubItem, Long> {
    List<OrderSubItem> findByOrder_IdOrderByLineNumAsc(String orderId);
}
