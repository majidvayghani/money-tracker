import pytest

# ToDO: Using a simple factory function or module to generate payload objects

@pytest.mark.django_db  
def test_signup_success(api_client) -> None:  
    """  
    Test the signup API   
    """  
    payload = {
        "email" : "majid@majid.com",
        "password" : "Himajid@57",
        "first_name" : "majid",
        "last_name" : "majid"
    }
  
    url = 'http://127.0.0.1:8000/api/v2/users/signup'

    response = api_client.post(url, data=payload, format="json")  
    assert response.status_code == 201  
    assert response.data["email"] == payload["email"]  
    assert response.data["first_name"] == payload["first_name"]  
    assert response.data["last_name"] == payload["last_name"]  

@pytest.mark.django_db  
def test_signup_failure_duplicate_email(api_client) -> None:  
    """
    Test the Signup API. failure with duplicate email.
    step1: User A calls signup endpoint having email X returens success
    step2: User B calls signup endpoint with same email returens duplicate error
    """
    
    payload = {
        "email" : "test@test.com",
        "password" : "Himajid@57",
        "first_name" : "first_name",
        "last_name" : "last_name"
    }
  
    url = 'http://127.0.0.1:8000/api/v2/users/signup'

    response1 = api_client.post(url, data=payload, format="json")
    response2 = api_client.post(url, data=payload, format="json")

    assert response1.status_code == 201
    assert response2.status_code == 400
    assert response1.data["email"] == payload["email"]
    """
    type of response.data is ReturnDict. ReturnDict is a class provided by DRF that behaves similarly to Python's built-in dict. 
    It is used internally by serializers to represent serialized data
    serializer.errors has key and value. the value is a list of ErrorDetail instances or strings describing the validation errors.
    so in this test, response.data's value is a list
    """
    assert response2.data['email'][0] == "user with this email already exists."
    assert response2.data['email'][0].code == 'unique'
    