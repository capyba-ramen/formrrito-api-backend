"""empty message

Revision ID: a0f4120d79ad
Revises: 1dfff7d784a2
Create Date: 2024-01-24 20:08:16.784356

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'a0f4120d79ad'
down_revision: Union[str, None] = '1dfff7d784a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('reply_ibfk_2', 'reply', type_='foreignkey')
    op.alter_column('reply', 'option_id',
                    existing_type=mysql.INTEGER(),
                    type_=sa.String(length=500),
                    existing_comment='問題是選擇題時才有值',
                    existing_nullable=True)
    op.alter_column('reply', 'response',
                    existing_type=mysql.VARCHAR(length=150),
                    type_=sa.String(length=500),
                    existing_comment='回覆(簡答/詳答的答案 & 選擇題的選項)',
                    existing_nullable=True)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('reply', 'response',
                    existing_type=sa.String(length=500),
                    type_=mysql.VARCHAR(length=150),
                    existing_comment='回覆(簡答/詳答的答案 & 選擇題的選項)',
                    existing_nullable=True)
    op.alter_column('reply', 'option_id',
                    existing_type=sa.String(length=500),
                    type_=mysql.INTEGER(),
                    existing_comment='問題是選擇題時才有值',
                    existing_nullable=True)
    op.create_foreign_key('reply_ibfk_2', 'reply', 'option', ['option_id'], ['id'])
    # ### end Alembic commands ###
