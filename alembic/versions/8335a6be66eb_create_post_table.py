"""create post table

Revision ID: 8335a6be66eb
Revises: 
Create Date: 2022-03-01 09:47:13.976154

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8335a6be66eb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), primary_key=True,
                    nullable=False), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
