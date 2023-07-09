"""add foreign key to post table

Revision ID: f5e5cb4f36b3
Revises: 6e0bdd574888
Create Date: 2023-07-09 20:53:13.182979

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5e5cb4f36b3'
down_revision = '6e0bdd574888'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk',
                            source_table='posts',
                            referent_table='users',
                            local_cols=['owner_id'],
                            remote_cols=['id'],
                            ondelete='CASCADE'
                        )
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
