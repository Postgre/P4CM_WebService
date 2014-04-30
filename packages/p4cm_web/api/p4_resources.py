import os
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
    message = fields.CharField(attribute='message', blank=True, null=True)


class P4ClientResource(P4Resource):
    client = fields.CharField(attribute='client', blank=True, null=True)
    workspace = fields.CharField(attribute='workspace', blank=True, null=True)

    class Meta:
        resource_name = 'clients'
        object_class = P4Object
        authentication = P4TicketAuthentication()
        authorization = Authorization()
        always_return_data = True

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}

        obj = bundle_or_obj

        if isinstance(bundle_or_obj, Bundle):
            obj = bundle_or_obj.obj

        kwargs['pk'] = obj.client

        return kwargs

    def obj_get(self, bundle, **kwargs):
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
        p4client = P4Client(P4Env(bundle.request))
        p4client.delete_temp_workspace(client)

    def obj_create(self, bundle, **kwargs):

        p4client = P4Client(P4Env(bundle.request))
        if 'client' in bundle.data:
            workspace = p4client.create_temp_workspace(bundle.data['client'])
        else:
            workspace = p4client.create_temp_workspace()

        data = {
            'client': os.path.basename(workspace),
            'workspace': workspace,
        }

        bundle.obj = P4Object(initial=data)

        return bundle





