"""empty message

Revision ID: 7d25638ad406
Revises: 
Create Date: 2024-11-04 15:38:18.600411

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7d25638ad406"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "favorite",
        sa.Column("movie_id", sa.Integer(), nullable=False),
        sa.Column(
            "date",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("user_tg_id", sa.BigInteger(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("movie_id", "user_tg_id", name="idx_uniq_user_movie"),
    )
    op.create_table(
        "history",
        sa.Column("movie_id", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.Column(
            "date",
            sa.Date(),
            server_default=sa.text("CURRENT_DATE"),
            nullable=False,
        ),
        sa.Column("user_tg_id", sa.BigInteger(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "movie_id", "user_tg_id", "date", name="idx_uniq_user_movie_date"
        ),
    )
    op.create_table(
        "requests",
        sa.Column("params", sa.JSON(), nullable=False),
        sa.Column("page", sa.Integer(), nullable=False),
        sa.Column("index", sa.Integer(), nullable=False),
        sa.Column("command", sa.String(), nullable=False),
        sa.Column(
            "date",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("user_tg_id", sa.BigInteger(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("requests")
    op.drop_table("history")
    op.drop_table("favorite")
    # ### end Alembic commands ###
