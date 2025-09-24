from ..port import ( 
    ITokenService,
)

class DomainServiceFactory:
    def __init__(
                self,
                token: ITokenService = None,
                ):
        self._token = token


    @property
    def token(self) -> ITokenService:
        """Returns an Token service."""
        return self._token