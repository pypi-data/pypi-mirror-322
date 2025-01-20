# coding: utf-8

"""
    Arthur Scope

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
from inspect import getfullargspec
import json
import pprint
import re  # noqa: F401
from pydantic import BaseModel, ConfigDict, Field, StrictStr, ValidationError, field_validator
from typing import Optional
from scope_client.api_bindings.models.dataset_scalar_type import DatasetScalarType
from typing import Union, Any, List, Set, TYPE_CHECKING, Optional, Dict
from typing_extensions import Literal, Self
from pydantic import Field

OBJECTVALUE_ANY_OF_SCHEMAS = ["DatasetListType", "DatasetObjectType", "DatasetScalarType"]

class ObjectValue(BaseModel):
    """
    ObjectValue
    """

    # data type: DatasetScalarType
    anyof_schema_1_validator: Optional[DatasetScalarType] = None
    # data type: DatasetObjectType
    anyof_schema_2_validator: Optional[DatasetObjectType] = None
    # data type: DatasetListType
    anyof_schema_3_validator: Optional[DatasetListType] = None
    if TYPE_CHECKING:
        actual_instance: Optional[Union[DatasetListType, DatasetObjectType, DatasetScalarType]] = None
    else:
        actual_instance: Any = None
    any_of_schemas: Set[str] = { "DatasetListType", "DatasetObjectType", "DatasetScalarType" }

    model_config = {
        "validate_assignment": True,
        "protected_namespaces": (),
    }

    def __init__(self, *args, **kwargs) -> None:
        if args:
            if len(args) > 1:
                raise ValueError("If a position argument is used, only 1 is allowed to set `actual_instance`")
            if kwargs:
                raise ValueError("If a position argument is used, keyword arguments cannot be used.")
            super().__init__(actual_instance=args[0])
        else:
            super().__init__(**kwargs)

    @field_validator('actual_instance')
    def actual_instance_must_validate_anyof(cls, v):
        instance = ObjectValue.model_construct()
        error_messages = []
        # validate data type: DatasetScalarType
        if not isinstance(v, DatasetScalarType):
            error_messages.append(f"Error! Input type `{type(v)}` is not `DatasetScalarType`")
        else:
            return v

        # validate data type: DatasetObjectType
        if not isinstance(v, DatasetObjectType):
            error_messages.append(f"Error! Input type `{type(v)}` is not `DatasetObjectType`")
        else:
            return v

        # validate data type: DatasetListType
        if not isinstance(v, DatasetListType):
            error_messages.append(f"Error! Input type `{type(v)}` is not `DatasetListType`")
        else:
            return v

        if error_messages:
            # no match
            raise ValueError("No match found when setting the actual_instance in ObjectValue with anyOf schemas: DatasetListType, DatasetObjectType, DatasetScalarType. Details: " + ", ".join(error_messages))
        else:
            return v

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> Self:
        return cls.from_json(json.dumps(obj))

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Returns the object represented by the json string"""
        instance = cls.model_construct()
        error_messages = []
        # anyof_schema_1_validator: Optional[DatasetScalarType] = None
        try:
            instance.actual_instance = DatasetScalarType.from_json(json_str)
            return instance
        except (ValidationError, ValueError) as e:
             error_messages.append(str(e))
        # anyof_schema_2_validator: Optional[DatasetObjectType] = None
        try:
            instance.actual_instance = DatasetObjectType.from_json(json_str)
            return instance
        except (ValidationError, ValueError) as e:
             error_messages.append(str(e))
        # anyof_schema_3_validator: Optional[DatasetListType] = None
        try:
            instance.actual_instance = DatasetListType.from_json(json_str)
            return instance
        except (ValidationError, ValueError) as e:
             error_messages.append(str(e))

        if error_messages:
            # no match
            raise ValueError("No match found when deserializing the JSON string into ObjectValue with anyOf schemas: DatasetListType, DatasetObjectType, DatasetScalarType. Details: " + ", ".join(error_messages))
        else:
            return instance

    def to_json(self) -> str:
        """Returns the JSON representation of the actual instance"""
        if self.actual_instance is None:
            return "null"

        if hasattr(self.actual_instance, "to_json") and callable(self.actual_instance.to_json):
            return self.actual_instance.to_json()
        else:
            return json.dumps(self.actual_instance)

    def to_dict(self) -> Optional[Union[Dict[str, Any], DatasetListType, DatasetObjectType, DatasetScalarType]]:
        """Returns the dict representation of the actual instance"""
        if self.actual_instance is None:
            return None

        if hasattr(self.actual_instance, "to_dict") and callable(self.actual_instance.to_dict):
            return self.actual_instance.to_dict()
        else:
            return self.actual_instance

    def to_str(self) -> str:
        """Returns the string representation of the actual instance"""
        return pprint.pformat(self.model_dump())

from scope_client.api_bindings.models.dataset_list_type import DatasetListType
from scope_client.api_bindings.models.dataset_object_type import DatasetObjectType
# TODO: Rewrite to not use raise_errors
ObjectValue.model_rebuild(raise_errors=False)

