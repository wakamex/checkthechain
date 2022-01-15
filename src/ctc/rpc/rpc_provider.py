import copy
import os

import ctc.config
from ctc import spec


def get_provider(provider: spec.ProviderSpec = None) -> spec.Provider:

    if provider is None:

        # case: return default provider
        return ctc.config.get_default_provider()

    elif isinstance(provider, str):

        # case: provider specified as url
        if provider.startswith('http'):
            return {
                'name': None,
                'network': None,
                'protocol': 'http',
                'url': provider,
                'session_kwargs': {},
                'chunk_size': None,
            }

        # case: provider specified as name in config
        elif ctc.config.has_provider(name=provider):
            return ctc.config.get_provider(name=provider)

        else:
            raise Exception('unknown provider format: ' + str(provider))

    elif isinstance(provider, dict):

        # case: partial provider
        if set(provider.keys()) != spec.provider_keys:
            default_provider = ctc.config.get_default_provider()
            default_provider = copy.copy(default_provider)
            default_provider.update(provider)

        return default_provider

    else:
        raise Exception('unknown provider type: ' + str(type(provider)))


def get_provider_key(provider: spec.Provider) -> spec.ProviderKey:
    """return a unique identifier for provider within this process"""

    session_kwargs = provider.get('session_kwargs')
    if session_kwargs is None:
        session_kwargs = {}

    return (os.getpid(), provider['url'], tuple(session_kwargs.items()))


def add_provider_parameters(
    provider: spec.ProviderSpec,
    parameters: spec.PartialProvider,
) -> spec.Provider:
    # TODO: decide whether parameters with value=None should be included
    provider = get_provider(provider)
    provider = copy.copy(provider)
    provider.update(parameters)
    return provider

