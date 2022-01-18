import asyncio
import typing

from ctc import directory
from ctc import evm
from ctc import rpc
from ctc import spec

from . import chainlink_metadata
from . import chainlink_spec


async def async_get_feed_data(
    *,
    feed_name=None,
    feed_address=None,
    start_block=None,
    end_block=None,
    normalize=True,
    answer_only=True,
    verbose=True,
):

    # get feed address
    if feed_address is None:
        feed_address = directory.get_oracle_address(
            name=feed_name, protocol='chainlink'
        )

    # get aggregator
    aggregator_address = await rpc.async_eth_call(
        to_address=feed_address,
        function_name='aggregator',
    )

    # parse block
    if end_block is None:
        end_block = 'latest'
    if start_block == 'latest':
        start_block = await evm.get_latest_block_number()
    if end_block == 'latest':
        end_block = evm.get_latest_block_number()
    if start_block is None:

        # once have eth_call storage should always just use genesis blocks here

        # use first recorded block if any blocks exist in storage
        events_list = evm.list_events(
            contract_address=aggregator_address,
            event_name='AnswerUpdated',
        )

        if (
            events_list is not None
            and events_list.get('block_range') is not None
            and len(events_list['block_range']) > 0
        ):
            # use first recorded block
            start_block = events_list['block_range'][0]
        else:
            # use aggregator creation block
            start_block = await evm.async_get_contract_creation_block(
                contract_address=aggregator_address
            )

    # events
    feed_data = evm.get_events(
        event_name='AnswerUpdated',
        contract_address=aggregator_address,
        start_block=start_block,
        end_block=end_block,
        verbose=verbose,
    )

    if normalize:
        pass

    if answer_only:
        feed_data = feed_data['arg__current']
        feed_data = feed_data.droplevel('transaction_index')
        feed_data = feed_data.droplevel('log_index')

    return feed_data
