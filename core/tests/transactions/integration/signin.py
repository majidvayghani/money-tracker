
def retrieve_token(api_client) -> str:  
    """  
    Test the Profile API

    Step1: Signup
    Step3: SignIn
    Step3: Get Profile
    """  

    payload1 = {
        "email" : "test@test.com",
        "password" : "Test@1234",
        "first_name" : "test",
        "last_name" : "test"
    }
    url1 = 'http://127.0.0.1:8000/api/v2/signup'
    response1 = api_client.post(url1, data=payload1, format="json")  
 


    payload2 = {
        "email" : "test@test.com",
        "password" : "Test@1234",
    }
    url2 = 'http://127.0.0.1:8000/api/v2/signin'
    response2 = api_client.post(url2, data=payload2, format="json")
    return response2.data['token']  

