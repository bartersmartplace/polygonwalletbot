from typing import Protocol
from app.application.service.common.contracts_enum import ContractsDTO


class IContractManager(Protocol):
    @classmethod
    def load_contract_abi_json(cls, contract_name: ContractsDTO):
        pass


    @classmethod        
    def get_contract_json_file_path(cls, contract_name: ContractsDTO):
        pass