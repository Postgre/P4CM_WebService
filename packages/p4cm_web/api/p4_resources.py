from django.conf.urls import url

from api.models import P4Object
from cmd_runner.p4_commands_runner import P4ClientRunner
from common.authentication import P4TicketAuthentication
from common.environment import P4Env
from common.p4commands import P4Client
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.bundle import Bundle
from tastypie.resources import Resource
from tastypie.utils import trailing_slash


__author__ = 'ericqu'


class P4Resource(Resource):
    message = fields.CharField(attribute='message')


class P4ClientResource(P4Resource):
    client = fields.CharField(attribute='client')

    class Meta:
        resource_name = 'client'
        object_class = P4Object
        authentication = P4TicketAuthentication()
        authorization = Authorization()

    def prepend_urls(self):
        return [
            url(
                r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/clone_to_temp%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('clone_to_temp'),
                name="client_clone_to_temp"
            ),
        ]

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        obj = bundle_or_obj

        if isinstance(bundle_or_obj, Bundle):
            obj = bundle_or_obj.obj

        kwargs['pk'] = obj.client

        return kwargs

    def obj_get(self, bundle, **kwargs):
        print(kwargs)
        print bundle.request.GET

        req_args = {'client': kwargs['pk']}
        for k in bundle.request.GET:
            req_args[k] = bundle.request.GET[k]

        runner = P4ClientRunner(P4Env(bundle.request), **req_args)

        result = runner.run()

        data = {
            'message': result.stdout if result.succeeded else result.stderr,
            'client': kwargs['pk'],
        }
        return P4Object(initial=data)

    def get_object_list(self, request):
        req_args = {'list': True}
        for k in request.GET:
            req_args[k] = request.GET[k]

        runner = P4ClientRunner(P4Env(request), **req_args)

        message = runner.run()

        if message.succeeded:
            result = []
            output_messages = message.stdout.splitlines()
            for msg in output_messages:
                result.append(P4Object(initial={'message': msg, 'client': msg.split()[1]}))
            return result
        else:
            raise ValueError(message.stdout)

    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle.request)

    def obj_delete(self, bundle, **kwargs):
        client = kwargs['pk']
        print client
        p4client = P4Client(P4Env(bundle.request))
        p4client.delete_temp_workspace(client)

    def clone_to_temp(self, request):
        req_args = {'clone_to_temp': True}
        for k in request.GET:
            req_args[k] = request.GET[k]
        runner = P4ClientRunner(P4Env(request), **req_args)

        data = runner.run()

        return P4Object(initial=data)




