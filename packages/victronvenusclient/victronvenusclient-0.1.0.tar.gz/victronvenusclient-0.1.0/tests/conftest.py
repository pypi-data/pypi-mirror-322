# SPDX-FileCopyrightText: 2024-present Johan du Plessis https://github.com/johanslab
#
# SPDX-License-Identifier: MIT


import pytest
import os

@pytest.fixture
def config_host():
    return os.getenv("VENUS_TEST_HOST", "venus.local.")


@pytest.fixture
def config_port():
    return int(os.getenv("VENUS_TEST_PORT", 1883))


@pytest.fixture
def config_username():
    return os.getenv("VENUS_TEST_USERNAME", None)

@pytest.fixture
def config_password():
    return os.getenv("VENUS_TEST_PASSWORD", None)


@pytest.fixture
def config_use_ssl() -> bool:
    use_ssl_str = os.getenv("VENUS_TEST_USESSL", "False")
    return use_ssl_str.lower() in ['true', '1', 't', 'y', 'yes', 'on']

