"""add user table

Revision ID: 6e0bdd574888
Revises: beed4ba1b6fe
Create Date: 2023-07-09 20:36:02.850735

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e0bdd574888'
down_revision = 'beed4ba1b6fe'
branch_labels = None
depends_on = None



def upgrade():
    op.create_table('users',
    sa.Column('id', sa. Integer (), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP (timezone=True),
        server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
pass


def downgrade() -> None:
    op.drop_table('users')
    pass
