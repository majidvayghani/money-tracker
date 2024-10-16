import pytest

# ToDO: Using a simple factory function or module to generate payload objects

@pytest.mark.integration
@pytest.mark.django_db  
def test_signup_success(api_client) -> None:  
    """  
    Test the signup API   
    """  
    payload = {
        "email" : "test@test.com",
        "password" : "Test@1234"
    }
  
    url = 'http://127.0.0.1:8000/api/v2/signup'

    response = api_client.post(url, data=payload, format="json")  
    assert response.status_code == 201  
    assert response.data["email"] == payload["email"]

@pytest.mark.integration
@pytest.mark.django_db  
def test_signup_failure_duplicate_email(api_client) -> None:  
    """
    Test the Signup API. failure with duplicate email.
    step1: User A calls signup endpoint having email X returens success
    step2: User B calls signup endpoint with same email returens duplicate error
    """
    
    payload = {
        "email" : "test@test.com",
        "password" : "Test@1234"
    }
  
    url = 'http://127.0.0.1:8000/api/v2/signup'

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

@pytest.mark.integration
@pytest.mark.django_db  
def test_signup_failure_empty_password(api_client) -> None:  
    """
    Test the Signup API. failure with password that does not meet the requirements.
    calling signup endpoint having no password or less than 8 characters
    """
    
    payload = {
        "email" : "test@test.com",
        "password" : ""
    }
  
    url = 'http://127.0.0.1:8000/api/v2/signup'

    response = api_client.post(url, data=payload, format="json")

    assert response.status_code == 400
    # assert response.data['password'][0] == "Password must be at least 8 characters long"

@pytest.mark.integration
@pytest.mark.django_db  
def test_signup_failure_invalid_password(api_client) -> None:  
    """
    Test the Signup API. failure with password that does not meet the requirements.
    requirement 1: password has at least 1 number
    requirement 2: password has at least 1 uppercase letter
    requirement 3: password has at least 1 lowercase letter
    requirement 4: password has at least 1 special character
    """
    
    payload = {
        "email" : "test@test.com",
        "password" : "123"
    }
  
    url = 'http://127.0.0.1:8000/api/v2/signup'

    response = api_client.post(url, data=payload, format="json")

    assert response.status_code == 400

    # value = response.data['password'][0]
    
    # match value:
    #     case "Password must contain at least one number.":
    #         assert value == "Password must contain at least one number."
    #     case "Password must contain at least one uppercase letter.":
    #         assert value == "Password must contain at least one uppercase letter."
    #     case "Password must contain at least one lowercase letter.":
    #         assert value == "Password must contain at least one lowercase letter."
    #     case "Password must contain at least one special character.":
    #         assert value == "Password must contain at least one special character."

