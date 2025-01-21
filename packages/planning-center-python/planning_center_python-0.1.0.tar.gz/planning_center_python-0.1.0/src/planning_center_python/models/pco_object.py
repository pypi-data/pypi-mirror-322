from collections.abc import Mapping
from typing import Any, ClassVar, Optional, cast
from planning_center_python.errors import InvalidParamsError, InvalidRequestError


class PCOObject:
    """Base class object from which all Planning Center objects should inherit from"""

    OBJECT_TYPE: ClassVar[str] = "BaseClass"

    def __init__(self, data: Mapping[str, Any] = {}, id: Optional[str] = None):
        self._data = data
        object_data = cast(Mapping[str, Any], data.get("data")) or {}
        self._id = id or object_data.get("id")
        self._type = object_data.get("type") or self.OBJECT_TYPE
        self._validate()

        if object_data:
            self._init_attributes(
                cast(Mapping[str, Any], object_data.get("attributes"))
            )

    # @classmethod
    # def retrieve(cls, id: str) -> Self:
    #     instance = cls(id=id)
    #     instance.refresh()
    #     return instance

    def _object_url(self) -> str:
        raise NotImplementedError

    def _instance_url(self) -> str:
        if not self.id:
            raise InvalidRequestError(
                "Cannot determine instance url without a valid id"
            )

        return "%s/%s" % (self._object_url(), self.id)

    # def refresh(self) -> None:
    #     """Makes a request to the API for the given object and refreshes
    #     the class properties.
    #     """
    #     response = self._client.request("get", self.instance_url())
    #     attributes = response.get("attributes")
    #     if attributes:
    #         self._refresh_props(attributes)

    # def _refresh_props(self, props: Dict[str, Any]) -> None:
    #     """Sets a class properties for each value passed in.

    #     Args:
    #         props (Dict[str, Any]): a set of values for which a property should be generated
    #     """
    #     self._init_attributes(props)

    # def _create_object(self, params: Dict[str, Any]) -> None:
    #     self._client.request("post", self._object_url(), payload=params)

    # def _update_object(self, params: Dict[str, Any]) -> None:
    #     self._client.request("patch", self._instance_url(), payload=params)

    # def _delete_object(self) -> None:
    #     self._client.request("delete", self._instance_url())

    def _validate(self):
        if not self.id:
            raise InvalidParamsError(self, "id")
        if not self.type:
            raise InvalidParamsError(self, "type")
        if self.type != self.OBJECT_TYPE:
            raise InvalidParamsError(self, "type", "Class types do not match")

    def _init_attributes(self, attributes: Mapping[str, Any]):
        for key, val in attributes.items():
            setattr(self, key, val)

    @property
    def id(self) -> str | None:
        return self._id

    @property
    def type(self) -> str | None:
        return self._type
