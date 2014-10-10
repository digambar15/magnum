
import ast
import base64
import copy
import datetime
import functools
import inspect
import json
#import pytz
import uuid
import pecan
import wsme
from oslo.config import cfg
from oslo.utils import netutils
from oslo.utils import strutils
from oslo.utils import timeutils
from wsme import types as wtypes
import wsmeext.pecan as wsme_pecan
from pecan import rest, response
import six


state_kind = ["ok", "containers", "insufficient data"]
state_kind_enum = wtypes.Enum(str, *state_kind)
operation_kind = ('lt', 'le', 'eq', 'ne', 'ge', 'gt')
operation_kind_enum = wtypes.Enum(str, *operation_kind)


class _Base(wtypes.Base):

    @classmethod
    def from_db_model(cls, m):
        return cls(**(m.as_dict()))

    @classmethod
    def from_db_and_links(cls, m, links):
        return cls(links=links, **(m.as_dict()))

    def as_dict(self, db_model):
        valid_keys = inspect.getargspec(db_model.__init__)[0]
        if 'self' in valid_keys:
            valid_keys.remove('self')
        return self.as_dict_from_keys(valid_keys)

    def as_dict_from_keys(self, keys):
        return dict((k, getattr(self, k))
                    for k in keys
                    if hasattr(self, k) and
                    getattr(self, k) != wsme.Unset)


class Query(_Base):

    """Query filter."""

    # The data types supported by the query.
    _supported_types = ['integer', 'float', 'string', 'boolean']

    # Functions to convert the data field to the correct type.
    _type_converters = {'integer': int,
                        'float': float,
                        'boolean': functools.partial(
                            strutils.bool_from_string, strict=True),
                        'string': six.text_type,
                        'datetime': timeutils.parse_isotime}

    _op = None  # provide a default

    def get_op(self):
        return self._op or 'eq'

    def set_op(self, value):
        self._op = value

    field = wtypes.text
    "The name of the field to test"

    # op = wsme.wsattr(operation_kind, default='eq')
    # this ^ doesn't seem to work.
    op = wsme.wsproperty(operation_kind_enum, get_op, set_op)
    "The comparison operator. Defaults to 'eq'."

    value = wtypes.text
    "The value to compare against the stored data"

    type = wtypes.text
    "The data type of value to compare against the stored data"

    def __repr__(self):
        # for logging calls
        return '<Query %r %s %r %s>' % (self.field,
                                        self.op,
                                        self.value,
                                        self.type)

    @classmethod
    def sample(cls):
        return cls(field='resource_id',
                   op='eq',
                   value='bd9431c1-8d69-4ad3-803a-8d4a6b89fd36',
                   type='string'
                   )

    def as_dict(self):
        return self.as_dict_from_keys(['field', 'op', 'type', 'value'])

    def _get_value_as_type(self, forced_type=None):
        """Convert metadata value to the specified data type.
        """
        type = forced_type or self.type
        try:
            converted_value = self.value
            if not type:
                try:
                    converted_value = ast.literal_eval(self.value)
                except (ValueError, SyntaxError):
                    # Unable to convert the metadata value automatically
                    # let it default to self.value
                    pass
            else:
                if type not in self._supported_types:
                    # Types must be explicitly declared so the
                    # correct type converter may be used. Subclasses
                    # of Query may define _supported_types and
                    # _type_converters to define their own types.
                    raise TypeError()
                converted_value = self._type_converters[type](self.value)
        except ValueError:
            msg = (_('Unable to convert the value %(value)s'
                     ' to the expected data type %(type)s.') %
                   {'value': self.value, 'type': type})
            raise ClientSideError(msg)
        except TypeError:
            msg = (_('The data type %(type)s is not supported. The supported'
                     ' data type list is: %(supported)s') %
                   {'type': type, 'supported': self._supported_types})
            raise ClientSideError(msg)
        except Exception:
            msg = (_('Unexpected exception converting %(value)s to'
                     ' the expected data type %(type)s.') %
                   {'value': self.value, 'type': type})
            raise ClientSideError(msg)
        return converted_value


class Container(_Base):
    container_id = wtypes.text
    """ The ID of the containers."""

    name = wsme.wsattr(wtypes.text, mandatory=True)
    """ The name of the container."""

    desc = wsme.wsattr(wtypes.text, mandatory=True)

    def __init__(self, **kwargs):
        super(Container, self).__init__(**kwargs)

    @classmethod
    def sample(cls):
        return cls(id=str(uuid.uuid1(),
                          name="Docker",
                          desc='Docker Containers'))


class ContainerController(rest.RestController):

    @wsme_pecan.wsexpose([Container], [Query], int)
    def get_all(self, q=None, limit=None):
        # TODO: Returns all the containers
        response.status = 200
        return

    @wsme_pecan.wsexpose(Container, wtypes.text)
    def get_one(self, container_id):
        # TODO: Returns all the containers
        response.status = 200
        return

    @wsme_pecan.wsexpose([Container], body=[Container])
    def post(self, data):
        # TODO: Create a new container
        response.status = 201
        return

    @wsme_pecan.wsexpose(None, status_code=204)
    def delete(self):
        # TODO: DELETE the containers
        response.status = 204
        return
