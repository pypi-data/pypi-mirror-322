from io import BytesIO
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import File, FileJsonType

T = TypeVar("T", bound="BodyIngestWFileIngestFilePost")


@_attrs_define
class BodyIngestWFileIngestFilePost:
    """
    Attributes:
        file (Union[File, None]):
    """

    file: Union[File, None]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        file: Union[FileJsonType, None]
        if isinstance(self.file, File):
            file = self.file.to_tuple()

        else:
            file = self.file

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "file": file,
            }
        )

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        file: tuple[None, bytes, str]

        if isinstance(self.file, File):
            file = self.file.to_tuple()
        else:
            file = (None, str(self.file).encode(), "text/plain")

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update(
            {
                "file": file,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_file(data: object) -> Union[File, None]:
            if data is None:
                return data
            try:
                if not isinstance(data, bytes):
                    raise TypeError()
                file_type_0 = File(payload=BytesIO(data))

                return file_type_0
            except:  # noqa: E722
                pass
            return cast(Union[File, None], data)

        file = _parse_file(d.pop("file"))

        body_ingest_w_file_ingest_file_post = cls(
            file=file,
        )

        body_ingest_w_file_ingest_file_post.additional_properties = d
        return body_ingest_w_file_ingest_file_post

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
