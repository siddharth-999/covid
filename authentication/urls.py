from django.urls import path
from rest_framework import routers

from authentication.views import SignUpView, CovidDataAPIView, \
    EmailCovidDataAPIView

app_name = 'authentication'

router = routers.DefaultRouter()

urlpatterns = [
    path("signup/", SignUpView.as_view(),
         name="Signup"),
    path("covid-data/", CovidDataAPIView.as_view(),
         name="Covid-Data"),
    path("email-covid-data/<email>/", EmailCovidDataAPIView.as_view(),
         name="Email-Covid-Data")
]

urlpatterns += router.urls
