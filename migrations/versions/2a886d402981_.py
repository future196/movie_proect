"""empty message

Revision ID: 2a886d402981
Revises: 6dd72b943aae
Create Date: 2018-12-11 19:43:08.377638

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a886d402981'
down_revision = '6dd72b943aae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('movie', 'release_time')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movie', sa.Column('release_time', sa.DATE(), nullable=True))
    # ### end Alembic commands ###
