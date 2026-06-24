from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    if sender.name != 'customers':
        return

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
        'view_user', 'view_coupon', 'add_coupon', 'change_coupon', 'delete_coupon',
        'view_return', 'add_return', 'change_return', 'delete_return',
    ]
    perms = Permission.objects.filter(codename__in=staff_codenames)
    staff_group.permissions.add(*perms)

    Group.objects.get_or_create(name='Cliente')