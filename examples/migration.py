"""empty message

Revision ID: e5a927bdb33c
Revises: 
Create Date: 2023-04-16 22:16:30.294433

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "e5a927bdb33c"
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
    sql = "DROP FUNCTION IF EXISTS uuid6;"
    op.execute(sql)


def upgrade() -> None:
    init_uuid6()
    # your code


def downgrade() -> None:
    # your code
    drop_uuid6()
