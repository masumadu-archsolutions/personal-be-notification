"""add more fields

Revision ID: 3732650e624f
Revises:
Create Date: 2022-01-24 13:17:58.294062

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "3732650e624f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "email_notification", sa.Column("message_subtype", sa.String(), nullable=False)
    )
    op.add_column(
        "email_notification", sa.Column("message_template", sa.String(), nullable=False)
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("email_notification", "message_template")
    op.drop_column("email_notification", "message_subtype")
    # ### end Alembic commands ###