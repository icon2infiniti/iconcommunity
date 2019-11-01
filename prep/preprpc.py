from iconsdk.builder.call_builder import CallBuilder
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider


class PrepRPCCalls:

    MAIN_NET = "https://ctz.solidwallet.io/api/v3"

    USE_NET = MAIN_NET
    USE_NET_NAME = "MAIN_NET"

    def __init__(self, to_contract="cx0000000000000000000000000000000000000000"):
        self._to_contract = to_contract

    def json_rpc_call(self, method_name, params):
        icon_service = IconService(HTTPProvider(PrepRPCCalls.USE_NET))

        call_builder = CallBuilder() \
            .to(self._to_contract) \
            .method(method_name) \
            .params(params) \
            .build()

        response = icon_service.call(call_builder)

        return response

    def get_block(self, block_height):
        icon_service = IconService(HTTPProvider(PrepRPCCalls.USE_NET))

        latest_block = icon_service.get_block("latest")
        if latest_block['height'] < block_height:
            return None

        block = icon_service.get_block(block_height)
        return block
