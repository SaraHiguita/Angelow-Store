from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Crea los grupos de usuario: Admin, Staff, Cliente con sus permisos'

    def handle(self, *args, **options):
        Group.objects.get_or_create(name='Admin')

        staff_group, _ = Group.objects.get_or_create(name='Staff')
        staff_codenames = [
            'view_category', 'add_category', 'change_category', 'delete_category',
            'view_product', 'add_product', 'change_product', 'delete_product',
            'view_productimage', 'add_productimage', 'change_productimage', 'delete_productimage',
            'view_order', 'add_order', 'change_order', 'delete_order',
            'view_orderitem', 'add_orderitem', 'change_orderitem', 'delete_orderitem',
            'view_cart', 'add_cart', 'change_cart', 'delete_cart',
            'view_cartitem', 'add_cartitem', 'change_cartitem', 'delete_cartitem',
            'view_supplier', 'add_supplier', 'change_supplier', 'delete_supplier',
            'view_stockmovement', 'add_stockmovement', 'change_stockmovement', 'delete_stockmovement',
            'view_inventoryalert', 'add_inventoryalert', 'change_inventoryalert', 'delete_inventoryalert',
            'view_profile', 'add_profile', 'change_profile', 'delete_profile',
            'view_address', 'add_address', 'change_address', 'delete_address',
            'view_user',
        ]
        perms = Permission.objects.filter(codename__in=staff_codenames)
        staff_group.permissions.add(*perms)
        self.stdout.write(self.style.SUCCESS(f'Permisos asignados a Staff: {perms.count()}'))

        Group.objects.get_or_create(name='Cliente')
        self.stdout.write(self.style.SUCCESS('Grupos creados: Admin, Staff, Cliente'))
