"""add last columns to posts table

Revision ID: 3a6597623ed3
Revises: 6ac4e5d805dd
Create Date: 2022-03-01 10:40:56.748822

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a6597623ed3'
down_revision = '6ac4e5d805dd'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(),
                  server_default='True', nullable=False))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(
        timezone=True), server_default=sa.text('now()'), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
