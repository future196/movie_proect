"""empty message

Revision ID: fd5719d1a115
Revises: afcf9bd898c6
Create Date: 2018-12-14 23:55:01.964440

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd5719d1a115'
down_revision = 'afcf9bd898c6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('action_log',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('admin_id', sa.Integer(), nullable=True),
    sa.Column('ip', sa.String(length=255), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('action', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['admin.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_action_log_time'), 'action_log', ['time'], unique=False)
    op.create_table('admin_login_log',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('admin_id', sa.Integer(), nullable=True),
    sa.Column('ip', sa.String(length=255), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['admin_id'], ['admin.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_admin_login_log_time'), 'admin_login_log', ['time'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_admin_login_log_time'), table_name='admin_login_log')
    op.drop_table('admin_login_log')
    op.drop_index(op.f('ix_action_log_time'), table_name='action_log')
    op.drop_table('action_log')
    # ### end Alembic commands ###
