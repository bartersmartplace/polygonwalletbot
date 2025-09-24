import asyncio
from web3 import AsyncWeb3, AsyncHTTPProvider
from infrastructure.database import get_async_session
from sqlalchemy import select
from notification_service.scanner import check_native_transfers, check_token_transfers
from infrastructure.database import RepositoryFactory, DAOFactory
from infrastructure.database.model import Token


async def start_monitor_tx():
    tokens_tasks: dict[int, asyncio.Task] = {}
    native_tokens_tasks: dict[int, asyncio.Task] = {}
    while True:
        async_session_generator = get_async_session()
        async_session = await async_session_generator.__anext__()

        async with async_session as session:
            for k, t in list(tokens_tasks.items()):
                if t.done():
                    del tokens_tasks[k]

            for k, t in list(native_tokens_tasks.items()):
                if t.done():
                    del native_tokens_tasks[k]
            
            repository_factory = RepositoryFactory(DAOFactory(session))
            network_repository = repository_factory.network_repository
            tokens = (await session.execute(select(Token))).scalars().all()
            need_update = []

            chain_block_number = 0
            for token in tokens:
                try:
                    network = await network_repository.get_network_by_id(token.network_id)
                    rpc_url = network.rpc_url
                    web3 = AsyncWeb3(AsyncHTTPProvider(rpc_url))
                    chain_block_number = await web3.eth.block_number
                except Exception as e:
                    print(f"web3.eth.block_number exception: {e}")
                    print(f"token.chain_id: {token.network_id}")

                if token.last_checked_block < chain_block_number and token.address:
                    need_update.append(token.id)

            for token_id in need_update:
                if token_id not in tokens_tasks:

                    tokens_tasks[token_id] = asyncio.create_task(check_token_transfers(token_id))

            repository_factory = RepositoryFactory(DAOFactory(session))
            network_repository = repository_factory.network_repository
            native_tokens = (await session.execute(select(Token))).scalars().all()
            need_update = []
            for token in native_tokens:
                try:
                    network = await network_repository.get_network_by_id(token.network_id)
                    rpc_url = network.rpc_url
                    web3 = AsyncWeb3(AsyncHTTPProvider(rpc_url))
                    chain_block_number = await web3.eth.block_number
                except Exception as e:
                    print(f"web3.eth.block_number exception: {e}")
                    print(f"token.chain_id: {token.network_id}")

                if token.last_checked_block < chain_block_number and not token.address:
                    need_update.append(token.id)

            for chain_id in need_update:
                if chain_id not in native_tokens_tasks:
                    native_tokens_tasks[chain_id] = asyncio.create_task(check_native_transfers(chain_id))

        await asyncio.sleep(1)


def run_parsing():
    asyncio.run(start_monitor_tx())