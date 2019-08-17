from iconsdk.builder.call_builder import CallBuilder
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider

class PrepRPCCalls():
    #https://bicon.net.solidwallet.io/api/v3
    #https://devorg.icon.foundation/api/v3
    def __init__(self, api_endpoint="https://devorg.icon.foundation/api/v3"):
        self._api_endpoint = api_endpoint

    def getPReps(self):
        icon_service = IconService(HTTPProvider(self._api_endpoint))
        call_builder = CallBuilder().to("cx0000000000000000000000000000000000000000") \
            .method("icx_getLastBlock") \
            .build()

        response = icon_service.call(call_builder)

        return response

    def show_game_room_list(self):
        _icon_service = IconService(HTTPProvider("https://bicon.net.solidwallet.io/api/v3"))
        _ = CallBuilder().from_(self._keywallet_address) \
            .to(self._sample_game_score_address) \
            .method("showGameRoomList") \
            .build()

        response = _icon_service.call(_)

        return response
