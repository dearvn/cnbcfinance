from __future__ import print_function

import requests,pytz,random
from urllib.parse import urlparse, urlencode
from datetime import datetime, timedelta
import pandas as pd

_API_URL_ = 'http://ts-api.cnbc.com'
_QUOTE_URL_ = 'https://quote.cnbc.com'
user_agent_list = [
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko)',
'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240',
'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063',
'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0',
'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
'Mozilla/5.0 (Windows NT 6.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7',
'Mozilla/5.0 (iPad; CPU OS 9_3_2 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13F69 Safari/601.1',
]
class Cnbc():
    def __init__(self, ticker, session=None):
        self.ticker = ticker.upper()
        self._quote_url = _QUOTE_URL_
        self._api_url = _API_URL_

    def get_history_df(self, interval='1M', from_date=None, end_date=None, proxy=None, tz='America/New_York'):
        datas = self.get_history(interval, from_date, end_date, proxy, tz)
        if datas == None:
            return None
        return pd.DataFrame.from_records(datas, index=['datetime'])

    def get_history(self, interval='1M', from_date=None, end_date=None, proxy=None, tz='America/New_York'):
        '''
        Get history data by interval
        :param interval: 1m, 5m, 10m, 30m, 1h, 1d, 1w
        :param from_date: is set when interval = None, format: YmdHis
        :param end_date: is set when interval = None, format: YmdHis
        :param proxy: is dict or string ex: {'https': 'https://103.17.213.100:8084'} or '103.17.213.100:8080'
        :param tz
        :return:
        '''
        if interval is None:
            return None

        if from_date is None:
            date_from = datetime.now(pytz.timezone(tz)) - timedelta(days=180)
            from_date = date_from.strftime('%Y%m%d') + '000000'

        if end_date is None:
            date_to = datetime.now(pytz.timezone(tz))
            end_date = date_to.strftime('%Y%m%d') + '000000'

        url = "{}/harmony/app/bars/{}/{}/{}/{}/adjusted/EST5EDT.json".format(
            self._api_url, self.ticker, interval.upper(), from_date, end_date)

        if proxy is not None and not isinstance(proxy, dict):
            proxy = {"https": proxy, "http": proxy}

        datas = []
        try:
            resp = requests.get(
                url=url,
                proxies=proxy,
                headers={'User-Agent': random.choice(user_agent_list)}
            ).json()
            if not resp or not resp['barData'] or not resp['barData']['priceBars']:
                return
            if len(resp['barData']['priceBars']) == 0:
                return
            for item in resp['barData']['priceBars']:
                s = {"close": float(item['close']), "open": float(item['open']), "high": float(item['high']),
                     "low": float(item['low']), "volume": int(item['volume']) if item['volume'] != None else 0,
                     "datetime": int(item['tradeTimeinMills'])}
                datas.append(s)
            return datas
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

    def get_quote(self, options=None, proxy=None):
        '''
        Get quote
        :param symbol:
        :param options: 'requestMethod': 'quick', 'exthrs': 1, 'noform': 1, 'fund': 1, 'output': 'json', 'events': 1
        :return:
        '''
        uri = "{}/quote-html-webservice/quote.htm?".format(self._quote_url)
        parsed = urlparse(uri)
        params = {'symbols': self.ticker}
        default_option = {'requestMethod': 'quick', 'exthrs': 1, 'noform': 1, 'fund': 1, 'output': 'json',
                          'events': 1}
        new_params = options if options != None else default_option
        url = uri + urlencode({**params, **new_params})

        if proxy is not None and not isinstance(proxy, dict):
            proxy = {"https": proxy, "http": proxy}

        try:
            resp = requests.get(
                url=url,
                proxies=proxy,
                headers={'User-Agent': random.choice(user_agent_list)}
            ).json()

            if resp['QuickQuoteResult'] is None or resp['QuickQuoteResult']['QuickQuote'] is None:
                return None
            data = resp['QuickQuoteResult']['QuickQuote']

            if "curmktstatus" in data and data['curmktstatus'] == 'REG_MKT':
                if 'last_time_msec' in data:
                    data['time'] = int(data['last_time_msec'])
                if 'change' in data:
                    data['change'] = float(data['change'])
                if 'change_pct' in data:
                    data['pct'] = float(data['change_pct'])
                if 'last' in data:
                    data['price'] = float(data['last'])
                if 'volume' in data:
                    data['volume'] = int(data['volume'])
            elif "ExtendedMktQuote" in data:
                if 'last_time_msec' in data['ExtendedMktQuote']:
                    data['time'] = int(data['ExtendedMktQuote']['last_time_msec'])
                if 'change' in data['ExtendedMktQuote']:
                    data['change'] = float(data['ExtendedMktQuote']['change'])
                if 'change_pct' in data['ExtendedMktQuote']:
                    data['pct'] = float(data['ExtendedMktQuote']['change_pct'])
                if 'last' in data['ExtendedMktQuote']:
                    data['price'] = float(data['ExtendedMktQuote']['last'])
                if 'volume' in data['ExtendedMktQuote']:
                    data['volume'] = int(data['ExtendedMktQuote']['volume'])
            if "FundamentalData" in data:
                mktcapView = data['FundamentalData']['mktcapView']
                if 'M' in mktcapView:
                    mktcapView = float(mktcapView.replace('M', '')) * 1000000
                elif 'B' in mktcapView:
                    mktcapView = float(mktcapView.replace('B', '')) * 1000000000
                data['mktcap'] = mktcapView

                data['yrhiprice'] = float(data['FundamentalData']['yrhiprice'])
                data['yrloprice'] = float(data['FundamentalData']['yrloprice'])
                if 'price' in data:
                    data['yrhipct'] = (data['price'] / data['yrhiprice']) * 100

            return data
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)