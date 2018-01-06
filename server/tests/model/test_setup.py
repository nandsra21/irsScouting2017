"""Tests database update and setup code.

Tests code in following modules:
    * server.model.update.py
    * server.model.setup.py
"""

import pytest
import sqlalchemy
import pandas

import server.model.connection as smc
import server.model.setup as sms

TEST_USER = "irs1318test"
TEST_PW = "irs1318test"
TEST_DB = "scouting_test"


@pytest.fixture
def db_test_engine():
    # Create engine using root db account
    root_conn_str = smc.create_conn_string(user="postgres",
                                           password="irs1318")
    root_engine = sqlalchemy.create_engine(root_conn_str)

    # Create test user account
    sql_user_check = sqlalchemy.text("SELECT COUNT(*) FROM pg_roles "
                                     "WHERE rolname = :usr;")
    res = root_engine.execute(sql_user_check, usr=TEST_USER)
    if not res.scalar():
        sql_user = sqlalchemy.text("CREATE USER " + TEST_USER + " " +
                                   "WITH PASSWORD :pw CREATEDB;" )
        root_engine.execute(sql_user, pw=TEST_PW)

    # Create test database
    sql_db_check = sqlalchemy.text("SELECT COUNT(*) FROM pg_database "
                                   "WHERE datname = :testdb")
    res = root_engine.execute(sql_db_check, testdb=TEST_DB)

    conn = root_engine.connect()
    if not res.scalar():
        sql_db = sqlalchemy.text("CREATE DATABASE " + TEST_DB +
                                 " OWNER " + TEST_USER + ";")
        # root_engine.execute doesn't work for creating databases.
        conn.execute("commit")
        conn.execute(sql_db)

    conn_str = smc.create_conn_string(user=TEST_USER, password=TEST_PW,
                                      dbname=TEST_DB)
    yield smc.reset_engine(conn_str)

    # Teardown code
    smc.engine.dispose()

    sql_drop = ("DROP DATABASE IF EXISTS " + TEST_DB + ";")
    conn.execute("commit")
    conn.execute(sql_drop)
    conn.close()
    root_engine.dispose()


@pytest.fixture
def db_test_conn(db_test_engine):
    conn = db_test_engine.connect()
    yield conn
    conn.close()


@pytest.fixture
def tables(db_test_conn):
    print(type(db_test_conn))
    sms.setup()
    return True


def test_tables(tables, db_test_engine):
    assert tables
    sql = ("SELECT * FROM information_schema.tables "
           "WHERE table_schema = 'public';")
    tables = pandas.read_sql_query(sql, db_test_engine)
    assert tables.shape == (19, 12)

    def test_table(table, shape):
        sql = "SELECT * FROM " + table + ";"
        dframe = pandas.read_sql_query(sql, db_test_engine)
        assert dframe.shape == shape

    test_table("levels", (3, 2))
    test_table("matches", (168, 2))
    test_table("alliances", (3, 2))
    test_table("dates", (1, 3))
    test_table("teams", (1, 7))
    test_table("stations", (4, 2))
    test_table("actors", (7, 2))
    test_table("tasks", (92, 4))
    test_table("measuretypes", (7, 2))
    test_table("phases", (5, 2))
    test_table("attempts", (31, 2))
    test_table("reasons", (4, 2))
    test_table("task_options", (88, 4))








