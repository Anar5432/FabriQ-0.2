from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class StageBase(BaseModel):
    id: str
    sector_id: str
    name: str
    capacity: int
    order_index: int

class Stage(StageBase):
    class Config:
        orm_mode = True
        from_attributes = True

class SectorBase(BaseModel):
    id: str
    name: str
    icon: str
    color_hex: str

class Sector(SectorBase):
    stages: List[Stage] = []
    class Config:
        orm_mode = True
        from_attributes = True

class CompanyBase(BaseModel):
    id: str
    name: str
    short_name: str
    bg_color: str
    text_color: str

class Company(CompanyBase):
    class Config:
        orm_mode = True
        from_attributes = True

class OrderBase(BaseModel):
    id: str
    sector_id: str
    company_id: str
    product_type: str
    quantity: str
    stage_index: int
    status: str
    deadline: str
    color: str
    notes: Optional[str] = None
    difficulty: Optional[str] = None
    workers_assigned: Optional[int] = None
    planned_days: Optional[int] = None
    created_at: Optional[datetime] = None
    priority: Optional[int] = 0

class MaterialBase(BaseModel):
    id: str
    name: str
    unit: str

class Material(MaterialBase):
    class Config:
        orm_mode = True
        from_attributes = True

class MaterialStockBase(BaseModel):
    id: int
    material_id: str
    location: str
    quantity: float

class MaterialStock(MaterialStockBase):
    class Config:
        orm_mode = True
        from_attributes = True

class ProductBOMBase(BaseModel):
    id: int
    product_type: str
    material_id: str
    quantity_per_unit: float

class ProductBOM(ProductBOMBase):
    class Config:
        orm_mode = True
        from_attributes = True

class OrderMaterialReserveBase(BaseModel):
    id: int
    order_id: str
    material_id: str
    quantity: float

class OrderMaterialReserve(OrderMaterialReserveBase):
    class Config:
        orm_mode = True
        from_attributes = True

class ProductProcessBase(BaseModel):
    id: int
    product_type: str
    stage_id: str
    step_order: int

class ProductProcess(ProductProcessBase):
    class Config:
        orm_mode = True
        from_attributes = True

class WorkerBase(BaseModel):
    id: str
    name: str

class Worker(WorkerBase):
    class Config:
        orm_mode = True
        from_attributes = True

class WorkerAbilityBase(BaseModel):
    id: int
    worker_id: str
    stage_id: str
    daily_capacity: float

class WorkerAbility(WorkerAbilityBase):
    class Config:
        orm_mode = True
        from_attributes = True

class WorkerCalendarBase(BaseModel):
    id: int
    worker_id: str
    order_id: str
    stage_id: str
    start_date: datetime
    end_date: datetime

class WorkerCalendar(WorkerCalendarBase):
    class Config:
        orm_mode = True
        from_attributes = True

class OrderStageAssignmentBase(BaseModel):
    id: int
    order_id: str
    stage_id: str
    worker_id: str
    daily_goal: float
    days_required: int

class OrderStageAssignment(OrderStageAssignmentBase):
    class Config:
        orm_mode = True
        from_attributes = True

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    class Config:
        orm_mode = True
        from_attributes = True

class OrderStageUpdate(BaseModel):
    stage_index: int

class OrderStatusUpdate(BaseModel):
    status: str

class PlanOrderInput(BaseModel):
    order_id: str
    workers: int
    difficulty: str

class OrderPlanRequest(BaseModel):
    orders: List[PlanOrderInput]

class PlannedOrderResponse(BaseModel):
    order_id: str
    planned_days: int
    new_deadline: str

class OrderPlanResponse(BaseModel):
    results: List[PlannedOrderResponse]

class ApplyPlanRequest(BaseModel):
    plans: List[PlannedOrderResponse]


