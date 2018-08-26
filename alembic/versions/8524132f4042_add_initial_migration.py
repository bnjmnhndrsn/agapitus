"""Add initial migration

Revision ID: 8524132f4042
Revises: 
Create Date: 2018-08-26 14:49:58.370444

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8524132f4042'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'post',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('date', sa.Date()),
        sa.Column('page_id', sa.Integer()),
        sa.Column('image_url', sa.String()),
        sa.Column('page_url', sa.String()),
        sa.Column('title', sa.String()),
        sa.Column('created_at', sa.DateTime()),
    )


def downgrade():
    pass
