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

from d3m_keeper.main import D3MKeeper, Helper
from unittest.mock import MagicMock, patch
from web3 import Web3


def test_no_execution():
    helper = MagicMock()
    helper.shouldExec = MagicMock(return_value=False)

    d3m = MagicMock()

    def __init__(self, args: list, **kwargs):
        self.web3 = Web3()
        self.helper = helper
        self.d3m = d3m

    with patch.object(D3MKeeper, "__init__", __init__):
        keeper = D3MKeeper([]).main()
        d3m.exec.assert_not_called()


def test_execution():
    helper = MagicMock()
    helper.shouldExec = MagicMock(return_value=True)
    d3m = MagicMock()
    transact = MagicMock()
    d3m.exec = MagicMock(return_value=transact)
    gas_strategy = MagicMock()

    def __init__(self, args: list, **kwargs):
        self.web3 = Web3()
        self.helper = helper
        self.d3m = d3m
        self.gas_strategy = gas_strategy

    with patch.object(D3MKeeper, "__init__", __init__):
        keeper = D3MKeeper([]).main()
        d3m.exec.assert_called_once()
        transact.transact.assert_called_once_with(gas_strategy=gas_strategy)

