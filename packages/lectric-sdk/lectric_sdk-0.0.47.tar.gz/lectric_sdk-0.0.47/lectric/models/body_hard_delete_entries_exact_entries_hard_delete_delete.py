from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="BodyHardDeleteEntriesExactEntriesHardDeleteDelete")


@_attrs_define
class BodyHardDeleteEntriesExactEntriesHardDeleteDelete:
    """
    Attributes:
        entry_ids (Union[Unset, list[int], list[str]]):
        urls (Union[Unset, list[str]]):
    """

    entry_ids: Union[Unset, list[int], list[str]] = UNSET
    urls: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        entry_ids: Union[Unset, list[int], list[str]]
        if isinstance(self.entry_ids, Unset):
            entry_ids = UNSET
        elif isinstance(self.entry_ids, list):
            entry_ids = self.entry_ids

        else:
            entry_ids = self.entry_ids

        urls: Union[Unset, list[str]] = UNSET
        if not isinstance(self.urls, Unset):
            urls = self.urls

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if entry_ids is not UNSET:
            field_dict["entry_ids"] = entry_ids
        if urls is not UNSET:
            field_dict["urls"] = urls

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()

        def _parse_entry_ids(data: object) -> Union[Unset, list[int], list[str]]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                entry_ids_type_0 = cast(list[int], data)

                return entry_ids_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, list):
                raise TypeError()
            entry_ids_type_1 = cast(list[str], data)

            return entry_ids_type_1

        entry_ids = _parse_entry_ids(d.pop("entry_ids", UNSET))

        urls = cast(list[str], d.pop("urls", UNSET))

        body_hard_delete_entries_exact_entries_hard_delete_delete = cls(
            entry_ids=entry_ids,
            urls=urls,
        )

        body_hard_delete_entries_exact_entries_hard_delete_delete.additional_properties = d
        return body_hard_delete_entries_exact_entries_hard_delete_delete

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
