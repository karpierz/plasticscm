# Copyright (c) 2019 Adam Karpierz
# SPDX-License-Identifier: Zlib

from __future__ import annotations

from typing_extensions import Self
from datetime import datetime
from pathlib import Path
from uuid import UUID

from .. import model as base
from ..util import inherit_docs

__all__ = ('RepId', 'Owner', 'Repository', 'Workspace', 'ObjectType',
           'Branch', 'Label', 'Changeset', 'LocalInfo', 'RevisionInfo',
           'RevisionHistoryItem', 'Change', 'OperationStatus', 'CheckinStatus',
           'XLink', 'Item', 'Merge', 'Diff', 'AffectedPaths')


@inherit_docs
class RepId(base.RepId):

    __id: int
    __module_id: int

    def __new__(cls, *, id: int, module_id: int) -> Self:  # noqa A002
        """Constructor"""
        self = super().__new__(cls)
        self.__id        = id
        self.__module_id = module_id
        return self

    id        = property(lambda self: self.__id)  # noqa A003
    module_id = property(lambda self: self.__module_id)


@inherit_docs
class Owner(base.Owner):

    __name: str
    __is_group: bool

    def __new__(cls, *, name: str, is_group: bool = False) -> Self:
        """Constructor"""
        self = super().__new__(cls)
        self.__name     = name
        self.__is_group = is_group
        return self

    name     = property(lambda self: self.__name)
    is_group = property(lambda self: self.__is_group)


@inherit_docs
class Repository(base.Repository):

    __name: str
    __server: str
    __owner: Owner | None
    __rep_id: RepId | None
    __guid: UUID | None

    def __new__(cls, *,
                name: str,
                server: str,
                owner: Owner | None,
                rep_id: RepId | None,
                guid: UUID | None) -> Self:
        """Constructor"""
        self = super().__new__(cls)
        self.__name   = name
        self.__server = server
        self.__owner  = owner
        self.__rep_id = rep_id
        self.__guid   = guid
        return self

    name      = property(lambda self: self.__name)
    server    = property(lambda self: self.__server)
    full_name = property(lambda self: self.__name + "@" + self.__server)
    owner     = property(lambda self: self.__owner)
    rep_id    = property(lambda self: self.__rep_id)
    guid      = property(lambda self: self.__guid)


@inherit_docs
class Workspace(base.Workspace):

    __name: str
    __path: Path
    __machine_name: str
    __guid: UUID

    def __new__(cls, *,
                name: str,
                path: Path,
                machine_name: str,
                guid: UUID) -> Self:
        """Constructor"""
        self = super().__new__(cls)
        self.__name         = name
        self.__path         = path
        self.__machine_name = machine_name
        self.__guid         = guid
        return self

    name         = property(lambda self: self.__name)
    path         = property(lambda self: self.__path)
    machine_name = property(lambda self: self.__machine_name)
    guid         = property(lambda self: self.__guid)


@inherit_docs
class ObjectType(base.ObjectType):
    CHANGESET = "changeset"
    LABEL     = "label"
    BRANCH    = "branch"


@inherit_docs
class Branch(base.Branch):

    __name: str
    __id: int
    __parent_id: int
    __last_changeset_id: int
    __comment: str | None
    __creation_date: datetime
    __guid: UUID
    __owner: Owner | None
    __repository: Repository

    def __new__(cls, *,
                name: str,
                id: int,  # noqa A002
                parent_id: int,
                last_changeset_id: int,
                comment: str | None,
                creation_date: datetime,
                guid: UUID,
                owner: Owner | None,
                repository: Repository) -> Self:
        """Constructor"""
        self = super().__new__(cls)
        self.__name              = name
        self.__id                = id
        self.__parent_id         = parent_id
        self.__last_changeset_id = last_changeset_id
        self.__comment           = comment
        self.__creation_date     = creation_date
        self.__guid              = guid
        self.__owner             = owner
        self.__repository        = repository
        return self

    name              = property(lambda self: self.__name)
    id                = property(lambda self: self.__id)  # noqa A003
    parent_id         = property(lambda self: self.__parent_id)
    last_changeset_id = property(lambda self: self.__last_changeset_id)
    comment           = property(lambda self: self.__comment)
    creation_date     = property(lambda self: self.__creation_date)
    guid              = property(lambda self: self.__guid)
    owner             = property(lambda self: self.__owner)
    repository        = property(lambda self: self.__repository)


@inherit_docs
class Label(base.Label):

    __name: str
    __id: int
    __changeset_id: int
    __comment: str | None
    __creation_date: datetime
    __branch: Branch
    __owner: Owner | None
    __repository: Repository
    #
    # private String server;

    def __new__(cls, *,
                name: str,
                id: int,  # noqa A002
                changeset_id: int,
                comment: str | None,
                creation_date: datetime,
                branch: Branch,
                owner: Owner | None,
                repository: Repository) -> Self:
        """Constructor"""
        self = super().__new__(cls)
        self.__name          = name
        self.__id            = id
        self.__changeset_id  = changeset_id
        self.__comment       = comment
        self.__creation_date = creation_date
        self.__branch        = branch
        self.__owner         = owner
        self.__repository    = repository
        return self

    name          = property(lambda self: self.__name)
    id            = property(lambda self: self.__id)  # noqa A003
    changeset_id  = property(lambda self: self.__changeset_id)
    comment       = property(lambda self: self.__comment)
    creation_date = property(lambda self: self.__creation_date)
    branch        = property(lambda self: self.__branch)
    owner         = property(lambda self: self.__owner)
    repository    = property(lambda self: self.__repository)


@inherit_docs
class Changeset(base.Changeset):

    __id: int
    __parent_id: int
    __comment: str | None
    __creation_date: datetime
    __guid: UUID
    __branch: Branch
    __owner: Owner | None
    __repository: Repository
    #
    # private String server;

    def __new__(cls, *,
                id: int,  # noqa A002
                parent_id: int,
                comment: str | None,
                creation_date: datetime,
                guid: UUID,
                branch: Branch,
                owner: Owner | None,
                repository: Repository) -> Self:
        """Constructor"""
        self = super().__new__(cls)
        self.__id            = id
        self.__parent_id     = parent_id
        self.__comment       = comment
        self.__creation_date = creation_date
        self.__guid          = guid
        self.__branch        = branch
        self.__owner         = owner
        self.__repository    = repository
        return self

    id            = property(lambda self: self.__id)  # noqa A003
    parent_id     = property(lambda self: self.__parent_id)
    comment       = property(lambda self: self.__comment)
    creation_date = property(lambda self: self.__creation_date)
    guid          = property(lambda self: self.__guid)
    branch        = property(lambda self: self.__branch)
    owner         = property(lambda self: self.__owner)
    repository    = property(lambda self: self.__repository)


@inherit_docs
class LocalInfo(base.LocalInfo):

    __modified_time: datetime
    __size: int
    __is_missing: bool

    def __new__(cls, *,
                modified_time: datetime,
                size: int,
                is_missing: bool) -> Self:
        """Constructor"""
        self = super().__new__(cls)
        self.__modified_time = modified_time
        self.__size          = size
        self.__is_missing    = is_missing
        return self

    modified_time = property(lambda self: self.__modified_time)
    size          = property(lambda self: self.__size)
    is_missing    = property(lambda self: self.__is_missing)


@inherit_docs
class RevisionInfo(base.RevisionInfo):

    __id: int
    __parent_id: int
    __item_id: int
    __type: str
    __size: int
    __hash: str
    __branch_id: int
    __changeset_id: int
    __is_checked_out: bool
    __creation_date: datetime
    __rep_id: RepId | None
    __owner: Owner | None

    def __new__(cls, *,
                id: int,  # noqa A002
                parent_id: int,
                item_id: int,
                type: str,  # noqa A002 # "text" # TODO change this to enum if possible
                size: int,
                hash: str,  # noqa A002 # "tLq1aWZ24MGupAHKZAgYFA=="
                branch_id: int,
                changeset_id: int,
                is_checked_out: bool,
                creation_date: datetime,
                rep_id: RepId | None,
                owner: Owner | None) -> Self:
        """Constructor"""
        self = super().__new__(cls)
        self.__id             = id
        self.__parent_id      = parent_id
        self.__item_id        = item_id
        self.__type           = type
        self.__size           = size
        self.__hash           = hash
        self.__branch_id      = branch_id
        self.__changeset_id   = changeset_id
        self.__is_checked_out = is_checked_out
        self.__creation_date  = creation_date
        self.__rep_id         = rep_id
        self.__owner          = owner
        return self

    id             = property(lambda self: self.__id)  # noqa A003
    parent_id      = property(lambda self: self.__parent_id)
    item_id        = property(lambda self: self.__item_id)
    type           = property(lambda self: self.__type)  # noqa A003
    size           = property(lambda self: self.__size)
    hash           = property(lambda self: self.__hash)  # noqa A003
    branch_id      = property(lambda self: self.__branch_id)
    changeset_id   = property(lambda self: self.__changeset_id)
    is_checked_out = property(lambda self: self.__is_checked_out)
    creation_date  = property(lambda self: self.__creation_date)
    rep_id         = property(lambda self: self.__rep_id)
    owner          = property(lambda self: self.__owner)


@inherit_docs
class RevisionHistoryItem(base.RevisionHistoryItem):

    __type: str
    __revision_id: int
    __revision_link: str | None
    __changeset_id: int
    __changeset_link: str | None
    __branch_name: str
    __branch_link: str | None
    __repo_name: str
    __repo_link: str | None
    __comment: str | None
    __creation_date: datetime
    __owner: Owner | None

    def __new__(cls, *,
                type: str,  # noqa A002 # "text"
                revision_id: int,
                revision_link: str | None,
                changeset_id: int,
                changeset_link: str | None,
                branch_name: str,
                branch_link: str | None,
                repo_name: str,
                repo_link: str | None,
                comment: str | None,
                creation_date: datetime,
                owner: Owner | None) -> Self:
        """Constructor"""
        self = super().__new__(cls)
        self.__type           = type
        self.__revision_id    = revision_id
        self.__revision_link  = revision_link
        self.__changeset_id   = changeset_id
        self.__changeset_link = changeset_link
        self.__branch_name    = branch_name
        self.__branch_link    = branch_link
        self.__repo_name      = repo_name
        self.__repo_link      = repo_link
        self.__comment        = comment
        self.__creation_date  = creation_date
        self.__owner          = owner
        return self

    type           = property(lambda self: self.__type)  # noqa A003
    revision_id    = property(lambda self: self.__revision_id)
    revision_link  = property(lambda self: self.__revision_link)
    changeset_id   = property(lambda self: self.__changeset_id)
    changeset_link = property(lambda self: self.__changeset_link)
    branch_name    = property(lambda self: self.__branch_name)
    branch_link    = property(lambda self: self.__branch_link)
    repo_name      = property(lambda self: self.__repo_name)
    repo_link      = property(lambda self: self.__repo_link)
    comment        = property(lambda self: self.__comment)
    creation_date  = property(lambda self: self.__creation_date)
    owner          = property(lambda self: self.__owner)


@inherit_docs
class Change(base.Change):

    @inherit_docs
    class Type(base.Change.Type):  # noqa D106
        ADDED              = "added"
        CHECKED_OUT        = "checkout"
        CHANGED            = "changed"
        COPIED             = "copied"
        REPLACED           = "replaced"
        DELETED            = "deleted"
        LOCALLY_DELETED    = "localdeleted"
        MOVED              = "moved"
        LOCALLY_MOVED      = "localmoved"
        PRIVATE            = "private"
        IGNORED            = "ignored"
        HIDDEN_CHANGED     = "hiddenchanged"
        CONTROLLED_CHANGED = "controlledchanged"
        ALL                = "all"

    __changes: list[str]
    __path: Path
    __old_path: Path | None
    __server_path: str
    __old_server_path: str | None
    __is_xlink: bool
    __local_info: LocalInfo
    __revision_info: RevisionInfo

    def __new__(cls, *,
                changes: list[str],
                path: Path,
                old_path: Path | None,
                server_path: str,
                old_server_path: str | None,
                is_xlink: bool,
                local_info: LocalInfo,
                revision_info: RevisionInfo) -> Self:
        """Constructor"""
        self = super().__new__(cls)
        self.__changes         = changes  # Pending of revision
        self.__path            = path
        self.__old_path        = old_path
        self.__server_path     = server_path
        self.__old_server_path = old_server_path
        self.__is_xlink        = is_xlink
        self.__local_info      = local_info
        self.__revision_info   = revision_info
        return self

    changes         = property(lambda self: self.__changes)
    path            = property(lambda self: self.__path)
    old_path        = property(lambda self: self.__old_path)
    server_path     = property(lambda self: self.__server_path)
    old_server_path = property(lambda self: self.__old_server_path)
    is_xlink        = property(lambda self: self.__is_xlink)
    local_info      = property(lambda self: self.__local_info)
    revision_info   = property(lambda self: self.__revision_info)


@inherit_docs
class OperationStatus(base.OperationStatus):

    __status: str | None
    __message: str | None
    __total_files: int | None
    __total_bytes: int | None
    __updated_files: int | None
    __updated_bytes: int | None

    def __new__(cls, *,
                status:  str | None = None,
                message: str | None = None,
                total_files: int | None = None,
                total_bytes: int | None = None,
                updated_files: int | None = None,
                updated_bytes: int | None = None) -> Self:
        """Constructor"""
        self = super().__new__(cls)
        self.__status        = status
        self.__message       = message
        self.__total_files   = total_files
        self.__total_bytes   = total_bytes
        self.__updated_files = updated_files
        self.__updated_bytes = updated_bytes
        return self

    status        = property(lambda self: self.__status)
    message       = property(lambda self: self.__message)
    total_files   = property(lambda self: self.__total_files   or 0)
    total_bytes   = property(lambda self: self.__total_bytes   or 0)
    updated_files = property(lambda self: self.__updated_files or 0)
    updated_bytes = property(lambda self: self.__updated_bytes or 0)


@inherit_docs
class CheckinStatus(base.CheckinStatus):

    __status: str | None
    __message: str | None
    __total: int | None
    __transferred: int | None

    def __new__(cls, *,
                status: str | None = None,
                message: str | None = None,
                total_size: int | None = None,
                transferred_size: int | None = None) -> Self:
        """Constructor"""
        self = super().__new__(cls)
        self.__status      = status
        self.__message     = message
        self.__total       = total_size
        self.__transferred = transferred_size
        return self

    status           = property(lambda self: self.__status)
    message          = property(lambda self: self.__message)
    total_size       = property(lambda self: self.__total       or 0)
    transferred_size = property(lambda self: self.__transferred or 0)


@inherit_docs
class XLink(base.XLink):

    __changeset_id: int
    __changeset_guid: UUID
    __repo_name: str
    __server: str

    def __new__(cls, *,
                changeset_id: int,
                changeset_guid: UUID,
                repo_name: str,
                server: str) -> Self:
        """Constructor"""
        self = super().__new__(cls)
        self.__changeset_id   = changeset_id
        self.__changeset_guid = changeset_guid
        self.__repo_name      = repo_name
        self.__server         = server
        return self

    changeset_id   = property(lambda self: self.__changeset_id)
    changeset_guid = property(lambda self: self.__changeset_guid)
    repo_name      = property(lambda self: self.__repo_name)
    server         = property(lambda self: self.__server)


@inherit_docs
class Item(base.Item):

    @inherit_docs
    class Type(base.Item.Type):  # noqa D106
        FILE      = "file"
        DIRECTORY = "directory"
        XLINK     = "xlink"

    __type: Type
    __name: str
    __path: str
    __revision_id: int | None
    __size: int
    __is_under_xlink: bool | None
    __content: str | None
    __hash: str | None
    __items: list[Item] | None
    __xlink_target: XLink | None
    __repository: Repository | None
    #
    # private String server;

    def __new__(cls, *,
                type: Type,  # noqa A002
                name: str,
                path: str,
                revision_id: int | None,
                size: int,
                is_under_xlink: bool | None,
                content: str | None,
                hash: str | None,  # noqa A002
                items: list['Item'] | None,
                xlink_target: XLink | None,
                repository: Repository | None) -> Self:
        """Constructor"""
        self = super().__new__(cls)
        self.__type           = type  # noqa A003
        self.__name           = name
        self.__path           = path
        self.__revision_id    = revision_id
        self.__size           = size
        self.__is_under_xlink = is_under_xlink
        self.__content        = content
        self.__hash           = hash  # noqa A003
        self.__items          = items
        self.__xlink_target   = xlink_target
        self.__repository     = repository
        return self

    type           = property(lambda self: self.__type)  # noqa A003
    name           = property(lambda self: self.__name)
    path           = property(lambda self: self.__path)
    revision_id    = property(lambda self: self.__revision_id)
    size           = property(lambda self: self.__size)
    is_under_xlink = property(lambda self: self.__is_under_xlink)
    content        = property(lambda self: self.__content)
    hash           = property(lambda self: self.__hash)  # noqa A003
    items          = property(lambda self: self.__items)
    xlink_target   = property(lambda self: self.__xlink_target)
    repository     = property(lambda self: self.__repository)


@inherit_docs
class Merge(base.Merge):

    @inherit_docs
    class Type(base.Merge.Type):  # noqa D106
        NONE     = "None"
        COPIED   = "Copied"
        REPLACED = "Replaced"
        MERGED   = "Merged"
        MOVED    = "Moved"
        DELETED  = "Deleted"
        ADDED    = "Added"
        ALL      = "All"

    __merge_type: Merge.Type
    __source_changeset: Changeset

    def __new__(cls, *,
                merge_type: Type,
                source_changeset: Changeset) -> Self:
        """Constructor"""
        self = super().__new__(cls)
        self.__merge_type       = merge_type
        self.__source_changeset = source_changeset
        return self

    merge_type       = property(lambda self: self.__merge_type)
    source_changeset = property(lambda self: self.__source_changeset)


@inherit_docs
class Diff(base.Diff):

    @inherit_docs
    class Status(base.Diff.Status):  # noqa D106
        ADDED   = "Added"
        DELETED = "Deleted"
        MOVED   = "Moved"
        CHANGED = "Changed"

    __status: Diff.Status
    __path: str
    __source_path: str | None
    __revision_id: int | None
    __source_revision_id: int | None
    __is_directory: bool
    __size: int | None
    __hash: str | None
    __source_hash: str | None
    __is_under_xlink: bool
    __xlink: XLink | None
    __base_xlink: XLink | None
    __merges: list[Merge] | None
    __is_item_fs_protection_changed: bool
    __item_fs_protection: str
    __repository: Repository
    __modified_time: datetime | None
    __created_by: Owner | None

    def __new__(cls, *,
                status: Status,
                path: str,
                source_path: str | None,
                revision_id: int | None,  # really optional ???
                source_revision_id: int | None,
                is_directory: bool,
                size: int | None,  # really optional ???
                hash: str | None,  # noqa A003  # "u0gJQzQnjLNUUHRI1+QQLg=="
                source_hash: str | None,  # str # "u0gJQzQnjLNUUHRI1+QQLg=="
                is_under_xlink: bool,
                xlink: XLink | None,
                base_xlink: XLink | None,
                merges: list[Merge] | None,
                is_item_fs_protection_changed: bool,
                item_fs_protection: str,  # TODO change this to enum if possible
                repository: Repository,
                modified_time: datetime | None,
                created_by: Owner | None) -> Self:
        """Constructor"""
        self = super().__new__(cls)
        self.__status             = status
        self.__path               = path
        self.__source_path        = source_path
        self.__revision_id        = revision_id
        self.__source_revision_id = source_revision_id
        self.__is_directory       = is_directory
        self.__size               = size
        self.__hash               = hash
        self.__source_hash        = source_hash
        self.__is_under_xlink     = is_under_xlink
        self.__xlink              = xlink
        self.__base_xlink         = base_xlink
        self.__merges             = merges
        self.__is_item_fs_protection_changed = is_item_fs_protection_changed
        self.__item_fs_protection = item_fs_protection
        self.__repository         = repository
        self.__modified_time      = modified_time
        self.__created_by         = created_by
        return self

    status             = property(lambda self: self.__status)
    path               = property(lambda self: self.__path)
    source_path        = property(lambda self: self.__source_path)
    revision_id        = property(lambda self: self.__revision_id)
    source_revision_id = property(lambda self: self.__source_revision_id)
    is_directory       = property(lambda self: self.__is_directory)
    size               = property(lambda self: self.__size)
    hash               = property(lambda self: self.__hash)  # noqa A003
    source_hash        = property(lambda self: self.__source_hash)
    is_under_xlink     = property(lambda self: self.__is_under_xlink)
    xlink              = property(lambda self: self.__xlink)
    base_xlink         = property(lambda self: self.__base_xlink)
    merges             = property(lambda self: self.__merges)
    is_item_fs_protection_changed = property(lambda self:
                                    self.__is_item_fs_protection_changed)
    item_fs_protection = property(lambda self: self.__item_fs_protection)
    repository         = property(lambda self: self.__repository)
    modified_time      = property(lambda self: self.__modified_time)
    created_by         = property(lambda self: self.__created_by)


@inherit_docs
class AffectedPaths(base.AffectedPaths):

    __paths: list[Path]

    def __new__(cls, *, paths: list[Path]) -> Self:
        """Constructor"""
        self = super().__new__(cls)
        self.__paths = paths
        return self

    paths = property(lambda self: self.__paths)
