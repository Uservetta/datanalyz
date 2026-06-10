from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.territories.models import Territory, TerritoryMetric
from app.territories.schemas import TerritoryCreate, TerritoryUpdate, TerritoryMetricCreate, TerritoryMetricUpdate

# --- CRUD ДЛЯ ТЕРРИТОРИЙ ---

def get_territories(db: Session, skip: int = 0, limit: int = 100):
    # Используем func.ST_AsText(Territory.geom), чтобы вытащить геометрию в текстовом формате WKT
    stmt = select(
        Territory.id,
        Territory.name,
        Territory.territory_type,
        Territory.level,
        Territory.description,
        func.ST_AsText(Territory.geom).label("geom_wkt"),
        Territory.created_at
    ).offset(skip).limit(limit)
    
    return db.execute(stmt).all()

def get_territory(db: Session, territory_id: int):
    stmt = select(
        Territory.id,
        Territory.name,
        Territory.territory_type,
        Territory.level,
        Territory.description,
        func.ST_AsText(Territory.geom).label("geom_wkt"),
        Territory.created_at
    ).where(Territory.id == territory_id)
    
    return db.execute(stmt).first()

def create_territory(db: Session, territory: TerritoryCreate):
    # Превращаем WKT-строку в геометрию PostGIS с SRID 4326
    db_territory = Territory(
        name=territory.name,
        territory_type=territory.territory_type,
        level=territory.level,
        description=territory.description,
        geom=func.ST_GeomFromText(territory.geom_wkt, 4326)
    )
    db.add(db_territory)
    db.commit()
    return get_territory(db, db_territory.id)

def update_territory(db: Session, territory_id: int, territory_data: TerritoryUpdate):
    db_territory = db.query(Territory).filter(Territory.id == territory_id).first()
    if not db_territory:
        return None
    
    update_data = territory_data.model_dump(exclude_unset=True)
    if "geom_wkt" in update_data:
        db_territory.geom = func.ST_GeomFromText(update_data.pop("geom_wkt"), 4326)
        
    for key, value in update_data.items():
        setattr(db_territory, key, value)
        
    db.commit()
    return get_territory(db, territory_id)

def delete_territory(db: Session, territory_id: int):
    db_territory = db.query(Territory).filter(Territory.id == territory_id).first()
    if db_territory:
        db.delete(db_territory)
        db.commit()
        return True
    return False

# --- ПРОСТРАНСТВЕННЫЙ ЗАПРОС (ST_Intersects) ---

def get_intersecting_territories(db: Session, polygon_wkt: str):
    # Ищем территории, которые пересекаются со строящимся полигоном
    stmt = select(
        Territory.id,
        Territory.name,
        Territory.territory_type,
        Territory.level,
        Territory.description,
        func.ST_AsText(Territory.geom).label("geom_wkt"),
        Territory.created_at
    ).where(
        func.ST_Intersects(
            Territory.geom,
            func.ST_GeomFromText(polygon_wkt, 4326)
        )
    )
    return db.execute(stmt).all()

# --- CRUD ДЛЯ МЕТРИК ---

def get_metrics_by_territory(db: Session, territory_id: int):
    return db.query(TerritoryMetric).filter(TerritoryMetric.territory_id == territory_id).all()

def create_territory_metric(db: Session, territory_id: int, metric: TerritoryMetricCreate):
    db_metric = TerritoryMetric(**metric.model_dump(), territory_id=territory_id)
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric

def update_territory_metric(db: Session, metric_id: int, metric_data: TerritoryMetricUpdate):
    db_metric = db.query(TerritoryMetric).filter(TerritoryMetric.id == metric_id).first()
    if not db_metric:
        return None
    for key, value in metric_data.model_dump(exclude_unset=True).items():
        setattr(db_metric, key, value)
    db.commit()
    db.refresh(db_metric)
    return db_metric

def delete_territory_metric(db: Session, metric_id: int):
    db_metric = db.query(TerritoryMetric).filter(TerritoryMetric.id == metric_id).first()
    if db_metric:
        db.delete(db_metric)
        db.commit()
        return True
    return False