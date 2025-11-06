from alembic import op
import sqlalchemy as sa

# Reemplaza por tu ID real de revisión y la anterior
revision = "<NUEVO_ID>"
down_revision = "8f43cbcd618"  # la última que tienes como head ahora
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
    )

def downgrade() -> None:
    op.drop_column("users", "created_at")
