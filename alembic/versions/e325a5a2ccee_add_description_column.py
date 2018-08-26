"""Add description column

Revision ID: e325a5a2ccee
Revises: 8524132f4042
Create Date: 2018-08-26 15:13:06.713278

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e325a5a2ccee'
down_revision = '8524132f4042'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('post', sa.Column('description', sa.Text))

def downgrade():
    op.drop_column('post', 'description')
