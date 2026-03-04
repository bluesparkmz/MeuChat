"""add push_devices table

Revision ID: 20260304_0001
Revises:
Create Date: 2026-03-04 08:20:00
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = "20260304_0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    existing_tables = set(inspector.get_table_names())

    if "push_devices" not in existing_tables:
        op.create_table(
            "push_devices",
            sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
            sa.Column("user_id", sa.Integer(), nullable=False),
            sa.Column("token", sa.String(length=255), nullable=False),
            sa.Column("device_id", sa.String(length=120), nullable=True),
            sa.Column("platform", sa.String(length=20), nullable=True),
            sa.Column("last_seen_at", sa.DateTime(), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
            sa.UniqueConstraint("token", name="uq_push_devices_token"),
            sa.UniqueConstraint("user_id", "device_id", name="uq_push_device_user_device"),
        )
        op.create_index("ix_push_devices_id", "push_devices", ["id"], unique=False)
        op.create_index("ix_push_devices_user_id", "push_devices", ["user_id"], unique=False)
        op.create_index("ix_push_devices_token", "push_devices", ["token"], unique=False)


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    existing_tables = set(inspector.get_table_names())

    if "push_devices" in existing_tables:
        op.drop_index("ix_push_devices_token", table_name="push_devices")
        op.drop_index("ix_push_devices_user_id", table_name="push_devices")
        op.drop_index("ix_push_devices_id", table_name="push_devices")
        op.drop_table("push_devices")
