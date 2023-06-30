"""create posts table

Revision ID: 334ee6241dad
Revises: 
Create Date: 2023-06-28 15:04:30.510393

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '334ee6241dad'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:  
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,
    primary_key=True), sa.Column('title', sa.String(), nullable= False))
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
