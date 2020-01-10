# Copyright (c) 2019-2020 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/licenses/zlib

from typing import List, Dict, Optional
from datetime import datetime
from uuid import UUID
from pathlib import Path

from public import public

from .. import model as base
from ..util import *  # noqa


@public
@inherit_docs
class RepId(base.RepId):

    def __new__(cls, *, id: int, module_id: int):
        self = super().__new__(cls)
        self.__id: int        = id
        self.__module_id: int = module_id
        return self

    id        = property(lambda self: self.__id)
    module_id = property(lambda self: self.__module_id)


@public
@inherit_docs
class Owner(base.Owner):

    def __new__(cls, *, name: str, is_group: bool=False):
        self = super().__new__(cls)
        self.__name: str      = name
        self.__is_group: bool = is_group
        return self

    name     = property(lambda self: self.__name)
    is_group = property(lambda self: self.__is_group)


@public
@inherit_docs
class Repository(base.Repository):

    def __new__(cls, *,
                name: str,
                server: str,
                owner: Optional[Owner],
                rep_id: Optional[RepId],
                guid: Optional[UUID]):
        self = super().__new__(cls)
        self.__name: str               = name
        self.__server: str             = server
        self.__owner: Optional[Owner]  = owner
        self.__rep_id: Optional[RepId] = rep_id
        self.__guid: Optional[UUID]    = guid
        return self

    name      = property(lambda self: self.__name)
    server    = property(lambda self: self.__server)
    full_name = property(lambda self: self.__name + "@" + self.__server)
    owner     = property(lambda self: self.__owner)
    rep_id    = property(lambda self: self.__rep_id)
    guid      = property(lambda self: self.__guid)


@public
@inherit_docs
class Workspace(base.Workspace):

    def __new__(cls, *,
                name: str,
                path: Path,
                machine_name: str,
                guid: UUID):
        self = super().__new__(cls)
        self.__name: str         = name
        self.__path: Path        = path
        self.__machine_name: str = machine_name
        self.__guid: UUID        = guid
        return self

    name         = property(lambda self: self.__name)
    path         = property(lambda self: self.__path)
    machine_name = property(lambda self: self.__machine_name)
    guid         = property(lambda self: self.__guid)


@public
@inherit_docs
class ObjectType(base.ObjectType):
    CHANGESET = "changeset"
    LABEL     = "label"
    BRANCH    = "branch"


@public
@inherit_docs
class Branch(base.Branch):

    def __new__(cls, *,
                name: str,
                id: int,
                parent_id: int,
                last_changeset_id: int,
                comment: Optional[str],
                creation_date: datetime,
                guid: UUID,
                owner: Optional[Owner],
                repository: Repository):
        self = super().__new__(cls)
        self.__name: str               = name
        self.__id: int                 = id
        self.__parent_id: int          = parent_id
        self.__last_changeset_id: int  = last_changeset_id
        self.__comment: Optional[str]  = comment
        self.__creation_date: datetime = creation_date
        self.__guid: UUID              = guid
        self.__owner: Optional[Owner]  = owner
        self.__repository: Repository  = repository
        return self

    name              = property(lambda self: self.__name)
    id                = property(lambda self: self.__id)
    parent_id         = property(lambda self: self.__parent_id)
    last_changeset_id = property(lambda self: self.__last_changeset_id)
    comment           = property(lambda self: self.__comment)
    creation_date     = property(lambda self: self.__creation_date)
    guid              = property(lambda self: self.__guid)
    owner             = property(lambda self: self.__owner)
    repository        = property(lambda self: self.__repository)


@public
@inherit_docs
class Label(base.Label):

    #
    # private String server;

    def __new__(cls, *,
                name: str,
                id: int,
                changeset_id: int,
                comment: Optional[str],
                creation_date: datetime,
                branch: Branch,
                owner: Optional[Owner],
                repository: Repository):
        self = super().__new__(cls)
        self.__name: str               = name
        self.__id: int                 = id
        self.__changeset_id: int       = changeset_id
        self.__comment: Optional[str]  = comment
        self.__creation_date: datetime = creation_date
        self.__branch: Branch          = branch
        self.__owner: Optional[Owner]  = owner
        self.__repository: Repository  = repository
        return self

    name          = property(lambda self: self.__name)
    id            = property(lambda self: self.__id)
    changeset_id  = property(lambda self: self.__changeset_id)
    comment       = property(lambda self: self.__comment)
    creation_date = property(lambda self: self.__creation_date)
    branch        = property(lambda self: self.__branch)
    owner         = property(lambda self: self.__owner)
    repository    = property(lambda self: self.__repository)


@public
@inherit_docs
class Changeset(base.Changeset):

    #
    # private String server;

    def __new__(cls, *,
                id: int,
                parent_id: int,
                comment: Optional[str],
                creation_date: datetime,
                guid: UUID,
                branch: Branch,
                owner: Optional[Owner],
                repository: Repository):
        self = super().__new__(cls)
        self.__id: int                 = id
        self.__parent_id: int          = parent_id
        self.__comment: Optional[str]  = comment
        self.__creation_date: datetime = creation_date
        self.__guid: UUID              = guid
        self.__branch: Branch          = branch
        self.__owner: Optional[Owner]  = owner
        self.__repository: Repository  = repository
        return self

    id            = property(lambda self: self.__id)
    parent_id     = property(lambda self: self.__parent_id)
    comment       = property(lambda self: self.__comment)
    creation_date = property(lambda self: self.__creation_date)
    guid          = property(lambda self: self.__guid)
    branch        = property(lambda self: self.__branch)
    owner         = property(lambda self: self.__owner)
    repository    = property(lambda self: self.__repository)


@public
@inherit_docs
class LocalInfo(base.LocalInfo):

    def __new__(cls, *,
                modified_time: datetime,
                size: int,
                is_missing: bool):
        self = super().__new__(cls)
        self.__modified_time: datetime = modified_time
        self.__size: int               = size
        self.__is_missing: bool        = is_missing
        return self

    modified_time = property(lambda self: self.__modified_time)
    size          = property(lambda self: self.__size)
    is_missing    = property(lambda self: self.__is_missing)


@public
@inherit_docs
class RevisionInfo(base.RevisionInfo):

    def __new__(cls, *,
                id: int,
                parent_id: int,
                item_id: int,
                type: str, # "text" # TODO change this to enum if possible
                size: int,
                hash: str, # str # "tLq1aWZ24MGupAHKZAgYFA=="
                branch_id: int,
                changeset_id: int,
                is_checked_out: bool,
                creation_date: datetime,
                rep_id: Optional[RepId],
                owner: Optional[Owner]):
        self = super().__new__(cls)
        self.__id: int                  = id
        self.__parent_id: int           = parent_id
        self.__item_id: int             = item_id
        self.__type                     = type
        self.__size: int                = size
        self.__hash                     = hash
        self.__branch_id: int           = branch_id
        self.__changeset_id: int        = changeset_id
        self.__is_checked_out: bool     = is_checked_out
        self.__creation_date: datetime  = creation_date
        self.__rep_id: Optional[RepId]  = rep_id
        self.__owner: Optional[Owner]   = owner
        return self

    id             = property(lambda self: self.__id)
    parent_id      = property(lambda self: self.__parent_id)
    item_id        = property(lambda self: self.__item_id)
    type           = property(lambda self: self.__type)
    size           = property(lambda self: self.__size)
    hash           = property(lambda self: self.__hash)
    branch_id      = property(lambda self: self.__branch_id)
    changeset_id   = property(lambda self: self.__changeset_id)
    is_checked_out = property(lambda self: self.__is_checked_out)
    creation_date  = property(lambda self: self.__creation_date)
    rep_id         = property(lambda self: self.__rep_id)
    owner          = property(lambda self: self.__owner)


@public
@inherit_docs
class RevisionHistoryItem(base.RevisionHistoryItem):

    def __new__(cls, *,
                type: str, # "text"
                revision_id: int,
                revision_link: Optional[str],
                changeset_id: int,
                changeset_link: Optional[str],
                branch_name: str,
                branch_link: Optional[str],
                repo_name: str,
                repo_link: Optional[str],
                comment: Optional[str],
                creation_date: datetime,
                owner: Optional[Owner]):
        self = super().__new__(cls)
        self.__type                          = type
        self.__revision_id: int              = revision_id
        self.__revision_link: Optional[str]  = revision_link
        self.__changeset_id: int             = changeset_id
        self.__changeset_link: Optional[str] = changeset_link
        self.__branch_name: str              = branch_name
        self.__branch_link: Optional[str]    = branch_link
        self.__repo_name: str                = repo_name
        self.__repo_link: Optional[str]      = repo_link
        self.__comment: Optional[str]        = comment
        self.__creation_date: datetime       = creation_date
        self.__owner: Optional[Owner]        = owner
        return self

    type           = property(lambda self: self.__type)
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


@public
@inherit_docs
class Change(base.Change):

    @inherit_docs
    class Type(base.Change.Type):
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

    def __new__(cls, *,
                changes: List[str],
                path: Path,
                old_path: Path,
                server_path: str,
                old_server_path: str,
                is_xlink: bool,
                local_info: LocalInfo,
                revision_info: RevisionInfo):
        self = super().__new__(cls)
        self.__changes: List[str]          = changes  # Pending of revision
        self.__path: Path                  = path
        self.__old_path: Path              = old_path
        self.__server_path: str            = server_path
        self.__old_server_path: str        = old_server_path
        self.__is_xlink: bool              = is_xlink        
        self.__local_info: LocalInfo       = local_info      
        self.__revision_info: RevisionInfo = revision_info   
        return self

    changes         = property(lambda self: self.__changes)
    path            = property(lambda self: self.__path)
    old_path        = property(lambda self: self.__old_path)
    server_path     = property(lambda self: self.__server_path)
    old_server_path = property(lambda self: self.__old_server_path)
    is_xlink        = property(lambda self: self.__is_xlink)
    local_info      = property(lambda self: self.__local_info)
    revision_info   = property(lambda self: self.__revision_info)


@public
@inherit_docs
class OperationStatus(base.OperationStatus):

    def __new__(cls, *,
                status:  Optional[str]=None,
                message: Optional[str]=None,
                total_files: Optional[int]=None,
                total_bytes: Optional[int]=None,
                updated_files: Optional[int]=None,
                updated_bytes: Optional[int]=None):
        self = super().__new__(cls)
        self.__status: Optional[str]  = status
        self.__message: Optional[str] = message
        self.__total_files: Optional[int] = total_files
        self.__total_bytes: Optional[int] = total_bytes
        self.__updated_files: Optional[int] = updated_files
        self.__updated_bytes: Optional[int] = updated_bytes
        return self

    status        = property(lambda self: self.__status)
    message       = property(lambda self: self.__message)
    total_files   = property(lambda self: self.__total_files   or 0) 
    total_bytes   = property(lambda self: self.__total_bytes   or 0) 
    updated_files = property(lambda self: self.__updated_files or 0) 
    updated_bytes = property(lambda self: self.__updated_bytes or 0) 


@public
@inherit_docs
class CheckinStatus(base.CheckinStatus):

    def __new__(cls, *,
                status: Optional[str]=None,
                message: Optional[str]=None,
                total_size: Optional[int]=None,
                transferred_size: Optional[int]=None):
        self = super().__new__(cls)
        self.__status: Optional[str]      = status
        self.__message: Optional[str]     = message
        self.__total: Optional[int]       = total_size
        self.__transferred: Optional[int] = transferred_size
        return self

    status           = property(lambda self: self.__status)
    message          = property(lambda self: self.__message)
    total_size       = property(lambda self: self.__total       or 0)
    transferred_size = property(lambda self: self.__transferred or 0)


@public
@inherit_docs
class XLink(base.XLink):

    def __new__(cls, *,
                changeset_id: int,
                changeset_guid: UUID,
                repo_name: str,
                server: str):
        self = super().__new__(cls)
        self.__changeset_id: int    = changeset_id
        self.__changeset_guid: UUID = changeset_guid
        self.__repo_name: str       = repo_name
        self.__server: str          = server
        return self

    changeset_id   = property(lambda self: self.__changeset_id)
    changeset_guid = property(lambda self: self.__changeset_guid)
    repo_name      = property(lambda self: self.__repo_name)
    server         = property(lambda self: self.__server)


@public
@inherit_docs
class Item(base.Item):

    @inherit_docs
    class Type(base.Item.Type):
        FILE      = "file"
        DIRECTORY = "directory"
        XLINK     = "xlink"

    #
    # private String server;

    def __new__(cls, *,
                type: Type,
                name: str,
                path: str,
                revision_id: Optional[int],
                size: int,
                is_under_xlink: Optional[bool],
                content: Optional[str],
                hash: Optional[str],
                items: Optional[List['Item']],
                xlink_target: Optional[XLink],
                repository: Optional[Repository]):
        self = super().__new__(cls)
        self.__type: Type                       = type
        self.__name: str                        = name
        self.__path: str                        = path
        self.__revision_id: Optional[int]       = revision_id
        self.__size: int                        = size
        self.__is_under_xlink: Optional[bool]   = is_under_xlink
        self.__content: Optional[str]           = content
        self.__hash: Optional[str]              = hash
        self.__items: Optional[List[Item]]      = items
        self.__xlink_target: Optional[XLink]    = xlink_target
        self.__repository: Optional[Repository] = repository
        return self

    type           = property(lambda self: self.__type)
    name           = property(lambda self: self.__name)
    path           = property(lambda self: self.__path)
    revision_id    = property(lambda self: self.__revision_id)
    size           = property(lambda self: self.__size)
    is_under_xlink = property(lambda self: self.__is_under_xlink)
    content        = property(lambda self: self.__content)
    hash           = property(lambda self: self.__hash)
    items          = property(lambda self: self.__items)
    xlink_target   = property(lambda self: self.__xlink_target)
    repository     = property(lambda self: self.__repository)


@public
@inherit_docs
class Merge(base.Merge):

    @inherit_docs
    class Type(base.Merge.Type):
        NONE     = "None"
        COPIED   = "Copied"
        REPLACED = "Replaced"
        MERGED   = "Merged"
        MOVED    = "Moved"
        DELETED  = "Deleted"
        ADDED    = "Added"
        ALL      = "All"

    def __new__(cls, *,
                merge_type: Type,
                source_changeset: Changeset):
        self = super().__new__(cls)
        self.__merge_type: Type            = merge_type
        self.__source_changeset: Changeset = source_changeset
        return self

    merge_type       = property(lambda self: self.__merge_type)
    source_changeset = property(lambda self: self.__source_changeset)


@public
@inherit_docs
class Diff(base.Diff):

    @inherit_docs
    class Status(base.Diff.Status):
        ADDED   = "Added"
        DELETED = "Deleted"
        MOVED   = "Moved"
        CHANGED = "Changed"

    def __new__(cls, *,
                status: Status,
                path: str,
                source_path: Optional[str],
                revision_id: Optional[int], # really optional ???
                source_revision_id: Optional[int],
                is_directory: bool,
                size: Optional[int], # really optional ???
                hash: Optional[str],        # str # "u0gJQzQnjLNUUHRI1+QQLg=="
                source_hash: Optional[str], # str # "u0gJQzQnjLNUUHRI1+QQLg=="
                is_under_xlink: bool,
                xlink: Optional[XLink],
                base_xlink: Optional[XLink],
                merges: Optional[List[Merge]],
                is_item_FS_protection_changed: bool,
                item_FS_protection: str,  # TODO change this to enum if possible
                repository: Repository,
                modified_time: Optional[datetime],
                created_by: Optional[Owner]):
        self = super().__new__(cls)
        self.__status: Status                      = status
        self.__path: str                           = path
        self.__source_path: Optional[str]          = source_path
        self.__revision_id: Optional[int]          = revision_id
        self.__source_revision_id: Optional[int]   = source_revision_id
        self.__is_directory: bool                  = is_directory
        self.__size: Optional[int]                 = size
        self.__hash: Optional[str]                 = hash
        self.__source_hash: Optional[str]          = source_hash
        self.__is_under_xlink: bool                = is_under_xlink
        self.__xlink: Optional[XLink]              = xlink
        self.__base_xlink: Optional[XLink]         = base_xlink
        self.__merges: Optional[List[Merge]]       = merges
        self.__is_item_FS_protection_changed: bool = is_item_FS_protection_changed
        self.__item_FS_protection: str             = item_FS_protection
        self.__repository: Repository              = repository
        self.__modified_time: Optional[datetime]   = modified_time
        self.__created_by: Optional[Owner]         = created_by
        return self

    status             = property(lambda self: self.__status)
    path               = property(lambda self: self.__path)
    source_path        = property(lambda self: self.__source_path)
    revision_id        = property(lambda self: self.__revision_id)
    source_revision_id = property(lambda self: self.__source_revision_id)
    is_directory       = property(lambda self: self.__is_directory)
    size               = property(lambda self: self.__size)
    hash               = property(lambda self: self.__hash)
    source_hash        = property(lambda self: self.__source_hash)
    is_under_xlink     = property(lambda self: self.__is_under_xlink)
    xlink              = property(lambda self: self.__xlink)
    base_xlink         = property(lambda self: self.__base_xlink)
    merges             = property(lambda self: self.__merges)
    is_item_FS_protection_changed = property(lambda self: 
                                    self.__is_item_FS_protection_changed)
    item_FS_protection = property(lambda self: self.__item_FS_protection)
    repository         = property(lambda self: self.__repository)
    modified_time      = property(lambda self: self.__modified_time)
    created_by         = property(lambda self: self.__created_by)


@public
@inherit_docs
class AffectedPaths(base.AffectedPaths):

    def __new__(cls, *, paths: List[Path]):
        self = super().__new__(cls)
        self.__paths: List[Path] = paths
        return self

    paths = property(lambda self: self.__paths) 
