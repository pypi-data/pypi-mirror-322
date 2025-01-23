from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.collection_metadata_ttls import CollectionMetadataTtls


T = TypeVar("T", bound="CollectionMetadata")


@_attrs_define
class CollectionMetadata:
    """
    Attributes:
        name (str):
        description (str):
        hash_algo (str):
        etag (str):
        is_marked_for_deletion (bool):
        soft_deleter (str):
        object_type (Union[Literal['CollectionMetadata'], Unset]):  Default: 'CollectionMetadata'.
        ttls (Union[Unset, CollectionMetadataTtls]):
    """

    name: str
    description: str
    hash_algo: str
    etag: str
    is_marked_for_deletion: bool
    soft_deleter: str
    object_type: Union[Literal["CollectionMetadata"], Unset] = "CollectionMetadata"
    ttls: Union[Unset, "CollectionMetadataTtls"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        description = self.description

        hash_algo = self.hash_algo

        etag = self.etag

        is_marked_for_deletion = self.is_marked_for_deletion

        soft_deleter = self.soft_deleter

        object_type = self.object_type

        ttls: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.ttls, Unset):
            ttls = self.ttls.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "hash_algo": hash_algo,
                "etag": etag,
                "is_marked_for_deletion": is_marked_for_deletion,
                "soft_deleter": soft_deleter,
            }
        )
        if object_type is not UNSET:
            field_dict["object_type"] = object_type
        if ttls is not UNSET:
            field_dict["ttls"] = ttls

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.collection_metadata_ttls import CollectionMetadataTtls

        d = src_dict.copy()
        name = d.pop("name")

        description = d.pop("description")

        hash_algo = d.pop("hash_algo")

        etag = d.pop("etag")

        is_marked_for_deletion = d.pop("is_marked_for_deletion")

        soft_deleter = d.pop("soft_deleter")

        object_type = cast(Union[Literal["CollectionMetadata"], Unset], d.pop("object_type", UNSET))
        if object_type != "CollectionMetadata" and not isinstance(object_type, Unset):
            raise ValueError(f"object_type must match const 'CollectionMetadata', got '{object_type}'")

        _ttls = d.pop("ttls", UNSET)
        ttls: Union[Unset, CollectionMetadataTtls]
        if isinstance(_ttls, Unset):
            ttls = UNSET
        else:
            ttls = CollectionMetadataTtls.from_dict(_ttls)

        collection_metadata = cls(
            name=name,
            description=description,
            hash_algo=hash_algo,
            etag=etag,
            is_marked_for_deletion=is_marked_for_deletion,
            soft_deleter=soft_deleter,
            object_type=object_type,
            ttls=ttls,
        )

        collection_metadata.additional_properties = d
        return collection_metadata

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
