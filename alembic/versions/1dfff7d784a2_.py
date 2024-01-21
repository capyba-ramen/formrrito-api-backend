"""empty message

Revision ID: 1dfff7d784a2
Revises: 35416ea07abf
Create Date: 2024-01-21 19:12:32.970435

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '1dfff7d784a2'
down_revision: Union[str, None] = '35416ea07abf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reply', sa.Column('response', sa.String(length=150), nullable=True, comment='回覆(簡答/詳答的答案 & 選擇題的選項)'))
    op.alter_column('reply', 'option_id',
               existing_type=mysql.INTEGER(),
               comment='問題是選擇題時才有值',
               existing_nullable=True)
    op.drop_index('answer', table_name='reply')
    op.drop_column('reply', 'answer')
    op.drop_column('reply', 'option_title')
    op.drop_column('reply', 'question_type')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reply', sa.Column('question_type', mysql.INTEGER(), autoincrement=False, nullable=True, comment='問題類型'))
    op.add_column('reply', sa.Column('option_title', mysql.VARCHAR(length=50), nullable=True, comment='選項名稱'))
    op.add_column('reply', sa.Column('answer', mysql.VARCHAR(length=150), nullable=True, comment='簡答/詳答的回覆'))
    op.create_index('answer', 'reply', ['answer'], unique=False)
    op.alter_column('reply', 'option_id',
               existing_type=mysql.INTEGER(),
               comment=None,
               existing_comment='問題是選擇題時才有值',
               existing_nullable=True)
    op.drop_column('reply', 'response')
    # ### end Alembic commands ###
