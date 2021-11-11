from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from cnbcfinance.cnbcfinance import get_history_df

if __name__ == '__main__':
    data = get_history_df('AAPL', '30m')
    print(data)



