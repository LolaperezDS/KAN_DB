"""creating test tables

Revision ID: 476c2091116f
Revises: a3b9c458610e
Create Date: 2023-06-18 15:31:14.756720

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '476c2091116f'
down_revision = 'a3b9c458610e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('courses',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('course_code', sa.String(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('description', sa.Text(), nullable=False),
                    sa.Column('teacher', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )
    op.create_table('students',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('student_code', sa.String(), nullable=False),
                    sa.Column('full_name', sa.String(), nullable=False),
                    sa.Column('date_of_birth', sa.TIMESTAMP(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('phone_number', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )
    op.create_table('assignments',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('course_id', sa.Integer(), nullable=True),
                    sa.Column('description', sa.Text(), nullable=False),
                    sa.Column('deadline', sa.TIMESTAMP(), nullable=False),
                    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )
    op.create_table('attendance',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('student_id', sa.Integer(), nullable=True),
                    sa.Column('course_id', sa.Integer(), nullable=True),
                    sa.Column('date', sa.TIMESTAMP(), nullable=False),
                    sa.Column('is_present', sa.Boolean(), nullable=False),
                    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
                    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )
    op.create_table('enrollments',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('student_id', sa.Integer(), nullable=True),
                    sa.Column('course_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
                    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )
    op.create_table('grades',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('student_id', sa.Integer(), nullable=True),
                    sa.Column('course_id', sa.Integer(), nullable=True),
                    sa.Column('grade', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
                    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('grades')
    op.drop_table('enrollments')
    op.drop_table('attendance')
    op.drop_table('assignments')
    op.drop_table('students')
    op.drop_table('courses')
    # ### end Alembic commands ###
