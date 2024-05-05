"""add new column to post table

Revision ID: c90be8ae8b2e
Revises: 1779831a5709
Create Date: 2024-05-05 23:32:20.987003

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c90be8ae8b2e'
down_revision: Union[str, None] = '1779831a5709'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
