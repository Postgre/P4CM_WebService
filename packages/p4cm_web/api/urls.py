from api.p4_resources import P4ClientResource
from api.p4cm_resources import P4CMInfo, P4CMConfig

_author__ = 'ericqu'

from tastypie.api import Api
from django.conf.urls import patterns, include, url

p4_api = Api(api_name='p4')
p4_api.register(P4ClientResource())


p4cm_api = Api(api_name='p4cm')
p4cm_api.register(P4CMInfo())
p4cm_api.register(P4CMConfig())

urlpatterns = patterns(
    '',
    url('', include(p4cm_api.urls)),
    url('', include(p4_api.urls)),
)
