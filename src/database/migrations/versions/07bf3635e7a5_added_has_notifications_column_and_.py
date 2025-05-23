"""added has notifications column and changed id to string for users table

Revision ID: 07bf3635e7a5
Revises: c1b38ea5a193
Create Date: 2025-03-30 00:00:16.984115

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "07bf3635e7a5"
down_revision: Union[str, None] = "c1b38ea5a193"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column(
            "has_notifications",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=False,
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "has_notifications")
    # ### end Alembic commands ###
