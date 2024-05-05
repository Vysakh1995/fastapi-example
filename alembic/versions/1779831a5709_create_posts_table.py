"""create posts table

Revision ID: 1779831a5709
Revises: 
Create Date: 2024-05-05 23:25:00.720156

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1779831a5709'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
                            sa.Column('title',sa.String(), nullable=False ))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
