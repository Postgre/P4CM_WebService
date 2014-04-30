from api.models import P4Object
from cmd_runner.p4cm_commands_runner import P4CMInfoRunner, P4CMConfigRunner
from common.authentication import P4TicketAuthentication
from common.environment import P4Env
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.bundle import Bundle
from tastypie.resources import Resource

__author__ = 'ericqu'


class P4CMResource(Resource):
    message = fields.CharField(attribute='message', blank=True, null=True)
    error = fields.CharField(attribute='error', blank=True, null=True)
    succeeded = fields.BooleanField(attribute='succeeded', blank=True, null=True)
    p4codeline = fields.FileField(attribute='p4codeline', blank=True, null=True)

    def deserialize(self, request, data, format=None):
        if not format:
            format = request.META.get('CONTENT_TYPE', 'application/json')

        if format == 'application/x-www-form-urlencoded':
            return request.POST

        if format.startswith('multipart'):
            data = request.POST.copy()
            data.update(request.FILES)
            return data
        return super(P4CMResource, self).deserialize(request, data, format)

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

    def obj_create(self, bundle, **kwargs):
        print bundle.data


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
        authorization = Authorization()
        runner_class = P4CMConfigRunner

    def obj_update(self, bundle, **kwargs):
        bundle.obj = P4Object(initial=kwargs)
        bundle = self.full_hydrate(bundle)

        return bundle

