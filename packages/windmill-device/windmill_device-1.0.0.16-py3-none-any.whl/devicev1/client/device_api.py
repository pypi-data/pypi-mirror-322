# -*- coding: utf-8 -*-
"""
Copyright(C) 2024 baidu, Inc. All Rights Reserved

# @Time : 2024/12/9 15:58
# @Author : leibin01
# @Email: leibin01@baidu.com
"""
from datetime import datetime
from enum import Enum
from typing import Optional, Any, Dict, TypeAlias, List

from bceinternalsdk.client.base_model import BaseModel
from bceinternalsdk.client.paging import PagingRequest
from pydantic import Field


class SpecKind(str, Enum):
    """
    The kind of spec.
    """
    K8S = "K8s"
    BIE = "BIE"


class ModuleConfigurationContent(BaseModel):
    """
    Module configuration content.
    """
    spec_kind: SpecKind = Field(default=SpecKind.BIE)
    content: Dict[str, Any]

class DeviceConfigurationContent(BaseModel):
    """
    Device configuration content.
    """
    device_group_name: str
    content: Any


class EdgeDeviceConfig(BaseModel):
    """
    Edge device configuration.
    """
    kind: Optional[str] = None
    gpu: Optional[str] = Field(None, alias="GPU")
    model_count: Optional[int] = None
    skill_count: Optional[int] = None
    datasource_count: Optional[int] = None


class Configuration(BaseModel):
    name: str
    local_name: str
    description: str

    device_content: Optional[DeviceConfigurationContent] = None
    modules_content: Optional[Dict[str, ModuleConfigurationContent]] = None
    device_configs: Optional[List[EdgeDeviceConfig]] = None
    selector: str
    priority: int
    tags: Dict[str, str]
    # ExtraData 其他配置，example:{"kinds":["DB-SL4", "DB-SH2", "DB-SH3", "DB-SH5"]}
    extra_data: Dict[str, Any]

    org_id: str
    user_id: str
    workspace_id: str
    device_hub_name: str

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config(BaseModel.Config):
        """
        Config is the configuration of the model.
        """

        use_uppercase_id = True


class GetConfigurationRequest(BaseModel):
    """
    Get configuration.
    """

    workspace_id: str
    device_hub_name: str
    local_name: str

    class Config(BaseModel.Config):
        """
        Config is the configuration of the model.
        """

        use_uppercase_id = True


GetConfigurationResponse: TypeAlias = Configuration


class ListDeviceRequest(PagingRequest):
    """
    Request for listing devices.
    """

    workspace_id: str = Field(alias="workspaceID")
    device_hub_name: str = Field(alias="deviceHubName")
    device_group_name: Optional[str] = Field(default=None, alias="deviceGroupName")
    status: Optional[str] = Field(default=None, alias="status")
    kind: Optional[str] = Field(default=None, alias="kind")
    dept_id: Optional[str] = Field(default=None, alias="deptID")
    filter: Optional[str] = Field(default=None, alias="filter")
    selects: Optional[list] = Field(default=None, alias="selects", max_items=100)
    deselects: Optional[list] = Field(default=None, alias="deselects", max_items=100)


class UpdateDeviceRequest(BaseModel):
    """
    Request for updating a device.
    """

    workspace_id: str = Field(alias="workspaceID")
    device_hub_name: str = Field(alias="deviceHubName")
    device_name: str = Field(alias="deviceName")
    display_name: Optional[str] = Field(default=None, alias="displayName")
    description: Optional[str] = Field(default=None, alias="description")
    tags: Optional[dict] = Field(default=None, alias="tags")
    status: Optional[str] = Field(default=None, alias="status")
    device_group_name: Optional[str] = Field(default=None, alias="deviceGroupName")
    category: Optional[str] = Field(default=None, alias="category")
    dept_id: Optional[str] = Field(default=None, alias="deptID")


class InvokeMethodHTTPRequest(BaseModel):
    """
    Request for invoking a method via HTTP.
    """
    workspace_id: str = Field(alias="workspaceID")
    device_hub_name: str = Field(alias="deviceHubName")
    device_name: str = Field(alias="deviceName")
    uri: str = Field(alias="uri")
    body: Optional[Any] = Field(default=None, alias="body")
    params: Optional[dict] = Field(default=None, alias="params")
    raw_query: Optional[str] = Field(default=None, alias="rawQuery")
