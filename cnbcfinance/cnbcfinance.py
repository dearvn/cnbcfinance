import requests, pytz, logging
from urllib.parse import urlparse, urlencode, parse_qsl
from datetime import datetime, timedelta
import pandas as pd

log = logging.getLogger(__name__)

def get_history_df(symbol, interval = '1M', from_date = None, end_date = None, tz = 'America/New_York'):
    datas = get_history(symbol, interval, from_date, end_date, tz)

    return pd.DataFrame.from_records(datas, index=['datetime'])

def get_history(symbol, interval = '1M', from_date = None, end_date = None, tz = 'America/New_York'):
    '''
    Get history data by interval
    :param symbol:
    :param interval: 1m, 5m, 10m, 30m, 1h, 1d, 1w
    :param from_date: is set when interval = None, format: YmdHis
    :param end_date: is set when interval = None, format: YmdHis
    :return:
    '''
    if interval != None:
        interval = interval.upper()
        date_from = datetime.now(pytz.timezone(tz)) - timedelta(days=180)
        from_date = date_from.strftime('%Y%m%d') + '000000'
        date_to = datetime.now(pytz.timezone(tz))
        end_date = date_to.strftime('%Y%m%d') + '000000'

    url = 'http://ts-api.cnbc.com/harmony/app/bars/' + symbol + '/' + interval + '/' + from_date + '/' + end_date + '/adjusted/EST5EDT.json'
    r = requests.get(url)
    resp = r.json()
    if not resp or not resp['barData'] or not resp['barData']['priceBars']:
        return
    if len(resp['barData']['priceBars']) == 0:
        return
    datas = []
    for item in resp['barData']['priceBars']:
        s = {"close": float(item['close']), "open": float(item['open']), "high": float(item['high']),
             "low": float(item['low']), "volume": int(item['volume']) if item['volume'] != None else 0,
             "datetime": int(item['tradeTimeinMills'])}
        datas.append(s)

    return datas

def get_quota(symbol, options = None):
    '''
    Get quote
    :param symbol:
    :param options: 'requestMethod': 'quick', 'exthrs': 1, 'noform': 1, 'fund': 1, 'output': 'json', 'events': 1
    :return:
    '''
    try:
        uri = 'https://quote.cnbc.com/quote-html-webservice/quote.htm?'
        parsed = urlparse(uri)
        params = {'symbols': symbol}
        default_option = {'requestMethod': 'quick', 'exthrs': 1, 'noform': 1, 'fund': 1, 'output': 'json', 'events': 1}
        new_params = options if options != None else default_option
        url = uri+urlencode({**params, **new_params})
        r = requests.get(url)
        resp = r.json()

        if resp['QuickQuoteResult'] == None or resp['QuickQuoteResult']['QuickQuote'] == None:
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
                data['yrhipct'] = (data['price']/data['yrhiprice']) * 100

        return data

    except AssertionError as e:
        log.exception(e)
    except Exception as e:
        log.exception(e)