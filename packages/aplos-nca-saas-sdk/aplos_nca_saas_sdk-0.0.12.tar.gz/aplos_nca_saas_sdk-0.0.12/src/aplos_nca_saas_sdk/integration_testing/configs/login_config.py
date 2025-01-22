"""
Copyright 2024 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from typing import List, Optional, Dict, Any
from aplos_nca_saas_sdk.integration_testing.configs._config_base import ConfigBase


class LoginConfig(ConfigBase):
    """
    Application Login: Defines the login that the application configuration tests will check against

    """

    def __init__(
        self,
        username: Optional[str] = None,
        passord: Optional[str] = None,
        domain: Optional[str] = None,
        roles: Optional[List[str]] = None,
    ):
        super().__init__()
        self.__username: Optional[str] = username
        self.__password: Optional[str] = passord
        self.__domain: Optional[str] = domain
        self.__roles: List[str] = roles if roles is not None else []

    @property
    def username(self) -> str:
        if self.__username is None:
            raise RuntimeError("Username is not set")
        return self.__username

    @username.setter
    def username(self, value: str):
        self.__username = value

    @property
    def password(self) -> str:
        if self.__password is None:
            raise RuntimeError("Password is not set")
        return self.__password

    @password.setter
    def password(self, value: str):
        self.__password = value

    @property
    def domain(self) -> str:
        if self.__domain is None:
            raise RuntimeError("Domain is not set")
        return self.__domain

    @domain.setter
    def domain(self, value: str):
        self.__domain = value

    @property
    def roles(self) -> List[str]:
        """A list of roles to check for"""
        return self.__roles

    @roles.setter
    def roles(self, value: List[str] | None):
        if value is None:
            value = []
        self.__roles = value


class LoginConfigs(ConfigBase):
    """
    Application Logins: Defines the logins that the application configuration tests will check against

    """

    def __init__(self):
        super().__init__()
        self.__logins: List[LoginConfig] = []

    @property
    def list(self) -> List[LoginConfig]:
        """List the logins"""
        return self.__logins

    def add(self, *, username: str, password: str, domain: str, enabled: bool = True):
        """Add a loging"""
        login = LoginConfig()
        login.username = username
        login.password = password
        login.domain = domain
        login.enabled = enabled
        self.__logins.append(login)

    def load(self, test_config: Dict[str, Any]):
        """Load the logins from a list of dictionaries"""

        super().load(test_config)
        logins: List[Dict[str, str]] = test_config.get("logins", [])
        for login in logins:
            login_config = LoginConfigs.try_load_login(login)
            if login_config is None:
                continue
            self.__logins.append(login_config)

    @staticmethod
    def try_load_login(login_config: Dict[str, Any]) -> LoginConfig | None:
        """Attempts to intialize a Login from a configuration object"""
        login: LoginConfig | None = None
        if login_config is not None:
            username = login_config.get("username", None)
            password = login_config.get("password", None)
            domain = login_config.get("domain", None)
            enabled = login_config.get("enabled", True)
            login = LoginConfig(username, password, domain)
            login.enabled = enabled
        return login
