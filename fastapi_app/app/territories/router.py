from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.common.db import get_db
from app.territories import crud, schemas

router = APIRouter(prefix="/territories", tags=["Territories"])

# Получение списка всех территорий
@router.get("/", response_model=List[schemas.TerritoryRead])
def read_territories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_territories(db, skip=skip, limit=limit)

# Пространственный поиск пересечений
@router.post("/intersects", response_model=List[schemas.TerritoryRead])
def find_intersecting_territories(polygon_wkt: str, db: Session = Depends(get_db)):
    return crud.get_intersecting_territories(db, polygon_wkt=polygon_wkt)

# Получение одной территории по id
@router.get("/{territory_id}", response_model=schemas.TerritoryRead)
def read_territory(territory_id: int, db: Session = Depends(get_db)):
    db_territory = crud.get_territory(db, territory_id=territory_id)
    if not db_territory:
        raise HTTPException(status_code=404, detail="Territory not found")
    return db_territory

# Создание территории
@router.post("/", response_model=schemas.TerritoryRead, status_code=status.HTTP_201_CREATED)
def create_territory(territory: schemas.TerritoryCreate, db: Session = Depends(get_db)):
    return crud.create_territory(db=db, territory=territory)

# Обновление территории
@router.put("/{territory_id}", response_model=schemas.TerritoryRead)
def update_territory(territory_id: int, territory: schemas.TerritoryUpdate, db: Session = Depends(get_db)):
    updated = crud.update_territory(db, territory_id, territory)
    if not updated:
        raise HTTPException(status_code=404, detail="Territory not found")
    return updated

# Удаление территории
@router.delete("/{territory_id}")
def delete_territory(territory_id: int, db: Session = Depends(get_db)):
    if not crud.delete_territory(db, territory_id):
        raise HTTPException(status_code=404, detail="Territory not found")
    return {"detail": "Territory deleted successfully"}


# --- ЭНДПОИНТЫ ДЛЯ МЕТРИК ---

@router.get("/{territory_id}/metrics", response_model=List[schemas.TerritoryMetricRead])
def read_territory_metrics(territory_id: int, db: Session = Depends(get_db)):
    return crud.get_metrics_by_territory(db, territory_id=territory_id)

@router.post("/{territory_id}/metrics", response_model=schemas.TerritoryMetricRead)
def create_metric(territory_id: int, metric: schemas.TerritoryMetricCreate, db: Session = Depends(get_db)):
    return crud.create_territory_metric(db, territory_id, metric)

@router.put("/{territory_id}/metrics/{metric_id}", response_model=schemas.TerritoryMetricRead)
def update_metric(metric_id: int, metric: schemas.TerritoryMetricUpdate, db: Session = Depends(get_db)):
    updated = crud.update_territory_metric(db, metric_id, metric)
    if not updated:
        raise HTTPException(status_code=404, detail="Metric not found")
    return updated

@router.delete("/{territory_id}/metrics/{metric_id}")
def delete_metric(metric_id: int, db: Session = Depends(get_db)):
    if not crud.delete_territory_metric(db, metric_id):
        raise HTTPException(status_code=404, detail="Metric not found")
    return {"detail": "Metric deleted successfully"}