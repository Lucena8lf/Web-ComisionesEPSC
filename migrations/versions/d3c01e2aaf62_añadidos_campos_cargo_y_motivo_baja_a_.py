"""Añadidos campos cargo y motivo_baja a miembros_comisiones

Revision ID: d3c01e2aaf62
Revises: 3d32127c6b9b
Create Date: 2023-05-18 12:34:00.031539

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3c01e2aaf62'
down_revision = '3d32127c6b9b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('miembros_comisiones', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cargo', sa.String(length=1000), nullable=True))
        batch_op.add_column(sa.Column('motivo_baja', sa.String(length=1000), nullable=True))
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=False,
               autoincrement=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('miembros_comisiones', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.INTEGER(),
               nullable=True,
               autoincrement=True)
        batch_op.drop_column('motivo_baja')
        batch_op.drop_column('cargo')

    # ### end Alembic commands ###
