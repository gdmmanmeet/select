
from django.conf.urls import url
from imageservice.views import ImageService, RegenerateAuthToken

urlpatterns = [
    url(r'^token/re-generate/', RegenerateAuthToken.as_view()),
    url(r'^images/(?P<filename>[a-zA-z0-9 ()_.-]*)', ImageService.as_view())
]
