from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

import models, schemas
from database import engine, get_db
import re

# Create DB tables
models.Base.metadata.create_all(bind=engine)

def reserve_materials_for_order(db: Session, order: models.Order):
    try:
        qty_str = str(order.quantity).replace(',', '')
        qty_str = re.sub(r'[^\d\.]', '', qty_str)
        qty = float(qty_str) if qty_str else 0.0
    except:
        qty = 0.0

    boms = db.query(models.ProductBOM).filter(models.ProductBOM.product_type == order.product_type).all()
    for bom in boms:
        reserve = models.OrderMaterialReserve(
            order_id=order.id,
            material_id=bom.material_id,
            quantity=bom.quantity_per_unit * qty
        )
        db.add(reserve)
    db.commit()

def seed_db():
    db = next(get_db())
    if db.query(models.Sector).count() == 0:
        # 1. Sektorlar
        s1 = models.Sector(id="corab", name="Corab", icon="🧦", color_hex="#c4b0ff")
        s2 = models.Sector(id="teks", name="Trikotaj", icon="👕", color_hex="#5ddba8")
        db.add_all([s1, s2])
        db.commit()

        # 2. Etaplar
        stages = [
            models.Stage(id="c1", sector_id="corab", name="Hörgü", capacity=2000, order_index=0),
            models.Stage(id="c2", sector_id="corab", name="Burun Tikişi", capacity=1500, order_index=1),
            models.Stage(id="c3", sector_id="corab", name="Forma", capacity=1800, order_index=2),
            models.Stage(id="c4", sector_id="corab", name="Qablaşdırma", capacity=3000, order_index=3),
            
            models.Stage(id="t1", sector_id="teks", name="Kəsim", capacity=1000, order_index=0),
            models.Stage(id="t2", sector_id="teks", name="Tikiş", capacity=800, order_index=1),
            models.Stage(id="t3", sector_id="teks", name="Ütü / Qablaşdır..", capacity=1200, order_index=2)
        ]
        db.add_all(stages)
        db.commit()

        # 3. Şirkətlər
        companies = [
            models.Company(id="brav", name="Bravo Supermarket", short_name="BR", bg_color="#e0f2fe", text_color="#0369a1"),
            models.Company(id="azar", name="Azər İlmə", short_name="AZ", bg_color="#fce7f3", text_color="#be185d"),
            models.Company(id="zel", name="ZelHome", short_name="ZH", bg_color="#dcfce7", text_color="#15803d")
        ]
        db.add_all(companies)
        db.commit()

        # 4. Sifarişlər
        orders = [
            models.Order(id="ORD-101", sector_id="corab", company_id="brav", product_type="Qış corabı (Qalın)", quantity="15,000", stage_index=2, status="Davam edir", deadline="24 Fevral", color="#b91c1c", notes="İplik sayı xüsusi olaraq 2 qat artırılıb."),
            models.Order(id="ORD-102", sector_id="corab", company_id="azar", product_type="İkili İdman Corabı", quantity="8,000", stage_index=1, status="Gecikmiş", deadline="18 Fevral", color="#1d4ed8", notes="Təcili sifariş!"),
            models.Order(id="ORD-103", sector_id="corab", company_id="zel", product_type="Qadın corabı", quantity="12,000", stage_index=3, status="Tamamlandı", deadline="20 Fevral", color="#047857", notes="Tamamlanıb və anbara təhvil verilib."),
            
            models.Order(id="ORD-201", sector_id="teks", company_id="brav", product_type="Polo T-Shirt", quantity="5,000", stage_index=0, status="Davam edir", deadline="10 Mart", color="#ca8a04", notes="Kəsim mərhələsindədir.", created_at=datetime.utcnow() - timedelta(days=1)),
            models.Order(id="ORD-202", sector_id="teks", company_id="zel", product_type="Şalvar", quantity="2,000", stage_index=2, status="Gözləyir", deadline="15 Mart", color="#4f46e5", notes="Aksesuar tədarükü gözlənilir.", created_at=datetime.utcnow())
        ]
        db.add_all(orders)
        db.commit()

        # Materials
        materials = [
            models.Material(id="m_yarn_thick", name="Thick Yarn", unit="kg"),
            models.Material(id="m_yarn_sport", name="Sport Yarn", unit="kg"),
            models.Material(id="m_fabric_cotton", name="Cotton Fabric", unit="meter"),
            models.Material(id="m_thread", name="Thread", unit="roll"),
            models.Material(id="m_buttons", name="Button", unit="pcs")
        ]
        db.add_all(materials)
        
        # Stocks
        stocks = [
            models.MaterialStock(material_id="m_yarn_thick", location="Warehouse", quantity=500.0),
            models.MaterialStock(material_id="m_yarn_thick", location="Production Floor", quantity=20.5),
            models.MaterialStock(material_id="m_yarn_sport", location="Warehouse", quantity=300.0),
            models.MaterialStock(material_id="m_fabric_cotton", location="Warehouse", quantity=1000.0),
            models.MaterialStock(material_id="m_thread", location="Warehouse", quantity=200.0),
            models.MaterialStock(material_id="m_buttons", location="Warehouse", quantity=5000.0)
        ]
        db.add_all(stocks)

        # BOMs
        boms = [
            models.ProductBOM(product_type="Qış corabı (Qalın)", material_id="m_yarn_thick", quantity_per_unit=0.05),
            models.ProductBOM(product_type="İkili İdman Corabı", material_id="m_yarn_sport", quantity_per_unit=0.04),
            models.ProductBOM(product_type="Qadın corabı", material_id="m_yarn_sport", quantity_per_unit=0.02),
            models.ProductBOM(product_type="Polo T-Shirt", material_id="m_fabric_cotton", quantity_per_unit=1.5),
            models.ProductBOM(product_type="Polo T-Shirt", material_id="m_thread", quantity_per_unit=0.1),
            models.ProductBOM(product_type="Polo T-Shirt", material_id="m_buttons", quantity_per_unit=3.0),
            models.ProductBOM(product_type="Şalvar", material_id="m_fabric_cotton", quantity_per_unit=1.2),
            models.ProductBOM(product_type="Şalvar", material_id="m_thread", quantity_per_unit=0.15)
        ]
        db.add_all(boms)

        # Product Processes
        processes = [
            models.ProductProcess(product_type="Qış corabı (Qalın)", stage_id="c1", step_order=1),
            models.ProductProcess(product_type="Qış corabı (Qalın)", stage_id="c2", step_order=2),
            models.ProductProcess(product_type="Qış corabı (Qalın)", stage_id="c3", step_order=3),
            models.ProductProcess(product_type="Qış corabı (Qalın)", stage_id="c4", step_order=4),
            models.ProductProcess(product_type="Polo T-Shirt", stage_id="t1", step_order=1),
            models.ProductProcess(product_type="Polo T-Shirt", stage_id="t2", step_order=2),
            models.ProductProcess(product_type="Polo T-Shirt", stage_id="t3", step_order=3),
            models.ProductProcess(product_type="Şalvar", stage_id="t1", step_order=1),
            models.ProductProcess(product_type="Şalvar", stage_id="t2", step_order=2),
            models.ProductProcess(product_type="Şalvar", stage_id="t3", step_order=3)
        ]
        db.add_all(processes)

        # Workers
        workers = [
            models.Worker(id="w1", name="Ali (Kəsim)"),
            models.Worker(id="w2", name="Vəli (Tikiş)"),
            models.Worker(id="w3", name="Həsən (Ütü)"),
            models.Worker(id="w4", name="Aygün (Hörgü/Corab)"),
        ]
        db.add_all(workers)

        abilities = [
            models.WorkerAbility(worker_id="w1", stage_id="t1", daily_capacity=1000),
            models.WorkerAbility(worker_id="w2", stage_id="t2", daily_capacity=800),
            models.WorkerAbility(worker_id="w3", stage_id="t3", daily_capacity=1200),
            models.WorkerAbility(worker_id="w4", stage_id="c1", daily_capacity=2000),
            models.WorkerAbility(worker_id="w4", stage_id="c2", daily_capacity=1500),
        ]
        db.add_all(abilities)
        
        db.commit()

        for o in orders:
            reserve_materials_for_order(db, o)

seed_db()

app = FastAPI(title="Factory Dashboard API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------
# SECTORS & STAGES
# -----------------
@app.get("/api/sectors", response_model=List[schemas.Sector])
def read_sectors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sectors = db.query(models.Sector).offset(skip).limit(limit).all()
    return sectors

# -----------------
# COMPANIES
# -----------------
@app.get("/api/companies", response_model=List[schemas.Company])
def read_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    companies = db.query(models.Company).offset(skip).limit(limit).all()
    return companies

@app.post("/api/companies", response_model=schemas.Company)
def create_company(company: schemas.CompanyBase, db: Session = Depends(get_db)):
    db_company = db.query(models.Company).filter(models.Company.id == company.id).first()
    if db_company:
        raise HTTPException(status_code=400, detail="Company ID already registered")
    new_company = models.Company(**company.dict())
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company

# -----------------
# ORDERS
# -----------------
@app.get("/api/orders", response_model=List[schemas.Order])
def read_orders(sector_id: str = None, company_id: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    query = db.query(models.Order)
    if sector_id:
        query = query.filter(models.Order.sector_id == sector_id)
    if company_id:
        query = query.filter(models.Order.company_id == company_id)
    orders = query.offset(skip).limit(limit).all()
    return orders

@app.post("/api/orders", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == order.id).first()
    if db_order:
        raise HTTPException(status_code=400, detail="Order ID already exists")
    new_order = models.Order(**order.dict())
    if new_order.created_at is None:
        new_order.created_at = datetime.utcnow()
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    
    # Auto-reserve materials
    reserve_materials_for_order(db, new_order)
    
    return new_order

@app.put("/api/orders/{order_id}", response_model=schemas.Order)
def update_order(order_id: str, order: schemas.OrderCreate, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    for key, value in order.dict().items():
        setattr(db_order, key, value)
        
    db.commit()
    db.refresh(db_order)
    return db_order

@app.patch("/api/orders/{order_id}/stage", response_model=schemas.Order)
def update_order_stage(order_id: str, stage_update: schemas.OrderStageUpdate, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db_order.stage_index = stage_update.stage_index
    db.commit()
    db.refresh(db_order)
    return db_order

@app.patch("/api/orders/{order_id}/status", response_model=schemas.Order)
def update_order_status(order_id: str, status_update: schemas.OrderStatusUpdate, db: Session = Depends(get_db)):
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db_order.status = status_update.status
    db.commit()
    db.refresh(db_order)
    return db_order

# -----------------
# PLANNING & MATERIALS
# -----------------
import math
from datetime import datetime, timedelta
from capacities import CAPACITIES
from pydantic import BaseModel

class MaterialRequirement(BaseModel):
    material_id: str
    material_name: str
    unit: str
    needed_for_this_order: float
    reserved_for_older_orders: float
    stock_in_warehouse: float
    stock_in_production: float
    shortage: float

class OrderMaterialPlanning(BaseModel):
    order_id: str
    product_type: str
    requirements: List[MaterialRequirement]

@app.get("/api/planning/materials", response_model=List[OrderMaterialPlanning])
def plan_materials(db: Session = Depends(get_db)):
    orders = db.query(models.Order).filter(models.Order.status != "Tamamlandı").order_by(models.Order.priority.desc(), models.Order.created_at.asc()).all()
    
    all_stocks = db.query(models.MaterialStock).all()
    warehouse_stock = {}
    production_stock = {}
    for s in all_stocks:
        if s.location == "Warehouse":
            warehouse_stock[s.material_id] = warehouse_stock.get(s.material_id, 0.0) + s.quantity
        else:
            production_stock[s.material_id] = production_stock.get(s.material_id, 0.0) + s.quantity
            
    materials_info = {m.id: m for m in db.query(models.Material).all()}
    
    running_reserves = {}
    results = []
    
    for order in orders:
        try:
            qty_str = str(order.quantity).replace(',', '')
            qty_str = re.sub(r'[^\d\.]', '', qty_str)
            qty = float(qty_str) if qty_str else 0.0
        except:
            qty = 0.0

        boms = db.query(models.ProductBOM).filter(models.ProductBOM.product_type == order.product_type).all()
        order_reqs = []
        for bom in boms:
            mat = materials_info.get(bom.material_id)
            if not mat: continue
            
            needed = bom.quantity_per_unit * qty
            wh_stock = warehouse_stock.get(mat.id, 0.0)
            prod_stock = production_stock.get(mat.id, 0.0)
            already_reserved = running_reserves.get(mat.id, 0.0)
            
            available_stock_for_me = max(0.0, wh_stock + prod_stock - already_reserved)
            shortage = max(0.0, needed - available_stock_for_me)
            
            order_reqs.append({
                "material_id": mat.id,
                "material_name": mat.name,
                "unit": mat.unit,
                "needed_for_this_order": needed,
                "reserved_for_older_orders": already_reserved,
                "stock_in_warehouse": wh_stock,
                "stock_in_production": prod_stock,
                "shortage": shortage
            })
            running_reserves[mat.id] = already_reserved + needed
            
        results.append({
            "order_id": order.id,
            "product_type": order.product_type,
            "requirements": order_reqs
        })
        
    return results

@app.get("/api/products/{product_type}/steps", response_model=List[schemas.ProductProcess])
def get_product_steps(product_type: str, db: Session = Depends(get_db)):
    steps = db.query(models.ProductProcess).filter(models.ProductProcess.product_type == product_type).order_by(models.ProductProcess.step_order.asc()).all()
    return steps

class AssignWorkerRequest(BaseModel):
    order_id: str
    stage_id: str
    worker_id: str

@app.post("/api/planning/assign_worker")
def assign_worker(req: AssignWorkerRequest, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == req.order_id).first()
    if not order: raise HTTPException(404, "Order not found")
    
    worker = db.query(models.Worker).filter(models.Worker.id == req.worker_id).first()
    if not worker: raise HTTPException(404, "Worker not found")
    
    ability = db.query(models.WorkerAbility).filter(
        models.WorkerAbility.worker_id == req.worker_id,
        models.WorkerAbility.stage_id == req.stage_id
    ).first()
    if not ability: raise HTTPException(400, "Worker cannot perform this stage")
    
    steps = db.query(models.ProductProcess).filter(models.ProductProcess.product_type == order.product_type).order_by(models.ProductProcess.step_order.asc()).all()
    target_step = next((s for s in steps if s.stage_id == req.stage_id), None)
    if not target_step: raise HTTPException(400, "Stage not required for this product")

    try:
        qty_str = str(order.quantity).replace(',', '')
        qty_str = re.sub(r'[^\d\.]', '', qty_str)
        qty = float(qty_str) if qty_str else 0.0
    except:
        qty = 0.0

    days_required = math.ceil(qty / ability.daily_capacity) if ability.daily_capacity > 0 else 0

    start_date = datetime.utcnow().replace(hour=8, minute=0, second=0, microsecond=0)
    
    if target_step.step_order > 1:
        prev_step = steps[target_step.step_order - 2]
        prev_assign = db.query(models.WorkerCalendar).filter(
            models.WorkerCalendar.order_id == req.order_id,
            models.WorkerCalendar.stage_id == prev_step.stage_id
        ).first()
        if prev_assign:
            start_date = prev_assign.end_date

    def add_working_days(start_dt, days):
        curr = start_dt
        added = 0
        while added < days:
            curr += timedelta(days=1)
            if curr.weekday() != 6:
                added += 1
        return curr
        
    worker_blocks = db.query(models.WorkerCalendar).filter(models.WorkerCalendar.worker_id == req.worker_id).all()
    for block in worker_blocks:
        if block.end_date > start_date and block.order_id != req.order_id:
            start_date = block.end_date
            
    if start_date.weekday() == 6:
        start_date += timedelta(days=1)
        
    end_date = add_working_days(start_date, days_required)

    db.query(models.OrderStageAssignment).filter(
        models.OrderStageAssignment.order_id == req.order_id,
        models.OrderStageAssignment.stage_id == req.stage_id
    ).delete()
    db.query(models.WorkerCalendar).filter(
        models.WorkerCalendar.order_id == req.order_id,
        models.WorkerCalendar.stage_id == req.stage_id
    ).delete()
    
    assignment = models.OrderStageAssignment(
        order_id=req.order_id,
        stage_id=req.stage_id,
        worker_id=req.worker_id,
        daily_goal=ability.daily_capacity,
        days_required=days_required
    )
    db.add(assignment)
    
    calendar = models.WorkerCalendar(
        worker_id=req.worker_id,
        order_id=req.order_id,
        stage_id=req.stage_id,
        start_date=start_date,
        end_date=end_date
    )
    db.add(calendar)
    db.commit()
    return {"status": "success", "start_date": start_date, "end_date": end_date}

class WorkerAbilitySchema(BaseModel):
    stage_id: str
    daily_capacity: float

class WorkerProfile(BaseModel):
    worker_id: str
    name: str
    abilities: List[WorkerAbilitySchema]

@app.get("/api/workers", response_model=List[WorkerProfile])
def get_workers(db: Session = Depends(get_db)):
    workers = db.query(models.Worker).all()
    results = []
    for w in workers:
        abilities = db.query(models.WorkerAbility).filter(models.WorkerAbility.worker_id == w.id).all()
        results.append(WorkerProfile(
            worker_id=w.id,
            name=w.name,
            abilities=[WorkerAbilitySchema(stage_id=a.stage_id, daily_capacity=a.daily_capacity) for a in abilities]
        ))
    return results

@app.get("/api/planning/details/{order_id}")
def get_planning_details(order_id: str, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order: raise HTTPException(404, "Order not found")
    
    all_materials = plan_materials(db)
    material_stats = next((o for o in all_materials if o["order_id"] == order_id), None)
    
    steps = db.query(models.ProductProcess).filter(models.ProductProcess.product_type == order.product_type).order_by(models.ProductProcess.step_order.asc()).all()
    
    assignments = []
    for step in steps:
        assign = db.query(models.OrderStageAssignment).filter(
            models.OrderStageAssignment.order_id == order_id,
            models.OrderStageAssignment.stage_id == step.stage_id
        ).first()
        cal = db.query(models.WorkerCalendar).filter(
            models.WorkerCalendar.order_id == order_id,
            models.WorkerCalendar.stage_id == step.stage_id
        ).first()
        worker = db.query(models.Worker).filter(models.Worker.id == assign.worker_id).first() if assign else None
        
        assignments.append({
            "step_order": step.step_order,
            "stage_id": step.stage_id,
            "assigned_worker": worker.name if worker else "Unassigned",
            "daily_goal": assign.daily_goal if assign else 0,
            "days_required": assign.days_required if assign else 0,
            "start_date": cal.start_date.isoformat() if cal else None,
            "end_date": cal.end_date.isoformat() if cal else None
        })
        
    return {
        "order": schemas.Order.from_orm(order),
        "materials": material_stats["requirements"] if material_stats else [],
        "assignments": assignments
    }

@app.post("/api/plan", response_model=schemas.OrderPlanResponse)
def plan_orders(request: schemas.OrderPlanRequest, db: Session = Depends(get_db)):
    active_orders = db.query(models.Order).filter(models.Order.status != "Tamamlandı").order_by(models.Order.id).all()
    plan_inputs = {req.order_id: req for req in request.orders}
    results = []
    current_days_accumulated = 0
    
    import re
    for order in active_orders:
        try:
            qty_str = str(order.quantity).replace(',', '')
            qty_str = re.sub(r'[^\d]', '', qty_str)
            qty = int(qty_str) if qty_str else 0
        except:
            qty = 0
            
        if qty <= 0:
            continue
            
        prod_type = order.product_type
        caps = CAPACITIES.get(prod_type, CAPACITIES["default"])
        is_selected = order.id in plan_inputs
        
        if is_selected:
            workers = plan_inputs[order.id].workers
            difficulty = plan_inputs[order.id].difficulty
            if workers <= 0: workers = 1
            
            cap_for_10 = caps.get(difficulty, caps["easy"])
            daily_cap = (cap_for_10 / 10.0) * workers
            days_required = math.ceil(qty / daily_cap) if daily_cap > 0 else 0
            current_days_accumulated += days_required
            
            new_date = datetime.now() + timedelta(days=current_days_accumulated)
            month_az = ["Yanvar", "Fevral", "Mart", "Aprel", "May", "İyun", "İyul", "Avqust", "Sentyabr", "Oktyabr", "Noyabr", "Dekabr"]
            deadline_str = f"{new_date.day} {month_az[new_date.month - 1]}"
            
            results.append(schemas.PlannedOrderResponse(
                order_id=order.id,
                planned_days=days_required,
                new_deadline=deadline_str
            ))
        else:
            standard_cap_10 = (0.8 * caps["hard"]) + (0.2 * caps["easy"])
            daily_cap = standard_cap_10
            days_required = math.ceil(qty / daily_cap) if daily_cap > 0 else 0
            current_days_accumulated += days_required

    return {"results": results}

@app.post("/api/apply_plan", response_model=dict)
def apply_plan(request: schemas.ApplyPlanRequest, db: Session = Depends(get_db)):
    for plan in request.plans:
        db_order = db.query(models.Order).filter(models.Order.id == plan.order_id).first()
        if db_order:
            db_order.deadline = plan.new_deadline
            db_order.planned_days = plan.planned_days
    db.commit()
    return {"status": "success"}

# -----------------
# DASHBOARD DATA
# -----------------
from pydantic import BaseModel

class DashboardResponse(BaseModel):
    sectors: List[schemas.Sector]
    companies: List[schemas.Company]
    orders: List[schemas.Order]

@app.get("/api/dashboardData", response_model=DashboardResponse)
def get_dashboard_data(db: Session = Depends(get_db)):
    # Composite endpoint for the frontend to pull everything at once if desired
    sectors = db.query(models.Sector).all()
    companies = db.query(models.Company).all()
    orders = db.query(models.Order).all()
    
    return {
        "sectors": sectors,
        "companies": companies,
        "orders": orders
    }

# -----------------
# FRONTEND DASHBOARD
# -----------------
import os
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_dashboard():
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"message": "static/index.html not found"}

