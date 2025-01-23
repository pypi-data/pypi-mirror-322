"""
Copyright 2024-2025 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

import requests

from aplos_nca_saas_sdk.nca_resources._api_base import NCAApiBaseClass


class NCAValidation(NCAApiBaseClass):
    """NCA Analysis Validation API"""

    def __init__(self, host: str) -> None:
        super().__init__(host)

    def validate(self, jwt: str) -> bool:
        """
        Validates the JWT

        Args:
            jwt (str): JWT

        Returns:
            bool: True if the JWT is valid
        """
        url = self.endpoints.validations
        response = requests.post(url, json={"jwt": jwt}, timeout=30)

        if response.status_code != 200:
            return False

        return True
