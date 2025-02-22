import pytest
from sqlalchemy.exc import TimeoutError, OperationalError
from db import DB


def test_db_connection_timeout(mocker):
    # Simulate TimeoutError
    mocker.patch("db.create_engine", side_effect=TimeoutError)

    # Test DB Connection
    with pytest.raises(TimeoutError):
        db = DB()  #


def test_session_failure(session, mocker, task1):
    db = DB()

    # Correctly instantiate an OperationalError for mocking
    operational_error = OperationalError(
        statement="some SQL statement",
        params={},
        orig=Exception("Session Cannot Be Created"),
    )

    # Mock the `commit` method of the session to raise the mocked OperationalError
    mocker.patch.object(session, "commit", side_effect=operational_error)

    with pytest.raises(OperationalError):
        db.create_task(task=task1, session=session)
