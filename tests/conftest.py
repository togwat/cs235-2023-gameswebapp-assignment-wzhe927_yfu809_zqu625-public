import pytest
from games.adapters.repository.memoryrepo import MemoryRepository
from games.adapters.repository.abstractrepo import populate
from games import create_app

@pytest.fixture
def empty_repo():
    repo = MemoryRepository(genres=[], games=[], users=[])
    return repo

TEST_CSV_PATH =  "../games/adapters/data/games.csv"

@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    populate(TEST_CSV_PATH, repo)
    return repo

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,                    # Set to True during testing.
        'TEST_CSV_PATH': TEST_CSV_PATH,     # Path for loading test data into the repository.
        'WTF_CSRF_ENABLED': False           # Disable CSRF protection in test environment.
    })
    return app


@pytest.fixture
def client(app):
    return app.test_client()
class AuthenticationManager:
    def __init__(self, client):
        self.__client = client
        self.__client.post('/register',
                    data={'username': 'validuser', 'password': 'Abc123456', 'password_repeat': 'Abc123456'})

    def login(self, user_name='validuser', password='Abc123456'):
        return self.__client.post(
            '/login',
            data={'username': user_name, 'password': password}
        )

    def logout(self):
        return self.__client.get('/logout')
      
@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
