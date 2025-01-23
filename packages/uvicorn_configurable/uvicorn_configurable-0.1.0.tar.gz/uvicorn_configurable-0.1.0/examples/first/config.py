"""File containing the config and setup of the example."""

from application_settings import ConfigBase, config_filepath_from_cli, dataclass

from uvicorn_configurable import UvicornConfigSection


@dataclass(frozen=True)
class ExampleConfig(ConfigBase):
    """Config for first example."""

    uvicorn_config: UvicornConfigSection = UvicornConfigSection()


# Load config.
config_filepath_from_cli(ExampleConfig, load=True)
