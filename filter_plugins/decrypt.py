"""
Copyright 2020 OSSO B.V., Walter Doekes <wjdoekes+ansible@osso.nl>
"""

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleFilterError

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()
    __main__ = None
else:
    import __main__


DOCUMENTATION = '''
    filter: decrypt
    short_description: Inline decryption of $ANSIBLE_VAULT;... strings.
    description:
        Example {{ "$ANSIBLE_VAULT;..."|decrypt }}
'''


def decrypt(stdin):
    vault = _get_vault()
    if vault:
        dec = _vault.decrypt(stdin.encode('ascii')).decode('utf-8')
    else:
        raise AnsibleFilterError('cannot set up decryption')
        dec = '<<DECRYPTION_FAILED_ERROR>>'
    return dec


class FilterModule(object):
    filter_map = {'decrypt': decrypt}

    def filters(self):
        return self.filter_map


def _setup_local_vault():
    from ansible.constants import DEFAULT_VAULT_IDENTITY_LIST  # = []
    from ansible.parsing.dataloader import DataLoader
    from ansible.parsing.vault import VaultLib

    try:
        CLI = __main__.cli  # does this make sense? or just use ansible.cli?
    except ImportError:
        from ansible.cli import CLI

    # NOTE: This is (re)run for every task that calls the |decrypt filter
    display.v('info: Setting up local VaultLib')
    loader = DataLoader()
    secrets = CLI.setup_vault_secrets(loader, DEFAULT_VAULT_IDENTITY_LIST)
    vault = VaultLib(secrets=secrets)

    test_value = 'test'
    encrypted = vault.encrypt(test_value)
    assert encrypted.startswith(b'$ANSIBLE_VAULT;'), test_value
    decrypted = vault.decrypt(encrypted).decode('utf-8')
    assert decrypted == test_value, '{!r} != {!r}'.format(
        decrypted, test_value)

    return vault


def _get_vault():
    global _vault
    if not _vault:
        try:
            _vault = _setup_local_vault()
        except Exception:
            import traceback
            display.error(
                'Trying to set up decryption vault, got error:\n{}'
                .format(traceback.format_exc()))
            display.error('Inline decryption will fail!')
            return None
    return _vault


_vault = None  # caching local _vault here
