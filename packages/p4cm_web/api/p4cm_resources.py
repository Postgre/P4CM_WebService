from api.models import P4Object
from cmd_runner.p4cm_commands_runner import P4CMInfoRunner, P4CMConfigRunner
from common.authentication import P4TicketAuthentication
from common.environment import P4Env
from tastypie import fields
from tastypie.bundle import Bundle
from tastypie.resources import Resource

__author__ = 'ericqu'


class P4CMResource(Resource):
    message = fields.CharField(attribute='message')
    error = fields.CharField(attribute='error')
    succeeded = fields.BooleanField(attribute='succeeded')
    input_file = fields.FileField(attribute='input')
    output_file = fields.FileField(attribute='output')

    def get_object_list(self, request):
        pass

    def obj_get_list(self, bundle, **kwargs):
        objList = [self.obj_get(bundle, **kwargs)]

        return objList

    def obj_get(self, bundle, **kwargs):
        req_args = {}
        for k in bundle.request.GET:
            req_args[k] = bundle.request.GET[k]

        runner = self._meta.runner_class(P4Env(bundle.request), **req_args)

        return P4Object(initial=runner.run())


class P4CMInfo(P4CMResource):
    class Meta:
        resource_name = 'info'
        object_class = P4Object
        authentication = P4TicketAuthentication()
        runner_class = P4CMInfoRunner


class P4CMConfig(P4CMResource):
    class Meta:
        resource_name = 'config'
        object_class = P4Object
        authentication = P4TicketAuthentication()
        runner_class = P4CMConfigRunner
