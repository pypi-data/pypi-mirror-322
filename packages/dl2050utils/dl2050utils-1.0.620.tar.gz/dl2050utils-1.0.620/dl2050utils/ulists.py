from dl2050utils.common import oget, now
from dl2050utils.core import LexIdx

# #############################################################################################################################
# Ulists
# #############################################################################################################################

async def ulists_insert(db, email, ulist_code=None, ulist_group=None, ulist_name=None, ulist_payload=None, id1=None, id2=None):
    """
    Inserts a new ulist into the database.
    Returns False on success, True on error.
    """
    # If ulist_code is provided, check if UList record exists, and returns it if it exists
    if ulist_code is not None:
        res = await db.select('ulists', filters={'email':email, 'ulist_code':ulist_code}, limit=1)
        rows = oget(res,['data'],[])
        if len(rows)!=0: return rows[0]
    # Otherwise create the record
    row = {'email':email, 'ulist_code':ulist_code, 'ulist_group':ulist_group, 'ulist_name':ulist_name,
           'ulist_payload':ulist_payload, 'created_at': now()}
    # Manage order
    l = LexIdx()
    # If id2 is not specified inserts in the end
    if id2 is None:
        seq = await db.execute(f"select max(lexseq) from ulists where email='{email}' and ulist_group='{ulist_group}'")
        lseq = l.next(oget(seq,[0,'max']))
    # Otherwise interpolates
    else:
        # Interpolation deals with None for id1
        lseq = l.interpolate(id1, id2)
    row['lexseq'] = lseq
    row['ulist_id'] = await db.insert('ulists', row, return_key='ulist_id')
    return row

async def ulists_update(db, email, ulist_id, ulist_code=None, ulist_group=None, ulist_name=None, ulist_payload=None, id1=None, id2=None):
    """
    Returns False on success, True on error.
    """
    # Create the record
    row = {'ulist_id':ulist_id, 'email':email, 'ulist_code':ulist_code, 'ulist_group':ulist_group, 'ulist_name':ulist_name,
           'ulist_payload':ulist_payload}
    # Re-order if necessary
    if id1 is not None or id2 is not None:
        l = LexIdx()
        # If id2 is not specified, moves to the end
        if id2 is None:
            res = await db.execute(f"select max(lexseq) from ulists where email='{email}' and ulist_group='{ulist_group}'")
            lseq = oget(res,[0,'max'])
            lseq = l.next(lseq)
        else:
            row1 = await db.select_one('ulists', filters={'id':id1})
            row2 = await db.select_one('ulists', filters={'id':id2})
            lseq1,lseq2 = oget(row1,['lexseq']),oget(row2,['lexseq'])
            lseq = l.interpolate(lseq1, lseq2)
        row['lexseq'] = lseq
    n = await db.update('ulists', 'ulist_id', row, read_only_cols=['ulist_id'])
    return n!=1

async def ulists_delete(db, email, ulist_id):
    """
    Returns False on success, True on error.
    """
    n = await db.delete('ulists', ['email', 'ulist_id'], [email, ulist_id])
    return n!=1

async def ulists_select(db, email, ulist_id=None, ulist_group=None, ulist_code=None):
    """
    Selects ulists for user defined by email, based on seach criteria id and code
    """
    filters = {'email':email}
    if ulist_id is not None: filters['ulist_id'] = ulist_id
    if ulist_group is not None: filters['ulist_group'] = ulist_group
    if ulist_code is not None: filters['ulist_code'] = ulist_code
    res = await db.select('ulists', filters=filters, sort='lexseq', limit=1024)
    rows = oget(res,['data'])
    return rows

# #############################################################################################################################
# Items
# #############################################################################################################################

async def ulist_items_insert(db, email, ulist_id, item_code=None, item_name=None, item_payload=None, id1=None, id2=None):
    """
    Inserts a new item for an ulist.
    Returns False on success, True on error.
    """
    # Create the record
    row = {'email':email, 'ulist_id':ulist_id, 'item_code':item_code, 'item_name':item_name,
           'item_payload':item_payload, 'created_at': now()}
    # Manage order
    l = LexIdx()
    # If id2 is not specified inserts in the end
    if id2 is None:
        seq = await db.execute(f"select max(lexseq) from ulists where email='{email}' and ulist_id='{ulist_id}'")
        lseq = l.next(oget(seq,[0,'max']))
    # Otherwise interpolates
    else:
        # Interpolation deals with None for id1
        lseq = l.interpolate(id1, id2)
    row['lexseq'] = lseq
    await db.insert('ulist_items', row)
    return None

async def ulist_items_update(db, email, item_id, ulist_id, item_code=None, item_name=None, item_payload=None, id1=None, id2=None):
    """
    Returns True on error, False if everything ok.
    """
    # Create the record
    row = {'item_id':item_id, 'email':email, 'item_code':item_code, 'item_name':item_name, 'item_payload':item_payload}
    # Re-order if necessary
    if id1 is not None or id2 is not None:
        l = LexIdx()
        # If id2 is not specified, moves to the end
        if id2 is None:
            res = await db.execute(f"select max(lexseq) from ulists where email='{email}' and ulist_group='{ulist_id}'")
            lseq = oget(res,[0,'max'])
            lseq = l.next(lseq)
        else:
            row1 = await db.select_one('ulists', filters={'id':id1})
            row2 = await db.select_one('ulists', filters={'id':id2})
            lseq1,lseq2 = oget(row1,['lexseq']),oget(row2,['lexseq'])
            lseq = l.interpolate(lseq1, lseq2)
        row['lexseq'] = lseq
    n = await db.update('ulist_items', 'ulist_id', row, read_only_cols=['item_id'])
    return n!=1

async def ulist_items_delete(db, email, ulist_item_id):
    """
    Returns False on success, True on error.
    """
    n = await db.delete('ulist_items', ['email', 'ulist_item_id'], [email, ulist_item_id])
    return n!=1

async def ulist_items_select(db, email, ulist_id):
    """
    Selects all items from an ulist with a 1024 limit.
    Returns de selected rows.
    """
    filters = {'email':email, 'ulist_id':ulist_id}
    res = await db.select('ulist_items', filters=filters, sort='lexseq', limit=1024)
    rows = oget(res,['data'])
    return rows
