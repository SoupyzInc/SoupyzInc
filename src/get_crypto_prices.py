"""
    Copyright 2021 Matthew Okashita <https://github.com/soupyzinc>

    Licensed under the Apache License, Version 2.0 (the "License"); you may not
    use this file except in compliance with the License. You may obtain a copy of
    the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
    License for the specific language governing permissions and limitations under
    the License.
"""

import requests
import sys
import re
import krakenex

if __name__ == "__main__":
    k = krakenex.API()

    # Assert that the Kraken REST API is functional before pulling data.
    if k.query_public('SystemStatus')['result']['status'] == "online":
        # Get timestamp
        timestamp = k.query_public('Time')['result']['rfc1123']

        # Get data first
        btc_data = k.query_public('OHLC', {'pair': 'XBTUSD', 'interval': '60'})['result']['XXBTZUSD']
        ltc_data = k.query_public('OHLC', {'pair': 'XLTCZUSD', 'interval': '60'})['result']['XLTCZUSD']

        # Get BTC prices
        btc_oldest = float(btc_data[0][4])
        btc_latest = float(btc_data[-1][4])

        # Calculate BTC data
        btc_percent = round((btc_latest - btc_oldest) / btc_oldest, 2)

        # Build BTC string
        btc_arrow = '▼'
        if btc_percent > 0:
            btc_arrow = '▲'
            
        btc_string = 'BTC: ${0} {1} {2}%'.format(btc_latest, btc_arrow, btc_percent)

        # Get LTC Prices
        ltc_oldest = float(ltc_data[0][4])
        ltc_latest = float(ltc_data[-1][4])
        
        # Calculate LTC data
        ltc_percent = round((ltc_latest - ltc_oldest) / ltc_oldest, 2)

        # Build LTC string
        ltc_arrow = '▼'
        if ltc_percent > 0:
            ltc_arrow = '▲'
        
        ltc_string = 'LTC: ${0} {1} {2}%'.format(ltc_latest, ltc_arrow, ltc_percent)

        # Build final string
        html = '```java\n'
        html += '| {0} | {1} | As of {2}, from Kraken.'.format(btc_string, ltc_string, timestamp)
        html +='\n```'

        assert(len(sys.argv) == 4)
        readmePath = sys.argv[3]

        with open(readmePath, "r") as readme:
            content = readme.read()

        newContent = re.sub(r"(?<=<!\-\-START_SECTION:crypto\-prices\-\->)[\s\S]*(?=<!\-\-END_SECTION:crypto\-prices\-\->)", f"\n{html}\n", content)

        with open(readmePath, "w") as readme:
            readme.write(newContent)
            
