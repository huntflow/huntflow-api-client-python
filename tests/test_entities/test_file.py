from typing import Any, Dict

from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities.file import File
from huntflow_api_client.models.request.file import UploadFileHeaders
from huntflow_api_client.models.response.file import UploadResponse
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL

ACCOUNT_ID = 1
UPLOAD_FILE_RESPONSE: Dict[str, Any] = {
    "id": 1,
    "url": "http://example.com",
    "content_type": "image/jpeg",
    "name": "0001.jpeg",
    "photo": {
        "id": 19,
        "url": "http://example.com",
        "content_type": "application/pdf",
        "name": "Resume.pdf",
    },
    "text": "string",
    "fields": {
        "name": {"first": "John", "last": "Doe", "middle": "Harvard"},
        "birthdate": {"year": 2000, "month": 10, "day": 7, "precision": "day"},
        "phones": ["+7 (999) 8887766"],
        "email": "mail@nomail.ru",
        "salary": 100500,
        "position": "Developer",
        "skype": "tproger",
        "telegram": "@tproger",
        "experience": [
            {"position": "Some position name", "company": "Some company name"},
        ],
    },
}


async def test_upload_file(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/upload",
        json=UPLOAD_FILE_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    files = File(api_client)
    headers = UploadFileHeaders(file_parse=True)
    upload_data = b"test data"

    response = await files.upload(ACCOUNT_ID, headers, upload_data)
    assert response == UploadResponse(**UPLOAD_FILE_RESPONSE)
