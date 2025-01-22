"""
Copyright 2024 Aplos Analytics
All Rights Reserved.   www.aplosanalytics.com   LICENSED MATERIALS
Property of Aplos Analytics, Utah, USA
"""

import time
from datetime import datetime, timedelta
from typing import Any, Dict, List

import requests
from aws_lambda_powertools import Logger
from aplos_nca_saas_sdk.integration_testing.configs.login_config import LoginConfig
from aplos_nca_saas_sdk.integration_testing.integration_test_base import (
    IntegrationTestBase,
)
from aplos_nca_saas_sdk.integration_testing.integration_test_response import (
    IntegrationTestResponse,
)
from aplos_nca_saas_sdk.nca_resources.nca_file_upload import NCAFileUpload
from aplos_nca_saas_sdk.nca_resources.nca_login import NCALogin
from aplos_nca_saas_sdk.utilities.http_utility import HttpUtilities

logger = Logger()


class FileUploadTest(IntegrationTestBase):
    """File Upload Test Container"""

    def __init__(self):
        super().__init__("file-upload")

    def test(self) -> bool:
        """Test file upload"""

        self.results.clear()

        for file_upload in self.config.file_uploads.list:
            test_response: IntegrationTestResponse = IntegrationTestResponse()
            test_response.name = self.name
            try:
                # Confirm Login
                nca_login = self.__login(file_upload.login)
                if not nca_login.jwt:
                    test_response.error = "Failed to authenticate"
                else:
                    # Confirm Upload
                    upload_response: Dict[str, Any] = self.__upload(
                        nca_login, file_upload.file_path
                    )
                    if upload_response is None:
                        test_response.error = "Failed to upload"
                    else:
                        # Confirm conversion and download
                        # Allow time buffer so file data is available
                        file_id: str = upload_response.get("file_id", "")
                        if not file_id:
                            raise RuntimeError(
                                "Failed to get a file_id from the upload"
                            )
                        time.sleep(3)
                        self.__download(nca_login, file_id, test_response)

            except Exception as e:  # pylint: disable=w0718
                test_response.error = str(e)

            self.results.append(test_response)

        return self.success()

    def __login(self, login: LoginConfig) -> NCALogin:
        nca_login = NCALogin(aplos_saas_domain=login.domain)
        nca_login.authenticate(username=login.username, password=login.password)
        return nca_login

    def __upload(self, nca_login: NCALogin, upload_file_path: str) -> Dict[str, Any]:
        logger.info({"message": "Uploading file", "file_path": upload_file_path})

        nca_file_upload = NCAFileUpload(nca_login)
        upload_response: Dict[str, Any] = nca_file_upload.upload(upload_file_path)
        return upload_response

    def __download(
        self,
        nca_login: NCALogin,
        file_id: str,
        test_response: IntegrationTestResponse,
    ):
        logger.info({"message": "Downloading file", "file_id": file_id})
        file_data_endpoint = nca_login.config.endpoints.file_data(
            nca_login.cognito.tenant_id,
            nca_login.cognito.user_id,
            file_id,
        )
        file_info_endpoint = nca_login.config.endpoints.file(
            nca_login.cognito.tenant_id,
            nca_login.cognito.user_id,
            file_id,
        )

        max_wait_in_minutes: int = 3
        headers = HttpUtilities.get_headers(nca_login.jwt)
        current_time = datetime.now()

        # Create a timedelta object representing 3 minutes
        time_delta = timedelta(minutes=max_wait_in_minutes)
        # Add the timedelta to the current time
        max_time = current_time + time_delta

        complete = False
        while not complete:
            response = requests.get(file_info_endpoint, headers=headers, timeout=60)
            json_response: dict = response.json()
            errors: List[Dict[str, Any]] = []
            errors.extend(json_response.get("errors") or [])
            status = json_response.get("workable_state")
            complete = status == "ready"

            if status == "invalid" or len(errors) > 0:
                test_response.success = False
                test_response.error = (
                    "File conversion failed."
                    if len(errors) < 0
                    else f"File conversion failed with errors ${errors}."
                )
                break
            if complete:
                break
            if not complete:
                time.sleep(5)
            if datetime.now() > max_time:
                test_response.success = False
                test_response.error = (
                    "Timeout attempting to get conversion file status. "
                    f"The current timeout limit is {max_wait_in_minutes} minutes. "
                    "You may need to up the timeout period, or check for errors. "
                )
                break

        if test_response.error is not None:
            return

        file_response = requests.get(file_data_endpoint, headers=headers, timeout=30)

        json_file_response: dict = file_response.json()
        data = json_file_response.get("data", None)
        error = json_file_response.get("error", None)

        if data is None:
            test_response.success = False
            test_response.error = "File download missing expected data. "
        if error is not None:
            test_response.success = False
            test_response.error = (
                test_response.error or ""
            ) + f"File download contained error ${error}"

        test_response.success = True
