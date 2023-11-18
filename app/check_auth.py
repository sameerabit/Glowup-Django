from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test


def permission_required(perm):
    def check_perms(user):
        if isinstance(perm, str):
            perms = (perm,)
        else:
            perms = perm
        if user.has_perms(perms):
            return True
        if user.is_authenticated:
            raise PermissionDenied
        return False
    return user_passes_test(check_perms, login_url='login')


def authentication_required():
    return user_passes_test(lambda user: user.is_authenticated, login_url='login')


def allow_anonymous():
    return user_passes_test(lambda user: True)
