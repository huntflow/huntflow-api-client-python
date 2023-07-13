from huntflow_api_client.entities.base import BaseEntity, ListEntityMixin
from huntflow_api_client.models.response.action_logs import ActionLogsResponse


class ActionLog(BaseEntity, ListEntityMixin):
    async def list(self, account_id: int) -> ActionLogsResponse:
        """
        API method reference https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/action_logs

        :param account_id: Organization ID
        :return: An applicant resume
        """
        response = await self._api.request("GET", f"/accounts/{account_id}/action_logs")
        return ActionLogsResponse.parse_obj(response.json())
