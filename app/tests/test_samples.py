import pytest
from django.urls import reverse

# sample tests
def test_sample_assertion():
    """
    A sample assertion test
    """
    sky = "blue"
    assert sky == "blue"

# def test_web_index_view(client):
#     """
#     A sample assertion test for index web view
#     """
#     url = "/"                                       # note this is the url pattern name
#     response = client.get(url)                      # pass client object to render page with get request
#     assert response.status_code == 200              # testing 200 response, we can test 404s etc etc
#     assert response.content == b"Hello, world"      # check body content for text string

# future models tests go here:
# @pytest.mark.django_db
# def test_sample_app_models():
#   assert models.something == 'something'
