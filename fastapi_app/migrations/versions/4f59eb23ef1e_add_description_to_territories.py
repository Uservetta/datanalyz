"""add description to territories

Revision ID: 002_add_description_to_territories
Revises: 001_create_territories_metrics
Create Date: 2026-06-10
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# Связываем вторую миграцию с первой через down_revision
revision: str = "002_add_description"
down_revision: Union[str, None] = "001_create_territories_metrics"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Добавляем колонку description в таблицу territories
    op.add_column(
        "territories",
        sa.Column("description", sa.String(length=500), nullable=True)
    )


def downgrade() -> None:
    # Удаляем колонку description при откате
    op.drop_column("territories", "description")