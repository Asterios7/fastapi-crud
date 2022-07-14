"""add foreign-key to posts table

Revision ID: 4fb9023976f2
Revises: 162caefee785
Create Date: 2022-07-13 15:16:54.010628

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4fb9023976f2'
down_revision = '162caefee785'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', 
                          source_table="posts", 
                          referent_table="users", 
                          local_cols=['owner_id'],
                          remote_cols=['id'],
                          ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
