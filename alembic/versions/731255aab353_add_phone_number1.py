"""add phone number1

Revision ID: 731255aab353
Revises: 463c4e41ab19
Create Date: 2022-07-13 16:00:53.667010

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '731255aab353'
down_revision = '463c4e41ab19'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    # ### end Alembic commands ###