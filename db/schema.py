from typing import Optional, Required

from pydantic import BaseModel

class user_login_token_schema(BaseModel):

    Email : str
    Key : str

    class ConfigDict:
        from_attributes = True

class long_live_access_token_schema(BaseModel):

    access_token : str

    class ConfigDict:
        from_attributes = True

class user_info_add_schema(BaseModel):

    UserName : Optional[str] = ''
    FirstName : str
    LastName : str
    Password : str
    Email : str
    Mobile : str
    Source : Optional[str] = ''
    Device : Optional[str] = ''

    class ConfigDict:
        from_attributes = True

class user_info_update_schema(BaseModel):

    UserToken : str
    UserName : Optional[str] = None
    FirstName : Optional[str] = None
    LastName : Optional[str] = None
    Email : Optional[str] = None
    Mobile : Optional[str] = None
    Source : Optional[str] = None
    Device : Optional[str] = None

    class ConfigDict:
        from_attributes = True

class current_user_info_schema(BaseModel):

    UserToken : str

    class ConfigDict:
        from_attributes = True
