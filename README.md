# Information
This package to fetch data from cnbc
## Get History by interval
* Get data by interval and period

## Get Quote
* Get quote data realtime

## Installation


### 0. Prerequisites

Make sure you have the following software installed on your system:

* Python 3.3+


### 1. Install CNBCFinance

#### 1.1 Install `cnbcfinance`
```bash
cd cnbcfinance

# Create an isolated Python virtual environment
pip install virtualenv
virtualenv ./virtualenv --python=$(which python3)

# Activate the virtualenv
# IMPORTANT: it needs to be activated every time before you run
#            a manage.py or cointrol-* command.
. virtualenv/bin/activate

# Get the code
git clone https://github.com/dearvn/cnbcfinance

# Install Python requirements
pip install -r requirements.txt

# Initialize the database
cointrol/manage.py migrate

# Install cnbcfinance-*
pip install -e .

```
