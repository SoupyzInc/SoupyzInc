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

        # Get BTC prices
        btc_oldest = float(k.query_public('OHLC', {'pair': 'XBTUSD', 'interval': '60'})['result']['XXBTZUSD'][0][4])
        btc_latest = float(k.query_public('OHLC', {'pair': 'XBTUSD', 'interval': '60'})['result']['XXBTZUSD'][-1][4])

        # Get LTC Prices
        ltc_oldest = float(k.query_public('OHLC', {'pair': 'XLTCZUSD', 'interval': '60'})['result']['XLTCZUSD'][0][4])
        ltc_latest = float(k.query_public('OHLC', {'pair': 'XLTCZUSD', 'interval': '60'})['result']['XLTCZUSD'][-1][4])

        # Get ETH Prices
        eth_oldest = float(k.query_public('OHLC', {'pair': 'XETHZUSD', 'interval': '60'})['result']['XETHZUSD'][0][4])
        eth_latest = float(k.query_public('OHLC', {'pair': 'XETHZUSD', 'interval': '60'})['result']['XETHZUSD'][-1][4])

        # Calculate BTC data
        btc_percent = round((btc_latest - btc_oldest) / btc_oldest, 2)

        btc_arrow = '▼'
        if btc_percent > 0:
            btc_arrow = '▲'
        
        # Build BTC string
        btc_string = 'BTC: ${0} {1} {2}%'.format(btc_latest, btc_arrow, btc_percent)

        # Calculate LTC data
        ltc_percent = round((ltc_latest - ltc_oldest) / ltc_oldest, 2)

        ltc_arrow = '▼'
        if ltc_percent > 0:
            ltc_arrow = '▲'
        
        # Build LTC string
        ltc_string = 'LTC: ${0} {1} {2}%'.format(ltc_latest, ltc_arrow, ltc_percent)

        # Calculate ETH data
        eth_percent = round((eth_latest - eth_oldest) / eth_oldest, 2)

        eth_arrow = '▼'
        if eth_percent > 0:
            eth_arrow = '▲'
        
        # Build ETH string
        eth_string = 'BTC: ${0} {1} {2}%'.format(eth_latest, eth_arrow, eth_percent)

        # Build final string
        html = '```java\n'
        html += '| {0} | {1} | {2} | As of {3} |'.format(btc_string, ltc_string, eth_string, timestamp)
        html +='\n```'

        assert(len(sys.argv) == 4)
        readmePath = sys.argv[3]

        with open(readmePath, "r") as readme:
            content = readme.read()

        newContent = re.sub(r"(?<=<!\-\-START_SECTION:crypto\-prices\-\->)[\s\S]*(?=<!\-\-END_SECTION:crypto\-prices\-\->)", f"\n{html}\n", content)

        with open(readmePath, "w") as readme:
            readme.write(newContent)
