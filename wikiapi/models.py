# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
import requests
import collections
import json

# TODO :
# support .exclude filters
# support slicing
# if queries return > 50 elements, fetch the rest
# cache http requests
# support > < <= >= filters

QUERY_URL = "http://wiki.urlab.be/api.php?action=ask&query="


class WikiManager(models.Manager):

    def get_query_set(self):
        return WikiQuerySet(self.model)

    def __getattr__(self, name):
        return getattr(self.get_query_set(), name)


class WikiQuerySet(object):

    def __init__(self, model=None, query="", using=None):
        self.model = model
        self._result = None
        self._order = None

    def all(self):
        q = WikiQuerySet(self.model)
        q._order = self._order
        return q

    def _request_crafter(self):
        if self._order:
            sort, order = [], []
            for conventional, col in self._order:
                sign = "ASC" if conventional else "DESC"
                order.append(sign)
                sort.append(col)
            sort_str = "|sort={sort}|order={order}".format(sort=','.join(sort), order=','.join(order))
        else:
            sort_str = ""

        columns = filter(lambda x: not x is None, map(lambda x: x.db_column, self.model._meta.fields))

        columns_str = ''.join(map(lambda x: "|?"+x, columns))

        return "{domain}[[Category:{model}]]{sort}{columns}&format=json".format(
            domain=QUERY_URL,
            sort=sort_str,
            model=self.model._meta.object_name,
            columns=columns_str
        )

    def _deserialize(self, text):
        return json.loads(text, object_pairs_hook=collections.OrderedDict, encoding='unicode_escape')

    @property
    def result(self):
        if not self._result:
            url = self._request_crafter()
            response = self._deserialize(requests.get(url).text)['query']['results']

            self._result = []
            for key, item in response.iteritems():
                new_item = {}
                new_item['key'] = ':'.join(key.split(':')[1:])
                new_item['url'] = item['fullurl']
                for colum, value in item['printouts'].iteritems():
                    new_item[colum] = value
                self._result.append(new_item)

        return self._result

    @property
    def ordered(self):
        return not self._order is None

    def reverse(self):
        # TODO : Check if query if done
        if self._order is None :
            raise Exception('Cannot reverse non-ordered query.')
        clone = self.all()
        clone._order = map(lambda (order, key): (not order,key), self._order)

        return clone
        
    def order_by(self, *fields):
        if self._result != None :
            raise Exception('Cannot order a query once it has been executed.')
        clone = self.all()
        if self._order is None:
            clone._order = []
        fields = map(lambda x: (x[0] != "-", x[1:] if x[0] == "-" else x),
            fields)
        clone._order += fields

        return clone

    def count(self):
        c = len(self.result)
        if c >= 50:
            return -1
        return len(self.result)

    def get(self, *args, **kwargs):
        clone = self.filter(*args, **kwargs)
        num = len(clone)
        if num == 1:
            return clone._create_model(clone.result[0])
        if not num:
            raise self.model.DoesNotExist(
                "%s matching query does not exist." %
                self.model._meta.object_name)
        raise self.model.MultipleObjectsReturned(
            "get() returned more than one %s -- it returned %s!" %
            (self.model._meta.object_name, num))
    
    def iterator(self):
        for item in self.result:
            yield self._create_model(item)

    __iter__ = iterator 

    def _create_model(self, line):
        fields = filter(lambda x: not x.db_column is None, self.model._meta.fields)
        cols = {}
        for field in fields:
            cols[field.name] = line[field.db_column.capitalize()]
        return self.model(name=line['key'], url=line['url'], **cols)

    def filter(self, *args, **kwargs):
        if self._result != None :
            raise Exception('Cannot filter a query once it has been executed.')

        clone = self.all()
        for key in kwargs:
            val = kwargs[key]
            if not key == 'Category':
                key += ":"
            clone.query += "[[{}:{}]]".format(key, val)
        return clone

class WikiModel(models.Model):
    objects = WikiManager()

    class Meta:
        abstract = True
