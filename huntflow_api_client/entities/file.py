from typing import BinaryIO, Dict, Optional, Tuple, Union

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
        filename: Optional[str] = None,
    ) -> UploadResponse:
        """
        API method reference https://api.huntflow.ai/v2/docs#post-/accounts/-account_id-/upload

        :param account_id: Organization ID
        :param file: File
        :param preset: Preset
        :param headers: Headers
        :param filename: Filename
        :return: Additional data
        """

        data = {}
        if preset:
            data["preset"] = preset

        files: Dict[str, Union[Union[bytes, BinaryIO], Tuple[str, Union[bytes, BinaryIO]]]] = {}
        if filename:
            files["file"] = (filename, file)
        else:
            files["file"] = file

        response = await self._api.request(
            "POST",
            f"/accounts/{account_id}/upload",
            files=files,
            data=data,
            headers=headers.jsonable_dict(exclude_none=True, by_alias=True),
        )
        return UploadResponse.model_validate(response.json())
