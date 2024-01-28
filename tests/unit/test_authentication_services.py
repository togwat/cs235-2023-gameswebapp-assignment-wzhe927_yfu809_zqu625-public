import pytest

from games.authentication.services import *
from games.domainmodel.model import User


@pytest.fixture
def test_user():
    user = User('username', 'dummypassword')
    return user


def test_add_user(test_user):
    add_user(test_user.username, test_user.password)

    # duplicate user
    with pytest.raises(NameNotUniqueException):
        add_user(test_user.username, 'different')


def test_get_user(test_user):
    # existing user
    assert get_user(test_user.username) == test_user

    # nonexistent user
    assert get_user('ghost') is None


def test_hash_password():
    # test invalid input
    with pytest.raises(Exception):
        hash_password(123)

    # test valid input
    assert hash_password("greetings!") == "2ccac904b966db5c0e3076e127bb12b9b0298dfe3539b91c3c01eb70a7ad8e2c"


def test_check_password():
    # test wrong password
    assert check_password("greetings!", "sire") is False

    # test correct password
    assert check_password("greetings!", "2ccac904b966db5c0e3076e127bb12b9b0298dfe3539b91c3c01eb70a7ad8e2c") is True
