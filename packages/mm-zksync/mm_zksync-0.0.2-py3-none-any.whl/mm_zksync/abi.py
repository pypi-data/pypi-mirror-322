import json
import pkgutil
from typing import cast

from eth_typing import ABI


def zksync_contract_abi() -> ABI:
    data = pkgutil.get_data(__name__, "abi/zksync.json")
    if data is None:
        raise RuntimeError("can't read abi/zksync.json")
    return cast(ABI, json.loads(data.decode()))
