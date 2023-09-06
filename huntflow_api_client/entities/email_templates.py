from huntflow_api_client.entities.base import BaseEntity, ListEntityMixin
from huntflow_api_client.models.response.email_templates import MailTemplatesResponse


class MailTemplate(BaseEntity, ListEntityMixin):
    async def list(self, account_id: int, editable: bool = False) -> MailTemplatesResponse:
        """
        API method reference
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/mail/templates

        :param account_id: Organization ID
        :param editable: Pass True if the method should return only templates that the current
            user can edit

        :return: List of email templates
        """
        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}/mail/templates",
            params={"editable": editable},
        )
        return MailTemplatesResponse.model_validate(response.json())
