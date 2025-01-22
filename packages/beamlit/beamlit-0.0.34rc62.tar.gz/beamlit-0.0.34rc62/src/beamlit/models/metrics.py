from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="Metrics")


@_attrs_define
class Metrics:
    """Metrics for resources

    Attributes:
        agents (Union[Unset, Any]): Metrics for agents
        functions (Union[Unset, Any]): Metrics for functions
        inference_global (Union[Unset, Any]): Historical requests for all resources globally
        models (Union[Unset, Any]): Metrics for models
        request_total (Union[Unset, Any]): Number of requests for all resources globally
        request_total_per_code (Union[Unset, Any]): Number of requests for all resources globally per code
        rps (Union[Unset, Any]): Number of requests per second for all resources globally
        rps_per_code (Union[Unset, Any]): Number of requests per second for all resources globally per code
    """

    agents: Union[Unset, Any] = UNSET
    functions: Union[Unset, Any] = UNSET
    inference_global: Union[Unset, Any] = UNSET
    models: Union[Unset, Any] = UNSET
    request_total: Union[Unset, Any] = UNSET
    request_total_per_code: Union[Unset, Any] = UNSET
    rps: Union[Unset, Any] = UNSET
    rps_per_code: Union[Unset, Any] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        agents = self.agents

        functions = self.functions

        inference_global = self.inference_global

        models = self.models

        request_total = self.request_total

        request_total_per_code = self.request_total_per_code

        rps = self.rps

        rps_per_code = self.rps_per_code

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if agents is not UNSET:
            field_dict["agents"] = agents
        if functions is not UNSET:
            field_dict["functions"] = functions
        if inference_global is not UNSET:
            field_dict["inferenceGlobal"] = inference_global
        if models is not UNSET:
            field_dict["models"] = models
        if request_total is not UNSET:
            field_dict["requestTotal"] = request_total
        if request_total_per_code is not UNSET:
            field_dict["requestTotalPerCode"] = request_total_per_code
        if rps is not UNSET:
            field_dict["rps"] = rps
        if rps_per_code is not UNSET:
            field_dict["rpsPerCode"] = rps_per_code

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        if not src_dict:
            return None
        d = src_dict.copy()
        agents = d.pop("agents", UNSET)

        functions = d.pop("functions", UNSET)

        inference_global = d.pop("inferenceGlobal", UNSET)

        models = d.pop("models", UNSET)

        request_total = d.pop("requestTotal", UNSET)

        request_total_per_code = d.pop("requestTotalPerCode", UNSET)

        rps = d.pop("rps", UNSET)

        rps_per_code = d.pop("rpsPerCode", UNSET)

        metrics = cls(
            agents=agents,
            functions=functions,
            inference_global=inference_global,
            models=models,
            request_total=request_total,
            request_total_per_code=request_total_per_code,
            rps=rps,
            rps_per_code=rps_per_code,
        )

        metrics.additional_properties = d
        return metrics

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
