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
    """Data Package as BigQuery dataset represesntation.

    Parameters
    ----------
    service: object
        Authentificated BigQuery service.
    project_id: str
        BigQuery project identifier.
    dataset_id: str
        BigQuery dataset identifier.

    """

    # Public

    def __init__(self, service, project_id, dataset_id):

        # Set attributes
        self.__service = service
        self.__project_id = project_id
        self.__dataset_id = dataset_id

        # Create dataset
        self.__dataset = Dataset(
                service=service,
                project_id=project_id,
                dataset_id=dataset_id)

    def __repr__(self):

        # Template
        template = 'Package <dataset: {dataset}>'

        # Format
        text = template.format(dataset=self.__dataset)

        return text

    @property
    def dataset(self):
        """Return underlaying dataset.
        """

        return self.__dataset

    @property
    def is_existent(self):
        """Return if packages (underlaying dataset) is existent.
        """

        return self.__dataset.is_existent

    def create(self, descriptor):
        """Create resource by Data Package descriptor.

        Raises
        ------
        RuntimeError
            If package (underlaying dataset) is already existent.

        """

        # Get model
        model = DataPackage(descriptor)

        # Create dataset
        self.__dataset.create()

        # Create resources
        for resource in model.resources:

            # Prepare metadata
            path = resource.local_data_path
            schema = resource.metadata['schema']
            table_id = path_module.package2dataset(resource.metadata['path'])

            # Initiate remote resource
            resource = jtsbq.Resource(
                   service=self.__service,
                   project_id=self.__project_id,
                   dataset_id=self.__dataset_id,
                   table_id=table_id)

            # Create resource
            resource.create(schema)

            # Import data
            resource.import_data(path)

    def delete(self):
        """Delete package (underlaying dataset).

        Raises
        ------
        RuntimeError
            If package (underlaying dataset) is not existent.

        """

        # Delete table
        self.__dataset.delete()

    def get_resources(self, plain=False):
        """Return dataset resources.

        Parameters
        ----------
        plain: bool
            Return names if True otherwise return Dataset instances.

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
        """Export package using descriptor path.

        Parameters
        ----------
        path: str
            Path where to store `datapackage.json`.

        """

        # Iterate over resources
        resources = []
        for resource in self.get_resources():

            # Export resource data
            rpath = resource.table.table_id
            rpath = path_module.dataset2package(rpath)
            rpath = os.path.join(os.path.dirname(path), rpath)
            resource.export_data(rpath)

            # Add resource metadata
            metadata = {'schema': resource.schema, 'path': rpath}
            resources.append(metadata)

        # Write descriptor
        descriptor = {'resources': resources}
        with io.open(path,
                     mode=self.__write_mode,
                     encoding=self.__write_encoding) as file:
            json.dump(descriptor, file, indent=4)

    # Private

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
