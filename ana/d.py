import logging
l = logging.getLogger('ana.d')

class D(object):
    def __new__(cls, uuid, child_cls, state):
        l.debug("Deserializing Storable with uuid %s", uuid)

        if uuid is None and state is None:
            raise ANAError("D received a None uuid and a None state")

        if uuid is not None and uuid in get_dl().uuid_cache:
            l.debug("... returning cached")
            return get_dl().uuid_cache[uuid]

        if uuid is not None and state is None:
            l.debug("... loading state")
            state = get_dl().load_state(uuid)

        self = super(Storable, child_cls).__new__(child_cls) #pylint:disable=bad-super-call
        self._ana_setstate(state)
        self._ana_uuid = uuid

        if uuid is not None:
            # cache and return
            get_dl().uuid_cache[uuid] = self
            self._stored = True
            l.debug("... returning newly cached")
        else:
            self._stored = False
            l.debug("... returning non-UUID storable")

        if not hasattr(self, '_ana_uuid'):
            raise ANAError("Storable somehow got through without an _ana_uuid attr")
        return self

from .storable import Storable
from .errors import ANAError
from . import get_dl
