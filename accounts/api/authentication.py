from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import exceptions
from rest_framework.authentication import (
    TokenAuthentication as BaseTokenAuthentication,
    get_authorization_header
)

from core.utils import get_logger, get_debug_str

User, logger = get_user_model(), get_logger()


class TokenAuthentication(BaseTokenAuthentication):
    """
    Base token authentication class. Extended from DRF TokenAuthentication,
    just to pass `request` object to authenticate_credentials method for logging purpose.
    """
    keyword = 'Bearer'

    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            logger.error(get_debug_str(request, None, msg))
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            logger.error(get_debug_str(request, None, msg))
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            logger.exception(get_debug_str(request, None, msg))
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token, request)

    def authenticate_credentials(self, key, request=None):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            msg = _('Invalid token.')
            logger.exception(get_debug_str(request, None, f'{msg} <token: {key}>'))
            raise exceptions.AuthenticationFailed(msg)

        user = token.user
        if not user.is_active:
            msg = _('User inactive or deleted.')
            logger.error(get_debug_str(request, None, f'{msg} <user: {user} ({user.id})>'))
            raise exceptions.AuthenticationFailed(msg)

        return token.user, token
