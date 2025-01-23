from typing import TYPE_CHECKING, Any, Literal, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.hit_result import HitResult


T = TypeVar("T", bound="Hit")


@_attrs_define
class Hit:
    """
    Attributes:
        id (Union[int, str]):
        distance (float):
        result (HitResult):
        object_type (Union[Literal['Hit'], Unset]):  Default: 'Hit'.
    """

    id: Union[int, str]
    distance: float
    result: "HitResult"
    object_type: Union[Literal["Hit"], Unset] = "Hit"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id: Union[int, str]
        id = self.id

        distance = self.distance

        result = self.result.to_dict()

        object_type = self.object_type

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "distance": distance,
                "result": result,
            }
        )
        if object_type is not UNSET:
            field_dict["object_type"] = object_type

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.hit_result import HitResult

        d = src_dict.copy()

        def _parse_id(data: object) -> Union[int, str]:
            return cast(Union[int, str], data)

        id = _parse_id(d.pop("id"))

        distance = d.pop("distance")

        result = HitResult.from_dict(d.pop("result"))

        object_type = cast(Union[Literal["Hit"], Unset], d.pop("object_type", UNSET))
        if object_type != "Hit" and not isinstance(object_type, Unset):
            raise ValueError(f"object_type must match const 'Hit', got '{object_type}'")

        hit = cls(
            id=id,
            distance=distance,
            result=result,
            object_type=object_type,
        )

        hit.additional_properties = d
        return hit

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
