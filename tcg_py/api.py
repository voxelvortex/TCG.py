import requests
import json


class Handler(object):

    def __init__(self, **kwargs):
        self.version = "v1.20.0"
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
        url = "http://api.tcgplayer.com/v1.19.0/catalog/categories"
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

    def __convert_list_to_str(self, item):
        return str(item).replace("[", "").replace("]", "")

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
        url = "http://api.tcgplayer.com/v1.19.0/catalog/categories/{0}/search".format(category_id)
        data = {}
        if "offset" in kwargs:
            data["offset"] = kwargs["offset"]
        if "limit" in kwargs:
            data["limit"] = kwargs["limit"]
        if "sort" in kwargs:
            data["sort"] = kwargs["sort"]
        if "include_aggregates" in kwargs:
            data["includeAggregates"] = kwargs["include_aggregates"]
        if "name" in kwargs:
            data["name"] = kwargs["name"]
        if "values" in kwargs:
            data["values"] = kwargs["values"]
        if "filters" in kwargs:
            data["filters"] = kwargs["filters"]
        return self.__request(url, data=data, method="POST")

    def list_all_category_groups(self, category_id, **kwargs):
        url = "http://api.tcgplayer.com/v1.19.0/catalog/categories/{0}/groups".format(category_id)
        params = {}
        if "offset" in kwargs:
            params["offset"] = kwargs["offset"]
        if "limit" in kwargs:
            params["limit"] = kwargs["limit"]

        return self.__request(url, params=params)

    def list_all_category_rarities(self, category_id):
        url = "http://api.tcgplayer.com/v1.19.0/catalog/categories/{0}/rarities".format(category_id)
        return self.__request(url)

    def list_all_category_printings(self, category_id):
        url = "http://api.tcgplayer.com/v1.19.0/catalog/categories/{0}/printings".format(category_id)
        return self.__request(url)

    def list_all_category_conditions(self, category_id):
        url = "http://api.tcgplayer.com/v1.19.0/catalog/categories/{0}/conditions".format(category_id)
        return self.__request(url)

    def list_all_category_languages(self, category_id):
        url = "http://api.tcgplayer.com/v1.19.0/catalog/categories/{0}/languages".format(category_id)
        return self.__request(url)

    def list_all_category_media(self, category_id):
        url = "http://api.tcgplayer.com/v1.19.0/catalog/categories/{0}/media".format(category_id)
        return self.__request(url)

    def list_all_group_details(self, **kwargs):
        url = "http://api.tcgplayer.com/{0}/catalog/groups".format(self.version)

        params = {}
        if "category_id" in kwargs:
            params["categoryId"] = kwargs["category_id"]
        if "category_name" in kwargs:
            params["categoryName"] = kwargs["category_id"]
        if "is_supplemental" in kwargs:
            params["isSupplemental"] = kwargs["is_supplemental"]
        if "has_sealed" in kwargs:
            params["hasSealed"] = kwargs["has_sealed"]
        if "sort_desc" in kwargs:
            params["sortDesc"] = kwargs["sort_desc"]
        if "sort_order" in kwargs:
            params["sortOrder"] = params["sort_order"]
        if "offset" in kwargs:
            params["offset"] = kwargs["offset"]
        if "limit" in kwargs:
            params["limit"] = kwargs["limit"]
        return self.__request(url, params=params)

    def get_group_details(self, group_id):
        group_id = self.__convert_list_to_str(group_id)
        url = "http://api.tcgplayer.com/v1.19.0/catalog/groups/{0}".format(group_id)
        return self.__request(url)

    def list_all_group_media(self, group_id):
        url = "http://api.tcgplayer.com/{0}/catalog/groups/{1}/media".format(self.version, group_id)
        return self.__request(url)

    def list_all_products(self, **kwargs):
        url = "http://api.tcgplayer.com/{0}/catalog/products".format(self.version)
        params = {}

        if "category_id" in kwargs:
            params["categoryId"] = kwargs["category_id"]
        if "category_name" in kwargs:
            params["categoryName"] = kwargs["category_name"]
        if "group_id" in kwargs:
            params["groupId"] = kwargs["group_id"]
        if "group_name" in kwargs:
            params["groupName"] = kwargs["group_name"]
        if "product_name" in kwargs:
            params["productName"] = kwargs["product_name"]
        if "get_extended_fields" in kwargs:
            params["getExtendedFields"] = kwargs["get_extended_fields"]
        if "product_types" in kwargs:
            params["productTypes"] = self.__convert_list_to_str(kwargs["product_types"])
        if "offset" in kwargs:
            params["offset"] = kwargs["offset"]
        if "limit" in kwargs:
            params["limit"] = kwargs["limit"]
        return self.__request(url, params=params)

    def get_product_details(self, product_ids, **kwargs):
        product_ids = self.__convert_list_to_str(product_ids)
        url = "http://api.tcgplayer.com/{0}/catalog/products/{1}".format(self.version, product_ids)

        params = {}
        if "get_extended_fields" in kwargs:
            params["getExtendedFields"] = kwargs["get_extended_fields"]

        return self.__request(url, params=params)

    def get_product_details_by_gtin(self, gtin, **kwargs):
        url = "http://api.tcgplayer.com/{0}/catalog/products/gtin/{0}".format(self.version, gtin)
        params = {}
        if "get_extended_fields" in kwargs:
            params["getExtendedFields"] = kwargs["get_extended_fields"]

        return self.__request(url, params=params)

    def list_product_skus(self, product_id):
        url = "http://api.tcgplayer.com/{0}/catalog/products/{1}/skus".format(self.version, product_id)
        return self.__request(url)

    def list_related_products(self, product_id, **kwargs):
        url = "http://api.tcgplayer.com/{0}/catalog/products/{1}/productsalsopurchased".format(self.version, product_id)

        params = {}
        if "limit" in kwargs:
            params["limit"] = kwargs["limit"]
        if "offset" in kwargs:
            params["offset"] = kwargs["offset"]

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
