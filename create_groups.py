from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from myapp.models import Course, Assignment

class Command(BaseCommand):
    help = 'Створення груп Administrator, Manager, Teacher'

    def handle(self, *args, **kwargs):

        admin_group, created = Group.objects.get_or_create(name='Administrator')
        if created:
            admin_group.permissions.set(Permission.objects.all())
            self.stdout.write('Групу "Administrator" створено.')


        manager_group, created = Group.objects.get_or_create(name='Manager')
        if created:
            manager_perms = Permission.objects.filter(content_type__model='course', codename__startswith='add')
            manager_group.permissions.set(manager_perms)
            self.stdout.write('Групу "Manager" створено.')


        teacher_group, created = Group.objects.get_or_create(name='Teacher')
        if created:
            teacher_perms = Permission.objects.filter(content_type__model__in=['course', 'assignment'])
            teacher_group.permissions.set(teacher_perms)
            self.stdout.write('Групу "Teacher" створено.')

        self.stdout.write(self.style.SUCCESS('Усі групи створено успішно.'))