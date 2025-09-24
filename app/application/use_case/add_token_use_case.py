from app.application.service.common.error import TokenAlreadyBeenAddedError
from app.application.service.common.port import IRepositoryFactory
from app.application.dto import TokenDTO


class AddTokenUseCase:
    def __init__(
            self,
            repository_factory: IRepositoryFactory,
            ) -> None:
        self.__repository_factory = repository_factory

    
    async def add_user_token(
            self,
            telegram_id: int,
            token: TokenDTO,
            network_name: str = "Polygon",
            ):
        token_repository = self.__repository_factory.token_repository
        token_to_add: TokenDTO = await token_repository.get_token_by_network_name_and_symbol(network_name, token.symbol)
        user_repository = self.__repository_factory.user_repository
        user = await user_repository.get_user_by_telegram_id(telegram_id)
        if not token_to_add:
            token = TokenDTO(
                id=0,
                name=token.name,
                symbol=token.symbol,
                address=token.address,
                standard=token.standard,
                decimal=token.decimal,
                network_id=token.network_id,
                is_base=token.is_base,
                last_checked_block=token.last_checked_block
            )
            token_to_add = await token_repository.create_token(token)

        else:
            raise TokenAlreadyBeenAddedError("This token has already been added.")
            
        is_token_already_added = await user_repository.user_has_token(user.id, token_to_add.id)
        if is_token_already_added:
            raise TokenAlreadyBeenAddedError("This token has already been added.")
        
        await token_repository.add_user_token(user, token_to_add)

        return None


    async def add_base_token(
        self,
        token: TokenDTO,
        network_name: str = "Polygon",
    ) -> TokenDTO:
        token_repository = self.__repository_factory.token_repository
        existing_token = await token_repository.get_token_by_network_name_and_symbol(network_name, token.symbol)

        if not existing_token:
            token.id = 0
            token.is_base = True
            created_token = await token_repository.create_token(token)
            return created_token

        if not existing_token.is_base:
            existing_token.is_base = True
            updated_token = await token_repository.update_token(existing_token.id, existing_token)
            return updated_token

        raise TokenAlreadyBeenAddedError("The token has already been added")