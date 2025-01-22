"""
Copyright 2024 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from typing import Optional


class Routes:
    """NCA Saas Routes"""

    NCA_EXECUTIONS = "nca/executions"
    NCA_GENERATE_UPLOAD = "nca/files"


class HttpUtilities:
    """Http Utilties"""

    @staticmethod
    def build_url(
        domain_name: str, tenant_id: Optional[str] = None, user_id: Optional[str] = None
    ) -> str:
        """Build the url"""
        url = domain_name.strip()
        if not domain_name.startswith("http"):
            url = f"https://{domain_name}"

        if tenant_id:
            url = f"{url}/tenants/{tenant_id}"
            if user_id:
                url = f"{url}/users/{user_id}"

        return url

    @staticmethod
    def get_headers(jwt: str) -> dict:
        """Get the Http Headers"""
        headers = {
            "Content-Type": "application/json",
        }

        if jwt:
            headers["Authorization"] = f"Bearer {jwt}"

        return headers
