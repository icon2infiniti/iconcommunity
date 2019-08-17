from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider

class PrepRPCCalls():
    #https://bicon.net.solidwallet.io/api/v3
    #https://devorg.icon.foundation/api/v3
    def __init__(self, api_endpoint="https://devorg.icon.foundation/api/v3"):
        self._api_endpoint = api_endpoint

    def getPReps(self):
        icon_service = IconService(HTTPProvider(self._api_endpoint))
        response = icon_service.getPReps()
        return response
