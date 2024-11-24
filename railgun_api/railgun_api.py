"""
Very basic API structure for Railgun.
Uses HTTP, so can and will encounter issues with large amounts of data. RPC version one day.
The end-user functions (public functions) signature will not change though.
See ReadMe for usage instructions.

TODO code doc
"""
import json
import requests
from pathlib import Path

from railgun_api.consts import RG_FIELD_TYPES


class Railgun():
    def __init__(self, host, username, password, schema):
        self.URL = host
        self.default_schema = schema
        self.field = StellarField(self)
        self.entity = StellarEntity(self)

        self.RG_AUTH_HEADER = {
            "Authorization": "Bearer {token}".format(
                token=self._login(username, password)
            )
        }


    def _login(self, username, password):
        """
        Authenticate credentials and return the access token.

        :param str username: username to log in with
        :param str password: password to log in with

        :raises AuthenticationException: if unable to authenticate the given credentials
        :returns: authorization header access token
        :rtype: str
        """
        LOGIN_BODY = f"grant_type=password&username={username}&password={password}"
        LOGIN_HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(
            self.URL+"/login",
            headers=LOGIN_HEADERS,
            data=LOGIN_BODY
        )
        if response.status_code in [401, 405]:
            raise AuthenticationException(
                "Cannot authenticate these credentials with this endpoint."
            )
        return response.json()["access_token"]


    def find(self, entity_type, filters=None, return_fields=[], pagination=5000, page=1, show_archived=False, include_count=False, schema=None):  # TODO pagination mechanic will change with RPC
        """
        """
        if filters and type(filters) == list:  # Simplify top-level for simple ops
            if type(filters[0]) != list:
                filters = [filters]
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
                "page": page,
                "show_archived": show_archived,
                "include_count": include_count
            }
        }
        return self._makeRGCall(self.URL+"/read", READ_REQUEST)


    def create(self, entity_type, data, schema=None):
        """
        """
        CREATE_REQUEST = {
            "schema": schema or self.default_schema,
            "entity": entity_type,
            "data": data
        }
        return self._makeRGCall(self.URL+"/create", CREATE_REQUEST)


    def update(self, entity_type, entity_id, data, schema=None):
        """
        """
        UPDATE_REQUEST = {
            "schema": schema or self.default_schema,
            "entity": entity_type,
            "entity_id": entity_id,
            "data": data
        }
        return self._makeRGCall(self.URL+"/update", UPDATE_REQUEST)


    def delete(self, entity_type, entity_id, permanent=False, schema=None):
        """
        """
        DELETE_REQUEST = {
            "schema": schema or self.default_schema,
            "entity": entity_type,
            "entity_id": entity_id,
            "permanent": permanent
        }
        return self._makeRGCall(self.URL+"/delete", DELETE_REQUEST)


    def batch(self, batchData, schema=None):
        """
        """
        BATCH_REQUEST = {
            "schema": schema or self.default_schema,
            "batch": batchData
        }
        return self._makeRGCall(self.URL+"/batch", BATCH_REQUEST)
    

    def upload(self, entity, field, path, schema=None):
        """
        """
        path = Path(path)
        if not path.exists() or path.is_dir():
            raise UploadFileException("File does not exist:\n%s" % str(path))

        entity["schema"] = schema or self.default_schema
        entity["field"] = field
        with open(path, "rb") as infile:
            resp = requests.post(
                self.URL+"/upload",
                headers=self.RG_AUTH_HEADER,
                files={"file":infile},
                data={"metadata":json.dumps(entity)}
            )
        resp.raise_for_status()
        return resp.json()


    def download(self, remotePath, localPath):
        """
        """
        # Make it easier
        remotePath = Path(remotePath)
        localPath = Path(localPath)
        final_destination = localPath

        if localPath.is_dir():
            final_destination = final_destination / remotePath.name

        if not final_destination.parent.exists():
            raise DownloadFileException("Local path does not exist:\n%s" % str(final_destination.parent))

        with requests.post(
            self.URL+"/download",
            json={"path": str(remotePath)},
            headers=self.RG_AUTH_HEADER,
            stream=True
        ) as resp:
            resp.raise_for_status()
            with open(final_destination, 'wb+') as outfile:
                # None for max chunk size. If you run into memory issues, you may need to change this.
                for chunk in resp.iter_content(None):
                    outfile.write(chunk)
        return final_destination


    def telescope(self):
        raise NotImplementedError


    def _makeRGCall(self, url, request):
        """
        """
        resp = requests.post(url, headers=self.RG_AUTH_HEADER, json=request)
        try:
            resp.raise_for_status()
        except requests.HTTPError as e:
            try:
                # Attempt to add any additional information from the error response ot the request
                e.add_note(json.loads(resp.content.decode())["detail"])
            except:
                raise
            raise
        return resp.json()



class StellarField:
    types = RG_FIELD_TYPES
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
        resp = requests.post(self.railgun.URL+"/stellar", headers=self.railgun.RG_AUTH_HEADER, json=FIELD_CREATE_REQUEST)
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
        resp = requests.post(self.railgun.URL+"/stellar", headers=self.railgun.RG_AUTH_HEADER, json=FIELD_DELETE_REQUEST)
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
        resp = requests.post(self.railgun.URL+"/stellar", headers=self.railgun.RG_AUTH_HEADER, json=TABLE_CREATE_REQUEST)
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
        resp = requests.post(self.railgun.URL+"/stellar", headers=self.railgun.RG_AUTH_HEADER, json=TABLE_CREATE_REQUEST)
        resp.raise_for_status()
        return resp.json()



class AuthenticationException(Exception):
    """Authentication Error"""

class DownloadFileException(Exception):
    """Can't download a file"""

class UploadFileException(Exception):
    """Can't upload a file"""