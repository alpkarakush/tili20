"""User password addition

Revision ID: d1f7068438e9
Revises: 73edc2773cd0
Create Date: 2024-01-30 16:19:38.513812

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1f7068438e9'
down_revision = '73edc2773cd0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('definition', 'upvotes',
               existing_type=sa.INTEGER,
               nullable=False)
    op.alter_column('definition', 'downvotes',
               existing_type=sa.INTEGER,
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('definition', 'downvotes',
               existing_type=sa.INTEGER,
               nullable=True)
    op.alter_column('definition', 'upvotes',
               existing_type=sa.INTEGER,
               nullable=True)
    # ### end Alembic commands ###
