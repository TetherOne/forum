"""delete some fields

Revision ID: e8969cc5d5c0
Revises: 1a77bb947a38
Create Date: 2024-01-08 14:04:05.349560

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e8969cc5d5c0'
down_revision: Union[str, None] = '1a77bb947a38'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'github')
    op.drop_column('users', 'bio')
    op.drop_column('users', 'telegram')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('telegram', sa.VARCHAR(), nullable=True))
    op.add_column('users', sa.Column('bio', sa.VARCHAR(), nullable=True))
    op.add_column('users', sa.Column('github', sa.VARCHAR(), nullable=True))
    # ### end Alembic commands ###