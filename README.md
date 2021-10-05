# Instructions

A [github actions workflow](https://github.com/features/actions) is included and can be trigered to execute brownie tasks.

The [workflow file](.github/workflows/python.yml) can be changed to choose what to execute (look
at the example `brownie run ape_invest --network mainnet-fork` line).

`Infura project id`, `etherscan token`, `sender private key` and `owners private keys` will be read from environment using
[Github actions secret storage](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository).
Expected format for `PRIVATE_KEYS` is multiple private keys with no spaces separated by commas `,`

As anyone can sent a signed Safe multisig transaction, a `PRIVATE_SENDER_KEY` must be provided. It could
be one of the owners.
