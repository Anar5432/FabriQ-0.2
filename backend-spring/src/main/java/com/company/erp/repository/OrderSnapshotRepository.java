package com.company.erp.repository;

import com.company.erp.modules.dashboard.model.OrderSnapshot;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface OrderSnapshotRepository extends JpaRepository<OrderSnapshot, String> {

    List<OrderSnapshot> findAllByOrderByOrderDateDescIdDesc();

    List<OrderSnapshot> findByConveyorLineOrderByOrderDateDescIdDesc(String conveyorLine);

    @Query("SELECT o FROM OrderSnapshot o ORDER BY o.orderDate DESC, o.id DESC")
    Page<OrderSnapshot> findAllOrdersPaged(Pageable pageable);

    @Query("SELECT o FROM OrderSnapshot o WHERE LOWER(o.conveyorLine) NOT LIKE '%underwear%' AND LOWER(o.conveyorLine) NOT LIKE '%sock%' ORDER BY o.orderDate DESC, o.id DESC")
    Page<OrderSnapshot> findWorkwearOrders(Pageable pageable);

    @Query("SELECT o FROM OrderSnapshot o WHERE LOWER(o.conveyorLine) LIKE '%underwear%' ORDER BY o.orderDate DESC, o.id DESC")
    Page<OrderSnapshot> findUnderwearOrders(Pageable pageable);

    @Query("SELECT o FROM OrderSnapshot o WHERE LOWER(o.conveyorLine) LIKE '%sock%' ORDER BY o.orderDate DESC, o.id DESC")
    Page<OrderSnapshot> findSocksOrders(Pageable pageable);

    @Query("SELECT o FROM OrderSnapshot o WHERE " +
           "(LOWER(o.id) LIKE CONCAT('%', :search, '%') OR " +
           "LOWER(o.id) LIKE CONCAT('%', :unpadded, '%') OR " +
           "LOWER(o.customerName) LIKE CONCAT('%', :search, '%') OR " +
           "REPLACE(REPLACE(UPPER(o.customerName), 'İ', 'I'), 'Ə', 'E') LIKE CONCAT('%', :searchUpper, '%') OR " +
           "(o.productType IS NOT NULL AND LOWER(o.productType.name) LIKE CONCAT('%', :search, '%'))) " +
           "ORDER BY o.orderDate DESC, o.id DESC")
    Page<OrderSnapshot> findAllWithSearch(@Param("search") String search,
                                         @Param("unpadded") String unpadded,
                                         @Param("searchUpper") String searchUpper,
                                         Pageable pageable);

    @Query("SELECT o FROM OrderSnapshot o WHERE " +
           "(LOWER(o.conveyorLine) NOT LIKE '%underwear%' AND LOWER(o.conveyorLine) NOT LIKE '%sock%') AND " +
           "(LOWER(o.id) LIKE CONCAT('%', :search, '%') OR " +
           "LOWER(o.id) LIKE CONCAT('%', :unpadded, '%') OR " +
           "LOWER(o.customerName) LIKE CONCAT('%', :search, '%') OR " +
           "REPLACE(REPLACE(UPPER(o.customerName), 'İ', 'I'), 'Ə', 'E') LIKE CONCAT('%', :searchUpper, '%') OR " +
           "(o.productType IS NOT NULL AND LOWER(o.productType.name) LIKE CONCAT('%', :search, '%'))) " +
           "ORDER BY o.orderDate DESC, o.id DESC")
    Page<OrderSnapshot> findWorkwearWithSearch(@Param("search") String search,
                                              @Param("unpadded") String unpadded,
                                              @Param("searchUpper") String searchUpper,
                                              Pageable pageable);

    @Query("SELECT o FROM OrderSnapshot o WHERE " +
           "LOWER(o.conveyorLine) LIKE '%underwear%' AND " +
           "(LOWER(o.id) LIKE CONCAT('%', :search, '%') OR " +
           "LOWER(o.id) LIKE CONCAT('%', :unpadded, '%') OR " +
           "LOWER(o.customerName) LIKE CONCAT('%', :search, '%') OR " +
           "REPLACE(REPLACE(UPPER(o.customerName), 'İ', 'I'), 'Ə', 'E') LIKE CONCAT('%', :searchUpper, '%') OR " +
           "(o.productType IS NOT NULL AND LOWER(o.productType.name) LIKE CONCAT('%', :search, '%'))) " +
           "ORDER BY o.orderDate DESC, o.id DESC")
    Page<OrderSnapshot> findUnderwearWithSearch(@Param("search") String search,
                                               @Param("unpadded") String unpadded,
                                               @Param("searchUpper") String searchUpper,
                                               Pageable pageable);

    @Query("SELECT o FROM OrderSnapshot o WHERE " +
           "LOWER(o.conveyorLine) LIKE '%sock%' AND " +
           "(LOWER(o.id) LIKE CONCAT('%', :search, '%') OR " +
           "LOWER(o.id) LIKE CONCAT('%', :unpadded, '%') OR " +
           "LOWER(o.customerName) LIKE CONCAT('%', :search, '%') OR " +
           "REPLACE(REPLACE(UPPER(o.customerName), 'İ', 'I'), 'Ə', 'E') LIKE CONCAT('%', :searchUpper, '%') OR " +
           "(o.productType IS NOT NULL AND LOWER(o.productType.name) LIKE CONCAT('%', :search, '%'))) " +
           "ORDER BY o.orderDate DESC, o.id DESC")
    Page<OrderSnapshot> findSocksWithSearch(@Param("search") String search,
                                           @Param("unpadded") String unpadded,
                                           @Param("searchUpper") String searchUpper,
                                           Pageable pageable);
}
