from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.collection_schema_ttls_type_0 import CollectionSchemaTtlsType0
    from ..models.field_schema import FieldSchema


T = TypeVar("T", bound="CollectionSchema")


@_attrs_define
class CollectionSchema:
    """
    Attributes:
        object_type (Union[Literal['CollectionSchema'], Unset]):  Default: 'CollectionSchema'.
        fields (Union[None, Unset, list['FieldSchema']]):
        description (Union[None, Unset, str]):  Default: ''.
        ttls (Union['CollectionSchemaTtlsType0', None, Unset]):
    """

    object_type: Union[Literal["CollectionSchema"], Unset] = "CollectionSchema"
    fields: Union[None, Unset, list["FieldSchema"]] = UNSET
    description: Union[None, Unset, str] = ""
    ttls: Union["CollectionSchemaTtlsType0", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.collection_schema_ttls_type_0 import CollectionSchemaTtlsType0

        object_type = self.object_type

        fields: Union[None, Unset, list[dict[str, Any]]]
        if isinstance(self.fields, Unset):
            fields = UNSET
        elif isinstance(self.fields, list):
            fields = []
            for fields_type_0_item_data in self.fields:
                fields_type_0_item = fields_type_0_item_data.to_dict()
                fields.append(fields_type_0_item)

        else:
            fields = self.fields

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        ttls: Union[None, Unset, dict[str, Any]]
        if isinstance(self.ttls, Unset):
            ttls = UNSET
        elif isinstance(self.ttls, CollectionSchemaTtlsType0):
            ttls = self.ttls.to_dict()
        else:
            ttls = self.ttls

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if object_type is not UNSET:
            field_dict["object_type"] = object_type
        if fields is not UNSET:
            field_dict["fields"] = fields
        if description is not UNSET:
            field_dict["description"] = description
        if ttls is not UNSET:
            field_dict["ttls"] = ttls

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.collection_schema_ttls_type_0 import CollectionSchemaTtlsType0
        from ..models.field_schema import FieldSchema

        d = src_dict.copy()
        object_type = cast(Union[Literal["CollectionSchema"], Unset], d.pop("object_type", UNSET))
        if object_type != "CollectionSchema" and not isinstance(object_type, Unset):
            raise ValueError(f"object_type must match const 'CollectionSchema', got '{object_type}'")

        def _parse_fields(data: object) -> Union[None, Unset, list["FieldSchema"]]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                fields_type_0 = []
                _fields_type_0 = data
                for fields_type_0_item_data in _fields_type_0:
                    fields_type_0_item = FieldSchema.from_dict(fields_type_0_item_data)

                    fields_type_0.append(fields_type_0_item)

                return fields_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, list["FieldSchema"]], data)

        fields = _parse_fields(d.pop("fields", UNSET))

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        def _parse_ttls(data: object) -> Union["CollectionSchemaTtlsType0", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                ttls_type_0 = CollectionSchemaTtlsType0.from_dict(data)

                return ttls_type_0
            except:  # noqa: E722
                pass
            return cast(Union["CollectionSchemaTtlsType0", None, Unset], data)

        ttls = _parse_ttls(d.pop("ttls", UNSET))

        collection_schema = cls(
            object_type=object_type,
            fields=fields,
            description=description,
            ttls=ttls,
        )

        collection_schema.additional_properties = d
        return collection_schema

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
