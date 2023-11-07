from typing import BinaryIO, Optional, Union

from huntflow_api_client.entities.base import BaseEntity
from huntflow_api_client.models.request.file import UploadFileHeaders
from huntflow_api_client.models.response.file import UploadResponse


class File(BaseEntity):
    async def upload(
        self,
        account_id: int,
        headers: UploadFileHeaders,
        file: Union[bytes, BinaryIO],
        preset: Optional[str] = None,
    ) -> UploadResponse:
        """
        API method reference https://api.huntflow.ai/v2/docs#post-/accounts/-account_id-/upload

        :param account_id: Organization ID
        :param file: File
        :param preset: Preset
        :param headers: Headers
        :return: Additional data
        """

        data = {}
        if preset:
            data["preset"] = preset
        response = await self._api.request(
            "POST",
            f"/accounts/{account_id}/upload",
            files={"file": file},
            data=data,
            headers=headers.jsonable_dict(exclude_none=True, by_alias=True),
        )
        return UploadResponse.model_validate(response.json())
