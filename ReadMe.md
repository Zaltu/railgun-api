# ReadMe
All of Railgun's functionality is exposed via REST endpoints defined and documented in [Railgun](https://github.com/zaltu/railgun). For ease of use however, a simple Python wrapper is provided in order to simplify integration.

## Installation
The package is currently not available on pip, but may be eventually. It can be installed via pip anyway directly from the repo.  
`pip install git+https://github.com/zaltu/railgun`


## Usage
When in doubt, refer to the in-line documentation of each function (TODO).  
You can also refer to the endpoint-specific documentation of [Railgun](https://github.com/zaltu/railgun), though that doc does not cover the abtractions (particularly in syntax) provided by this pre-made API wrapper.
### Connection
```python
from railgun_api import Railgun

# You must provide a schema to be used by this session by default.
# It can be overwritten in any operation by providing the optional "schema" parameter
rg = Railgun("https://railgun.mysite.com", "login", "password", "default_schema")
# Login credentials are the login/password of any existing user.
# No distinction is made between Human and API users by Railgun.
```

### Standard CRUD Operations Quickstart
```python
# See find/filter syntax later in documentation for more info
rg.find("Entity Soloname", ["filter", "is", True], ["type", "id"])

rg.create("Entity Soloname", {"code": "example"})

rg.update("Entity Soloname", 42, {"code": "updated"})

# If permanent is set to True, record will be deleted instead of archived.
rg.delete("Entity Soloname", 42, permanent=False)
```

### Batch Operations
It is possible to batch multiple operations of different types (CUD) together in a single `batch` request.
```python
batchData = [
    {
        "request_type": "create",
        "entity_type": "Entity Soloname",
        "data": {"code": "example"}
    },
    {
        "request_type": "udpate",
        "entity_type": "Entity Soloname",
        "entity_id": 42,
        "data": {"code": "updated"}
    },
    {
        "request_type": "delete",
        "entity_type": "Entity Soloname",
        "entity_id": 42
    }
]
rg.batch(batchData)
```

### Media Operations
```python
rg.upload("Entity Soloname", "media_field", "/path/to/my/file.ext")

# SUBJECT TO CHANGE
# Fetch the remote path first by fetching the field of the entity, then download that remote path
# This will likely change to simply providing the media field containing the desired downloadable content
# If the local path is a directory, the file will retain its server-side name.
rg.download("/remote/path/to/media", "/local/intended/path.ext")
```

### Telescope/Schema Read
NYI (TODO)

### STELLAR Field Operations
```python

######################
### Field Creation ###
######################
rg.field.create(
    entity="Entity Soloname",
    field_code="backend_code",
    field_name="Human Readable Name",
    field_type=rg.RG_FIELD_TYPES.TEXT,
    options=None
)
# Check available field types with
print(rg.RG_FIELD_TYPES)
# Options are needed for List, Entity and MultiEntity field types.
# For list fields, provide a List of valid values:
options=["Live-Action", "CG", "Anime", "Cartoon"]
# For Entity/MultiEntity fields, provide a list of valid linkable entity types:
options=["Genre"]

######################
###  Field Update  ###
######################
NYI (TODO)
# If you know what you're doing, you can forcibly update the field parameters directly in railgun_internal.

######################
### Field  Removal ###
######################
rg.delete(
    entity="Entity Soloname",
    field_code="field_code"
)
# Note that currently, the first time this function is called the field will be archived, and deleted on the second (TODO)
# Note that deleting a media field will delete all stored media for that field from the server.
```

### STELLAR Entity Operations
```python
#######################
### Entity Creation ###
#######################
rg.entity.create(
    entity_code="sql_table_name",
    entity_soloname="My New Entity",
    entity_multiname="My New Entities"
)
# The plural name is provided by the user for display purposes. Language modules just aren't good enough.
# Language hard. Go figure.

######################
### Entity  Update ###
######################
NYI (TODO)
# If you know what you're doing, you can forcibly update the entity parameters directly in railgun_internal.

######################
### Entity Removal ###
######################
rg.entity.delete(
    entity="entity_code"
)
# Note that currently, the first time this function is called the entity will be archived, and deleted on the second (TODO)
# It should go without saying, but this will drop the table and everything in it :) .
```

### Deletion and Archival
It is important to note that while documentation generally refers to "deletion" directly, there is a strong distinction between **Deletion** and **Archival**.
- Deletion is permanent. The record is dropped from the "physical" database, any media related to the record is deleted and any relations pointing to it are defacto removed.
- Archival is closer to a display status. By default, Railgun itself will filter out any archived records, fields, entities, etc from responses. This should always be done first by default, similar to the "trash can" on your desktop. Only permanently delete things you're absolutely certain you won't need anymore.


### Find/Filter Syntax
Syntax of the `find` functionality is a bit more complex to allow for fitlering, ordering, paging, etc. Following is a breakdown of the `Railgun.find` parameters.
```python
rg.find(
    entity_type="Entity Soloname",
    filters={"filter_operator": "AND", "filters": [["uid", "is", 42]]},
    return_fields=["type", "uid"],
    pagination=5000,
    page=1,
    show_archived=False,
    include_count=False,
    schema=None
)
# entity_type
# entity soloname to query, including any special characters.

# (See "Filter Syntax" section below)

# (See "Return Fields" section below)

# pagination
# You may specify the number of results per page to return. Default is 5000.

# page
# Page to return, default 1.

# show_archived
# Toggle whether or not to query only archived data, default False.

# include_count
# If True, the last element returned in the list will be a simple dictionary of {"count": <int>} defining the total number of records matching your query.
# this requires making two full calls to the DB (one to fetch within pagination constraints and one to query the COUNT). Default is False.

# schema
# Specify an override to the default schema provided when initiating the session if desired. Default None.
```

### Filter Syntax
Filters are represented as a resursive dictionary of conditions, with a supplied filter operator ("AND"/"OR") at each level. For example:
```python
{
    "filter_operator": "AND",
    "filters": [
        ["video_type", "is", "Feature Film"],
        {
            "filter_operator": "OR",
            "filters": [
                ["code", "contains", "Big"],
                ["code", "contains", "Small"]
            ]
        }
    ]
}
```
This will return all entities where the field `video_type` is "Feature Film" *and* where the field `code` contains *either* "Big" *or* "Small". This format of filter can be repeated ad-nauseam

For convenience, since 95% of filters used in practice are quite simple, railgun_api will automatically wrap more simple structures.
```python
# If you provide a list of lists, it will automatically be transformed into an "AND"-type filter:
filters=[["video_type", "is", "Feature Film"], ["code", "contains", "GOAT"]]
# is *automatically* transformed into
{
    "filter_operator": "AND",
    "filters": [
        ["video_type", "is", "Feature Film"],
        ["code", "contains", "GOAT"]
    ]
}

# For even more simple use, you can even provide a single filter element:
filters=["uid", "is", 42]
# is *automatically* transformed into
{
    "filter_operator": "AND",
    "filters": [
        ["uid", "is", 42],
    ]
}
```

### Filter Options
The following filter options are currently defined:
- `is`
- `is_not`
- `contains`
- `not_contains`
- `starts_with`
- `ends_with`
- `greater_than`
- `less_than`


### Filter Discrepencies to Note (TODO)
- Filtering based on entity/multi-entity fields is not supported yet.
- Filtering based on linked fields is not supported yet.


### Return Fields
Specify here a list of the fields you wish to retrieve from the record.

***Important!***  
By default, `type`, `uid` and the field defined as the entity's display name column (`code`, by default) are always returned!  
There's nothing preventing you from specifying them manually, but it is not necessary. `return_fields` is not a required parameter.

### Linked Return Fields
Railgun's return structure varies slightly from that of other similar commercial software. The syntax for specifying a linked return field is standard:
```python
["field.Linked Entity Type.linked_field"]
# For example
["page_settings.Page Setting.entity.Entity.schema.Schema.code"]
```
There is no limit on how deep the linkage can go. Bear in mind that the deeper you go, the slower the query will be (more JOINS required on the DB).

The exact string set in the `return_fields` parameter will *not* be included in the response. Instead, sub-objects, *including default fields (type, uid, display_name_col)*, are included under the linked field's code.
```python
rg.find("Page", ["uid", "is", 1], ["page_settings.Page Setting.entity.Entity.schema.Schema.code"])
# Response entity object:
{
    "type": "Page",
    "uid": 1,
    "code": "Archive Browser",
    "page_settings": [
        {
            "type": "Page Setting", 
            "uid": 76,
            "code": "Archived Videos",
            "entity": {
                "type": "Entity",
                "uid": 7,
                "soloname": "Video",
                "schema": {
                    "type": "Schema",
                    "uid": 2,
                    "code": "Archive"
                }
            }
        }
        {
            "type": "Page Setting", 
            "uid": 77,
            "code": "Archived Books",
            "entity": {
                "type": "Entity",
                "uid": 6,
                "soloname": "Book",
                "schema": {
                    "type": "Schema",
                    "uid": 2,
                    "code": "Archive"
                }
            }
        }
    ]
}
```
Note as well the ability to fetch linked fields from Multi-Entity sources without issue.


## Release Process
Bump versionin `pyproject.toml` as necessary.
```bash
python -m build
pip install dist/railgun_api.egg.<version>
```
And that's it!