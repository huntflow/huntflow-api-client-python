import asyncio

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.entities.dictionaries import Dictionary
from huntflow_api_client.entities.divisions import AccountDivision
from huntflow_api_client.entities.tags import AccountTag
from huntflow_api_client.models.request.dictionaries import DictionaryCreateRequest, DictionaryItem
from huntflow_api_client.models.request.divisions import BatchDivisionsRequest, Division
from huntflow_api_client.tokens import ApiToken


async def main():
    account_id = 14
    token = ApiToken(access_token="ebac5b230f7cc151c08d9d7c62a172192d925b21f5abfc147d6f2f8f371b2d30")
    api = "https://dev-9691-api.huntflow.dev/v2"
    api_client = HuntflowAPI(api, token=token, auto_refresh_tokens=True)

    data = BatchDivisionsRequest.parse_obj(
        {
            "items": [
                Division(name="1")
            ]
        }
    )

    divisions = AccountDivision(api_client)
    response = await divisions.create(account_id, data)
    print(response)


if __name__ == "__main__":

    asyncio.run(main())