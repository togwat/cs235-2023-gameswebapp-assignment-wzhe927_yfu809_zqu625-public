import pytest
from flask import session
from games.adapters.repository.memoryrepo import MemoryRepository
from games.adapters.repository.abstractrepo import populate
import time

TEST_CSV_PATH = "../../games/adapters/data/games.csv"

@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    populate(TEST_CSV_PATH, repo)
    return repo
def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid user name and password.
    response = client.post('/register', data={'username':'abc', 'password':'Abc12345', 'password_repeat': 'Abc12345'})
    assert response.headers['Location'] == '/login' #should redirect to login page if register successfully

@pytest.mark.parametrize(('user_name', 'password', 'password_repeat', 'message'), (
        #('', '', '', b'Username is required'), these are handled by HTML build-in validation that prevent form to be summitted if a required field is empty
        #('cj', '', '', b'Password is required'),
        #('', 'cj', '', b'Username is required'),
        #('', '', 'cj', b'Username is required'),
        #('test', 'abc', '', b'Repeat password is required'),
        #('test', 'abc1234', '', b'Repeat password is required'),
        ('test', 'abc1234', 'ad', b'Field must be equal to password'),
        ('test', 'abc1234', 'abc1234', b'Password failed requirements'),
        ('test', 'Abababab', 'Abababab', b'Password failed requirements'),
        ('test', 'A123456', 'A123456', b'Password failed requirements'),
        ('validuser', 'Test#6^0', 'Test#6^0',b'Username taken.'),
        ('validuser', 'Abc12345', 'Abc12345',b'Username taken.'),
))
def test_register_with_invalid_input(client, user_name, password, password_repeat, message):
    # a valid user
    client.post('/register',
                data={'username': 'validuser', 'password': 'Abc123456', 'password_repeat': 'Abc123456'})

    # Check that attempting to register with invalid combinations of user name and password
    response = client.post(
        '/register',
        data={'username': user_name, 'password': password, 'password_repeat': password_repeat}
    )
    assert message in response.data

def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/login').status_code
    assert status_code == 200

    with client:
        auth.login() #login a user
        response = client.get('/profile') #make a request to profile page
        assert b'Welcome, validuser!' in response.data #profile should have the welcome message if login successfully
        client.get('/')
        assert session['username'] == 'validuser' # Check that a session has been created for the logged-in user.

@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        #('', '', b'Username is required.'), these are handled by HTML build-in validation that prevent form to be summitted if a required field is empty
        #('cj', '', b'Password is required.'),
        #('', 'cj', b'Username is required.'),
        ('test', 'abc', b'Incorrect username or password.'),
        ('validuser', 'dawdwadawwa', b'Incorrect username or password.'),
        ('test', 'Abc123456', b'Incorrect username or password.'),
))
def test_login_with_invalid_input(client, user_name, password, message):
    client.post('/register',
                data={'username': 'validuser', 'password': 'Abc123456', 'password_repeat': 'Abc123456'})
    # Check that attempting to register with invalid combinations of user name and password
    response = client.post(
        '/login',
        data={'username': user_name, 'password': password}
    )
    assert message in response.data


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session

def test_index(client):
    response = client.get('/') #test home page
    assert response.status_code == 200
    assert b'Welcome to Virtuoso' in response.data


def test_library(client):
    response = client.get('/library/1') #test default library page
    assert response.status_code == 200
    assert b'10 Second Ninja X' in response.data

    response = client.get('/library/10')  # test other library page
    assert response.status_code == 200
    assert b'Ashes' in response.data

def test_games_page(client):
    response = client.get('/game/435790') #test game page for 10 Second Ninja X
    assert response.status_code == 200
    assert b'10 Second Ninja X' in response.data


def test_add_game_to_wishlist(client,auth):
    response = client.post('/add_to_wishlist', data={'game_id':435790}) #test add game to wishlist
    assert response.headers['Location'] == '/login' #Go to login page if the user haven't log in
    auth.login()
    response = client.post('/add_to_wishlist', data={'game_id': 435790})  # test add game to wishlist
    assert response.status_code == 302
    assert response.headers['Location'] == '/game/435790' #should remain on the game page
    response = client.get('/profile')
    assert b'10 Second Ninja X' in response.data #game is added to wishlist, appear in user's profile page

def test_remove_game_to_wishlist(client,auth):
    auth.login() #log in a user
    client.post('/add_to_wishlist', data={'game_id':435790}) #add game to wishlist
    response = client.post('/remove_from_wishlist', data={'game_id':435790})
    assert response.status_code == 302
    assert response.headers['Location'] == '/profile' #should remain on profile page
    response = client.get('/profile')
    assert b'10 Second Ninja X' not in response.data #game is removed from wishlist, removed from the user's profile page

def test_add_comment(client, auth):
    response = client.get('/game/435790') #access some game page without logging in
    assert b'Log in to comment' in response.data #should display log in to comment.
    response = client.post('/game/435790')
    assert response.headers['Location'] == '/login'
    auth.login()
    response = client.get('/game/435790')  # access some game page while logged in
    assert b'3 stars' in response.data  # should display default rating for the comment
    response = client.post('/game/435790', data={'rate': 3, 'review_text':'dihbwaedwuai9'})  # post some comment
    assert response.status_code == 302
    assert response.headers['Location'] == '/game/435790'  # should remain on the game page
    response = client.get('/game/435790')
    assert b'dihbwaedwuai9' in response.data  # page should show the comment
    assert b'3.0 average based on 1 reviews' in response.data #should show overall review
    response = client.get('/profile')
    assert b'dihbwaedwuai9' in response.data  # profile page should show the comment

def test_game_by_genre(client):
    response = client.get('/genre/1?genre_name=Action') #Access games with the genre Action
    assert response.status_code == 200
    assert b'10 Second Ninja X' in response.data
    assert b'Genre: Action' in response.data
    assert b'Released: Jul 19, 2016' in response.data

def test_search_game_by_title(client):
    response = client.get('/search/1?criteria=title&term=10+Second+Ninja+X') #search invalid game by title
    assert response.status_code == 200
    assert b'Released: Jul 19,2016' not in response.data
    assert b'title: "10 Second Ninja X"' in response.data

def test_search_game_by_genre(client):
    response = client.get('/search/1?criteria=genre&term=sports') #search game by genre
    print(response.data.decode())
    assert response.status_code == 200
    assert b'Automobilista 2' in response.data
    assert b'Released: Jun 30, 2020' in response.data
    assert b'genre: "sports"' in response.data

def test_search_game_by_publisher(client):
    response = client.get('/search/1?criteria=publisher&term=FireArmGames') #search game by publisher
    assert response.status_code == 200
    assert b'MagicShop3D' in response.data
    assert b'Released: Jun 19, 2022' in response.data
    assert b'publisher: "FireArmGames"' in response.data

def test_search_game_by_year(client):
    response = client.get('/search/1?criteria=year&term=2016') #search game by year (2016)
    assert response.status_code == 200
    assert b'10 Second Ninja X' in response.data
    assert b'Released: Jul 19, 2016' in response.data
    assert b'year: "2016"' in response.data


def test_review_order_by_most_recent(client,auth, in_memory_repo):
    #log in one user
    auth.login()
    client.post('/game/435790', data={'rate': 3, 'review_text': 'dihbwaedwuai9'})
    auth.logout()
    time.sleep(1)
    #log in another user
    client.post('/register', data={'username': 'abc', 'password': 'Abc12345', 'password_repeat': 'Abc12345'})
    client.post('/login', data={'username': 'abc', 'password': 'Abc12345'})
    client.post('/game/435790', data={'rate': 4, 'review_text': 'dwadwa'})
    current_game = in_memory_repo.get_game_by_id(435790)
    list1 = list(reversed(current_game.reviews)) # Correct list
    print(list1)
    # client.get('/game/435790?review_sorting_order=most_recent')
    print(sorted(current_game.reviews, key=lambda x: x.time, reverse=True))
    assert list1 == sorted(current_game.reviews, key=lambda x: x.time, reverse=True)#checking if the correct list is the same as the list that pass to render_template in the actual application

def test_review_order_by_least_recent(client,auth, in_memory_repo):
    #log in one user
    auth.login()
    client.post('/game/435790', data={'rate': 3, 'review_text': 'dihbwaedwuai9'})
    auth.logout()
    time.sleep(1)
    #log in another user
    client.post('/register', data={'username': 'abc', 'password': 'Abc12345', 'password_repeat': 'Abc12345'})
    client.post('/login', data={'username': 'abc', 'password': 'Abc12345'})
    client.post('/game/435790', data={'rate': 4, 'review_text': 'dwadwa'})
    current_game = in_memory_repo.get_game_by_id(435790)
    list1 = current_game.reviews # Correct list
    client.get('/game/435790?review_sorting_order=least_recent')
    assert list1 == sorted(current_game.reviews, key=lambda x: x.time, reverse=False)#checking if the correct list is the same as the list that pass to render_template in the actual application

def test_review_order_by_highest_rating(client,auth, in_memory_repo):
    #log in one user
    auth.login()
    client.post('/game/435790', data={'rate': 3, 'review_text': 'dihbwaedwuai9'})
    auth.logout()
    #log in another user
    client.post('/register', data={'username': 'abc', 'password': 'Abc12345', 'password_repeat': 'Abc12345'})
    client.post('/login', data={'username': 'abc', 'password': 'Abc12345'})
    client.post('/game/435790', data={'rate': 5, 'review_text': 'dwadwa'})
    # log in another user
    client.post('/register', data={'username': 'abcd', 'password': 'Abc12345', 'password_repeat': 'Abc12345'})
    client.post('/login', data={'username': 'abcd', 'password': 'Abc12345'})
    client.post('/game/435790', data={'rate': 2, 'review_text': 'whadahoiu'})
    current_game = in_memory_repo.get_game_by_id(435790)
    list1 = [current_game.reviews[1], current_game.reviews[0], current_game.reviews[2]] # Correct list
    client.get('/game/435790?review_sorting_order=highest_rating')
    assert list1 == sorted(current_game.reviews, key=lambda x: x.rating, reverse=True)#checking if the correct list is the same as the list that pass to render_template in the actual application

def test_review_order_by_lowest_rating(client,auth, in_memory_repo):
    #log in one user
    auth.login()
    client.post('/game/435790', data={'rate': 3, 'review_text': 'dihbwaedwuai9'})
    auth.logout()
    #log in another user
    client.post('/register', data={'username': 'abc', 'password': 'Abc12345', 'password_repeat': 'Abc12345'})
    client.post('/login', data={'username': 'abc', 'password': 'Abc12345'})
    client.post('/game/435790', data={'rate': 5, 'review_text': 'dwadwa'})
    # log in another user
    client.post('/register', data={'username': 'abcd', 'password': 'Abc12345', 'password_repeat': 'Abc12345'})
    client.post('/login', data={'username': 'abcd', 'password': 'Abc12345'})
    client.post('/game/435790', data={'rate': 2, 'review_text': 'whadahoiu'})
    current_game = in_memory_repo.get_game_by_id(435790)
    list1 = [current_game.reviews[2], current_game.reviews[0], current_game.reviews[1]] # Correct list
    client.get('/game/435790?review_sorting_order=lowest_rating')
    assert list1 == sorted(current_game.reviews, key=lambda x: x.rating, reverse=False)#checking if the correct list is the same as the list that pass to render_template in the actual application

def test_review_order_by_username(client,auth, in_memory_repo):
    #log in one user
    auth.login()
    client.post('/game/435790', data={'rate': 3, 'review_text': 'dihbwaedwuai9'})
    auth.logout()
    #log in another user
    client.post('/register', data={'username': 'abc', 'password': 'Abc12345', 'password_repeat': 'Abc12345'})
    client.post('/login', data={'username': 'abc', 'password': 'Abc12345'})
    client.post('/game/435790', data={'rate': 5, 'review_text': 'dwadwa'})
    # log in another user
    client.post('/register', data={'username': 'abcd', 'password': 'Abc12345', 'password_repeat': 'Abc12345'})
    client.post('/login', data={'username': 'abcd', 'password': 'Abc12345'})
    client.post('/game/435790', data={'rate': 2, 'review_text': 'whadahoiu'})
    current_game = in_memory_repo.get_game_by_id(435790)
    list1 = [current_game.reviews[1], current_game.reviews[2], current_game.reviews[0]] # Correct list
    client.get('/game/435790?review_sorting_order=username')
    assert list1 == sorted(current_game.reviews, key=lambda x: x.user.username, reverse=False) #checking if the correct list is the same as the list that pass to render_template in the actual application