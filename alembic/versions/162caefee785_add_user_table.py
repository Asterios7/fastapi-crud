"""add user table

Revision ID: 162caefee785
Revises: 4d48f60c8434
Create Date: 2022-07-13 14:58:20.862161

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '162caefee785'
down_revision = '4d48f60c8434'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                               server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
