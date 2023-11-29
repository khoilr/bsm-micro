"""empty message

Revision ID: 2e65c8df4fd2
Revises: 26e9d5629a1a
Create Date: 2023-11-13 16:39:42.372641

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2e65c8df4fd2"
down_revision: Union[str, None] = "26e9d5629a1a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("faces", sa.Column("drawed_image_url", sa.String(length=255), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("faces", "drawed_image_url")
    # ### end Alembic commands ###