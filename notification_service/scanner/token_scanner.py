import asyncio
from decimal import Decimal
from web3.middleware import async_geth_poa_middleware
from web3 import AsyncWeb3, AsyncHTTPProvider
from sqlalchemy import select
from infrastructure.database import get_async_session
from infrastructure.database import RepositoryFactory, DAOFactory
from infrastructure.database.model import Token
from infrastructure.operating_system import ContractManager
from app.application.service.common.contracts_enum import ContractsDTO
from notification_service.dto import Deposit
from notification_service.notification import notify_about_deposits

erc20_abi = ContractManager.load_contract_abi_json(ContractsDTO.ERC20)


async def check_token_transfers(token_id):
    async_session_generator = get_async_session()
    async_session = await async_session_generator.__anext__()
    async with async_session as session:
        repository_factory = RepositoryFactory(DAOFactory(session))
        address_repository = repository_factory.address_repository
        user_repository = repository_factory.user_repository
        network_repository = repository_factory.network_repository

        token = (
            (await session.execute(select(Token).where(Token.id == token_id)))
            .scalars()
            .first()
        )

        network = await network_repository.get_network_by_id(token.network_id)
        rpc_url = network.rpc_url
        web3 = AsyncWeb3(AsyncHTTPProvider(rpc_url))
        web3.middleware_onion.inject(async_geth_poa_middleware, layer=0)

        contract = web3.eth.contract(address=token.address, abi=erc20_abi)
        decimals = await contract.functions.decimals().call()
        last_block = await web3.eth.get_block_number()

        addresses = await address_repository.get_all_addresses()
        addresses = [address.address for address in addresses]
        while True:
            deposits = []
            from_block = token.last_checked_block + 1
            to_block = min(from_block + 200, last_block)

            if to_block < from_block:
                break

            events = await contract.events.Transfer().get_logs(
                fromBlock=from_block, toBlock=to_block
            )
            for event in events:
                from_addr = event.args["from"]
                to_addr = event.args["to"]
                value = event.args.value
                if (
                    (to_addr in addresses)
                ):

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
                            token.symbol,
                            Decimal(value) / Decimal(10**decimals),
                            event.transactionHash.hex(),
                        )
                    )

            token.last_checked_block = to_block

            await session.commit()
            asyncio.create_task(notify_about_deposits(deposits))