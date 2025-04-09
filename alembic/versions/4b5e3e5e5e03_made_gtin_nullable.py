"""Made GTIN nullable

Revision ID: 4b5e3e5e5e03
Revises: 07f3398b467e
Create Date: 2025-04-09 20:13:24.542550

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b5e3e5e5e03'
down_revision: Union[str, None] = '07f3398b467e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('products', 'GTIN',
               existing_type=sa.NUMERIC(precision=14, scale=0),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('products', 'GTIN',
               existing_type=sa.NUMERIC(precision=14, scale=0),
               nullable=False)
    # ### end Alembic commands ###
