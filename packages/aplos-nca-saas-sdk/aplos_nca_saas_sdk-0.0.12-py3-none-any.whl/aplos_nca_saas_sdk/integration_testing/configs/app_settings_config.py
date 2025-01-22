"""
Copyright 2024 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from typing import List, Dict, Any
from aplos_nca_saas_sdk.integration_testing.configs._config_base import ConfigBase


class ApplicationDomainConfig(ConfigBase):
    """
    Application Domain: Defines the domains that the application configuration tests will check against

    """

    def __init__(self, domain: str | None = None):
        super().__init__()
        self.__domain: str | None = domain

    @property
    def domain(self) -> str:
        """The domain to validate"""
        if self.__domain is None:
            raise RuntimeError("Domain is not set")
        return self.__domain

    @domain.setter
    def domain(self, value: str):
        self.__domain = value


class ApplicationDomainConfigs(ConfigBase):
    """
    Application ApplicationDomain: Defines the Domains that the application configuration tests will check against

    """

    def __init__(self):
        super().__init__()
        self.__domains: List[ApplicationDomainConfig] = []

    @property
    def list(self) -> List[ApplicationDomainConfig]:
        """List the logins"""
        return self.__domains

    def add(self, *, domain: str, enabled: bool = True):
        """Add a loging"""
        app_domain = ApplicationDomainConfig()
        app_domain.domain = domain
        app_domain.enabled = enabled
        self.__domains.append(app_domain)

    def load(self, test_config: Dict[str, Any]):
        """Load the logins from a list of dictionaries"""
        # self.enabled = bool(test_config.get("enabled", True))
        super().load(test_config)
        domains: List[Dict[str, Any]] = test_config.get("domains", [])

        domain: Dict[str, Any]
        for domain in domains:
            app_domain = ApplicationDomainConfig()
            app_domain.domain = domain.get("domain", None)
            app_domain.enabled = bool(domain.get("enabled", True))

            self.__domains.append(app_domain)


class ApplicationSettings(ConfigBase):
    """
    Application Settings: Defines the domains that the application settings (configuration endpoint) tests will check against

    """

    def __init__(self):
        super().__init__()
        self.__domains: ApplicationDomainConfigs = ApplicationDomainConfigs()

    @property
    def domains(self) -> ApplicationDomainConfigs:
        """List of the domain"""
        return self.__domains

    def load(self, test_config: Dict[str, Any]):
        """Load the domains from the config"""
        super().load(test_config)
        self.domains.load(test_config)
