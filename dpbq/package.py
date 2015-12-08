# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import os
import re
import jtsbq
import datapackage


class Package(object):

    # Public

    def __init__(self, path):
        self.__dp = datapackage.DataPackage(path)

    def upload(self, client_email, private_key, project_id, dataset_id):

        # Iterate over resources
        for resource in self.__dp.resources:

            # Prepare metadata
            path = resource.local_data_path
            schema = resource.metadata['schema']
            table_id = self.__make_table_id(resource.metadata['path'])

            # Create table
            table = jtsbq.Table(
                   client_email=client_email,
                   private_key=private_key,
                   project_id=project_id,
                   dataset_id=dataset_id,
                   table_id=table_id)

            # Upload table
            table.upload(schema, path)

    # Private

    def __make_table_id(self, path):
        name = path
        name = os.path.splitext(name)[0]
        name = name.replace(os.path.sep, '__')
        name = re.sub('[^0-9a-zA-Z_]+', '_', name)
        return name
