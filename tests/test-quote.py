from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from src.cnbcfinance import get_quota

if __name__ == '__main__':
    data = get_quota('AAPL')
    print(data)



