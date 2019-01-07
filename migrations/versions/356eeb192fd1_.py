"""empty message

Revision ID: 356eeb192fd1
Revises: 27c121cb88e1
Create Date: 2018-12-06 13:34:21.248736

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '356eeb192fd1'
down_revision = '27c121cb88e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'email',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('user', 'icon',
               existing_type=mysql.VARCHAR(length=64),
               nullable=True)
    op.alter_column('user', 'telephone',
               existing_type=mysql.VARCHAR(length=11),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'telephone',
               existing_type=mysql.VARCHAR(length=11),
               nullable=False)
    op.alter_column('user', 'icon',
               existing_type=mysql.VARCHAR(length=64),
               nullable=False)
    op.alter_column('user', 'email',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###
