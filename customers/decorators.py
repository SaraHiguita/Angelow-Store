from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied


def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name='Admin').exists())


def is_staff(user):
    return user.is_authenticated and (
        user.is_superuser or
        user.groups.filter(name='Staff').exists() or
        user.groups.filter(name='Admin').exists()
    )


def is_cliente(user):
    return user.is_authenticated and user.groups.filter(name='Cliente').exists()


def admin_required(view_func=None, login_url=None, raise_exception=False):
    actual_decorator = user_passes_test(
        is_admin,
        login_url=login_url,
        redirect_field_name=None,
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


def staff_required(view_func=None, login_url=None, raise_exception=False):
    actual_decorator = user_passes_test(
        is_staff,
        login_url=login_url,
        redirect_field_name=None,
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


class AdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not is_admin(request.user):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class StaffRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not is_staff(request.user):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
