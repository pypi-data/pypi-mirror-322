from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.index_params import IndexParams


T = TypeVar("T", bound="Index")


@_attrs_define
class Index:
    """
    Attributes:
        index_type (str):
        metric_type (str):
        params (IndexParams):
        object_type (Union[Literal['Index'], Unset]):  Default: 'Index'.
    """

    index_type: str
    metric_type: str
    params: "IndexParams"
    object_type: Union[Literal["Index"], Unset] = "Index"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        index_type = self.index_type

        metric_type = self.metric_type

        params = self.params.to_dict()

        object_type = self.object_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "index_type": index_type,
                "metric_type": metric_type,
                "params": params,
            }
        )
        if object_type is not UNSET:
            field_dict["object_type"] = object_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.index_params import IndexParams

        d = src_dict.copy()
        index_type = d.pop("index_type")

        metric_type = d.pop("metric_type")

        params = IndexParams.from_dict(d.pop("params"))

        object_type = cast(Union[Literal["Index"], Unset], d.pop("object_type", UNSET))
        if object_type != "Index" and not isinstance(object_type, Unset):
            raise ValueError(f"object_type must match const 'Index', got '{object_type}'")

        index = cls(
            index_type=index_type,
            metric_type=metric_type,
            params=params,
            object_type=object_type,
        )

        index.additional_properties = d
        return index

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
