import requests
from django.core.validators import validate_email
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.helpers import date_validation, \
    send_report
from authentication.permissions import SignUpPermission, \
    CovidDataPermission
from .serializers import SignUpSerializer


class SignUpView(GenericAPIView):
    """
    post:
    API for user signup
    ```
    {
        "first_name": "string",(required)
        "last_name": "string",(required)
        "email": "string",(required)
        "password": "string",(required)
        "country": "string"(required)
    }
    ```
    """
    permission_classes = (AllowAny, SignUpPermission,)
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        token_obj, created = Token.objects.get_or_create(
            user=instance)
        return Response({"token": str(token_obj.key)},
                        status=status.HTTP_200_OK)


class CovidDataAPIView(APIView):
    """
    API to view covid data
    ```
    > To view covid data for specific country pass country
    e.g.: "/api/auth/covid-data/country={country_name}"
    > To view covid data for specific date range
    e.g.: "/api/auth/covid-data/?from_date={date}&to_date={date}"
         date format should be yyyy-mm-dd
    ```
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, CovidDataPermission,)

    def get(self, request, *args, **kwargs):
        data_filter_applied = False
        country = request.user.country
        report_of_country = self.request.GET.get('country', None)
        from_date = self.request.GET.get('from_date', None)
        to_date = self.request.GET.get('to_date', None)
        if report_of_country:
            country = report_of_country
        if (from_date or to_date) or (from_date and to_date):
            day_difference = date_validation(from_date, to_date)
            data_filter_applied = True
        response_data = requests.get(
            'https://corona-api.com/countries/{}'.format(country)
        )
        if response_data.status_code == 200:
            all_data = response_data.json().get('data').get('timeline')
            if data_filter_applied:
                custom_date = []
                for index, data in enumerate(all_data):
                    if data.get('date') == to_date:
                        custom_date.extend(
                            all_data[index:index + day_difference])
                        break
                return Response(custom_date,
                                status=status.HTTP_200_OK)
            return Response(all_data[:15],
                            status=status.HTTP_200_OK)
        else:
            return Response(response_data.json(),
                            status=response_data.status_code)


class EmailCovidDataAPIView(APIView):
    """
    API to sent covid data to email

    ```
    > valid email id is required
    > To sent covid data for specific country pass country
    e.g.: "/api/auth/covid-data/country={country_name}"
    > To sent covid data for specific date range
    e.g.: "/api/auth/covid-data/?from_date={date}&to_date={date}"
         date format should be yyyy-mm-dd
    ```
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, CovidDataPermission,)

    def get(self, request, email):
        try:
            validate_email(email)
        except Exception as e:
            print("exception", e)
            return Response(
                {"message": "Please enter valid email address."},
                status=status.HTTP_400_BAD_REQUEST)
        data_filter_applied = False
        country = request.user.country
        report_of_country = self.request.GET.get('country', None)
        from_date = self.request.GET.get('from_date', None)
        to_date = self.request.GET.get('to_date', None)
        if report_of_country:
            country = report_of_country
        if (from_date or to_date) or (from_date and to_date):
            day_difference = date_validation(from_date, to_date)
            data_filter_applied = True
        response_data = requests.get(
            'https://corona-api.com/countries/{}'.format(country)
        )
        if response_data.status_code == 200:
            all_data = response_data.json().get('data').get('timeline')
            if data_filter_applied:
                custom_date = []
                for index, data in enumerate(all_data):
                    if data.get('date') == to_date:
                        custom_date.extend(
                            all_data[index:index + day_difference])
                        break
                send_report.delay(custom_date, email)
                return Response(
                    {"message": "Email sent successfully."},
                    status=status.HTTP_200_OK)
            send_report.delay(all_data, email)
            return Response({"message": "Email sent successfully."},
                            status=status.HTTP_200_OK)
        else:
            return Response(response_data.json(),
                            status=response_data.status_code)
