package com.company.erp.repository;

import com.company.erp.modules.catalog.model.ProductType;
import com.company.erp.modules.catalog.model.RecipeBOM;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.*;

import java.util.List;

@Repository
public interface RecipeBOMRepository extends JpaRepository <RecipeBOM, Long>{
    List<RecipeBOM> findByProductType (ProductType productType);
}
