import asyncio
from decimal import Decimal
from web3 import AsyncWeb3, AsyncHTTPProvider
from sqlalchemy import select
from infrastructure.database import get_async_session
from infrastructure.database import RepositoryFactory, DAOFactory
from notification_service.dto import Deposit
from notification_service.notification import notify_about_deposits
from web3.middleware import async_geth_poa_middleware
from infrastructure.database.model import Token


async def check_native_transfers(token_id):
    async_session_generator = get_async_session()
    async_session = await async_session_generator.__anext__()

    async with async_session as session:
        repository_factory = RepositoryFactory(DAOFactory(session))
        address_repository = repository_factory.address_repository
        network_repository = repository_factory.network_repository
        user_repository = repository_factory.user_repository
        native_token = (
            (await session.execute(select(Token).where(Token.id == token_id)))
            .scalars()
            .first()
        )
        network = await network_repository.get_network_by_id(native_token.network_id)
        rpc_url = network.rpc_url
        web3 = AsyncWeb3(AsyncHTTPProvider(rpc_url))
        web3.middleware_onion.inject(async_geth_poa_middleware, layer=0)
        last_block = await web3.eth.get_block_number()
        while True:
            deposits = []
            from_block = native_token.last_checked_block + 1
            to_block = min(from_block + 10, last_block)

            if to_block < from_block:
                break
            
            blocks = await asyncio.gather(
                *[
                    web3.eth.get_block(block, full_transactions=True)
                    for block in range(from_block, to_block + 1)
                ]
            )

            addresses = await address_repository.get_all_addresses()
            addresses = [address.address for address in addresses] 
            for block in blocks:
                for transaction in block["transactions"]:

                    to_addr = transaction["to"]
                    value = transaction["value"]
                    hash = transaction["hash"].hex()
                    if (
                        to_addr in addresses
                    ):

                        receipt = await web3.eth.get_transaction_receipt(
                            hash
                        )
                        if not receipt.status:
                            continue
                        user_address = await address_repository.get_user_address_obj(
                            to_addr
                        )
                        user = await user_repository.get_user_by_id(user_address.user_id)
                        telegram_id = user.tg_id
                        await session.flush()
                        deposits.append(
                            Deposit(
                                user.language,
                                telegram_id,
                                user_address.address,
                                native_token.symbol,
                                Decimal(value) / Decimal(10**18),
                                hash
                            )
                        )

            native_token.last_checked_block = to_block

            await session.commit()

            asyncio.create_task(notify_about_deposits(deposits))