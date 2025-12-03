from app.models.user import User

def test_password_hashing(app):
    u = User(username='test', email='test@example.com')
    u.set_password('cat')
    assert u.check_password('cat')
    assert not u.check_password('dog')

def test_user_registration(client, app):
    response = client.post('/register', data={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'password123',
        'confirm_password': 'password123'
    }, follow_redirects=True)
    # Check if registration was successful (redirects to login or shows success message)
    # Note: In our implementation, it redirects to login with a flash message
    assert response.status_code == 200
    assert b'Your account has been created' in response.data

def test_login_logout(client, app):
    # Create a user first
    with app.app_context():
        from app import db
        u = User(username='loginuser', email='login@example.com')
        u.set_password('password')
        db.session.add(u)
        db.session.commit()

    # Login
    response = client.post('/login', data={
        'username': 'loginuser',
        'password': 'password'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Dashboard' in response.data # Redirects to index

    # Logout
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Login' in response.data
