#!/usr/bin/env python

# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import os

import pytest

import automl_natural_language_dataset

project_id = os.environ["GCLOUD_PROJECT"]
compute_region = "us-central1"
sentiment_max = 4

@pytest.mark.slow
def test_dataset_create_import_delete(capsys):
    # create sentiment dataset
    dataset_name = "test_" + datetime.datetime.now().strftime("%Y_%m_%dT%H_%M_%SZ")
    automl_natural_language_dataset.create_dataset(
        project_id, compute_region, dataset_name, 10
    )
    out, _ = capsys.readouterr()
    create_dataset_output = out.splitlines()
    assert "Dataset id: " in create_dataset_output[1]

    # import data
    dataset_id = create_dataset_output[1].split()[2]
    data = "gs://python-docs-samples-tests-lcm/crowdflower.csv"
    automl_natural_language_dataset.import_data(
        project_id, compute_region, dataset_id, data
    )
    out, _ = capsys.readouterr()
    assert "Data imported." in out

    # delete dataset
    automl_natural_language_dataset.delete_dataset(
        project_id, compute_region, dataset_id
    )
    out, _ = capsys.readouterr()
    assert "Dataset deleted." in out


def test_dataset_list_get_export(capsys):
    # list datasets
    automl_natural_language_dataset.list_datasets(
        project_id, compute_region, ""
    )
    out, _ = capsys.readouterr()
    list_dataset_output = out.splitlines()
    assert "Dataset id: " in list_dataset_output[2]

    # get dataset
    dataset_id = list_dataset_output[2].split()[2]
    automl_natural_language_dataset.get_dataset(
        project_id, compute_region, dataset_id
    )
    out, _ = capsys.readouterr()
    assert "Dataset name: " in out
    
    # export data
    dataset_id = list_dataset_output[2].split()[2]
    export_uri = "gs://{}-lcm/export.csv".format(project_id)
    automl_natural_language_dataset.export_data(
        project_id, compute_region, dataset_id, export_uri
    )
    out, _ = capsys.readouterr()
    assert "Data exported." in out