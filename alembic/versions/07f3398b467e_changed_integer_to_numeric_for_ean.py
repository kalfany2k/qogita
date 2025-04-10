"""Changed Integer to Numeric for EAN

Revision ID: 07f3398b467e
Revises: 9a5f431af57f
Create Date: 2025-04-09 20:11:41.248029

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '07f3398b467e'
down_revision: Union[str, None] = '9a5f431af57f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('products', 'GTIN',
               existing_type=sa.INTEGER(),
               type_=sa.Numeric(precision=14, scale=0),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('products', 'GTIN',
               existing_type=sa.Numeric(precision=14, scale=0),
               type_=sa.INTEGER(),
               existing_nullable=False)
    # ### end Alembic commands ###
