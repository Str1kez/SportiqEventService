"""empty message

Revision ID: f42147c6d873
Revises: 373208e26881
Create Date: 2023-05-01 22:04:04.505014

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "f42147c6d873"
down_revision = "373208e26881"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index(op.f("ix__event__type"), "event", ["type"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix__event__type"), table_name="event")
