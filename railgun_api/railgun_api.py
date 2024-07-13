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
        self.field = StellarField(self)
        self.entity = StellarEntity(self)
        # TODO auth would be done here
        # IF THERE WAS ANY!!!
        # At least validate the URL is real
        # I knew heartbeat would come in handy
        requests.get(self.URL+"/heartbeat").raise_for_status()


    def find(self, entity_type, filters=None, return_fields=[], pagination=10000, page=1, schema=None):  # TODO pagination mechanic will change with RPC
        """
        """
        if filters and type(filters) == list:  # Simplify top-level for simple ops
            filters = {
                "filter_operator": "AND",
                "filters": filters
            }
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
    

    def telescope(self):
        raise NotImplementedError



class StellarField:
    def __init__(self, railgun):
        self.railgun = railgun


    def create(self, entity, field_code, field_name, field_type, options=None, schema=None):
        FIELD_CREATE_REQUEST = {
            "part": "field",
            "request_type": "create",
            "schema": schema or self.railgun.default_schema,
            "entity": entity,
            "data": {
                "code": field_code,
                "name": field_name,
                "type": field_type,
                "options": options
            }
        }
        resp = requests.post(self.railgun.URL+"/stellar", json=FIELD_CREATE_REQUEST)
        resp.raise_for_status()
        return resp.json()


    def update(self):
        raise NotImplementedError


    def delete(self, entity, field_code, schema=None):
        FIELD_DELETE_REQUEST = {
            "part": "field",
            "request_type": "delete",
            "schema": schema or self.railgun.default_schema,
            "entity": entity,
            "data": {
                "code": field_code,
            }
        }
        resp = requests.post(self.railgun.URL+"/stellar", json=FIELD_DELETE_REQUEST)
        resp.raise_for_status()
        return resp.json()


class StellarEntity:
    def __init__(self, railgun):
        self.railgun = railgun


    def create(self, entity_code, entity_soloname, entity_multiname, schema=None):
        TABLE_CREATE_REQUEST = {
            "part": "entity",
            "request_type": "create",
            "schema": schema or self.railgun.default_schema,
            "data": {
                "code": entity_code,
                "soloname": entity_soloname,
                "multiname": entity_multiname
            }
        }
        resp = requests.post(self.railgun.URL+"/stellar", json=TABLE_CREATE_REQUEST)
        resp.raise_for_status()
        return resp.json()


    def update(self):
        raise NotImplementedError


    def delete(self, entity, schema=None):
        TABLE_CREATE_REQUEST = {
            "part": "entity",
            "request_type": "delete",
            "schema": schema or self.railgun.default_schema,
            "data": {
                "type": entity
            }
        }
        resp = requests.post(self.railgun.URL+"/stellar", json=TABLE_CREATE_REQUEST)
        resp.raise_for_status()
        return resp.json()
