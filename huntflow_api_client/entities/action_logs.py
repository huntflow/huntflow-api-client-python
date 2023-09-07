from typing import Any, Dict, List, Optional

from huntflow_api_client.entities.base import BaseEntity, ListEntityMixin
from huntflow_api_client.models.consts import ActionLogType
from huntflow_api_client.models.response.action_logs import ActionLogsResponse


class ActionLog(BaseEntity, ListEntityMixin):
    async def list(
        self,
        account_id: int,
        types: Optional[List[ActionLogType]] = None,
        next_id: Optional[int] = None,
        previous_id: Optional[int] = None,
        count: Optional[int] = 30,
    ) -> ActionLogsResponse:
        """
        API method reference https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/action_logs

        :param account_id: Organization ID
        :param types: Action log types
        :param next_id:
            Security logs with IDs less than or equal to the specified one will be received
        :param previous_id:
            Security logs with IDs strictly greater than the specified one will be received
        :param count: Number of items per page
        :return: List of security logs sorted in descending order (from newest to older)
        """
        params: Dict[str, Any] = {"count": count}
        if types:
            params["type"] = [type_item.value for type_item in types]
        if next_id:
            params["next_id"] = next_id
        if previous_id:
            params["previous_id"] = previous_id
        response = await self._api.request(
            "GET",
            f"/accounts/{account_id}/action_logs",
            params=params,
        )
        return ActionLogsResponse.model_validate(response.json())
