import json

import requests

from maitai._config import config
from maitai._utils import __version__ as version
from maitai._utils import required_args
from maitai.models.application import ApplicationContext


class ContextManager:
    @required_args(
        ["application", "reference", "context_body"],
        ["application", "reference", "file_path"],
    )
    def update(
        self,
        *,
        application: str,
        reference: str,
        context_body: str = "",
        file_path: str = "",
    ):
        if not reference:
            raise ValueError("Reference is required")
        if context_body and file_path:
            raise ValueError("Only one of context_body and file can be specified")

        if file_path:
            s3_path = self.upload_context_file(file_path).get("s3_path")
            if not s3_path:
                raise Exception("Failed to upload context")
            context_type = "FILE"
            context_path = s3_path
        else:
            context_type = "TEXT"
            context_path = None
        context = ApplicationContext(
            reference=reference,
            context_type=context_type,
            context_path=context_path,
            context_body=context_body,
        )

        host = config.maitai_host
        url = f"{host}/context/application"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": config.api_key,
            "x-client-version": version,
        }
        response = requests.put(
            url,
            headers=headers,
            data=json.dumps(
                {
                    "application_ref_name": application,
                    "context": context.model_dump(),
                }
            ),
        )

        if response.status_code != 200:
            raise RuntimeError(f"Error updating context: {response.text}")

    def upload_context_file(self, file_path: str):
        host = config.maitai_host
        url = f"{host}/context/application/file"
        headers = {
            "x-api-key": config.api_key,
            "x-client-version": version,
        }
        with open(file_path, "rb") as file:
            files = {"file": file}
            response = requests.post(url, headers=headers, files=files)
        if response.status_code != 200:
            raise RuntimeError(f"Error uploading context: {response.text}")
        return response.json()
