"""create payloads table

Revision ID: 0002
Revises: 0001
Create Date: 2026-10-07 13:48:59.405274

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = '0002'
down_revision: str | Sequence[str] | None = '0001'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'payloads',
        sa.Column('input_hash', sa.String(length=64), nullable=False),
        sa.Column('output', sa.Text(), nullable=False),
        sa.Column('id', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('input_hash'),
    )


def downgrade() -> None:
    op.drop_table('payloads')
