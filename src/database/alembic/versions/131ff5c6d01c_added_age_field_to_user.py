"""Added age field to user

Revision ID: 131ff5c6d01c
Revises: 2040e7fae3b2
Create Date: 2024-08-11 07:13:20.241431

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '131ff5c6d01c'
down_revision = '2040e7fae3b2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tg_bot_users', sa.Column('age', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tg_bot_users', 'age')
    # ### end Alembic commands ###
