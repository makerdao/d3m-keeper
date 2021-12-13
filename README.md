# d3m-keeper
![Build Status](https://github.com/makerdao/d3m-keeper/actions/workflows/.github/workflows/aws-prod.yaml/badge.svg?branch=main)

This repository contains a Keeper to periodically call exec on d3m contract

## Installation

This project uses *Python 3.6.6* and requires *virtualenv* to be installed.

In order to clone the project and install required third-party packages please execute:
```
git clone https://github.com/makerdao/d3m-keeper.git
cd d3m-keeper
git submodule update --init --recursive
./install.sh
```

Can be also installed as a Docker image (makerdao/d3m-keeper)

## Running

```
usage: d3m-keeper [-h] --rpc-url RPC_URL [--rpc-timeout RPC_TIMEOUT]
                   --eth-from ETH_FROM --eth-private-key ETH_PRIVATE_KEY
                   [--d3m-address D3M_ADDRESS]
                   [--helper-address HELPER_ADDRESS]
                   [--blocknative-key BLOCKNATIVE_KEY]

optional arguments:
  -h, --help            show this help message and exit
  --rpc-url RPC_URL     JSON-RPC host URL
  --rpc-timeout RPC_TIMEOUT
                        JSON-RPC timeout (in seconds, default: 10)
  --eth-from ETH_FROM   Ethereum account from which to send transactions
  --eth-private-key ETH_PRIVATE_KEY
                        Ethereum private key(s) to use
  --d3m-address D3M_ADDRESS
                        Address of d3m contract (defaults to 0xa13c0c8eb109f5a13c6c90fc26afb23beb3fb04a)
  --helper-address HELPER_ADDRESS
                        Address of helper contract (defaults to 0xf06386f557be828ee71bfaea5bdadeb70ef57d69)
  --blocknative-key BLOCKNATIVE_KEY
                        Blocknative API key to use
```

## Sample startup script

```
#!/bin/bash

bin/d3m-keeper \
    --rpc-url https://localhost:8545/ \
    --eth-from 0x..... \
    --eth-private-key 8110..... \
    --d3m-address 0xa13C0c8eB109F5A13c6c90FC26AFb23bEB3Fb04a \
    --helper-address 0xf06386F557Be828EE71bfaEA5BDadeB70EF57D69 \
    --blocknative-key MY_API_KEY
```


