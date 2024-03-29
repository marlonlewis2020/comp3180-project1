"""empty message

Revision ID: 0cfb45ca9142
Revises: 13a350e07828
Create Date: 2023-03-12 11:20:43.585646

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0cfb45ca9142'
down_revision = '13a350e07828'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('property', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.String(length=80), nullable=True))
        batch_op.drop_column('name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('property', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.VARCHAR(length=80), autoincrement=False, nullable=True))
        batch_op.drop_column('title')

    # ### end Alembic commands ###
