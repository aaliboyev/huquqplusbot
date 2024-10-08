"""Add inquiry media fields

Revision ID: 496add647bec
Revises: 7b4c0ff52a00
Create Date: 2024-08-20 22:44:56.846508

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '496add647bec'
down_revision = '7b4c0ff52a00'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tg_bot_inquiries', sa.Column('question_mediatype', sa.Enum('text', 'voice', 'video_note', 'video', name='inquirymediatype'), nullable=False))
    op.add_column('tg_bot_inquiries', sa.Column('answer_mediatype', sa.Enum('text', 'voice', 'video_note', 'video', name='inquirymediatype'), nullable=False))
    op.add_column('tg_bot_inquiries', sa.Column('answer_media', sa.Text(), nullable=True))
    op.drop_column('tg_bot_inquiries', 'question_media_type')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tg_bot_inquiries', sa.Column('question_media_type', mysql.ENUM('text', 'voice'), nullable=False))
    op.drop_column('tg_bot_inquiries', 'answer_media')
    op.drop_column('tg_bot_inquiries', 'answer_mediatype')
    op.drop_column('tg_bot_inquiries', 'question_mediatype')
    # ### end Alembic commands ###
