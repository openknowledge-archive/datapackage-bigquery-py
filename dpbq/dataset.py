# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import jtsbq


# Module API

class Dataset(object):
    """BigQuery native dataset representation.
    """

    # Public

    def __init__(self, service, project_id, dataset_id):

        # Set attributes
        self.__service = service
        self.__project_id = project_id
        self.__dataset_id = dataset_id
        # TODO: ensure existent

    def __repr__(self):

        # Template
        template = 'Dataset <{project_id}:{dataset_id}>'

        # Format
        text = template.format(
                project_id=self.__project_id,
                dataset_id=self.__dataset_id)

        return text

    @property
    def service(self):
        return self.__service

    @property
    def project_id(self):
        return self.__project_id

    @property
    def dataset_id(self):
        return self.__dataset_id

    def get_tables(self, plain=False):
        """Return names of all dataset's tables.
        """

        # Get response
        response = self.__service.tables().list(
                projectId=self.__project_id,
                datasetId=self.__dataset_id).execute()

        # Extract tables
        tables = []
        for table in response['tables']:
            table = table['id'].rsplit('.', 1)[1]
            if not plain:
                table = jtsbq.Table(
                        service=self.__service,
                        project_id=self.__project_id,
                        dataset_id=self.__dataset_id,
                        table_id=table)
            tables.append(table)

        return tables
