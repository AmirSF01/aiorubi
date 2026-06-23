from dataclasses import dataclass


@dataclass(frozen=True)
class RubikaAPIServer:
    """
    Base config for API Endpoints
    """

    base: str
    """Base URL"""

    def api_url(self, token: str, method: str) -> str:
        """
        Generate URL for API methods

        :param token: Bot token
        :param method: API method name (case insensitive)
        :return: URL
        """
        return self.base.format(token=token, method=method)

    @classmethod
    def from_base(cls, base: str) -> "RubikaAPIServer":
        """
        Use this method to auto-generate RubikaAPIServer instance from base URL

        :param base: Base URL
        :return: instance of :class:`RubikaAPIServer`
        """
        base = base.rstrip("/")
        return cls(
            base=f"{base}/v3/{{token}}/{{method}}",
        )


PRODUCTION = RubikaAPIServer(
    base="https://botapi.rubika.ir/v3/{token}/{method}",
)
