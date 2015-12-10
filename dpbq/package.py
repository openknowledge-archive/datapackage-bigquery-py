# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import os
import six
import json
import jtsbq
from datapackage import DataPackage

from . import path as path_module
from .dataset import Dataset


# Module API

class Package(object):

    # Public

    def __init__(self, service, project_id, dataset_id, descriptor=None):

        # Set attributes
        self.__service = service
        self.__project_id = project_id
        self.__dataset_id = dataset_id
        self.__descriptor = descriptor

        # Create dataset
        self.__dataset = Dataset(
                service=service,
                project_id=project_id,
                dataset_id=dataset_id)

        # TODO: ensure created

    def __repr__(self):

        # Template
        template = 'Package <dataset: {dataset}>'

        # Format
        text = template.format(dataset=self.__dataset)

        return text

    @property
    def dataset(self):
        return self.__dataset

    def get_resources(self, plain=False):
        """Return dataset resources.
        """

        # Collect resources
        resources = []
        for table in self.__dataset.get_tables(plain=True):
            resource = table
            if not plain:
                resource = jtsbq.Resource(
                        service=self.__service,
                        project_id=self.__project_id,
                        dataset_id=self.__dataset_id,
                        table_id=table)
            resources.append(resource)

        return resources

    def export(self, path):
        """Export package to descriptor path.
        """

        # Iterate over resources
        resources = []
        for resource in self.get_resources():

            # Add resource schema
            resources.append({'schema': resource.schema})

            # Export resource data
            rpath = resource.table.table_id
            rpath = path_module.dataset2package(rpath)
            rpath = os.path.join(os.path.dirname(path), rpath)
            resource.export_data(rpath)

        # Write descriptor
        descriptor = {'resources': resources}
        with io.open(path,
                     mode=self.__write_mode,
                     encoding=self.__write_encoding) as file:
            json.dump(descriptor, file, indent=4)

    # Private

    def __create(self):

        # Get model
        model = DataPackage(self.__descriptor)

        # Iterate over resources
        for resource in model.resources:

            # Prepare metadata
            path = resource.local_data_path
            schema = resource.metadata['schema']
            table_id = path_module.resource2dataset(resource.metadata['path'])

            # Create remote resource
            resource = jtsbq.Resource(
                   service=self.__service,
                   project_id=self.__project_id,
                   dataset_id=self.__dataset_id,
                   table_id=table_id,
                   schema=schema)

            # Import data
            resource.import_data(path)

    @property
    def __write_mode(self):
        if six.PY2:
            return 'wb'
        return 'w'

    @property
    def __write_encoding(self):
        if six.PY2:
            return None
        return 'utf-8'
