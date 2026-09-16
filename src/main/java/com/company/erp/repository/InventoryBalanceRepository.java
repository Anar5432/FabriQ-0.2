package com.company.erp.repository;

import com.company.erp.modules.inventory.model.InventoryBalance;
import com.company.erp.modules.catalog.model.Material;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface InventoryBalanceRepository extends JpaRepository<InventoryBalance, Long> {

    List<InventoryBalance> findAllByMaterial(Material material);

    @Query("SELECT COALESCE(SUM(ib.availableQuantity), 0.0) FROM InventoryBalance ib WHERE ib.material = :material")
    Double getTotalAvailableQuantityByMaterial(@Param("material") Material material);
}
