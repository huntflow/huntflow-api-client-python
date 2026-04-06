from huntflow_api_client.entities.base import BaseEntity, UpdateEntityMixin
from huntflow_api_client.models.request.token import RefreshTokenRequest
from huntflow_api_client.models.response.token import RefreshTokenResponse


class Token(BaseEntity, UpdateEntityMixin):

    async def update(self, data: RefreshTokenRequest) -> RefreshTokenResponse:
        """
        API method reference
            https://api.huntflow.ru/latest/docs#post-/token/refresh

        :param data: Token request data
        :return: Refreshed token data
        """
        response = await self._api.request(
            "POST",
            "/token/refresh",
            json=data.jsonable_dict(),
        )
        return RefreshTokenResponse.model_validate(response.json())
