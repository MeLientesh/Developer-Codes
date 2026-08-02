import pytest
from lifemap.api.routes import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_nodes(client):
    response = client.get('/api/nodes')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_node(client):
    response = client.post('/api/nodes', json={'label': 'Test Node', 'type': 'knowledge'})
    assert response.status_code == 201
    assert response.json['label'] == 'Test Node'

def test_get_relationships(client):
    response = client.get('/api/relationships')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_relationship(client):
    response = client.post('/api/relationships', json={'source_node': 1, 'target_node': 2, 'strength': 5})
    assert response.status_code == 201
    assert response.json['source_node'] == 1
    assert response.json['target_node'] == 2
    assert response.json['strength'] == 5