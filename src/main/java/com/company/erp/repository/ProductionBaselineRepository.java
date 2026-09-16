package com.company.erp.repository;

import com.company.erp.modules.catalog.model.ProductType;
import com.company.erp.modules.planning.model.ProductionBaseline;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.*;

@Repository
public interface ProductionBaselineRepository extends JpaRepository<ProductionBaseline, Long> {
    ProductionBaseline findByProductType(ProductType productType);
}
