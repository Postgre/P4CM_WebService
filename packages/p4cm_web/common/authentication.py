from common.environment import P4Env
from common.p4commands import P4Login
from tastypie.authentication import Authentication
from tastypie.http import HttpUnauthorized

__author__ = 'ericqu'


class P4TicketAuthentication(Authentication):
    def _unauthorized(self):
        return HttpUnauthorized()

    def is_authenticated(self, request, **kwargs):
        """
        Finds the user and checks their API key.

        Should return either ``True`` if allowed, ``False`` if not or an
        ``HttpResponse`` if you need something custom.
        """

        try:
            p4env = P4Env(request)
        except ValueError:
            return self._unauthorized()

        if not p4env.user or not p4env.password:
            return self._unauthorized()

        p4login = P4Login(p4env)

        status = p4login.login_status()

        if status:
            request.p4env = p4env

        request._read_started = False

        return status

    def get_identifier(self, request):
        """
        Provides a unique string identifier for the requestor.

        This implementation returns the user's username.
        """
        username, api_key = P4Env.extract_credentials(request)
        return username or 'nouser'
