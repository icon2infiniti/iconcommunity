from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider


class JsonRPCCalls():
    #https://devorg.icon.foundation/api/v3
    def __init__(self, keywallet_address="hx5638ee91e18574a1f0a29b4813578389f0e142a7", api_endpoint="https://bicon.net.solidwallet.io/api/v3"):
        self._keywallet_address = keywallet_address
        self._api_endpoint = api_endpoint

    def getLatestBlock(self):
        _icon_service = IconService(HTTPProvider(self._api_endpoint))
        response = _icon_service.get_block("latest")
        return response
