"""Initial migration

Revision ID: 24d136733651
Revises: 
Create Date: 2024-09-18 08:32:31.339508

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '24d136733651'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('microsoft_id', sa.String(), nullable=True),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('user_profile', sa.String(), nullable=True),
    sa.Column('timezone', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_microsoft_id'), 'users', ['microsoft_id'], unique=True)
    op.create_table('preferences',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('persona', sa.String(), nullable=True),
    sa.Column('tone', sa.String(), nullable=True),
    sa.Column('voice', sa.Enum('Ava', 'Andrew', 'Emma', 'Brian', 'Jenny', 'Guy', 'Aria', 'Davis', 'Jane', 'Jason', 'Sara', 'Tony', 'Nancy', 'Amber', 'Ana', 'Ashley', 'Brandon', 'Christopher', 'Cora', 'Elizabeth', 'Eric', 'Jacob', 'Michelle', 'Monica', 'Roger', 'Steffan', name='voiceenum'), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_preferences_id'), 'preferences', ['id'], unique=False)
    op.create_table('schedules',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('day_of_week', sa.String(), nullable=True),
    sa.Column('time_of_day', sa.Time(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_schedules_id'), 'schedules', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_schedules_id'), table_name='schedules')
    op.drop_table('schedules')
    op.drop_index(op.f('ix_preferences_id'), table_name='preferences')
    op.drop_table('preferences')
    op.drop_index(op.f('ix_users_microsoft_id'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
