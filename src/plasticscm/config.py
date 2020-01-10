# Copyright (c) 2019-2020 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/licenses/zlib

from typing  import Optional, List
from pathlib import Path
import configparser

from public import public


@public
class PlasticConfigParser:

    _DEFAULT_CONFIG_FILES = (
        Path(__file__).resolve().parent/"plasticscm.cfg",
        Path.home()/".plasticscm.cfg",
    )

    def __init__(self,
                 plastic_id: Optional[str]=None,
                 config_files: Optional[List[Path]]=None):
        self.plastic_id = plastic_id
        config_files = config_files or self._DEFAULT_CONFIG_FILES
        if all(not file.is_file() for file in config_files):
            raise PlasticConfigMissingError(
                "Config file not found.\n"
                "Please create one in one of the following locations: {}\n"
                "or specify a config file using the '-c' parameter.".format(
                ", ".join(str(file) for file in self._DEFAULT_CONFIG_FILES)))

        self._config = configparser.ConfigParser()
        self._config.read((str(file) for file in config_files), encoding="utf-8")

        if self.plastic_id is None:
            try:
                self.plastic_id = self._config.get("global", "default")
            except Exception:
                raise PlasticIDError("Impossible to get the plastic id "
                                     "(not specified in config file)")

        sections = ("global", self.plastic_id)

        try:
            self.url = self._config.get(self.plastic_id, "url")
        except Exception:
            raise PlasticDataError("Impossible to get plastic informations from "
                                   "configuration ({})".format(self.plastic_id))

        self.http_username = None
        self.http_password = None
        try:
            self.http_username = self._config.get(self.plastic_id, "http_username")
            self.http_password = self._config.get(self.plastic_id, "http_password")
        except Exception:
            pass

        self.ssl_verify = True
        for section in sections:
            try:
                self.ssl_verify = self._config.getboolean(section, "ssl_verify")
            except ValueError:
                # Value Error means the option exists but isn't a boolean.
                # Get as a string instead as it should then be a local path to a
                # CA bundle.
                try:
                    self.ssl_verify = self._config.get(section, "ssl_verify")
                except Exception:
                    pass
            except Exception:
                pass

        self.timeout = 60
        for section in sections:
            try:
                self.timeout = self._config.getint(section, "timeout")
            except Exception:
                pass

        self.private_token = None
        try:
            self.private_token = self._config.get(self.plastic_id, "private_token")
        except Exception:
            pass

        self.oauth_token = None
        try:
            self.oauth_token = self._config.get(self.plastic_id, "oauth_token")
        except Exception:
            pass

        self.job_token = None
        try:
            self.job_token = self._config.get(self.plastic_id, "job_token")
        except Exception:
            pass

        self.api_version = "1"
        for section in sections:
            try:
                self.api_version = self._config.get(section, "api_version")
            except Exception:
                pass
        if self.api_version not in ("1",):
            raise PlasticDataError("Unsupported API version: {}".format(self.api_version))

        self.per_page = None
        for section in sections:
            try:
                self.per_page = self._config.getint(section, "per_page")
            except Exception:
                pass
        if self.per_page is not None and not 0 <= self.per_page <= 100:
            raise PlasticDataError("Unsupported per_page number: {}".format(self.per_page))


@public
class ConfigError(Exception):
    """ """

@public
class PlasticConfigMissingError(ConfigError):
    """ """

@public
class PlasticIDError(ConfigError):
    """ """

@public
class PlasticDataError(ConfigError):
    """ """
