# coding: utf-8

"""
    Arthur Scope

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field
from typing import Any, ClassVar, Dict, List
from scope_client.api_bindings.models.alert import Alert
from scope_client.api_bindings.models.infinite_pagination import InfinitePagination
from typing import Optional, Set
from typing_extensions import Self

class InfiniteResourceListAlert(BaseModel):
    """
    InfiniteResourceListAlert
    """ # noqa: E501
    records: List[Alert] = Field(description="List of records.")
    pagination: InfinitePagination = Field(description="Pagination information.")
    __properties: ClassVar[List[str]] = ["records", "pagination"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of InfiniteResourceListAlert from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in records (list)
        _items = []
        if self.records:
            for _item_records in self.records:
                if _item_records:
                    _items.append(_item_records.to_dict())
            _dict['records'] = _items
        # override the default output from pydantic by calling `to_dict()` of pagination
        if self.pagination:
            _dict['pagination'] = self.pagination.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of InfiniteResourceListAlert from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "records": [Alert.from_dict(_item) for _item in obj["records"]] if obj.get("records") is not None else None,
            "pagination": InfinitePagination.from_dict(obj["pagination"]) if obj.get("pagination") is not None else None
        })
        return _obj


