# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import logging
import sys
import requests

from web3 import Web3, HTTPProvider
from pymaker.keys import register_private_key
from pymaker.gas import GeometricGasPrice
from pymaker import Contract, Address, Transact


class D3MKeeper:
    """D3MKeeper."""

    logger = logging.getLogger()

    def __init__(self, args: list, **kwargs):
        parser = argparse.ArgumentParser(prog='d3m-keeper')

        parser.add_argument("--rpc-url", type=str, required=True,
                            help="JSON-RPC host URL")

        parser.add_argument("--rpc-timeout", type=int, default=10,
                            help="JSON-RPC timeout (in seconds, default: 10)")

        parser.add_argument("--eth-from", type=str, required=True,
                            help="Ethereum account from which to send transactions")

        parser.add_argument("--eth-private-key", type=str, required=True,
                            help="Ethereum private key(s) to use")

        parser.add_argument("--d3m-address", type=str,
                            default="0xa13C0c8eB109F5A13c6c90FC26AFb23bEB3Fb04a",
                            help="Address of D3M contract")

        parser.add_argument("--helper-address", type=str,
                            default="0xf06386F557Be828EE71bfaEA5BDadeB70EF57D69",
                            help="Address of helper contract")

        parser.add_argument('--blocknative-api-key', type=str, required=True,
                            help="Blocknative key")

        self.arguments = parser.parse_args(args)

        self.web3 = kwargs['web3'] if 'web3' in kwargs else Web3(HTTPProvider(endpoint_uri=self.arguments.rpc_url,
                                                                              request_kwargs={"timeout": self.arguments.rpc_timeout}))
        self.web3.eth.defaultAccount = self.arguments.eth_from
        register_private_key(self.web3, self.arguments.eth_private_key)

        self.gas_strategy = GeometricGasPrice(
            web3=self.web3,
            initial_price=None,
            initial_tip=self.get_initial_tip(self.arguments),
            every_secs=180
        )
        self.helper = Helper(self.web3, Address(self.arguments.helper_address))
        self.d3m = D3M(self.web3, Address(self.arguments.d3m_address))

    def main(self):

        # check if ready to exec
        shouldExec = self.helper.shouldExec(self.d3m.address)

        if shouldExec:
            try:
                receipt = self.d3m.exec().transact(gas_strategy=self.gas_strategy)
                if receipt is not None and receipt.successful:
                    logging.info("Exec on D3M done!")
                else:
                    logging.error("Failed to run exec on D3M!")

            except Exception as e:
                logging.error(str(e))
                logging.error("Failed to run exec on D3M!")
        else:
            logging.info("Not ready to exec yet")

    @staticmethod
    def get_initial_tip(arguments) -> int:
        try:
            result = requests.get(
                url='https://api.blocknative.com/gasprices/blockprices',
                headers={
                    'Authorization': arguments.blocknative_api_key
                },
                timeout=15
            )

            if result.ok and result.content:
                confidence_80_tip = result.json().get('blockPrices')[0]['estimatedPrices'][3]['maxPriorityFeePerGas']
                logging.info(f"Using Blocknative 80% confidence tip {confidence_80_tip}")
                return int(confidence_80_tip * GeometricGasPrice.GWEI)
        except Exception as e:
            logging.error(str(e))

        return int(1.5 * GeometricGasPrice.GWEI)


class Helper(Contract):
    """A client for the `Helper` contract.

    Attributes:
        web3: An instance of `Web` from `web3.py`.
        address: Ethereum address of the `Helper` contract.
    """

    abi = Contract._load_abi(__name__, 'abi/Helper.abi')

    def __init__(self, web3: Web3, address: Address):
        assert (isinstance(web3, Web3))
        assert (isinstance(address, Address))

        self.web3 = web3
        self.address = address
        self._contract = self._get_contract(web3, self.abi, address)

    def shouldExec(self, _direct: Address) -> bool:
        return self._contract.functions.shouldExec(_direct.address, 5000000000000000000000000).call()

    def __repr__(self):
        return f"Helper('{self.address}')"


class D3M(Contract):
    """A client for the `D3M` contract.

    Attributes:
        web3: An instance of `Web` from `web3.py`.
        address: Ethereum address of the `D3M` contract.
    """

    abi = Contract._load_abi(__name__, 'abi/D3M.abi')

    def __init__(self, web3: Web3, address: Address):
        assert (isinstance(web3, Web3))
        assert (isinstance(address, Address))

        self.web3 = web3
        self.address = address
        self._contract = self._get_contract(web3, self.abi, address)

    def exec(self) -> Transact:
        return Transact(self, self.web3, self.abi, self.address, self._contract, 'exec()', [])

    def __repr__(self):
        return f"D3M('{self.address}')"


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)-15s %(levelname)-8s %(message)s', level=logging.INFO)
    D3MKeeper(sys.argv[1:]).main()
