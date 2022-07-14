"""add last few columns to posts table

Revision ID: 36ab400c8bb4
Revises: 4fb9023976f2
Create Date: 2022-07-13 15:31:24.498573

"""
from pickle import TRUE
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36ab400c8bb4'
down_revision = '4fb9023976f2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', 
                  sa.Column('published', sa.Boolean(), nullable=False, server_default='True'),)
    op.add_column('posts', 
                  sa.Column('created_at', sa.TIMESTAMP(), nullable=False, server_default=sa.text('now()')),)
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
