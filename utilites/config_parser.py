import configparser
import pathlib


def get_config_data(section, field=None):
    conf_file_path = pathlib.Path(__file__).parent.parent.absolute().joinpath(f"config/config.ini")
    config = configparser.ConfigParser()
    config.read(conf_file_path)

    try:
        data = config[section]
    except KeyError:
        raise KeyError(f"Invalid section '{section}' specified. Must be one of [{config.sections()}]")
    if field:
        return data[field]
    return dict(data)

