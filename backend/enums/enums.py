# -*- encoding: utf-8 -*-


import inspect
from enum import Enum


class ChoiceEnum(Enum):

    @classmethod
    def choices(cls):
        # get all members of the class
        members = inspect.getmembers(cls, lambda m: not(inspect.isroutine(m)))
        # filter down to just properties
        props = [m for m in members if not(m[0][:2] == '__')]
        # format into django choice tuple
        choices = tuple([(str(p[1].value), p[0]) for p in props])
        return choices


class UserType(ChoiceEnum):
    CUSTOMER = 'Customer'
    COMPANY = 'Company'
    BRANCH = "Branch"
    FRANCHISE = "Franchise"


class TicketStatus(ChoiceEnum):
    ATTENDED = "Attended"
    PENDING = "Pending"
    CANCEL = "Canceled"


class UserPermissions():
    IS_CUSTOMER = "is_customer"
    IS_COMPANY = "is_company"
    IS_BRANCH = "is_branch"
    IS_FRANCHISE = "is_franchise"
