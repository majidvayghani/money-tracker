import pytest
from signin import retrieve_token

# ToDO: Using a simple factory function or module to generate payload objects

# @pytest.mark.django_db  
# def test_create_success_v2(api_client) -> None:
#     """
#     Test the Transaction API
    
#     Step0: User is Authenticated
#     Step1: create a Transaction (api/v2: nothing will be cached)

#     """  
          
#     assert 1 == 1
@pytest.mark.django_db  
def test_create_success(api_client) -> None:
    """
    Test the Transaction API
    
    Step0: User is Authenticated
    Step1: create a Transaction

    """  

    token = retrieve_token(api_client)
  
    payload = {
        "amount" : '123.00',
        "description" : "description",
        "category" : "category"
    }
  
    url = 'http://127.0.0.1:8000/api/v2/transactions/'
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

    response = api_client.post(url, data=payload, format="json")  
    assert response.status_code == 201  
    assert response.data["amount"] == payload["amount"]  
    assert response.data["description"] == payload["description"]  
    assert response.data["category"] == payload["category"]  
    assert response.data["origin"] == "db"  









# @pytest.mark.django_db  
# def test_create_failue_unauthirzed_user(api_client) -> None:  
#     assert 1 == 1

# @pytest.mark.django_db  
# def test_create_failue_wrong_amount(api_client) -> None:  
#     assert 1 == 1

# @pytest.mark.django_db  
# def test_get_success_v3(api_client) -> None:  
#     assert 1 == 1


#     """
#     Test the Transaction API

#     Step1: create a Transaction
#     Step2: retrieve
#     Step3: response
#     asser(pa)ca a
#     Step3: Get Profile
#     """  

