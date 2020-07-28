"""initial migration

Revision ID: b7353917367e
Revises: 9f31002244c8
Create Date: 2020-07-26 19:42:11.273574

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7353917367e'
down_revision = '9f31002244c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('sex', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_users_sex'), 'users', ['sex'], unique=False)
    op.drop_index('ix_users_class_name', table_name='users')
    op.create_index(op.f('ix_users_class_name'), 'users', ['class_name'], unique=False)
    op.drop_index('ix_users_college', table_name='users')
    op.create_index(op.f('ix_users_college'), 'users', ['college'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_college'), table_name='users')
    op.create_index('ix_users_college', 'users', ['college'], unique=1)
    op.drop_index(op.f('ix_users_class_name'), table_name='users')
    op.create_index('ix_users_class_name', 'users', ['class_name'], unique=1)
    op.drop_index(op.f('ix_users_sex'), table_name='users')
    op.drop_column('users', 'sex')
    # ### end Alembic commands ###
