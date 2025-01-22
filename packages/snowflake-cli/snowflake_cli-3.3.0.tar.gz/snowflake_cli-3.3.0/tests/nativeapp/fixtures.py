# Copyright (c) 2024 Snowflake Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest.mock as mock

import factory
import pytest
from snowflake.cli._plugins.nativeapp.artifacts import BundleMap
from snowflake.cli._plugins.nativeapp.entities.application import (
    ApplicationEntity,
    ApplicationEntityModel,
)
from snowflake.cli._plugins.nativeapp.entities.application_package import (
    ApplicationPackageEntity,
    ApplicationPackageEntityModel,
)

from tests.nativeapp.factories import (
    ApplicationEntityModelFactory,
    ApplicationPackageEntityModelFactory,
)


@pytest.fixture()
def mock_bundle_map():
    yield mock.Mock(spec=BundleMap)


@pytest.fixture()
def application_package_entity(workspace_context) -> ApplicationPackageEntity:
    data = ApplicationPackageEntityModelFactory(identifier=factory.Faker("word"))
    model = ApplicationPackageEntityModel(**data)
    return ApplicationPackageEntity(model, workspace_context)


@pytest.fixture()
def application_entity(workspace_context):
    data = ApplicationEntityModelFactory(identifier=factory.Faker("word"))
    model = ApplicationEntityModel(**data)
    return ApplicationEntity(model, workspace_context)
