import pytest

# ToDO: Using a simple factory function or module to generate payload objects


@pytest.mark.django_db  
def test_create_success(api_client) -> None:  
    assert 1 == 1

@pytest.mark.django_db  
def test_create_failue_unauthirzed_user(api_client) -> None:  
    assert 1 == 1

@pytest.mark.django_db  
def test_create_failue_wrong_amount(api_client) -> None:  
    assert 1 == 1
