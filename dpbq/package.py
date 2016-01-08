# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import os
import re
import csv
import six
import json
from copy import deepcopy
from jsontableschema.model import SchemaModel
from datapackage import DataPackage


# Module API

def import_package(storage, descriptor):
    """Import Data Package to storage.

    Parameters
    ----------
    storage: object
        Storage object.
    descriptor: str
        Path to descriptor.

    """

    # Init maps
    tables = []
    schemas = []
    datamap = {}
    mapping = {}

    # Init model
    model = DataPackage(descriptor)

    # Collect tables/schemas/data
    for resource in model.resources:
        name = resource.metadata.get('name', None)
        table = _convert_path(resource.metadata['path'], name)
        schema = resource.metadata['schema']
        data = resource.iter()
        tables.append(table)
        schemas.append(schema)
        datamap[table] = data
        if name is not None:
            mapping[name] = table
    schemas = _convert_schemas(mapping, schemas)

    # Create tables
    for table in tables:
        if storage.check(table):
            storage.delete(table)
    storage.create(tables, schemas)

    # Write data to tables
    for table in storage.tables:
        storage.write(table, datamap[table])


def export_package(storage, descriptor):
    """Export Data Package from storage.

    Parameters
    ----------
    storage: object
        Storage object.
    descriptor: str
        Path where to store descriptor.

    """

    # Iterate over tables
    resources = []
    mapping = {}
    for table in storage.tables:

        # Prepare
        schema = storage.describe(table)
        base = os.path.dirname(descriptor)
        path, name = _restore_path(table)
        fullpath = os.path.join(base, path)
        if name is not None:
            mapping[table] = name

        # Write data
        _ensure_dir(fullpath)
        with io.open(fullpath,
                     mode=_write_mode,
                     newline=_write_newline,
                     encoding=_write_encoding) as file:
            model = SchemaModel(deepcopy(schema))
            data = storage.read(table)
            writer = csv.writer(file)
            writer.writerow(model.headers)
            for row in data:
                writer.writerow(row)

        # Add resource
        resource = {'schema': schema, 'path': path}
        if name is not None:
            resource['name'] = name
        resources.append(resource)

    # Write descriptor
    resources = _restore_resources(mapping, resources)
    _ensure_dir(descriptor)
    with io.open(descriptor,
                 mode=_write_mode,
                 encoding=_write_encoding) as file:
        descriptor = {'resources': resources}
        json.dump(descriptor, file, indent=4)


# Internal

_write_mode = 'w'
if six.PY2:
    _write_mode = 'wb'

_write_encoding = 'utf-8'
if six.PY2:
    _write_encoding = None

_write_newline = ''
if six.PY2:
    _write_newline = None


def _convert_path(path, name):
    table = os.path.splitext(path)[0]
    table = table.replace(os.path.sep, '__')
    table = re.sub('[^0-9a-zA-Z_]+', '_', table)
    if name is not None:
        table = '___'.join([table, name])
    return table


def _restore_path(table):
    name = None
    splited = table.split('___')
    path = splited[0]
    if len(splited) == 2:
        name = splited[1]
    path = path.replace('__', os.path.sep)
    path += '.csv'
    return path, name


def _convert_schemas(mapping, schemas):
    for schema in schemas:
        for fk in schema.get('foreignKeys', []):
            resource = fk['reference']['resource']
            if resource != 'self':
                if resource not in mapping:
                    message = (
                        'Resource "%s" for foreign key "%s" '
                        'doesn\'t exist.' % (resource, fk))
                    raise ValueError(message)
                fk['reference']['resource'] = '<table>'
                fk['reference']['table'] = mapping[resource]
    return schemas


def _restore_resources(mapping, resources):
    for resource in resources:
        schema = resource['schema']
        for fk in schema.get('foreignKeys', []):
            fkresource = fk['reference']['resource']
            if fkresource == '<table>':
                table = fk['reference']['table']
                _, name = _restore_path(table)
                del fk['reference']['table']
                fk['reference']['resource'] = name
    return resources


def _ensure_dir(path):
    dirpath = os.path.dirname(path)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
