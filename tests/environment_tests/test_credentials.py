import logging
import os

import pytest

logger = logging.getLogger(__name__)

from config.all_config_loader import configs


def test_using_development_config():
    os.environ['CONFIG_FILE'] = 'development.py'
    assert (os.environ['CONFIG_FILE'] == 'development.py')

@pytest.mark.skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", "Skipping this test on Travis CI.")
@pytest.mark.parametrize("test_input", [item for item in configs.keys()])
def test_configs_not_default(test_input):
    os.environ['CONFIG_FILE'] = 'development.py'
    assert (os.environ['CONFIG_FILE'] == 'development.py')
    from config.all_config_loader import configs
    assert (configs[test_input] != 'default')


@pytest.mark.parametrize("test_input", [item for item in configs.keys()])
def test_configs_not_empty(test_input):
    os.environ['CONFIG_FILE'] = 'development.py'
    assert (os.environ['CONFIG_FILE'] == 'development.py')
    from config.all_config_loader import configs
    assert (configs[test_input] != '')

@pytest.mark.skipIf("TRAVIS" in os.environ and os.environ["TRAVIS"] == "true", "Skipping this test on Travis CI.")
@pytest.mark.parametrize("test_input", [item for item in configs.keys()])
def test_configs_not_default(test_input):
    os.environ['CONFIG_FILE'] = 'development.py'
    assert (os.environ['CONFIG_FILE'] == 'development.py')
    from config.all_config_loader import configs
    assert (configs[test_input] != 'default')
