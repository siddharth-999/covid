import os
from datetime import datetime

import plotly.graph_objects as go
from celery import shared_task
from django.conf import settings
from django.contrib.auth.models import BaseUserManager
from django.core.mail import EmailMessage
from rest_framework.exceptions import ValidationError


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.username = email
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


def date_validation(start_date, end_date):
    try:
        valid_start_date = datetime.strptime(
            start_date, '%Y-%m-%d').date()
    except ValueError as e:
        print("exception", e)
        raise ValidationError(
            {"message": "Please enter valid from date."}
        )
    try:
        valid_end_date = datetime.strptime(
            end_date, '%Y-%m-%d').date()
    except ValueError as e:
        print("exception", e)
        raise ValidationError(
            {"message": "Please enter valid to date."})
    if valid_end_date > valid_start_date:
        day_difference = (valid_end_date - valid_start_date).days
        return day_difference
    else:
        raise ValidationError(
            {"message": "Please enter valid date range."})


@shared_task
def send_report(data, email):
    x_frame = []
    death_list = []
    confirmed_list = []
    recovered_list = []
    new_confirmed_list = []
    new_recovered_list = []
    new_death_list = []
    active_list = []
    for single_date in data:
        x_frame.append(single_date['date'])
        death_list.append(single_date['deaths'])
        confirmed_list.append(single_date['confirmed'])
        recovered_list.append(single_date['recovered'])
        new_confirmed_list.append(single_date['new_confirmed'])
        new_recovered_list.append(single_date['new_recovered'])
        new_death_list.append(single_date['new_deaths'])
        active_list.append(single_date['active'])
    fig = go.Figure()
    fig.add_trace(go.Bar(x=x_frame, y=death_list, name='Death'))
    fig.add_trace(go.Bar(x=x_frame, y=confirmed_list, name='Confirmed'))
    fig.add_trace(go.Bar(x=x_frame, y=recovered_list, name='recovered'))
    fig.add_trace(go.Bar(x=x_frame, y=new_confirmed_list, name='New Confirmed'))
    fig.add_trace(go.Bar(x=x_frame, y=new_recovered_list, name='New Recovered'))
    fig.add_trace(go.Bar(x=x_frame, y=new_death_list, name='New Deaths'))
    fig.add_trace(go.Bar(x=x_frame, y=active_list, name='Active'))
    fig.update_layout(barmode='group', xaxis_tickangle=-45)
    if not os.path.exists("media"):
        os.mkdir("media")
    file_name = datetime.now()
    fig.write_image("media/{}.png".format(file_name))
    subject = "Covid Report Has Arrived!"
    message = "Please Find Report Below"
    msg = EmailMessage(subject=subject, body=message, to=(email,),
                       from_email=settings.DEFAULT_FROM_EMAIL)
    with open("media/{}.png".format(file_name), 'rb') as file:
        msg.attach('{}.png'.format(file_name),
                   file.read())
    msg.content_subtype = 'html'
    msg.send()
