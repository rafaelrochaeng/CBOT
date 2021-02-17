import ccxt
import sys


class Exchange:
    def __init__(self, exchange, api_key, secret_key):

        self.id = exchange
        self.params = {
            'enableRateLimit': True,
        }

        self.previous_tickers = None

        self.exchange_client = getattr(ccxt, self.id)(self.params)
        # self.novadax_client = ccxt.novadax({
        #     'apiKey': api_key,
        #     'secret': secret_key
        # })

    def get_tick(self):
        try:
            self.previous_tickers = self.exchange_client.fetch_tickers()

        except ccxt.RequestTimeout as e:
            # recoverable error, do nothing and retry later
            print(type(e).__name__, str(e))

        except ccxt.DDoSProtection as e:
            # recoverable error, you might want to sleep a bit here and retry later
            print(type(e).__name__, str(e))

        except ccxt.ExchangeNotAvailable as e:
            # recoverable error, do nothing and retry later
            print(type(e).__name__, str(e))

        except ccxt.NetworkError as e:
            # do nothing and retry later...
            print(type(e).__name__, str(e))

        except Exception as e:
            # panic and halt the execution in case of any other error
            print(type(e).__name__, str(e))
            sys.exit()

        return self.previous_tickers

