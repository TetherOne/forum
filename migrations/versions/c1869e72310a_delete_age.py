"""delete age

Revision ID: c1869e72310a
Revises: 8a5835abd125
Create Date: 2023-12-26 15:39:05.172550

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c1869e72310a'
down_revision: Union[str, None] = '8a5835abd125'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('articles', 'age')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('articles', sa.Column('age', sa.INTEGER(), nullable=False))
    # ### end Alembic commands ###
