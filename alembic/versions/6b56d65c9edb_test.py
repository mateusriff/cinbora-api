"""test

Revision ID: 6b56d65c9edb
Revises:
Create Date: 2025-07-09 20:19:25.279802

"""

from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "6b56d65c9edb"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
