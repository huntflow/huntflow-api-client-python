import asyncio
from argparse import ArgumentParser
from typing import List

from huntflow_api_client import HuntflowAPI
from huntflow_api_client.tokens.locker import AsyncioLockLocker
from huntflow_api_client.tokens.proxy import HuntflowTokenProxy
from huntflow_api_client.tokens.storage import HuntflowTokenFileStorage


async def get_and_print_org_info(api_client: HuntflowAPI):
    response = await api_client.request("GET", "/accounts")
    print(response.json())


async def main(concurrent_client_count: int, token_filename: str, base_url: str):
    token_storage = HuntflowTokenFileStorage(token_filename)
    locker = AsyncioLockLocker()
    api_clients: List[HuntflowAPI] = []
    for _ in range(concurrent_client_count):
        token_proxy = HuntflowTokenProxy(token_storage, locker)
        client = HuntflowAPI(
            base_url,
            token_proxy=token_proxy,
            auto_refresh_tokens=True,
        )
        api_clients.append(client)
    calls = [get_and_print_org_info(client) for client in api_clients]
    await asyncio.gather(*calls)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "--count",
        type=int,
        default=3,
        help="Number of concurrent requests",
    )
    parser.add_argument("--url", type=str, help="https://<api domain>/v2")
    parser.add_argument(
        "--token-file",
        type=str,
        help=(
            "Path to json file. File must include 'access_token' and 'refresh_token' keys."
            " File will be rewritten when token is refreshed."
        ),
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args.count, args.token_file, args.url))
