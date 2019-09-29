"""empty message

Revision ID: 189f5fae2a81
Revises: 0d537c83a490
Create Date: 2019-09-28 09:26:24.725884

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '189f5fae2a81'
down_revision = '0d537c83a490'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('user_type', sa.Enum('ADMIN', 'FREE', 'PAID', name='usertypemodel'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('habits',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('habit_name', sa.String(), nullable=False),
    sa.Column('habit_create_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('days',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('habit_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('habit_complete', sa.Boolean(), nullable=True),
    sa.Column('day_desc', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['habit_id'], ['habits.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('days')
    op.drop_table('habits')
    op.drop_table('users')
    # ### end Alembic commands ###