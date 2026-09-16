package com.company.erp.repository;

import com.company.erp.modules.catalog.model.Material;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.*;

@Repository
public interface MaterialRepository extends JpaRepository<Material, String>  {


}
