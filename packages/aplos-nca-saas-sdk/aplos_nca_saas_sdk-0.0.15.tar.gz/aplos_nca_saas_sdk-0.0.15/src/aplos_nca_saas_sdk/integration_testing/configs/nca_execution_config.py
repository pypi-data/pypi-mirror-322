"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

import json
import os
from typing import Any, Dict, List

from aws_lambda_powertools import Logger

from aplos_nca_saas_sdk.integration_testing.configs._config_base import ConfigBase
from aplos_nca_saas_sdk.integration_testing.configs.login_config import (
    LoginConfig,
    LoginConfigs,
)
from aplos_nca_saas_sdk.utilities.file_utility import FileUtility

logger = Logger(service="NCAExecutionConfig")


class NCAExecutionConfig(ConfigBase):
    """
    NCA Execution Config: Defines an NCA Execution configuration that the application execution tests will check against

    """

    def __init__(
        self,
        login: LoginConfig,
        input_file_path: str,
        config_data: dict,
        meta_data: str | dict | None = None,
        output_dir: str | None = None,
        unzip_after_download: bool = False,
    ):
        super().__init__()

        if login is None:
            raise RuntimeError("login is required")
        self.__login = login

        if input_file_path is None:
            raise RuntimeError("input_file_path is required")
        self.__input_file_path = input_file_path

        if config_data is None:
            raise RuntimeError("config_data is required")
        self.__config_data = config_data

        self.__meta_data = meta_data
        self.__output_dir = output_dir
        self.__unzip_after_download = unzip_after_download

    @property
    def login(self) -> LoginConfig:
        """Login Configuration"""
        return self.__login

    @property
    def input_file_path(self) -> str:
        """Input File Path"""
        return self.__input_file_path

    @property
    def config_data(self) -> Dict[str, Any]:
        """Config Data"""
        return self.__config_data

    @property
    def meta_data(self) -> str | Dict[str, Any] | None:
        """Optional Meta Data"""
        return self.__meta_data

    @property
    def output_dir(self) -> str | None:
        """Local Output Directory"""
        return self.__output_dir

    @property
    def unzip_after_download(self) -> bool:
        """Indicates if the download should be unzipped"""
        return self.__unzip_after_download


class NCAExecutionConfigs(ConfigBase):
    """
    NCA Execution Configs: Defines the configurations that the application NCA Engine tests will check against

    """

    def __init__(self):
        super().__init__()
        self.__nca_executions: List[NCAExecutionConfig] = []

    @property
    def list(self) -> List[NCAExecutionConfig]:
        """List the nca execution configurations"""
        return list(filter(lambda x: x.enabled, self.__nca_executions))

    def add(
        self,
        *,
        login: LoginConfig,
        input_file_path: str,
        config_data: dict,
        meta_data: str | dict | None = None,
        output_dir: str | None = None,
        unzip_after_download: bool = False,
        enabled: bool = True,
    ):
        """Add an NCA Execution Config"""
        nca_excution_config = NCAExecutionConfig(
            login,
            input_file_path,
            config_data,
            meta_data,
            output_dir,
            unzip_after_download,
        )
        nca_excution_config.enabled = enabled
        self.__nca_executions.append(nca_excution_config)

    def load(self, test_config: Dict[str, Any]):
        """Loads the NCA Execution configs from a list of dictionaries"""

        super().load(test_config)
        if not self.enabled:
            return

        base_login: LoginConfig | None = LoginConfigs.try_load_login(
            test_config.get("login", None)
        )
        base_output_dir: str = test_config.get("output_dir", None)
        analyses: List[Dict[str, Any]] = test_config.get("analyses", [])
        for analysis in analyses:
            enabled = bool(analysis.get("enabled", True))
            login: LoginConfig | None = None
            if "login" in analysis:
                login = LoginConfigs.try_load_login(analysis["login"])
            else:
                login = base_login

            if "output_dir" in analysis:
                output_dir = analysis["output_dir"]
            else:
                output_dir = base_output_dir

            if not login:
                raise RuntimeError("Failed to load the login configuration")

            self.add(
                login=login,
                input_file_path=analysis["file"],
                config_data=self.__load_config_data(analysis=analysis),
                meta_data=self.__load_meta_data(analysis=analysis),
                output_dir=output_dir,
                unzip_after_download=True,
                enabled=enabled,
            )

    def __load_meta_data(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        data: Dict[str, Any] = {}
        data = analysis.get("meta", {}).get("data", {})

        return data

    def __load_config_data(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        config_data: Dict[str, Any] = {}
        config_data = analysis.get("config", {}).get("data")

        if config_data:
            return config_data

        config_file_path: str = analysis.get("config", {}).get("file")

        logger.info(
            {
                "message": "Initializing config_data from file",
                "config_data": config_file_path,
            }
        )
        config_path = FileUtility.load_filepath(config_file_path)
        if os.path.exists(config_path) is False:
            raise RuntimeError(f"Config file not found: {config_path}")
        with open(config_path, "r", encoding="utf-8") as f:
            config_data = json.load(f)

        return config_data
