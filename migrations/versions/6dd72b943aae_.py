"""empty message

Revision ID: 6dd72b943aae
Revises: d2848667622c
Create Date: 2018-12-10 19:08:07.838663

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6dd72b943aae'
down_revision = 'd2848667622c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('admin', sa.Column('create_time', sa.DateTime(), nullable=True))
    op.add_column('admin', sa.Column('grade', sa.String(length=10), nullable=True))
    op.create_index(op.f('ix_admin_create_time'), 'admin', ['create_time'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_admin_create_time'), table_name='admin')
    op.drop_column('admin', 'grade')
    op.drop_column('admin', 'create_time')
    # ### end Alembic commands ###
