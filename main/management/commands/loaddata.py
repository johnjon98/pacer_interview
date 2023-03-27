from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from main.models import User

#Admin Group Permission
GROUPS1 = ['Admin']
MODELS1      = ['ScoreAPILog']
PERMISSIONS1 = ['view', 'add', 'delete', 'change']


class Command(BaseCommand):
    help = 'Load initial admin user data into DB'
    def create_group_and_permission(self, groups, models, permissions):
        for group in groups:
            print(group)
            new_group, _ = Group.objects.get_or_create(name=group)
            for model in models:
                for permission in permissions:
                    codename = '{}_{}'.format(permission, slugify(model))
                    print('\tCreating {}'.format(codename))

                    try:
                        model_add_perm = Permission.objects.get(codename=codename)
                    except Permission.DoesNotExist:
                        print("\tPermission not found with codename '{}'".format(codename))
                    else:
                        new_group.permissions.add(model_add_perm)
            print('Assigned permissions to {}'.format(group))
    
    def create_superuser(self, email, password, name, phone):
        try:
            User.objects.get(email=email)
        except Exception:
            User.objects.create_superuser(email=email, password=password, name=name, phone=phone)
            print("Superuser Created. Email: '{}'. Password: '{}'".format(email, password))
        else:
            print("Superuser '{}' Exists, Not Creating".format(email))


    def create_admin(self, email, password, name, phone):
        try:
            User.objects.get(email=email)
        except Exception:
            User.objects.create_admin(email=email, password=password, name=name, phone=phone)
            print("Admin Created. Email: '{}'. Password: '{}'".format(email, password))
        else:
            print("Admin     '{}' Exists, Not Creating".format(email))

   
    def handle(self, *args, **options):
        self.create_group_and_permission(['Superuser'], [], [])
        self.create_group_and_permission(GROUPS1, MODELS1, PERMISSIONS1)
        self.create_superuser(email='1234@superuser.com', password='abcd1234', name='Superuser', phone='0123456789')
        self.create_admin(email='1234@admin.com', password='abcd1234', name='Admin', phone='0123456789')
        