import server.model.event as sm_event
import server.model.connection as sm_conn
import sqlalchemy


def test_list_events():
    events = sm_event.EventDal.list_events()

    assert isinstance(events, list)
    assert len(events) > 8
    event_name_list = [dct["event"] for dct in events]
    assert "orlak" in event_name_list
    assert "orore" in event_name_list
    assert "turing" in event_name_list


def test_get_current_event():
    event = sm_event.EventDal.set_current_event("test_add_events", 1993)
    result = sm_event.EventDal.get_current_event()
    assert event == result[0]


def test_get_event_id():
    event_id = sm_event.EventDal.get_event_id("turing", "2017")
    assert event_id == 18193


def test_set_current_event():
    conn = sm_conn.engine.connect()
    sm_event.EventDal.set_current_event('turing', '2017')
    #sql = sqlalchemy.text("SELECT * FROM events;")
    #event = conn.execute(sql)
    #sql = sqlalchemy.text("SELECT * FROM status")
    #other = conn.execute(sql)
    event = sm_event.EventDal.set_current_event('turing', '2017')
    #other =
    #assert event =

# Add event_id to status table
    # Add event_id to table definition in setup. DONE.
    # Add version update function. DONE.
    # Modify set_event function
    # Modify get_event function