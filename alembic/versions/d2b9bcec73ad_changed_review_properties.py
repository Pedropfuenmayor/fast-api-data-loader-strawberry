"""changed review properties

Revision ID: d2b9bcec73ad
Revises: 25ecdd6dccb2
Create Date: 2024-11-17 17:49:49.846998

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd2b9bcec73ad'
down_revision: Union[str, None] = '25ecdd6dccb2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('reviews', 'title', new_column_name='comment')
    pass


def downgrade() -> None:
    op.alter_column('reviews', 'comment', new_column_name='title')
    pass
