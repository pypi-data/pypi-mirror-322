"""
Copyright 2024 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

from typing import Any, Dict
from aplos_nca_saas_sdk.aws_resources.aws_s3_presigned_upload import S3PresignedUpload
from aplos_nca_saas_sdk.nca_resources.nca_login import NCALogin
from aplos_nca_saas_sdk.utilities.http_utility import HttpUtilities


class NCAFileUpload:
    """NCA File Upload"""

    def __init__(self, nca_login: NCALogin) -> None:
        if nca_login is None or nca_login.jwt is None or not nca_login.jwt:
            raise ValueError("Authenticated nca_login is required.")

        self.__api_domain: str = nca_login.domain or ""
        self.__tenant_id: str = nca_login.cognito.tenant_id
        self.__user_id: str = nca_login.cognito.user_id
        self.__jwt: str = nca_login.jwt

    @property
    def api_root(self) -> str:
        """Gets the base url"""

        if self.__api_domain is None:
            raise RuntimeError("Missing Aplos Api Domain")

        url = HttpUtilities.build_url(
            self.__api_domain, self.__tenant_id, self.__user_id
        )

        return url

    def upload(self, input_file_path: str) -> Dict[str, Any]:
        """
        Uploads a file to the Aplos NCA Cloud

        Args:
            input_file_path (str): local path to the file

        Raises:
            ValueError: _description_

        Returns:
            Dict: {"file_id": id, "statu_code": 204}
        """
        if input_file_path is None or not input_file_path:
            raise ValueError("Valid input_file_path is required.")

        uploader: S3PresignedUpload = S3PresignedUpload(self.__jwt, str(self.api_root))
        upload_response: Dict[str, Any] = uploader.upload_file(input_file_path)

        return upload_response
