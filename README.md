# Information
This package to fetch data from cnbc
## Installation
```bash
pip install cnbcfinance

```
## Get History by interval
* Get data by interval and period
```bash
from cnbcfinance import Cnbc

cnbc = Cnbc('AAPL')
df = cnbc.get_history_df('5M', proxy='138.201.120.214:1080')
```
## Get Quote
* Get quote data realtime
```bash
from cnbcfinance import Cnbc

cnbc = Cnbc('AAPL')
quote = cnbc.get_quote(proxy='184.180.90.226:8080')
```
