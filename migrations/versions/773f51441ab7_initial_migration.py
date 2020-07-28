"""initial migration

Revision ID: 773f51441ab7
Revises: b7353917367e
Create Date: 2020-07-26 21:14:55.834345

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '773f51441ab7'
down_revision = 'b7353917367e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_num', sa.String(length=11), nullable=True))
    op.create_index(op.f('ix_users_phone_num'), 'users', ['phone_num'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_phone_num'), table_name='users')
    op.drop_column('users', 'phone_num')
    # ### end Alembic commands ###
