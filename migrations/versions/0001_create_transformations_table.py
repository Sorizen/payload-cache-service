"""create transformations table

Revision ID: 0001
Revises:
Create Date: 2026-10-07 13:37:37.756933

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = '0001'
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'transformations',
        sa.Column('input_hash', sa.String(length=64), nullable=False),
        sa.Column('input_text', sa.Text(), nullable=False),
        sa.Column('output_text', sa.Text(), nullable=False),
        sa.Column('id', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('input_hash'),
    )


def downgrade() -> None:
    op.drop_table('transformations')
