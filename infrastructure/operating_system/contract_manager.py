import os
import json
from app.application.service.common.contracts_enum import ContractsDTO


class ContractManager():
    @classmethod
    def load_contract_abi_json(cls, contract_name: ContractsDTO):
        path_to_file = ContractManager.get_contract_json_file_path(contract_name)
        with open(path_to_file) as json_file:
            abi = json.load(json_file)
        
        return abi
    
    @classmethod
    def get_contract_json_file_path(cls, contract_name: ContractsDTO):
        return os.path.join("infrastructure", "network", "contracts", f"{contract_name}.json")