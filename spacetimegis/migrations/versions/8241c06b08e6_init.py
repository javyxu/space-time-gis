"""init

Revision ID: 8241c06b08e6
Revises: 47fb57036054
Create Date: 2019-04-27 10:39:48.577587

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8241c06b08e6'
down_revision = '47fb57036054'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('dbs',
        # sa.Column('created_on', sa.DateTime(), nullable=False),
        # sa.Column('changed_on', sa.DateTime(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('database_name', sa.String(length=250), nullable=True),
        sa.Column('sqlalchemy_uri', sa.String(length=1024), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('database_name'))


def downgrade():
    op.drop_table('dbs')
