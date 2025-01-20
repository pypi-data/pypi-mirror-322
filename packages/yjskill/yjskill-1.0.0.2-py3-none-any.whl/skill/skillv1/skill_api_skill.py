# -*- coding: utf-8 -*-
"""
Copyright(C) 2024 baidu, Inc. All Rights Reserved

# @Time : 2024/12/9 15:58
# @Author : leibin01
# @Email: leibin01@baidu.com
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class GetSkillRequest(BaseModel):
    """
    Request for get skill.
    """

    workspace_id: str = Field(alias="workspaceID")
    local_name: str = Field(alias="localName")
    version: str = Field(alias="version")


class CreateSkillRequest(BaseModel):
    """
    Request for create skill.
    """

    class Config(ConfigDict):
        """
        Configuration for the request model.
        """

        arbitrary_types_allowed = True

    workspace_id: str = Field(alias="workspaceID")
    local_name: str = Field(alias="localName")
    display_name: str = Field(alias="displayName")
    description: Optional[str] = Field(default=None, alias="description")
    kind: str = Field(alias="kind")
    crerate_kind: str = Field(alias="createKind")
    from_kind: str = Field(alias="fromKind")
    tags: Optional[dict] = Field(default=None, alias="tags")
    graph: Optional[dict] = Field(default=None, alias="graph")
    image_uri: Optional[str] = Field(default=None, alias="imageURI")
    default_level: int = Field(default=4, alias="defaultLevel")
    alarm_configs: Optional[list] = Field(default=None, alias="alarmConfigs")
