from typing import Any, Dict

from pytest_httpx import HTTPXMock

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities import MailTemplate
from huntflow_api_client.models.response.email_templates import MailTemplatesResponse
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from tests.api import BASE_URL

ACCOUNT_ID = 1
TEMPLATE_LIST_RESPONSE: Dict[str, Any] = {
    "items": [
        {
            "id": 1,
            "subject": "{{Applicant.FirstName}}, we have a position "
            "of {{Vacancy.Position}} for you",
            "name": "Vacancy Invitation",
            "member": 8,
            "html": "<div><p>Hi {{Applicant.FirstName}}</p>,\n\n"
            "<p>We are looking for talented {{Vacancy.Position}}at"
            "{{Organization.Name}}.</p>\n\n<"
            "p>Are you interested to discuss? I will be glad to tell more.</p>\n\n"
            "<p>{{User.Sign}}</p></div>",
            "type": "organization",
            "followups": [
                {"id": 2, "account_member_template": 7, "html": "<p>Hello John!</p>", "days": 1},
            ],
            "attendees": [{"type": "bcc", "email": "user@example.com"}],
            "divisions": [{"id": 3}],
            "files": [
                {
                    "id": 19,
                    "url": "http://example.com",
                    "content_type": "application/pdf",
                    "name": "Resume.pdf",
                },
            ],
        },
    ],
}


async def test_list_templates(
    httpx_mock: HTTPXMock,
    token_proxy: HuntflowTokenProxy,
) -> None:
    httpx_mock.add_response(
        url=f"{BASE_URL}/accounts/{ACCOUNT_ID}/mail/templates?editable=false",
        json=TEMPLATE_LIST_RESPONSE,
    )
    api_client = HuntflowAPI(BASE_URL, token_proxy=token_proxy)
    templates = MailTemplate(api_client)

    response = await templates.list(ACCOUNT_ID)
    assert response == MailTemplatesResponse(**TEMPLATE_LIST_RESPONSE)
