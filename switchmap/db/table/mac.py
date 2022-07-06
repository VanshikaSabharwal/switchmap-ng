"""Module for querying the Mac table."""

from sqlalchemy import select, update, null

# Import project libraries
from switchmap.db import db
from switchmap.db.models import Mac
from switchmap.db.table import RMac
from switchmap.db.table import oui
from switchmap.core import general


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_mac

    Returns:
        result: RMac object

    """
    # Initialize key variables
    result = False
    rows = []

    # Get data
    statement = select(Mac).where(Mac.idx_mac == idx)
    rows = db.db_select_row(1097, statement)

    # Return
    for row in rows:
        result = _row(row)
        break
    return result


def exists(_mac):
    """Determine whether idx_event exists in the Mac table.

    Args:
        _mac: Mac address

    Returns:
        result: RMac tuple

    """
    # Initialize key variables
    result = False
    rows = []

    # Fix the MAC address
    mac = general.mac(_mac)

    # Get row from dataase
    statement = select(Mac).where(Mac.mac == mac.encode())
    rows = db.db_select_row(1178, statement)

    # Return
    for row in rows:
        result = _row(row)
        break
    return result


def insert_row(rows):
    """Create a Mac table entry.

    Args:
        rows: TopologyMac objects

    Returns:
        None

    """
    # Initialize key variables
    inserts = []

    # Create list
    if isinstance(rows, list) is False:
        rows = [rows]

    # Create objects
    for row in rows:
        # Fix the MAC address
        mac = general.mac(row.mac)

        # Find the true idx_oui
        idx_oui = oui.idx_oui(mac)

        # Do the insertion
        inserts.append(
            Mac(
                idx_oui=idx_oui,
                idx_event=row.idx_event,
                idx_zone=row.idx_zone,
                mac=(
                    null() if bool(mac) is False else mac.encode()),
                enabled=row.enabled
            )
        )

    # Insert
    if bool(inserts):
        db.db_add_all(1087, inserts)


def update_row(idx, row):
    """Upadate a Mac table entry.

    Args:
        idx: idx_mac value
        row: IMac object

    Returns:
        None

    """
    # Fix the MAC address
    mac = general.mac(row.mac)

    # Find the true idx_oui
    idx_oui = oui.idx_oui(mac)

    # Update
    statement = update(Mac).where(
        Mac.idx_mac == idx).values(
            {
                'idx_oui': idx_oui,
                'idx_event': row.idx_event,
                'idx_zone': row.idx_zone,
                'mac': (
                    null() if bool(mac) is False else mac.encode()),
                'enabled': row.enabled
            }
        )
    db.db_update(1114, statement)


def _row(row):
    """Convert table row to tuple.

    Args:
        row: Mac row

    Returns:
        result: RMac tuple

    """
    # Initialize key variables
    result = RMac(
        idx_mac=row.idx_mac,
        idx_oui=row.idx_oui,
        idx_event=row.idx_event,
        idx_zone=row.idx_zone,
        mac=(
            None if bool(row.mac) is False else row.mac.decode()),
        enabled=row.enabled,
        ts_created=row.ts_created,
        ts_modified=row.ts_modified
    )
    return result
