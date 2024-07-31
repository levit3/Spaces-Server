def test_protected_route_with_token(test_client):
    
    user = User.query.filter_by(name='testuser').first()
    token = jwt.encode({
        'id': user.id, 
        'expiration': str(datetime.utcnow() + timedelta(days=5))
    }, app.config['SECRET_KEY'], algorithm="HS256")
    
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = test_client.get('/api/users/1', headers=headers)
    print(response.data)
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['name'] == 'testuser'