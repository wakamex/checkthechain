from __future__ import annotations

from ctc import spec

from .. import rpc_constructors
from .. import rpc_digestors
from .. import rpc_request


def sync_eth_block_number(
    *,
    context: spec.Context = None,
    decode_response: bool = True,
    raw_output: bool = False,
) -> spec.RpcSingularResponse:
    request = rpc_constructors.construct_eth_block_number()
    response = rpc_request.sync_send(
        request,
        context=context,
        raw_output=raw_output,
    )

    if raw_output:
        return response
    else:
        return rpc_digestors.digest_eth_block_number(
            response=response,
            decode_response=decode_response,
        )


def sync_eth_get_block_by_hash(
    block_hash: str,
    *,
    include_full_transactions: bool = False,
    context: spec.Context = None,
    decode_response: bool = True,
    snake_case_response: bool = True,
) -> spec.RpcSingularResponse:
    request = rpc_constructors.construct_eth_get_block_by_hash(
        block_hash=block_hash,
        include_full_transactions=include_full_transactions,
    )
    response = rpc_request.sync_send(request, context=context)
    return rpc_digestors.digest_eth_get_block_by_hash(
        response=response,
        decode_response=decode_response,
        snake_case_response=snake_case_response,
    )


def sync_eth_get_block_by_number(
    block_number: spec.StandardBlockNumber,
    *,
    include_full_transactions: bool = False,
    decode_response: bool = True,
    context: spec.Context = None,
    snake_case_response: bool = True,
    raw_output: bool = False,
) -> spec.RpcSingularResponse:
    request = rpc_constructors.construct_eth_get_block_by_number(
        block_number=block_number,
        include_full_transactions=include_full_transactions,
    )
    response = rpc_request.sync_send(
        request,
        context=context,
        raw_output=raw_output,
    )

    if raw_output:
        return response
    else:
        return rpc_digestors.digest_eth_get_block_by_number(
            response=response,
            decode_response=decode_response,
            snake_case_response=snake_case_response,
        )


def sync_eth_get_uncle_count_by_block_hash(
    block_hash: str,
    *,
    context: spec.Context = None,
    decode_response: bool = True,
) -> spec.RpcSingularResponse:
    request = rpc_constructors.construct_eth_get_uncle_count_by_block_hash(
        block_hash=block_hash,
    )
    response = rpc_request.sync_send(request, context=context)
    return rpc_digestors.digest_eth_get_uncle_count_by_block_hash(
        response=response,
        decode_response=decode_response,
    )


def sync_eth_get_uncle_count_by_block_number(
    block_number: spec.StandardBlockNumber,
    *,
    context: spec.Context = None,
    decode_response: bool = True,
) -> spec.RpcSingularResponse:
    request = rpc_constructors.construct_eth_get_uncle_count_by_block_number(
        block_number=block_number,
    )
    response = rpc_request.sync_send(request, context=context)
    return rpc_digestors.digest_eth_get_uncle_count_by_block_number(
        response=response,
        decode_response=decode_response,
    )


def sync_eth_get_uncle_by_block_hash_and_index(
    block_hash: str,
    uncle_index: str,
    *,
    context: spec.Context = None,
    decode_response: bool = True,
    snake_case_response: bool = True,
) -> spec.RpcSingularResponse:
    request = rpc_constructors.construct_eth_get_uncle_by_block_hash_and_index(
        block_hash=block_hash,
        uncle_index=uncle_index,
    )
    response = rpc_request.sync_send(request, context=context)
    return rpc_digestors.digest_eth_get_uncle_by_block_hash_and_index(
        response=response,
        decode_response=decode_response,
        snake_case_response=snake_case_response,
    )


def sync_eth_get_uncle_by_block_number_and_index(
    block_number: spec.StandardBlockNumber,
    uncle_index: str,
    *,
    context: spec.Context = None,
    decode_response: bool = True,
    snake_case_response: bool = True,
) -> spec.RpcSingularResponse:
    request = (
        rpc_constructors.construct_eth_get_uncle_by_block_number_and_index(
            block_number=block_number,
            uncle_index=uncle_index,
        )
    )
    response = rpc_request.sync_send(request, context=context)
    return rpc_digestors.digest_eth_get_uncle_by_block_number_and_index(
        response=response,
        decode_response=decode_response,
        snake_case_response=snake_case_response,
    )

