from huntflow_api_client.entities.base import BaseEntity, GetEntityMixin
from huntflow_api_client.models.response.delayed_tasks import DelayedTaskResponse


class DelayedTask(BaseEntity, GetEntityMixin):
    async def get(self, account_id: int, task_id: str) -> DelayedTaskResponse:
        """
        API method reference:
            https://api.huntflow.ai/v2/docs#get-/accounts/-account_id-/delayed_tasks/-task_id-

        :param account_id: Organization ID
        :param task_id: Task ID

        :return: Information about specified task
        """

        path = f"/accounts/{account_id}/delayed_tasks/{task_id}"
        response = await self._api.request("GET", path)
        return DelayedTaskResponse.model_validate(response.json())
