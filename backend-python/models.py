from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Sector(Base):
    __tablename__ = "sectors"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    icon = Column(String)
    color_hex = Column(String)

    stages = relationship("Stage", back_populates="sector")
    orders = relationship("Order", back_populates="sector")


class Stage(Base):
    __tablename__ = "stages"

    id = Column(String, primary_key=True, index=True)
    sector_id = Column(String, ForeignKey("sectors.id"))
    name = Column(String)
    capacity = Column(Integer)
    order_index = Column(Integer)

    sector = relationship("Sector", back_populates="stages")


class Company(Base):
    __tablename__ = "companies"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    short_name = Column(String)
    bg_color = Column(String)
    text_color = Column(String)

    orders = relationship("Order", back_populates="company")


class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, index=True)
    sector_id = Column(String, ForeignKey("sectors.id"))
    company_id = Column(String, ForeignKey("companies.id"))
    product_type = Column(String)
    quantity = Column(String)
    stage_index = Column(Integer)
    status = Column(String)
    deadline = Column(String)
    color = Column(String)
    notes = Column(String)
    difficulty = Column(String, nullable=True)
    workers_assigned = Column(Integer, nullable=True)
    planned_days = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    priority = Column(Integer, default=0)

    sector = relationship("Sector", back_populates="orders")
    company = relationship("Company", back_populates="orders")

class Material(Base):
    __tablename__ = "materials"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    unit = Column(String)

class MaterialStock(Base):
    __tablename__ = "material_stocks"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    material_id = Column(String, ForeignKey("materials.id"))
    location = Column(String) # 'Warehouse' or 'Production Floor'
    quantity = Column(Float)

class ProductBOM(Base):
    __tablename__ = "product_boms"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_type = Column(String, index=True)
    material_id = Column(String, ForeignKey("materials.id"))
    quantity_per_unit = Column(Float)

class OrderMaterialReserve(Base):
    __tablename__ = "order_material_reserves"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(String, ForeignKey("orders.id"))
    material_id = Column(String, ForeignKey("materials.id"))
    quantity = Column(Float)

class ProductProcess(Base):
    __tablename__ = "product_processes"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_type = Column(String, index=True)
    stage_id = Column(String, ForeignKey("stages.id"))
    step_order = Column(Integer)

class Worker(Base):
    __tablename__ = "workers"
    id = Column(String, primary_key=True, index=True)
    name = Column(String)

class WorkerAbility(Base):
    __tablename__ = "worker_abilities"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    worker_id = Column(String, ForeignKey("workers.id"))
    stage_id = Column(String, ForeignKey("stages.id"))
    daily_capacity = Column(Float)

class WorkerCalendar(Base):
    __tablename__ = "worker_calendars"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    worker_id = Column(String, ForeignKey("workers.id"))
    order_id = Column(String, ForeignKey("orders.id"))
    stage_id = Column(String, ForeignKey("stages.id"))
    start_date = Column(DateTime)
    end_date = Column(DateTime)

class OrderStageAssignment(Base):
    __tablename__ = "order_stage_assignments"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(String, ForeignKey("orders.id"))
    stage_id = Column(String, ForeignKey("stages.id"))
    worker_id = Column(String, ForeignKey("workers.id"))
    daily_goal = Column(Float)
    days_required = Column(Integer)
