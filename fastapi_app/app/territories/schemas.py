from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

# --- Схемы для ТЕРРИТОРИЙ ---
class TerritoryBase(BaseModel):
    name: str = Field(..., max_length=255)
    territory_type: str = Field(..., max_length=100)
    level: int = Field(..., ge=0)
    description: Optional[str] = Field(None, max_length=500)
    geom_wkt: str  # Будем принимать/отдавать геометрию строкой WKT

class TerritoryCreate(TerritoryBase):
    pass

class TerritoryUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    territory_type: Optional[str] = Field(None, max_length=100)
    level: Optional[int] = Field(None, ge=0)
    description: Optional[str] = Field(None, max_length=500)
    geom_wkt: Optional[str] = None

class TerritoryRead(TerritoryBase):
    id: int
    created_at: datetime
    
    # Включаем автоматический маппинг из SQLAlchemy ORM объектов
    model_config = ConfigDict(from_attributes=True)


# --- Схемы для ПОКАЗАТЕЛЕЙ (METRICS) ---
class TerritoryMetricBase(BaseModel):
    year: int
    population: Optional[int] = None
    area_km2: Optional[Decimal] = None
    source: Optional[str] = Field(None, max_length=255)

class TerritoryMetricCreate(TerritoryMetricBase):
    pass

class TerritoryMetricUpdate(BaseModel):
    year: Optional[int] = None
    population: Optional[int] = None
    area_km2: Optional[Decimal] = None
    source: Optional[str] = Field(None, max_length=255)

class TerritoryMetricRead(TerritoryMetricBase):
    id: int
    territory_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)