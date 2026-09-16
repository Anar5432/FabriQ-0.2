"""
erp_connector.py — Read-only connection pool to BTFERPDB (SQL Server).
All queries use NOLOCK hint to avoid blocking ERP users.
"""
import pymssql
import threading
from django.conf import settings
from django.core.cache import cache

# Thread-local storage so each thread gets its own connection dictionaries
_local = threading.local()

def get_connection(db_name=None):
    """Return a thread-local persistent connection to SQL Server."""
    if not hasattr(_local, 'conns'):
        _local.conns = {}
        
    actual_db = db_name or settings.MSSQL_CONFIG['DATABASE']
    conn = _local.conns.get(actual_db)
    
    def connect():
        server = settings.MSSQL_CONFIG['SERVER'].replace(',', ':')
        return pymssql.connect(
            server=server,
            user=settings.MSSQL_CONFIG['USERNAME'],
            password=settings.MSSQL_CONFIG['PASSWORD'],
            database=actual_db,
            charset='UTF-8',
            autocommit=True
        )

    if conn is None:
        conn = connect()
        _local.conns[actual_db] = conn
    else:
        try:
            conn.cursor().execute("SELECT 1")
        except Exception:
            conn = connect()
            _local.conns[actual_db] = conn
    return conn


def query(sql, params=None, cache_key=None, cache_ttl=240, db_name=None):
    """
    Execute a read-only SQL query.
    - cache_key: if set, result is cached for cache_ttl seconds
    - Returns list of dicts
    """
    if cache_key:
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

    for attempt in range(2):
        conn = get_connection(db_name)
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            columns = [col[0] for col in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
            break
        except pymssql.OperationalError:
            actual_db = db_name or settings.MSSQL_CONFIG['DATABASE']
            if actual_db in _local.conns:
                del _local.conns[actual_db]
            if attempt == 1:
                raise
        finally:
            if 'cursor' in locals() and cursor:
                try:
                    cursor.close()
                except Exception:
                    pass

    if cache_key:
        cache.set(cache_key, rows, cache_ttl)

    return rows


def query_one(sql, params=None, cache_key=None, cache_ttl=240, db_name=None):
    """Same as query() but returns the first row or None."""
    rows = query(sql, params, cache_key, cache_ttl, db_name)
    return rows[0] if rows else None
