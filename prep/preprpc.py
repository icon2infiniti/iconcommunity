from iconsdk.builder.call_builder import CallBuilder
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider


class PrepRPCCalls:

    MAIN_NET = "https://ctz.solidwallet.io/api/v3"
    TEST_NET = "https://bicon.net.solidwallet.io/api/v3"
    TEMP_NET = "https://devorg.icon.foundation/api/v3"

    def __init__(self, to_contract="cx0000000000000000000000000000000000000000"):
        self._to_contract = to_contract

    def json_rpc_call(self, method_name, params):
        icon_service = IconService(HTTPProvider(PrepRPCCalls.TEMP_NET))
        call_builder = CallBuilder() \
            .to(self._to_contract) \
            .method(method_name) \
            .build()

        response = icon_service.call(call_builder)

        return response
