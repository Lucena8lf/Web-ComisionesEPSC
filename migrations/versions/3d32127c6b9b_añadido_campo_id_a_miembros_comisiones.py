"""Añadido campo id a miembros_comisiones

Revision ID: 3d32127c6b9b
Revises: d17d4c7e770e
Create Date: 2023-05-11 09:28:35.265985

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d32127c6b9b'
down_revision = 'd17d4c7e770e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('miembros_comisiones', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('miembros_comisiones', schema=None) as batch_op:
        batch_op.drop_column('id')

    # ### end Alembic commands ###
