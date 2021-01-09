"""empty message

Revision ID: 407c3e402506
Revises: 868f08499429
Create Date: 2021-01-06 22:41:26.302929

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '407c3e402506'
down_revision = '868f08499429'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'users', ['user_name'])
    op.create_unique_constraint(None, 'users', ['email'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'users', type_='unique')
    # ### end Alembic commands ###