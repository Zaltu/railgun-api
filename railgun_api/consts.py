"""
File to store some helpful constants, most of which are ultimately exposed to
the API in a meaningful way.
"""


class _RG_FIELD_TYPES:
    """
    Namespace class representing available field types
    """
    TEXT="TEXT"
    PASSWORD="PASSWORD"
    MEDIA="MEDIA"
    INT="INT"
    FLOAT="FLOAT"
    DATE="DATE"
    JSON="JSON"
    BOOLEAN="BOOL"
    LIST="LIST"
    ENTITY="ENTITY"
    MULTI_ENTITY="MULTIENTITY"

    def __str__(self):
        """Simple convenience"""
        return str(["TEXT", "PASSWORD", "MEDIA", "INT", "FLOAT", "DATE", "JSON", "BOOLEAN", "LIST", "ENTITY", "MUTLI_ENTITY"])

RG_FIELD_TYPES = _RG_FIELD_TYPES()