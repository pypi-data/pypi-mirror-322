from typing import Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="QuerySpec")


@_attrs_define
class QuerySpec:
    """
    Attributes:
        expr (str):
        collection_name (str):
        object_type (Union[Literal['QuerySpec'], Unset]):  Default: 'QuerySpec'.
        output_fields (Union[None, Unset, list[str]]):
    """

    expr: str
    collection_name: str
    object_type: Union[Literal["QuerySpec"], Unset] = "QuerySpec"
    output_fields: Union[None, Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        expr = self.expr

        collection_name = self.collection_name

        object_type = self.object_type

        output_fields: Union[None, Unset, list[str]]
        if isinstance(self.output_fields, Unset):
            output_fields = UNSET
        elif isinstance(self.output_fields, list):
            output_fields = self.output_fields

        else:
            output_fields = self.output_fields

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "expr": expr,
                "collection_name": collection_name,
            }
        )
        if object_type is not UNSET:
            field_dict["object_type"] = object_type
        if output_fields is not UNSET:
            field_dict["output_fields"] = output_fields

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        expr = d.pop("expr")

        collection_name = d.pop("collection_name")

        object_type = cast(Union[Literal["QuerySpec"], Unset], d.pop("object_type", UNSET))
        if object_type != "QuerySpec" and not isinstance(object_type, Unset):
            raise ValueError(f"object_type must match const 'QuerySpec', got '{object_type}'")

        def _parse_output_fields(data: object) -> Union[None, Unset, list[str]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                output_fields_type_0 = cast(list[str], data)

                return output_fields_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list[str]], data)

        output_fields = _parse_output_fields(d.pop("output_fields", UNSET))

        query_spec = cls(
            expr=expr,
            collection_name=collection_name,
            object_type=object_type,
            output_fields=output_fields,
        )

        query_spec.additional_properties = d
        return query_spec

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
