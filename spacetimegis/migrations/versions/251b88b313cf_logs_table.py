"""logs_table

Revision ID: 251b88b313cf
Revises: 
Create Date: 2019-04-23 22:14:00.888300

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '251b88b313cf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('json', sa.Text(), nullable=True),
    )


def downgrade():
    op.drop_table('logs')
