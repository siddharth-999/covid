from django_countries.serializer_fields import CountryField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False, allow_blank=False,
                                       allow_null=False, max_length=254)
    last_name = serializers.CharField(required=False, allow_blank=False,
                                      allow_null=False, max_length=254)
    password = serializers.CharField(required=True, allow_blank=False,
                                     allow_null=False)
    email = serializers.EmailField(max_length=255,
                                   required=True, allow_blank=False,
                                   allow_null=False)
    country = CountryField(allow_null=False, allow_blank=False,
                           required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password',
                  'country',)

    def validate(self, attrs):
        if User.objects.filter(email__iexact=attrs.get(
                'email').lower().strip()).exists():
            raise ValidationError(
                {"message": "User is already exists with this email."}
            )
        attrs['username'] = attrs.get('email').lower().strip()
        return attrs
