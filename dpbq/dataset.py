# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import jtsbq
from apiclient.errors import HttpError


# Module API

class Dataset(object):
    """BigQuery native dataset representation.

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
        """Return BigQuery service instance.
        """

        return self.__service

    @property
    def project_id(self):
        """Return BigQuery project identifier.
        """

        return self.__project_id

    @property
    def dataset_id(self):
        """Return BigQuery dataset identifier.
        """

        return self.__dataset_id

    @property
    def is_existent(self):
        """Return dataset if is existent.
        """

        # If tables
        try:
            # TODO: use other call?
            self.get_tables()
            return True

        # No dataset
        except HttpError as error:
            if error.resp.status != 404:
                raise
            return False

    def create(self):
        """Create dataset.

        Raises
        ------
        RuntimeError
            If dataset is already existent.

        """

        # Check not existent
        if self.is_existent:
            message = 'Dataset "%s" is already existent.' % self
            raise RuntimeError(message)

        # Prepare job body
        body = {
            'datasetReference': {
                'projectId': self.__project_id,
                'datasetId': self.__dataset_id,
            },
        }

        # Make request
        self.__service.datasets().insert(
                projectId=self.__project_id,
                body=body).execute()

    def delete(self):
        """Delete dataset.

        Raises
        ------
        RuntimeError
            If dataset is not existent.

        """

        # Check existent
        if not self.is_existent:
            message = 'Dataset "%s" is not existent.' % self
            raise RuntimeError(message)

        # Make request
        self.__service.datasets().delete(
                projectId=self.__project_id,
                datasetId=self.__dataset_id).execute()

    def get_tables(self, plain=False):
        """Return dataset's tables.

        Parameters
        ----------
        plain: bool
            Return names if True otherwise return Table instances.

        """

        # Get response
        response = self.__service.tables().list(
                projectId=self.__project_id,
                datasetId=self.__dataset_id).execute()

        # Extract tables
        tables = []
        for table in response.get('tables', []):
            table = table['id'].rsplit('.', 1)[1]
            if not plain:
                table = jtsbq.Table(
                        service=self.__service,
                        project_id=self.__project_id,
                        dataset_id=self.__dataset_id,
                        table_id=table)
            tables.append(table)

        return tables
