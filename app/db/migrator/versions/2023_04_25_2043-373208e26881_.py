"""empty message

Revision ID: 373208e26881
Revises: 
Create Date: 2023-04-25 20:43:44.735026

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "373208e26881"
down_revision = None
branch_labels = None
depends_on = None


def init_uuid6() -> None:
    sql = """
    create or replace function uuid6() returns uuid as $$
    declare
        v_time timestamp with time zone:= null;
        v_secs bigint := null;
        v_usec bigint := null;

        v_timestamp bigint := null;
        v_timestamp_hex varchar := null;

        v_clkseq_and_nodeid bigint := null;
        v_clkseq_and_nodeid_hex varchar := null;

        v_bytes bytea;

        c_epoch bigint := -12219292800; -- RFC-4122 epoch: '1582-10-15 00:00:00'
        c_variant bit(64):= x'8000000000000000'; -- RFC-4122 variant: b'10xx...'
    begin

        -- Get seconds and micros
        v_time := clock_timestamp();
        v_secs := EXTRACT(EPOCH FROM v_time);
        v_usec := mod(EXTRACT(MICROSECONDS FROM v_time)::numeric, 10^6::numeric);

        -- Generate timestamp hexadecimal (and set version 6)
        v_timestamp := (((v_secs - c_epoch) * 10^6) + v_usec) * 10;
        v_timestamp_hex := lpad(to_hex(v_timestamp), 16, '0');
        v_timestamp_hex := substr(v_timestamp_hex, 2, 12) || '6' || substr(v_timestamp_hex, 14, 3);

        -- Generate clock sequence and node identifier hexadecimal (and set variant b'10xx')
        v_clkseq_and_nodeid := ((random()::numeric * 2^62::numeric)::bigint::bit(64) | c_variant)::bigint;
        v_clkseq_and_nodeid_hex := lpad(to_hex(v_clkseq_and_nodeid), 16, '0');

        -- Concat timestemp, clock sequence and node identifier hexadecimal
        v_bytes := decode(v_timestamp_hex || v_clkseq_and_nodeid_hex, 'hex');

        return encode(v_bytes, 'hex')::uuid;
    end $$ language plpgsql;
    """
    op.execute(sql)


def drop_uuid6() -> None:
    sql = "DROP FUNCTION IF EXISTS uuid6"
    op.execute(sql)


def drop_status_enum() -> None:
    sql = "drop type if exists eventstatus"
    op.execute(sql)


def upgrade() -> None:
    init_uuid6()
    op.create_table(
        "event_type",
        sa.Column("name", sa.TEXT(), nullable=False),
        sa.PrimaryKeyConstraint("name", name=op.f("pk__event_type")),
    )
    op.create_table(
        "event",
        sa.Column("title", sa.TEXT(), nullable=False),
        sa.Column("description", sa.TEXT(), nullable=True),
        sa.Column("address", sa.TEXT(), nullable=True),
        sa.Column("city", sa.TEXT(), nullable=False),
        sa.Column("longitude", sa.FLOAT(), nullable=False),
        sa.Column("latitude", sa.FLOAT(), nullable=False),
        sa.Column(
            "status",
            postgresql.ENUM("Удалено", "Запланировано", "Завершено", "Идет", name="eventstatus"),
            nullable=False,
            server_default=sa.text("'Запланировано'"),
        ),
        sa.Column("creator_id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("type", sa.TEXT(), nullable=False),
        sa.Column("id", sa.UUID(as_uuid=False), server_default=sa.text("uuid6()"), nullable=False),
        sa.Column("is_active", sa.BOOLEAN(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(
            ["type"], ["event_type.name"], name=op.f("fk__event__type__event_type"), ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__event")),
    )
    op.create_index(op.f("ix__event__city"), "event", ["city"], unique=False)
    op.create_index(op.f("ix__event__status"), "event", ["status"], unique=False)
    op.create_index(op.f("ix__event__latitude"), "event", ["latitude"], unique=False)
    op.create_index(op.f("ix__event__longitude"), "event", ["longitude"], unique=False)
    op.create_index(
        op.f("ix__event__location"),
        "event",
        [sa.text("point(latitude, longitude)")],
        postgresql_using="gist",
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix__event__location"), table_name="event")
    op.drop_index(op.f("ix__event__status"), table_name="event")
    op.drop_index(op.f("ix__event__city"), table_name="event")
    op.drop_index(op.f("ix__event__latitude"), table_name="event")
    op.drop_index(op.f("ix__event__longitude"), table_name="event")
    op.drop_table("event")
    op.drop_table("event_type")
    drop_uuid6()
    drop_status_enum()
