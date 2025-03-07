from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from myapp.models import Course, Assignment

@receiver(post_migrate)
def create_groups(sender, **kwargs):
    admin_group, created = Group.objects.get_or_create(name='Administrator')
    if created:
        admin_group.permissions.set(Permission.objects.all())

    manager_group, created = Group.objects.get_or_create(name='Manager')
    if created:
        manager_perms = Permission.objects.filter(content_type__model='course', codename__startswith='add')
        manager_group.permissions.set(manager_perms)

    teacher_group, created = Group.objects.get_or_create(name='Teacher')
    if created:
        teacher_perms = Permission.objects.filter(content_type__model__in=['course', 'assignment'])
        teacher_group.permissions.set(teacher_perms)

    print("Групи успішно створено.")