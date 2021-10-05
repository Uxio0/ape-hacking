from binascii import Error

from brownie import Contract
from eth_account import Account
from ape_safe import ApeSafe
from os import environ


def main():
    private_keys = environ.get('PRIVATE_KEYS')  # Private keys separated by ,
    sender_key = environ.get('PRIVATE_SENDER_KEY')  # Private key
    safe_address = environ.get('SAFE_ADDRESS') or 'ychad.eth'

    try:
        owner_accounts = [Account.from_key(private_key) for private_key in private_keys.split(',')] if private_keys else []
    except (ValueError, Error):
        print('Not valid private keys on $PRIVATE_KEYS')
        raise

    try:
        sender_account = Account.from_key(sender_key) if sender_key else None
    except (ValueError, Error):
        print('Not valid private keys on $PRIVATE_KEYS')
        raise

    safe = ApeSafe(safe_address)

    dai = Contract.from_explorer('0x6B175474E89094C44Da98b954EedeAC495271d0F')
    vault = Contract.from_explorer('0x19D3364A399d251E894aC732651be8B0E4e85001')
    dai = safe.contract('0x6B175474E89094C44Da98b954EedeAC495271d0F')
    vault = safe.contract('0x19D3364A399d251E894aC732651be8B0E4e85001')

    amount = dai.balanceOf(safe.account)
    dai.approve(vault, amount - 2)
    dai.approve(vault, 2)

    safe_tx = safe.multisend_from_receipts()
    safe.preview(safe_tx)
    print('Estimated Gas', safe.estimate_gas(safe_tx))

    if owner_accounts:
        for account in owner_accounts:
            safe.sign_transaction(safe_tx, signer=account)
        safe.post_transaction(safe_tx)

        if sender_account:
            safe_tx.execute(tx_sender_private_key=sender_account.key)
