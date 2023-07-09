"""add last few columns to posts table

Revision ID: 228009f270ac
Revises: f5e5cb4f36b3
Create Date: 2023-07-09 21:00:09.189328

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '228009f270ac'
down_revision = 'f5e5cb4f36b3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'), )
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
