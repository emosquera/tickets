# -*- encoding: utf-8 -*-


from django.db import models
from django.contrib.auth.models import User
from enums.enums import UserType, TicketStatus, UserPermissions
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.


class State(models.Model):
    name = models.CharField(max_length=100)


class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, related_name='cities')


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='userProfile')
    type = models.CharField(max_length=20, choices=UserType.choices())


class Customer(UserProfile):
    name = models.TextField(max_length=100, blank=True)
    lastName = models.TextField(max_length=100, blank=True)
    address = models.TextField(max_length=1000, null=True, blank=True)
    identityDoc = models.IntegerField(unique=True, null=False)
    homePhone = models.TextField(max_length=20, null=True, blank=True)
    cellPhone = models.TextField(max_length=20, null=True, blank=True)
    email = models.EmailField()
    city = models.ForeignKey(City, related_name='customer')

    class Meta:
        permissions = ((UserPermissions.IS_CUSTOMER, "Es un cliente"),)


class Company(UserProfile):
    name = models.TextField(max_length=100, blank=True)
    identityDoc = models.CharField(max_length=12, unique=True, null=False)
    address = models.TextField(max_length=1000, blank=True)
    phone = models.TextField(max_length=20, blank=True)
    city = models.ForeignKey(City)

    class Meta:
        permissions = ((UserPermissions.IS_COMPANY, "Es una empresa"),)


class Branch(UserProfile):
    nickName = models.CharField(max_length=300)
    address = models.TextField(max_length=1000, blank=True)
    phone = models.TextField(max_length=20, blank=True)
    city = models.ForeignKey(City)
    branchCompany = models.ForeignKey(Company)

    class Meta:
        permissions = ((UserPermissions.IS_BRANCH, "Es una sucursal"),)


class Brand(models.Model):
    name = models.TextField(max_length=100, blank=True)


class Franchise(Company):
    brand = models.ForeignKey(Brand)

    class Meta:
        permissions = ((UserPermissions.IS_FRANCHISE, "Es una franquicia"),)


class Ticket(models.Model):
    date = models.DateField(blank=True, null=True)
    number = models.IntegerField(null=True, default=None)
    serie = models.CharField(max_length=90)
    limit = models.Q(app_label='backend', model='costumer') | models.Q(app_label='backend', model='company') | \
            models.Q(app_label='backend', model='branch') | models.Q(app_label='backend', model='franchise')
    content_type = models.ForeignKey(
        ContentType,
        verbose_name='content type',
        limit_choices_to=limit,
        null=True,
        blank=True,
    )
    object_id = models.PositiveIntegerField(
        verbose_name='related object',
        null=True,
    )
    content_object = GenericForeignKey('content_type', 'object_id')
    status = models.CharField(max_length=20, choices=TicketStatus.choices())
