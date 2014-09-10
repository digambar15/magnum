from pecan import expose, redirect
from api.controllers import v2


class RootController(object):
    v2 = v2.ContainerController()
