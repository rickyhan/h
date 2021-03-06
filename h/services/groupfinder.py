# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from zope.interface import implementer

from h import models
from h.interfaces import IGroupService
from h.util.db import lru_cache_in_transaction
from h.groups.util import WorldGroup


# Ideally this would be called the GroupService to match nomenclature in memex.
# FIXME: rename / split existing GroupService and rename this.
@implementer(IGroupService)
class GroupfinderService(object):
    def __init__(self, session, authority):
        self.session = session
        self.authority = authority

        self._cached_find = lru_cache_in_transaction(self.session)(self._find)

    def find(self, id_):
        return self._cached_find(id_)

    def _find(self, id_):
        if id_ == '__world__':
            return WorldGroup(self.authority)

        return (self.session.query(models.Group)
                    .filter_by(pubid=id_)
                    .one_or_none())


def groupfinder_service_factory(context, request):
    return GroupfinderService(request.db, request.authority)
