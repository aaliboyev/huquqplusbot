"""added username to user

Revision ID: fcd9da75e18a
Revises: 1349ab971d6a
Create Date: 2024-08-13 16:34:23.431123

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = 'fcd9da75e18a'
down_revision = '1349ab971d6a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tg_bot_users', sa.Column('username', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tg_bot_users', 'username')
    # ### end Alembic commands ###
