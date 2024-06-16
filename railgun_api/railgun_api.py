"""
Very basic API structure for Railgun.
Uses HTTP, so can and will encounter issues with large amounts of data. RPC version one day.
The end-user functions (public functions) signature will not change though.
See ReadMe for usage instructions.

TODO code doc
"""
import requests


class Railgun():
    def __init__(self, host, schema):
        self.URL = host
        self.default_schema = schema
        self.stellar = Stellar
        # TODO auth would be done here
        # IF THERE WAS ANY!!!
        # At least validate the URL is real
        # I knew heartbeat would come in handy
        requests.get(self.URL+"/heartbeat").raise_for_status()


    def find(self, entity_type, filters, return_fields, pagination=10000, page=1, schema=None):  # TODO pagination mechanic will change with RPC
        """
        """
        READ_REQUEST = {
            "schema": schema or self.default_schema,
            "entity": entity_type,
            "read": {
                "return_fields": return_fields,
                "filters": filters or None,  # Prevent weird issues with []
                "pagination": pagination,
                "page": page
            }
        }
        resp = requests.post(self.URL+"/read", json=READ_REQUEST)
        resp.raise_for_status()
        return resp.json()


    def create(self, entity_type, data, schema=None):
        """
        """
        CREATE_REQUEST = {
            "schema": schema or self.default_schema,
            "entity": entity_type,
            "data": data
        }
        resp = requests.post(self.URL+"/create", json=CREATE_REQUEST)
        resp.raise_for_status()
        return resp.json()


    def update(self, entity_type, entity_id, data, schema=None):
        """
        """
        UPDATE_REQUEST = {
            "schema": schema or self.default_schema,
            "entity": entity_type,
            "entity_id": entity_id,
            "data": data
        }
        resp = requests.post(self.URL+"/update", json=UPDATE_REQUEST)
        resp.raise_for_status()
        return resp.json()


    def delete(self, entity_type, entity_id, schema=None):
        """
        """
        DELETE_REQUEST = {
            "schema": schema or self.default_schema,
            "entity": entity_type,
            "entity_id": entity_id
        }
        resp = requests.post(self.URL+"/delete", json=DELETE_REQUEST)
        resp.raise_for_status()
        return resp.json()


    def batch(self, batchData, schema=None):
        """
        """
        BATCH_REQUEST = {
            "schema": schema or self.default_schema,
            "batch": batchData
        }
        resp = requests.post(self.URL+"/batch", json=BATCH_REQUEST)
        resp.raise_for_status()
        return resp.json()



class StellarField:
    def create():
        raise NotImplementedError

    def update():
        raise NotImplementedError

    def delete():
        raise NotImplementedError


class StellarEntity:
    def create():
        raise NotImplementedError

    def update():
        raise NotImplementedError

    def delete():
        raise NotImplementedError


class Stellar:
    field = StellarField
    entity = StellarEntity
