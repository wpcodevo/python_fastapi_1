"""add content column to posts table

Revision ID: 316a315fa34b
Revises: 8335a6be66eb
Create Date: 2022-03-01 10:02:43.329951

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '316a315fa34b'
down_revision = '8335a6be66eb'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
