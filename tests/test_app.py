from http import HTTPStatus

from fastapi.testclient import TestClient

from learning_fastapi.app import app


def test_root_deve_retornar_ola():
    """
    Esse teste tem 3 etapas (AAA)
    - A: Arrange
    - A: Act
    - A: Assert
    """

    # arrange
    client = TestClient(app)

    # act
    response = client.get('/')

    # assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'ola'}
