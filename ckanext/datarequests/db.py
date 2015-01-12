# -*- coding: utf-8 -*-

# Copyright (c) 2015 CoNWeT Lab., Universidad Politécnica de Madrid

# This file is part of CKAN Data Requests Extension.

# CKAN Data Requests Extension is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# CKAN Data Requests Extension is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with CKAN Data Requests Extension. If not, see <http://www.gnu.org/licenses/>.

import sqlalchemy as sa
import uuid

from sqlalchemy import func

DataRequest = None


def uuid4():
    return str(uuid.uuid4())


def init_db(model):

    global DataRequest
    if DataRequest is None:

        class _DataRequest(model.DomainObject):

            @classmethod
            def get(cls, **kw):
                '''Finds all the instances required.'''
                query = model.Session.query(cls).autoflush(False)
                return query.filter_by(**kw).all()

            @classmethod
            def datarequest_exists(cls, title):
                '''Returns true if there is a Data Request with the same title (case insensitive)'''
                query = model.Session.query(cls).autoflush(False)
                return query.filter(func.lower(cls.title) == func.lower(title)).first() is not None

        DataRequest = _DataRequest

        # FIXME: Maybe a default value should not be included...
        datarequests_table = sa.Table('datarequests', model.meta.metadata,
            sa.Column('user_id', sa.types.UnicodeText, primary_key=False, default=u''),
            sa.Column('id', sa.types.UnicodeText, primary_key=True, default=uuid4),
            sa.Column('title', sa.types.UnicodeText, primary_key=True, default=u''),
            sa.Column('description', sa.types.UnicodeText, primary_key=False, default=u''),
            sa.Column('organization', sa.types.UnicodeText, primary_key=False, default=u''),
            sa.Column('open_time', sa.types.DateTime, primary_key=False, default=None),
            sa.Column('accepted_dataset', sa.types.UnicodeText, primary_key=False, default=u''),
            sa.Column('close_time', sa.types.DateTime, primary_key=False, default=None),
            sa.Column('closed', sa.types.Boolean, primary_key=False, default=False)
        )

        # Create the table only if it does not exist
        datarequests_table.create(checkfirst=True)

        model.meta.mapper(DataRequest, datarequests_table,)