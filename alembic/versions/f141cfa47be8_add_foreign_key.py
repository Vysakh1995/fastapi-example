"""add foreign key

Revision ID: f141cfa47be8
Revises: 27d5f4644e90
Create Date: 2024-05-05 23:55:22.257992

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f141cfa47be8'
down_revision: Union[str, None] = '27d5f4644e90'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('posts_users_fk',source_table='posts',referent_table='users',
                          local_cols=['owner_id'],remote_cols=['id'],ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk',table_name='posts')
    op.drop_column('posts','owner_id')
    pass
