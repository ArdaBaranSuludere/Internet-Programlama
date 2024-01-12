"""initial migration

Revision ID: d1af458240e9
Revises: 
Create Date: 2024-01-03 13:50:52.609995

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1af458240e9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('movie', schema=None) as batch_op:
        batch_op.add_column(sa.Column('price', sa.Float(), nullable=False, server_default='0.00'))
        batch_op.add_column(sa.Column('stock', sa.Integer(), nullable=False, server_default='0'))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('movie', schema=None) as batch_op:
        batch_op.drop_column('stock')
        batch_op.drop_column('price')

    # ### end Alembic commands ###