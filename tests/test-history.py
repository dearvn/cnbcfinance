from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from cnbcfinance.cnbc import Cnbc

if __name__ == '__main__':
    cnbc = Cnbc('AAPL')
    data = cnbc.get_history_df('5M', proxy='138.201.120.214:1080')
    print(data)



