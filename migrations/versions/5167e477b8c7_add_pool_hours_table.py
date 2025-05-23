"""Add pool_hours table

Revision ID: 5167e477b8c7
Revises: 58836fe13f59
Create Date: 2025-04-10 12:30:57.015972

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5167e477b8c7'
down_revision = '58836fe13f59'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pool_hours',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name_da', sa.String(length=100), nullable=False),
    sa.Column('name_en', sa.String(length=100), nullable=True),
    sa.Column('name_de', sa.String(length=100), nullable=True),
    sa.Column('name_nl', sa.String(length=100), nullable=True),
    sa.Column('description_da', sa.Text(), nullable=True),
    sa.Column('description_en', sa.Text(), nullable=True),
    sa.Column('description_de', sa.Text(), nullable=True),
    sa.Column('description_nl', sa.Text(), nullable=True),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=False),
    sa.Column('weekday_open_time', sa.Time(), nullable=True),
    sa.Column('weekday_close_time', sa.Time(), nullable=True),
    sa.Column('weekend_open_time', sa.Time(), nullable=True),
    sa.Column('weekend_close_time', sa.Time(), nullable=True),
    sa.Column('special_note_da', sa.Text(), nullable=True),
    sa.Column('special_note_en', sa.Text(), nullable=True),
    sa.Column('special_note_de', sa.Text(), nullable=True),
    sa.Column('special_note_nl', sa.Text(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('order_index', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pool_hours')
    # ### end Alembic commands ###
