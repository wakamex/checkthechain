from __future__ import annotations

import typing
from typing_extensions import TypedDict

import asyncio
import json
import time

from ctc import config
from ctc import evm
from ctc import spec

from . import etherscan_spec


class EtherscanRatelimit(TypedDict):
    requests_per_second: int | float
    last_request_time: int | float
    lock: asyncio.Lock | None
    recent_results: typing.MutableMapping[spec.Address, typing.Any]


_etherscan_ratelimit: EtherscanRatelimit = {
    'requests_per_second': 0.2,
    'last_request_time': 0,
    'lock': None,
    'recent_results': {},
}


def set_etherscan_ratelimit(requests_per_second: int | float) -> None:
    _etherscan_ratelimit['requests_per_second'] = requests_per_second


async def async_get_contract_abi(
    contract_address: spec.Address,
    network: spec.NetworkReference | None = None,
    verbose: bool = True,
) -> spec.ContractABI:
    """fetch contract abi using etherscan"""

    import aiohttp

    # process inputs
    if network is None:
        network = config.get_default_network()
    if not evm.is_address_str(contract_address):
        raise Exception('not a valid address: ' + str(contract_address))

    if verbose:
        network = evm.get_network_name(network)
        print(
            'fetching ' + str(network) + ' abi from etherscan:',
            contract_address,
        )

    # create lock
    lock = _etherscan_ratelimit['lock']
    if lock is None:
        lock = asyncio.Lock()
        _etherscan_ratelimit['lock'] = lock

    # acquire lock
    async with lock:

        if contract_address in _etherscan_ratelimit['recent_results']:
            return _etherscan_ratelimit['recent_results'][contract_address]

        # ratelimit
        now = time.time()
        time_since_last = now - _etherscan_ratelimit['last_request_time']
        seconds_per_request = 1 / _etherscan_ratelimit['requests_per_second']
        time_to_sleep = seconds_per_request - time_since_last
        if time_to_sleep > 0:
            if verbose:
                print(
                    'etherscan ratelimit hit, sleeping for '
                    + str(time_to_sleep)
                    + ' seconds'
                )
            await asyncio.sleep(time_to_sleep)

        # create url
        url_template = etherscan_spec.get_abi_url_template(network)
        abi_endpoint = url_template.format(address=contract_address)

        # make request
        async with aiohttp.ClientSession() as session:
            async with session.get(abi_endpoint) as response:
                content = await response.text()
        _etherscan_ratelimit['last_request_time'] = time.time()

        # process request
        if content == 'Contract source code not verified':
            raise spec.AbiNotFoundException()
        abi = json.loads(content)
        if isinstance(abi, dict) and abi.get('status') == '0':
            raise Exception(
                'could not obtain contract abi from etherscan for '
                + str(contract_address)
            )

        _etherscan_ratelimit['recent_results'][contract_address] = abi

    return abi
