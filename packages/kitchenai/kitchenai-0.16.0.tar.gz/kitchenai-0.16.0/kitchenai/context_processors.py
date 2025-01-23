from django.conf import settings
from kitchenai import __version__ as VERSION
def theme_context(request):
    return {
        'KITCHENAI_THEME': getattr(settings, 'KITCHENAI_THEME', 'cupcake')
    } 

def version_context(request):
    return {
        'VERSION': VERSION
    }

def local_context(request):
    return {
        'KITCHENAI_LOCAL': getattr(settings, 'KITCHENAI_LOCAL')
    }

def license_context(request):
    return {
        'KITCHENAI_LICENSE': getattr(settings, 'KITCHENAI_LICENSE')
    }

def allow_registration_context(request):
    return {
        'ACCOUNT_ALLOW_REGISTRATION': getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)
    }
