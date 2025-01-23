import datetime
from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.exact_collection_entry_metadata import ExactCollectionEntryMetadata


T = TypeVar("T", bound="ExactCollectionEntry")


@_attrs_define
class ExactCollectionEntry:
    """
    Attributes:
        id (str):
        fk (str):
        link (str):
        metadata (ExactCollectionEntryMetadata):
        timestamp (datetime.datetime):
        is_file_upload (bool):
        ingestor (str):
        is_marked_for_deletion (bool):
        object_type (Union[Literal['ExactCollectionEntry'], Unset]):  Default: 'ExactCollectionEntry'.
    """

    id: str
    fk: str
    link: str
    metadata: "ExactCollectionEntryMetadata"
    timestamp: datetime.datetime
    is_file_upload: bool
    ingestor: str
    is_marked_for_deletion: bool
    object_type: Union[Literal["ExactCollectionEntry"], Unset] = "ExactCollectionEntry"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        fk = self.fk

        link = self.link

        metadata = self.metadata.to_dict()

        timestamp = self.timestamp.isoformat()

        is_file_upload = self.is_file_upload

        ingestor = self.ingestor

        is_marked_for_deletion = self.is_marked_for_deletion

        object_type = self.object_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "fk": fk,
                "link": link,
                "metadata": metadata,
                "timestamp": timestamp,
                "is_file_upload": is_file_upload,
                "ingestor": ingestor,
                "is_marked_for_deletion": is_marked_for_deletion,
            }
        )
        if object_type is not UNSET:
            field_dict["object_type"] = object_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.exact_collection_entry_metadata import ExactCollectionEntryMetadata

        d = src_dict.copy()
        id = d.pop("id")

        fk = d.pop("fk")

        link = d.pop("link")

        metadata = ExactCollectionEntryMetadata.from_dict(d.pop("metadata"))

        timestamp = isoparse(d.pop("timestamp"))

        is_file_upload = d.pop("is_file_upload")

        ingestor = d.pop("ingestor")

        is_marked_for_deletion = d.pop("is_marked_for_deletion")

        object_type = cast(Union[Literal["ExactCollectionEntry"], Unset], d.pop("object_type", UNSET))
        if object_type != "ExactCollectionEntry" and not isinstance(object_type, Unset):
            raise ValueError(f"object_type must match const 'ExactCollectionEntry', got '{object_type}'")

        exact_collection_entry = cls(
            id=id,
            fk=fk,
            link=link,
            metadata=metadata,
            timestamp=timestamp,
            is_file_upload=is_file_upload,
            ingestor=ingestor,
            is_marked_for_deletion=is_marked_for_deletion,
            object_type=object_type,
        )

        exact_collection_entry.additional_properties = d
        return exact_collection_entry

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
