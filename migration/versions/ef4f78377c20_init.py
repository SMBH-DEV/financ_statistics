"""init

Revision ID: ef4f78377c20
Revises: 
Create Date: 2025-02-25 16:38:39.825953

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef4f78377c20'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('statistics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.Date(), server_default=sa.text("TIMEZONE('utc', current_date)"), nullable=False),
    sa.Column('organization', sa.String(), nullable=False),
    sa.Column('object_', sa.String(), nullable=False),
    sa.Column('spent', sa.Float(), nullable=False),
    sa.Column('impressions', sa.Integer(), nullable=False),
    sa.Column('clicks', sa.Integer(), nullable=False),
    sa.Column('goals', sa.Integer(), nullable=False),
    sa.Column('ctr', sa.Float(), nullable=False, comment='Click-Through Rate - Коэффициент кликабельности (clicks / impressions)'),
    sa.Column('cpm', sa.Float(), nullable=False, comment='Cost Per Mille - Стоимость за 1000 показов (spent / impressions * 1000)'),
    sa.Column('cpc', sa.Float(), nullable=False, comment='Cost Per Click - Стоимость за клик (spent / clicks)'),
    sa.Column('cps', sa.Float(), nullable=False, comment='Cost Per Subscription - Стоимость за подписку (spent / goals)'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('statistics')
    # ### end Alembic commands ###
