"""add content column to posts table

Revision ID: beed4ba1b6fe
Revises: 334ee6241dad
Create Date: 2023-07-09 20:29:31.455918

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'beed4ba1b6fe'
down_revision = '334ee6241dad'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
