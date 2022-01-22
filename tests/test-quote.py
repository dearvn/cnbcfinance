from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from cnbcfinance import Cnbc

if __name__ == '__main__':
    cnbc = Cnbc('AAPL')
    data = cnbc.get_quote(proxy='184.180.90.226:8080')
    print(data)



