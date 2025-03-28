import pytest

@pytest.mark.integration
@pytest.mark.django_db  
def test_retrieve_profile_success(api_client) -> None:  
    """  
    Test the Profile API

    Step1: Signup
    Step3: SignIn
    Step3: Get Profile
    """  

    payload1 = {
        "email" : "test@test.com",
        "password" : "Test@1234"
    }

    url1 = 'http://127.0.0.1:8000/api/v2/signup'
    response1 = api_client.post(url1, data=payload1, format="json")  
    assert response1.status_code == 201

    payload2 = {
        "email" : "test@test.com",
        "password" : "Test@1234",
    }
    
    url2 = 'http://127.0.0.1:8000/api/v2/signin'
    response2 = api_client.post(url2, data=payload2, format="json")  
    assert response2.status_code == 200 

    api_client.credentials(HTTP_AUTHORIZATION=f"Token {response2.data['token']}")
    url = 'http://127.0.0.1:8000/api/v2/profile'
    response3 = api_client.get(url)

    assert response3.status_code == 200
