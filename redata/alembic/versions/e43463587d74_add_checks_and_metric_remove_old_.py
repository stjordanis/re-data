"""add checks and metric, remove old metrics tables

Revision ID: e43463587d74
Revises: 3144636397e6
Create Date: 2021-02-21 11:01:06.156833

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "e43463587d74"
down_revision = "3144636397e6"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "checks",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("table_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("metrics", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("query", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=True),
        sa.ForeignKeyConstraint(
            ["table_id"],
            ["monitored_table.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_checks_created_at"), "checks", ["created_at"], unique=False
    )
    op.create_index(op.f("ix_checks_table_id"), "checks", ["table_id"], unique=False)
    op.create_table(
        "metric",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("check_id", sa.Integer(), nullable=True),
        sa.Column("table_id", sa.Integer(), nullable=True),
        sa.Column("table_column", sa.String(), nullable=True),
        sa.Column("metric", sa.String(), nullable=True),
        sa.Column("params", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("result", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("created_at", sa.TIMESTAMP(), nullable=False),
        sa.ForeignKeyConstraint(
            ["check_id"],
            ["checks.id"],
        ),
        sa.ForeignKeyConstraint(
            ["table_id"],
            ["monitored_table.id"],
        ),
        sa.PrimaryKeyConstraint("id", "created_at"),
    )
    op.create_index(op.f("ix_metric_check_id"), "metric", ["check_id"], unique=False)
    op.create_index(
        op.f("ix_metric_created_at"), "metric", ["created_at"], unique=False
    )
    op.create_index(op.f("ix_metric_table_id"), "metric", ["table_id"], unique=False)
    op.create_index(op.f("ix_metric_table_column"), "metric", ["metric"], unique=False)
    op.create_index(op.f("ix_metric_metric"), "metric", ["metric"], unique=False)

    op.execute(
        f"""
        SELECT create_hypertable('metric', 'created_at', migrate_data => true)
    """
    )

    op.drop_index(
        "ix_metrics_data_volume_diff_created_at", table_name="metrics_data_volume_diff"
    )
    op.drop_index(
        "ix_metrics_data_volume_diff_table_id", table_name="metrics_data_volume_diff"
    )
    op.drop_table("metrics_data_volume_diff")
    op.drop_index("ix_metrics_data_volume_created_at", table_name="metrics_data_volume")
    op.drop_index("ix_metrics_data_volume_table_id", table_name="metrics_data_volume")
    op.drop_table("metrics_data_volume")
    op.drop_index("ix_metrics_data_delay_created_at", table_name="metrics_data_delay")
    op.drop_index("ix_metrics_data_delay_table_id", table_name="metrics_data_delay")
    op.drop_table("metrics_data_delay")
    op.drop_index(
        "ix_metrics_table_schema_changes_created_at",
        table_name="metrics_table_schema_changes",
    )
    op.drop_index(
        "ix_metrics_table_schema_changes_table_id",
        table_name="metrics_table_schema_changes",
    )
    op.drop_table("metrics_table_schema_changes")
    op.drop_index("ix_metrics_data_values_created_at", table_name="metrics_data_values")
    op.drop_index("ix_metrics_data_values_table_id", table_name="metrics_data_values")
    op.drop_table("metrics_data_values")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "metrics_data_values",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("table_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("column_name", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("column_value", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("check_name", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column(
            "check_value",
            postgresql.DOUBLE_PRECISION(precision=53),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("time_interval", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column(
            "created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=False
        ),
        sa.PrimaryKeyConstraint("id", "created_at", name="metrics_data_values_pkey"),
    )
    op.create_index(
        "ix_metrics_data_values_table_id",
        "metrics_data_values",
        ["table_id"],
        unique=False,
    )
    op.create_index(
        "ix_metrics_data_values_created_at",
        "metrics_data_values",
        ["created_at"],
        unique=False,
    )
    op.create_table(
        "metrics_table_schema_changes",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("table_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("column_name", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("column_type", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("column_count", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("operation", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column(
            "created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=False
        ),
        sa.PrimaryKeyConstraint(
            "id", "created_at", name="metrics_table_schema_changes_pkey"
        ),
    )
    op.create_index(
        "ix_metrics_table_schema_changes_table_id",
        "metrics_table_schema_changes",
        ["table_id"],
        unique=False,
    )
    op.create_index(
        "ix_metrics_table_schema_changes_created_at",
        "metrics_table_schema_changes",
        ["created_at"],
        unique=False,
    )
    op.create_table(
        "metrics_data_delay",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("table_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("value", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column(
            "created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=False
        ),
        sa.PrimaryKeyConstraint("id", "created_at", name="metrics_data_delay_pkey"),
    )
    op.create_index(
        "ix_metrics_data_delay_table_id",
        "metrics_data_delay",
        ["table_id"],
        unique=False,
    )
    op.create_index(
        "ix_metrics_data_delay_created_at",
        "metrics_data_delay",
        ["created_at"],
        unique=False,
    )
    op.create_table(
        "metrics_data_volume",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("table_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("time_interval", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column("count", sa.BIGINT(), autoincrement=False, nullable=True),
        sa.Column(
            "created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=False
        ),
        sa.PrimaryKeyConstraint("id", "created_at", name="metrics_data_volume_pkey"),
    )
    op.create_index(
        "ix_metrics_data_volume_table_id",
        "metrics_data_volume",
        ["table_id"],
        unique=False,
    )
    op.create_index(
        "ix_metrics_data_volume_created_at",
        "metrics_data_volume",
        ["created_at"],
        unique=False,
    )
    op.create_table(
        "metrics_data_volume_diff",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("table_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("date", sa.DATE(), autoincrement=False, nullable=True),
        sa.Column("count", sa.BIGINT(), autoincrement=False, nullable=True),
        sa.Column(
            "created_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=False
        ),
        sa.PrimaryKeyConstraint(
            "id", "created_at", name="metrics_data_volume_diff_pkey"
        ),
    )
    op.create_index(
        "ix_metrics_data_volume_diff_table_id",
        "metrics_data_volume_diff",
        ["table_id"],
        unique=False,
    )
    op.create_index(
        "ix_metrics_data_volume_diff_created_at",
        "metrics_data_volume_diff",
        ["created_at"],
        unique=False,
    )
    op.drop_index(op.f("ix_metric_table_id"), table_name="metric")
    op.drop_index(op.f("ix_metric_created_at"), table_name="metric")
    op.drop_index(op.f("ix_metric_check_id"), table_name="metric")
    op.drop_table("metric")
    op.drop_index(op.f("ix_checks_table_id"), table_name="checks")
    op.drop_index(op.f("ix_checks_created_at"), table_name="checks")
    op.drop_table("checks")
    # ### end Alembic commands ###
