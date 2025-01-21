import requests


class UnleashNFTApi:
    def __init__(self):
        self.url_base = 'https://api.unleashnfts.com/api/v2/nft'
        self.api_key = None

    def set_api_key_token(self, api_key: str):
        self.api_key = api_key

    def api_request(self, endpoint, method="GET", request_data=None):
        try:
            headers = {
                "x-api-key": self.api_key
            }
            response = requests.request(url=self.url_base + endpoint, method=method, headers=headers, data=request_data)
            if response.status_code == 200:
                response_object = response.json()
                # response_object['status_code'] = 200
                return response_object
            elif response.status_code == 404:
                return f'{self.url_base}{endpoint} is not found'
            else:
                return response.json()
        except Exception as err:
            print(f'Got Exception :{err}')

    def market_analytics_report(self, blockchain: str = "ethereum", time_range: str = "24h"):
        endpoint = f'/market-insights/analytics?blockchain={blockchain}&time_range={time_range}'
        return self.api_request(endpoint)

    def market_holders_insights(self, blockchain: str = "ethereum", time_range: str = "24h"):
        endpoint = f'/market-insights/holders?blockchain={blockchain}&time_range={time_range}'
        return self.api_request(endpoint)

    def market_traders_insights(self, blockchain: str = "ethereum", time_range: str = "24h"):
        endpoint = f'/market-insights/traders?blockchain={blockchain}&time_range={time_range}'
        return self.api_request(endpoint)

    def market_place_analytics(self, blockchain: str = "ethereum", sort_by: str = "name"):
        endpoint = f'/marketplace/analytics?blockchain={blockchain}&sort_by={sort_by}'
        return self.api_request(endpoint)

    def market_place_holders(self, blockchain: str = "ethereum", sort_by: str = "name"):
        endpoint = f'/marketplace/holders?blockchain={blockchain}&sort_by={sort_by}'
        return self.api_request(endpoint)

    def collection_analytics(self, blockchain: str = "ethereum", sort_by: str = "sales"):
        endpoint = f'/collection/analytics?blockchain={blockchain}&sort_by={sort_by}'
        return self.api_request(endpoint)

    def collection_holders(self, blockchain: str = "ethereum", sort_by: str = "holders"):
        endpoint = f'/collection/holders?blockchain={blockchain}&sort_by={sort_by}'
        return self.api_request(endpoint)

    def wallet_analytics(self, blockchain: str = "ethereum", sort_by: str = "volume"):
        endpoint = f'/wallet/analytics?blockchain={blockchain}&sort_by={sort_by}'
        return self.api_request(endpoint)

    def wallet_traders(self, blockchain: str = "ethereum", sort_by: str = "traders"):
        endpoint = f'/wallet/traders?blockchain={blockchain}&sort_by={sort_by}'
        return self.api_request(endpoint)

    def nft_analytics(self, blockchain: str = "ethereum", sort_by: str = "sales"):
        endpoint = f'/analytics?blockchain={blockchain}&sort_by={sort_by}'
        return self.api_request(endpoint)

    def nft_traders(self, blockchain: str = "ethereum", sort_by: str = "traders"):
        endpoint = f'/traders?blockchain={blockchain}&sort_by={sort_by}'
        return self.api_request(endpoint)

    def gaming_metrics(self, blockchain: str = "ethereum", sort_by: str = "total_users"):
        endpoint = f'/wallet/gaming/metrics?blockchain={blockchain}&sort_by={sort_by}'
        return self.api_request(endpoint)

    def gaming_collection_metrics(self, blockchain: str = "ethereum", sort_by: str = "total_users"):
        endpoint = f'/wallet/gaming/collection/metrics?blockchain={blockchain}&sort_by={sort_by}'
        return self.api_request(endpoint)

    def transactions(self, blockchain: str = "ethereum", time_range: str = "24h"):
        endpoint = f'/transactions?blockchain={blockchain}&time_range={time_range}'
        return self.api_request(endpoint)

    def brand_metadata(self, blockchain: str = "ethereum"):
        endpoint = f'/brand/metadata?blockchain={blockchain}'
        return self.api_request(endpoint)

    def brand_metrics(self, blockchain: str = "ethereum", sort_by: str = "mint_tokens"):
        endpoint = f'/brand/metrics?blockchain={blockchain}&sort_by={sort_by}'
        return self.api_request(endpoint)

    def token_price_estimate(self, blockchain: str = "ethereum", token_id: str = "7412",
                             contract_address: str = "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d"):
        endpoint = (f'/liquify/price_estimate?blockchain={blockchain}&contract_address={contract_address}'
                    f'&token_id={token_id}')
        return self.api_request(endpoint)

    def collection_price_estimate(self, blockchain: str = "ethereum",
                                  contract_address: str = "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d"):
        endpoint = f'/liquify/collection/price_estimate?blockchain={blockchain}&contract_address={contract_address}'
        return self.api_request(endpoint)

