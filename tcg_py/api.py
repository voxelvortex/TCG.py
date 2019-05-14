import requests
import json


class Handler(object):

    def __init__(self, **kwargs):
        self.version = "v1.27.0"
        if "version" in kwargs:
            self.version = kwargs["version"]
        if "bearer" in kwargs:
            self.bearer = kwargs["bearer"]
        elif "public" in kwargs and "private" in kwargs:
            self.__get_login_data(kwargs["public"], kwargs["private"])

            if "error" in self.login_data:
                # replace with custom exception later? :thinking:
                raise ValueError(self.login_data["error"]
                                 + ", description: "
                                 + self.login_data["error_description"])
            else:
                self.bearer = self.login_data["access_token"]
        else:
            raise ValueError("Test requires a bearer or both public"
                             " and private arguments. You provided: "
                             + ", ".join(kwargs.keys()))

    def __get_login_data(self, public, private):
        token_url = "https://api.tcgplayer.com/token"
        data = "grant_type=client_credentials&client_id={0}&client_secret={1}"
        data = data.format(public, private)
        response = requests.request("POST", token_url, data=data)
        self.login_data = json.loads(response.text)

    def __check_bearer(self):
        headers = {
            "Accept": "application/json",
            "Authorization": "bearer {0}".format(self.bearer)
        }
        url = "http://api.tcgplayer.com/{0}/catalog/categories".format(self.version)
        response = requests.request("GET", url, headers=headers)
        data = json.loads(response.text)
        return data["success"]

    def __request(self, url, method="GET", **kwargs):
        params, data = {}, {}
        if "params" in kwargs:
            params = kwargs["params"]
        if "data" in kwargs:
            data = kwargs["data"]
        headers = {
            "Accept": "application/json",
            "Authorization": "bearer {0}".format(self.bearer)
        }
        # call request method according to what data is passed to the method

        if not params and not data:
            response = requests.request(method, url, headers=headers)
        elif not params:
            response = requests.request(method, url, headers=headers, data=data)
        elif not data:
            response = requests.request(method, url, headers=headers, params=params)
        else:
            response = requests.request(method, url, headers=headers, params=params, data=data)

        data = json.loads(response.text)
        return data

    def __to_camel_case(self, str):
        components = str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])

    def __get_params(self, **kwargs):
        params = {}
        for item in kwargs:
            params[self.__to_camel_case(item)] = kwargs[item]
        return params

    def __convert_list_to_str(self, item):
        return str(item).replace("[", "").replace("]", "")

    ''' CATALOG CATALOG CATALOG CATALOG CATALOG CATALOG'''

    def list_categories(self, **kwargs):
        params = {}
        if "offset" in kwargs:
            params["offset"] = kwargs["offset"]
        if "limit" in kwargs:
            params["limit"] = kwargs["limit"]
        if "sort_order" in kwargs:
            params["sortOrder"] = kwargs["sort_order"]
        if "sort_desc" in kwargs:
            params["sortDesc"] = kwargs["sort_desc"]

        url = "http://api.tcgplayer.com/{0}/catalog/categories".format(self.version)
        return self.__request(url, params=params)

    def get_category_details(self, category_id):
        url = "http://api.tcgplayer.com/{0}/catalog/categories/{1}".format(self.version, category_id)
        return self.__request(url)

    def get_category_search_manifest(self, category_id):
        url = "http://api.tcgplayer.com/{0}/catalog/categories/{1}".format(self.version, category_id)
        headers = {
            "Accept": "application/json",
            "Authorization": "bearer {0}".format(self.bearer)
        }
        return self.__request(url, headers)

    def search_category_products(self, category_id, **kwargs):
        url = "http://api.tcgplayer.com/{0}/catalog/categories/{1}/search".format(self.version, category_id)
        data = self.__get_params(**kwargs)

        return self.__request(url, data=data, method="POST")

    def list_all_category_groups(self, category_id, **kwargs):
        url = "http://api.tcgplayer.com/{0}/catalog/categories/{1}/groups".format(self.version, category_id)
        params = self.__get_params(**kwargs)

        return self.__request(url, params=params)

    def list_all_category_rarities(self, category_id):
        url = "http://api.tcgplayer.com/{0}/catalog/categories/{1}/rarities".format(self.version, category_id)
        return self.__request(url)

    def list_all_category_printings(self, category_id):
        url = "http://api.tcgplayer.com/{0}/catalog/categories/{1}/printings".format(self.version, category_id)
        return self.__request(url)

    def list_all_category_conditions(self, category_id):
        url = "http://api.tcgplayer.com/{0}/catalog/categories/{1}/conditions".format(self.version, category_id)
        return self.__request(url)

    def list_all_category_languages(self, category_id):
        url = "http://api.tcgplayer.com/{0}/catalog/categories/{1}/languages".format(self.version, category_id)
        return self.__request(url)

    def list_all_category_media(self, category_id):
        url = "http://api.tcgplayer.com/{0}/catalog/categories/{1}/media".format(self.version, category_id)
        return self.__request(url)

    def list_all_group_details(self, **kwargs):
        url = "http://api.tcgplayer.com/{0}/catalog/groups".format(self.version)
        params = self.__get_params(**kwargs)

        return self.__request(url, params=params)

    def get_group_details(self, group_id):
        group_id = self.__convert_list_to_str(group_id)
        url = "http://api.tcgplayer.com/{0}/catalog/groups/{1}".format(self.version, group_id)
        return self.__request(url)

    def list_all_group_media(self, group_id):
        url = "http://api.tcgplayer.com/{0}/catalog/groups/{1}/media".format(self.version, group_id)
        return self.__request(url)

    def list_all_products(self, **kwargs):
        url = "http://api.tcgplayer.com/{0}/catalog/products".format(self.version)
        params = self.__get_params(**kwargs)

        return self.__request(url, params=params)

    def get_product_details(self, product_ids, **kwargs):
        product_ids = self.__convert_list_to_str(product_ids)
        url = "http://api.tcgplayer.com/{0}/catalog/products/{1}".format(self.version, product_ids)
        params = self.__get_params(**kwargs)

        return self.__request(url, params=params)

    def get_product_details_by_gtin(self, gtin, **kwargs):
        url = "http://api.tcgplayer.com/{0}/catalog/products/gtin/{0}".format(self.version, gtin)
        params = self.__get_params(**kwargs)

        return self.__request(url, params=params)

    def list_product_skus(self, product_id):
        url = "http://api.tcgplayer.com/{0}/catalog/products/{1}/skus".format(self.version, product_id)
        return self.__request(url)

    def list_related_products(self, product_id, **kwargs):
        url = "http://api.tcgplayer.com/{0}/catalog/products/{1}/productsalsopurchased".format(self.version, product_id)
        params = self.__get_params(**kwargs)

        return self.__request(url, params=params)

    def list_all_product_media_types(self, product_id):
        url = "http://api.tcgplayer.com{0}/catalog/products/{1}/media".format(self.version, product_id)
        return self.__request(url)

    def get_sku_details(self, sku_id):
        url = "http://api.tcgplayer.com/{0}/catalog/skus/{1}".format(self.version, sku_id)
        return self.__request(url)

    def list_conditions(self):
        url = "http://api.tcgplayer.com/{0}/catalog/conditions".format(self.version)
        return self.__request(url)

    ''' INVENTORY INVENTORY INVENTORY INVENTORY INVENTORY'''

    def get_product_list_by_id(self, product_list_id):
        url = "http://api.tcgplayer.com/{0}/inventory/productlists/{1}".format(self.version, product_list_id)
        return self.__request(url)

    def get_product_list_by_key(self, product_list_key):
        url = "http://api.tcgplayer.com/{0}/inventory/productlists/{1}".format(self.version, product_list_key)
        return self.__request(url)

    def list_all_product_lists(self):
        url = "http://api.tcgplayer.com/{0}/inventory/productLists".format(self.version)
        return self.__request(url)

    ''' PRICING PRICING PRICING PRICING PRICING'''

    def get_market_price_by_sku(self, product_condition_id):
        url = "http://api.tcgplayer.com/{1}/pricing/marketprices/{1}".format(self.version, product_condition_id)
        return self.__request(url)

    def list_product_prices_by_group(self, group_id):
        url = "http://api.tcgplayer.com/{0}/pricing/group/{1}".format(self.version, group_id)
        return self.__request(url)

    def list_product_market_prices(self, product_ids):
        product_ids = self.__convert_list_to_str(product_ids)
        url = "http://api.tcgplayer.com/{0}/pricing/product/{1}".format(self.version, product_ids)
        return self.__request(url)

    def list_sku_market_prices(self,sku_ids):
        sku_ids = self.__convert_list_to_str(sku_ids)
        url = "http://api.tcgplayer.com/{0}/pricing/sku/{1}".format(self.version, sku_ids)
        return self.__request(url)

    def list_product_buylist_prices(self, product_ids):
        product_ids = self.__convert_list_to_str(product_ids)
        url = "http://api.tcgplayer.com/{0}/pricing/buy/product/{1}".format(self.version, product_ids)
        return self.__request(url)

    def list_sku_buylist_prices(self, sku_ids):
        sku_ids = self.__convert_list_to_str(sku_ids)
        url = "http://api.tcgplayer.com/{0}/pricing/buy/sku/{1}".format(self.version, sku_ids)
        return self.__request(url)

    ''' Stores Stores Stores Stores Stores Stores Stores'''

    def batch_update_store_buylist_prices(self, store_key):
        url = "http://api.tcgplayer.com/{0}/stores/{1}/buylist/skus/batch".format(self.version, store_key)
        return self.__request(url, method="POST")

    def create_sku_buylist(self, store_key, sku_id, **kwargs):
        url = "http://api.tcgplayer.com/{0}/stores/{1}/buylist/skus/{2}".format(self.version, store_key, sku_id)
        data = self.__get_params(**kwargs)

        return self.__request(url, data=data, method="PUT")

    def update_sku_buylist_price(self, store_key, sku_id, **kwargs):
        url = "http://api.tcgplayer.com/{0}/stores/{1}/buylist/skus/{2}/price".format(self.version, store_key, sku_id)

        data = {}
        if "sku_id" in kwargs:
            data["skuId"] = kwargs["sku_id"]
        if "price" in kwargs:
            data["price"] = data["price"]

        return self.__request(url, data=data, method="PUT")

    def update_sku_buylist_quantity(self, store_key, sku_id):
        url = "http://api.tcgplayer.com/{0}/stores/{1}/buylist/skus/{2}/quantity".format(self.version, store_key,
                                                                                         sku_id)
        return self.__request(url, method="PUT")

    def get_buylist_categories(self, store_key):
        url = "http://api.tcgplayer.com/{0}/stores/{1}/buylist/categories".format(self.version, store_key)
        return self.__request(url)

    def get_buylist_groups(self, store_key):
        url = "http://api.tcgplayer.com/{0}/stores/{1}/buylist/groups".format(self.version, store_key)
        return  self.__request(url)

    def get_store_buylist_settings(self, store_key):
        url = "http://api.tcgplayer.com/{0}/stores/{1}/buylist/settings".format(self.version, store_key)
        return self.__request(url)

    def search_stores(self, **kwargs):
        url = "http://api.tcgplayer.com/{0}/stores".format(self.version)
        params = self.__get_params(**kwargs)

        return self.__request(url, params=params)

    def get_free_shipping_option(self, store_key, **kwargs):
        url = "http://api.tcgplayer.com/{0}/stores/{1}/freeshipping/settings".format(self.version, store_key)
        params = self.__get_params(**kwargs)

        return self.__request(url, params=params)

    def get_store_address(self, store_key):
        url = "http://api.tcgplayer.com/{0}/stores/{1}/address".format(self.version, store_key)
        return self.__request(url)

    def get_store_feedback(self, store_key):
        url = "http://api.tcgplayer.com/{0}/stores/{1}/feedback".format(self.version, store_key)
        return self.__request(url)

    def set_store_status(self, store_key, status):
        url = "http://api.tcgplayer.com/{0}/stores/{1}/status/{2}".format(self.version, store_key, status)
        return self.__request(url, method="POST")

    def get_customer_summary(self, store_key, token):
        url = "http://api.tcgplayer.com/{0}/stores/{1}/customers/{2}".format(self.version, store_key, token)
        return self.__request(url)

    def search_store_customers(self, store_key, **kwargs):
        url = "http://api.tcgplayer.com/{0}/stores/{1}/customers".format(self.version, store_key)
        params = self.__get_params(**kwargs)

        return self.__request(url, params=params)

    def get_customer_addresses(self, store_key, token, **kwargs):
        url = "http://api.tcgplayer.com/{0}/stores/{1}/customers/{2}/addresses".format(self.version, store_key, token)
        params = self.__get_params(**kwargs)

        return self.__request(url, params=params)

    def get_customer_addresses(self, store_key, token, **kwargs):
        url = "http://api.tcgplayer.com/{0}/stores/{1}/customers/{2}/orders".format(self.version, store_key, token)
        params = self.__get_params(**kwargs)

        return self.__request(url, params=params)

    def get_store_info(self):
        url = "http://api.tcgplayer.com/{0}/stores/self".format(self.version)

        return self.__request(url)

    def get_product_inventory_quantities(self, store_key, product_id, **kwargs):
        url = "http://api.tcgplayer.com/{0}/stores/{1}/inventory/products/{2}/quantity".format(
            self.version, store_key, product_id)
        params = self.__get_params(**kwargs)

        return self.__request(url, params=params)

    def list_product_summary(self, store_key, product_id, **kwargs):
        url = "http://api.tcgplayer.com/{0}/stores/{1}/inventory/products/{2}/quantity".format(
            self.version, store_key, product_id)
        params = self.__get_params(**kwargs)

        return self.__request(url, params=params)

    def list_product_skus(self, store_key, product_id, **kwargs):
        url = "http://api.tcgplayer.com/{0}/stores/{1}/inventory/products/{2}/skus".format(
            self.version, store_key, product_id)
        params = self.__get_params(**kwargs)

        return self.__request(url, params=params)

    def list_related_products(self, store_key, product_id, **kwargs):
        url = "http://api.tcgplayer.com/{0}/stores/{1}/inventory/products/{2}/relatedproducts".format(
            self.version, store_key, product_id)
        params = self.__get_params(**kwargs)

        return self.__request(url, params=params)

    def list_shopping_options(self, store_key, product_id, **kwargs):
        url = "http://api.tcgplayer.com/{0}/stores/{1}/inventory/products/{2}/shippingoptions".format(
            self.version, store_key, product_id)
        params = self.__get_params(**kwargs)

        return self.__request(url, params=params)

    def get_sku_quantity(self, store_key, sku_id, **kwargs):
        url = "http://api.tcgplayer.com/{0}/stores/{1}/inventory/skus/{2}/quantity".format(
            self.version, store_key, sku_id)
        params = self.__get_params(**kwargs)

        return self.__request(url, params=params)

    def increment_sku_inventory_quantity(self, store_key, sku_id, **kwargs):
        url = "http://api.tcgplayer.com/{0}/stores/{1}/inventory/skus/{2}/quantity".format(
            self.version, store_key, sku_id)
        params = self.__get_params(**kwargs)

        return self.__request(url, params=params)
