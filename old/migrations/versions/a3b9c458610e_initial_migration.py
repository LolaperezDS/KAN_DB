"""Initial migration

Revision ID: a3b9c458610e
Revises: 
Create Date: 2023-06-18 15:06:50.602078

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a3b9c458610e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('is_active', sa.Boolean(), nullable=False),
                    sa.Column('vk_id', sa.VARCHAR(length=50), unique=True),
                    sa.Column('tg_id', sa.VARCHAR(length=50), unique=True),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('full_name', sa.String(), nullable=False),
                    sa.Column('kpd_score', sa.Integer(), nullable=False),
                    sa.Column('role_id', sa.Integer(), sa.ForeignKey("roles.id")),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )
    op.create_table('roles',
                    sa.Column('id', sa.Integer(), primary_key=True, index=True),
                    sa.Column('privilege', sa.String(), index=True)
                    )
    op.create_table('events',
                    sa.Column('id', sa.Integer(), primary_key=True),
                    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.func.current_timestamp()),
                    sa.Column('event_type', sa.String(), nullable=False),
                    sa.Column('message', sa.Text(), nullable=False),
                    sa.Column('kpd_diff', sa.Integer(), nullable=False),
                    sa.Column('event_initiator_id', sa.Integer(), sa.ForeignKey("users.id")),
                    sa.Column('event_target_id', sa.Integer()),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('notification',
                    sa.Column('id', sa.Integer(), primary_key=True),
                    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.func.current_timestamp()),
                    sa.Column('event_date', sa.TIMESTAMP(), server_default=sa.func.current_timestamp()),
                    sa.Column('remind_hours', sa.Integer(), nullable=False),
                    sa.Column('message', sa.Text(), nullable=False),
                    sa.Column('is_notificated', sa.Boolean(), nullable=False),
                    sa.Column('initiator_id', sa.Integer(), sa.ForeignKey("users.id")),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('feedback',
                    sa.Column('id', sa.Integer(), primary_key=True),
                    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.func.current_timestamp()),
                    sa.Column('message', sa.Text(), nullable=False),
                    sa.Column('feedback_score', sa.Enum('value1', 'value2', name='feedbackscore')),
                    sa.Column('user_id', sa.Integer(), sa.ForeignKey("users.id")),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade():
    op.drop_table('feedback')
    op.drop_table('notification')
    op.drop_table('events')
    op.drop_table('roles')
    op.drop_table('users')
    # ### end Alembic commands ###
