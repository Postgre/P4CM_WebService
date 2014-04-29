import copy
from django.conf import settings

__author__ = 'ericqu'


class P4Env(object):
    @staticmethod
    def extract_credentials(request):
        if request.META.get('HTTP_AUTHORIZATION') and request.META['HTTP_AUTHORIZATION'].lower().startswith(
                'p4ticket '):
            (auth_type, data) = request.META['HTTP_AUTHORIZATION'].split()

            if auth_type.lower() != 'p4ticket':
                raise ValueError("Incorrect authorization header.")

            username, p4ticket = data.split(':', 1)
        else:
            username = request.GET.get('username') or request.POST.get('username')
            p4ticket = request.GET.get('p4ticket') or request.POST.get('p4ticket')

        return username, p4ticket

    def __init__(self, request):
        username, password = P4Env.extract_credentials(request)
        env = copy.deepcopy(settings.P4_ENV['default'])

        if username:
            env['P4USER'] = username
        if password:
            env['P4PASSWD'] = password

        client = request.GET.get('client') or request.POST.get('client')
        if client:
            env['P4CLIENT'] = client

        env['WORKSPACE'] = request.META.get('HTTP_WORKSPACE')

        self.env = env

    @property
    def user(self):
        return self.env['P4USER']

    @property
    def password(self):
        return self.env['P4PASSWD']

    @property
    def port(self):
        return self.env['P4PORT']

    @property
    def charset(self):
        return self.env['P4CHARSET']

    @property
    def client(self):
        return self.env['P4CLIENT']

    @property
    def p4config(self):
        return self.env['P4CONFIG']

    @property
    def workspace(self):
        return self.env['WORKSPACE']

    def dict(self):
        env_copy = copy.deepcopy(self.env)
        # NOT TO USE P4CLIENT FOR environment variable
        env_copy.pop('P4CLIENT')
        env_copy.pop('WORKSPACE')
        return env_copy
