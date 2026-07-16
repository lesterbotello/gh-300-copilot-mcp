"""Initial database schema.

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-07-16 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "activities",
        sa.Column("name", sa.String(length=255), primary_key=True, nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("schedule", sa.String(length=255), nullable=False),
        sa.Column("max_participants", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.create_table(
        "users",
        sa.Column("email", sa.String(length=255), primary_key=True, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=True),
        sa.Column("role", sa.String(length=50), nullable=False, server_default=sa.text("'member'")),
        sa.Column("grade_level", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.create_table(
        "registrations",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("activity_name", sa.String(length=255), sa.ForeignKey("activities.name", ondelete="CASCADE"), nullable=False),
        sa.Column("email", sa.String(length=255), sa.ForeignKey("users.email", ondelete="CASCADE"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.UniqueConstraint("activity_name", "email", name="uq_registration_activity_email"),
    )
    op.create_table(
        "complaints",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default=sa.text("'open'")),
        sa.Column("activity_name", sa.String(length=255), sa.ForeignKey("activities.name", ondelete="SET NULL"), nullable=True),
        sa.Column("submitted_by_email", sa.String(length=255), sa.ForeignKey("users.email", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.create_table(
        "feedback",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("complaint_id", sa.Integer(), sa.ForeignKey("complaints.id", ondelete="CASCADE"), nullable=False),
        sa.Column("author_email", sa.String(length=255), sa.ForeignKey("users.email", ondelete="SET NULL"), nullable=True),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("feedback")
    op.drop_table("complaints")
    op.drop_table("registrations")
    op.drop_table("users")
    op.drop_table("activities")
