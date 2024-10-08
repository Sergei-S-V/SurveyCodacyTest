"""Add ondelete to scheduled inquiry

Revision ID: 99c1c47b8606
Revises: 77f3f29a016b
Create Date: 2024-10-01 03:30:32.760381

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "99c1c47b8606"
down_revision = "77f3f29a016b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "scheduledinquiry_inquiry_id_fkey", "scheduledinquiry", type_="foreignkey"
    )
    op.create_foreign_key(
        None, "scheduledinquiry", "inquiry", ["inquiry_id"], ["id"], ondelete="CASCADE"
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "scheduledinquiry", type_="foreignkey")
    op.create_foreign_key(
        "scheduledinquiry_inquiry_id_fkey",
        "scheduledinquiry",
        "inquiry",
        ["inquiry_id"],
        ["id"],
    )
    # ### end Alembic commands ###
