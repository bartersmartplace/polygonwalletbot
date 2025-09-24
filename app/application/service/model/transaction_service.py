from app.application.service.common.port import IAppWeb3Provider
from app.application.dto import AccountDTO


class Transaction:
    MAX_RETRIES = 2

    @classmethod
    async def send_tx(
        cls,
        web3_adapter: IAppWeb3Provider,
        tx_params: dict,
        account: AccountDTO,
    ) -> str:
        retries = 0
        while retries < cls.MAX_RETRIES:
            try:
                tx_params["gas"] = await web3_adapter.estimate_gas(tx_params)
                signed_tx = web3_adapter.sign_transaction(account, tx_params)                
                tx_hash = await web3_adapter.send_transaction(signed_tx)
                if tx_hash is not None:
                    await web3_adapter.check_transaction_status(tx_hash)
                    return tx_hash

            except Exception as e:
                if "nonce too low" in str(e).lower():
                    tx_params["nonce"] += 1
                    retries += 1
                    print(f"Retrying due to nonce too low error. Attempt {retries}")
                    continue
                else:
                    raise e