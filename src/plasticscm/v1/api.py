# Copyright (c) 2019-2020 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/licenses/zlib

from typing import List, Tuple, Dict, Optional, Union
from datetime import datetime
from uuid import UUID
from pathlib import Path
import json

from public import public
from dateutil.parser import isoparse

from ..rest import *  # noqa
from .model import *  # noqa


@public
class API:

    #
    # API Interface.
    #

    def __new__(cls,
                url: str="http://localhost:9090", *,
                http_username: Optional[str]=None,
                http_password: Optional[str]=None,
                ssl_verify: bool=True,
                timeout: Union[int, float]=None):
        self = super().__new__(cls)
        self.__api_url = "{}/api/v1".format(url)
        self.__http_username = http_username
        self.__http_username = http_password
        self.__ssl_verify = ssl_verify   # Whether SSL certificates should be validated
        self.__timeout = float(timeout) if timeout is not None else None
        return self

    # Repositories

    @REST.GET("/repos")
    def get_repositories(self) -> Tuple[Repository]:
        url, action = self.get_repositories.REST
        response = action(self.__api_url + url,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return tuple(self.__json2Repository(repo) for repo in response.json())

    @REST.POST("/repos")
    def create_repository(self, repo_name: str, *, server: Optional[str]=None) -> Repository:
        url, action = self.create_repository.REST
        params = {
            "name": repo_name,
        }
        if server is not None:
            params.update({"server": server})
        response = action(self.__api_url + url, data=params,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return self.__json2Repository(response.json())

    @REST.GET("/repos/{repo_name}")
    def get_repository(self, repo_name: str) -> Repository:
        url, action = self.get_repository.REST
        url = url.format(repo_name=repo_name)
        response = action(self.__api_url + url,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return self.__json2Repository(response.json())

    @REST.PUT("/repos/{repo_name}")
    def rename_repository(self, repo_name: str, repo_new_name: str) -> Repository:
        url, action = self.rename_repository.REST
        url = url.format(repo_name=repo_name)
        params = {
            "name": repo_new_name,
        }
        response = action(self.__api_url + url, data=params,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return self.__json2Repository(response.json())

    @REST.DELETE("/repos/{repo_name}")
    def delete_repository(self, repo_name: str) -> None:
        url, action = self.delete_repository.REST
        url = url.format(repo_name=repo_name)
        response = action(self.__api_url + url,
                          verify=self.__ssl_verify, timeout=self.__timeout)

    def __json2Repository(self, repo: Dict):
        return Repository(name=repo["name"],
                          server=repo["server"],
                          owner=Owner(name=repo["owner"]["name"],
                                      is_group=repo["owner"]["isGroup"])
                                if "owner" in repo else None,
                          rep_id=RepId(id=repo["repId"]["id"],
                                       module_id=repo["repId"]["moduleId"])
                                 if "repId" in repo else None,
                          guid=UUID("{" + repo["guid"] + "}")
                               if "guid" in repo else None)

    # Workspaces

    @REST.GET("/wkspaces")
    def get_workspaces(self) -> Tuple[Workspace]:
        url, action = self.get_workspaces.REST
        response = action(self.__api_url + url,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return tuple(self.__json2Workspace(wkspace) for wkspace in response.json())

    @REST.POST("/wkspaces")
    def create_workspace(self, wkspace_name: str, wkspace_path: Path, *,
                         repo_name: Optional[str]=None) -> Workspace:
        url, action = self.create_workspace.REST
        params = {
            "name": wkspace_name,
            "path": str(wkspace_path),
        }
        if repo_name is not None:
            params.update({"repository": repo_name})
        response = action(self.__api_url + url, data=params,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return self.__json2Workspace(response.json())

    @REST.GET("/wkspaces/{wkspace_name}")
    def get_workspace(self, wkspace_name: str) -> Workspace:
        url, action = self.get_workspace.REST
        url = url.format(wkspace_name=wkspace_name)
        response = action(self.__api_url + url,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return self.__json2Workspace(response.json())

    @REST.PATCH("/wkspaces/{wkspace_name}")                   # !!! was: -> Repository:
    def rename_workspace(self, wkspace_name: str, wkspace_new_name: str) -> Workspace:
        url, action = self.rename_workspace.REST
        url = url.format(wkspace_name=wkspace_name)
        params = {
            "name": wkspace_new_name,
        }
        response = action(self.__api_url + url, data=params,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return self.__json2Workspace(response.json())

    @REST.DELETE("/wkspaces/{wkspace_name}")
    def delete_workspace(self, wkspace_name: str) -> None:
        url, action = self.delete_workspace.REST
        url = url.format(wkspace_name=wkspace_name)
        response = action(self.__api_url + url,
                          verify=self.__ssl_verify, timeout=self.__timeout)

    def __json2Workspace(self, wkspace: Dict):
        return Workspace(name=wkspace["name"],
                         path=Path(wkspace["path"]),
                         machine_name=wkspace["machineName"],
                         guid=UUID("{" + wkspace["guid"] + "}"))

    # Branches

    @REST.GET("/repos/{repo_name}/branches")
    def get_branches(self, repo_name: str, *, query: Optional[str]=None) -> Tuple[Branch]:
        url, action = self.get_branches.REST
        url = url.format(repo_name=repo_name)
        params = {}
        if query is not None:
            params.update({"q": query})
        response = action(self.__api_url + url, params=params or None,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return tuple(self.__json2Branch(branch) for branch in response.json())

    @REST.POST("/repos/{repo_name}/branches")
    def create_branch(self,
                      repo_name: str,
                      branch_name: str,
                      origin_type: ObjectType,
                      origin: Union[str, int], *,
                      top_level: bool=False) -> Branch:
        url, action = self.create_branch.REST
        url = url.format(repo_name=repo_name)
        params = {
            "name":       branch_name.strip("/"),
            "originType": origin_type.value,
            "origin":     str(origin),
            "topLevel":   top_level,
        }
        response = action(self.__api_url + url, data=params,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return self.__json2Branch(response.json())

    @REST.GET("/repos/{repo_name}/branches/{branch_name}")
    def get_branch(self, repo_name: str, branch_name: str) -> Branch:
        url, action = self.get_branch.REST
        url = url.format(repo_name=repo_name,
                         branch_name=branch_name.strip("/"))
        response = action(self.__api_url + url,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return self.__json2Branch(response.json())

    @REST.PATCH("/repos/{repo_name}/branches/{branch_name}")
    def rename_branch(self, repo_name: str, branch_name: str, branch_new_name: str) -> Branch:
        url, action = self.rename_branch.REST
        url = url.format(repo_name=repo_name,
                         branch_name=branch_name.strip("/"))
        params = {
            "name": branch_new_name,
        }
        response = action(self.__api_url + url, data=params,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return self.__json2Branch(response.json())

    @REST.DELETE("/repos/{repo_name}/branches/{branch_name}")
    def delete_branch(self, repo_name: str, branch_name: str) -> None:
        url, action = self.delete_branch.REST
        url = url.format(repo_name=repo_name,
                         branch_name=branch_name.strip("/"))
        response = action(self.__api_url + url,
                          verify=self.__ssl_verify, timeout=self.__timeout)

    def __json2Branch(self, branch: Dict):
        return Branch(# ???
                      name=branch["name"],
                      id=branch["id"],
                      parent_id=branch["parentId"],
                      last_changeset_id=branch["lastChangeset"],
                      comment=branch.get("comment"),
                      creation_date=isoparse(branch["creationDate"]),
                      guid=UUID("{" + branch["guid"] + "}"),
                      owner=Owner(name=branch["owner"]["name"],
                                  is_group=branch["owner"]["isGroup"])
                            if "owner" in branch else None,
                      repository=self.__json2Repository(branch["repository"]))

    # Labels

    @REST.GET("/repos/{repo_name}/labels")
    def get_labels(self, repo_name: str, *, query: Optional[str]=None) -> Tuple[Label]:
        url, action = self.get_labels.REST
        url = url.format(repo_name=repo_name)
        params = {}
        if query is not None:
            params.update({"q": query})
        response = action(self.__api_url + url, params=params or None,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return tuple(self.__json2Label(label) for label in response.json())

    @REST.POST("/repos/{repo_name}/labels")
    def create_label(self, repo_name: str, label_name: str, changeset_id: int, *,
                     comment: Optional[str]=None, apply_to_xlinks: bool=False) -> Label:
        url, action = self.create_label.REST
        url = url.format(repo_name=repo_name)
        params = {
            "name":          label_name,
            "changeset":     changeset_id,
            "applyToXlinks": apply_to_xlinks,
        }
        if comment is not None:
            params.update({"comment": comment})
        response = action(self.__api_url + url, data=params,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return self.__json2Label(response.json())

    @REST.GET("/repos/{repo_name}/labels/{label_name}")
    def get_label(self, repo_name: str, label_name: str) -> Label:
        url, action = self.get_label.REST
        url = url.format(repo_name=repo_name, label_name=label_name)
        response = action(self.__api_url + url,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return self.__json2Label(response.json())

    @REST.PATCH("/repos/{repo_name}/labels/{label_name}")
    def rename_label(self, repo_name: str, label_name: str, label_new_name: str) -> Label:
        url, action = self.rename_label.REST
        url = url.format(repo_name=repo_name, label_name=label_name)
        params = {
            "name": label_new_name,
        }
        response = action(self.__api_url + url, data=params,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return self.__json2Label(response.json())

    @REST.DELETE("/repos/{repo_name}/labels/{label_name}")
    def delete_label(self, repo_name: str, label_name: str) -> None:
        url, action = self.delete_label.REST
        url = url.format(repo_name=repo_name, label_name=label_name)
        response = action(self.__api_url + url,
                          verify=self.__ssl_verify, timeout=self.__timeout)

    def __json2Label(self, label: Dict):
        return Label(# ???
                     name=label["name"],
                     id=label["id"],
                     changeset_id=label["changeset"],
                     comment=label.get("comment"),
                     creation_date=isoparse(label["creationDate"]),
                     branch=self.__json2Branch(label["branch"]),
                     owner=Owner(name=label["owner"]["name"],
                                 is_group=label["owner"]["isGroup"])
                           if "owner" in label else None,
                     repository=self.__json2Repository(label["repository"]))

    # Changesets

    @REST.GET("/repos/{repo_name}/changesets")
    def get_changesets(self, repo_name: str, *, query: Optional[str]=None) -> Tuple[Changeset]:
        url, action = self.get_changesets.REST
        url = url.format(repo_name=repo_name)
        params = {}
        if query is not None:
            params.update({"q": query})
        response = action(self.__api_url + url, params=params or None,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return tuple(self.__json2Changeset(chset) for chset in response.json())

    @REST.GET("/repos/{repo_name}/branches/{branch_name}/changesets")
    def get_changesets_in_branch(self, repo_name: str, branch_name: str, *,
                                 query: Optional[str]=None) -> Tuple[Changeset]:
        url, action = self.get_changesets_in_branch.REST
        url = url.format(repo_name=repo_name,
                         branch_name=branch_name.strip("/"))
        params = {}
        if query is not None:
            params.update({"q": query})
        response = action(self.__api_url + url, params=params or None,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return tuple(self.__json2Changeset(chset) for chset in response.json())

    @REST.GET("/repos/{repo_name}/changesets/{changeset_id}")
    def get_changeset(self, repo_name: str, changeset_id: int) -> Changeset:
        url, action = self.get_changeset.REST
        url = url.format(repo_name=repo_name, changeset_id=changeset_id)
        response = action(self.__api_url + url,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return self.__json2Changeset(response.json())

    def __json2Changeset(self, chset: Dict):
        return Changeset(# ???
                         id=chset["id"],
                         parent_id=chset["parentId"],
                         comment=chset.get("comment"),
                         creation_date=isoparse(chset["creationDate"]),
                         guid=UUID("{" + chset["guid"] + "}"),
                         branch=self.__json2Branch(chset["branch"]),
                         owner=Owner(name=chset["owner"]["name"],
                                     is_group=chset["owner"]["isGroup"])
                               if "owner" in chset else None,
                         repository=self.__json2Repository(chset["repository"]))

    # Changes

    @REST.GET("/wkspaces/{wkspace_name}/changes")
    def get_pending_changes(self, wkspace_name: str, *,
                            change_types: List[Change.Type]=[Change.Type.ALL]) -> Tuple[Change]:
        url, action = self.get_pending_changes.REST
        url = url.format(wkspace_name=wkspace_name)
        params = {
            "types": ",".join(chtype.value for chtype in change_types),
        }
        response = action(self.__api_url + url, params=params,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return tuple(self.__json2Change(change) for change in response.json())

    @REST.DELETE("/wkspaces/{wkspace_name}/changes")
    def undo_pending_changes(self, wkspace_name: str, paths: List[Path]) -> AffectedPaths:
        url, action = self.undo_pending_changes.REST
        url = url.format(wkspace_name=wkspace_name)
        params = {
            "paths": [str(path) for path in paths],
        }
        response = action(self.__api_url + url, json=json.dumps(params),
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return self.__json2AffectedPaths(response.json())

    def __json2Change(self, change: Dict):
        return Change(# ???
                      changes=change["changes"],
                      path=Path(change["path"]),
                      old_path=Path(change["oldPath"]),
                      server_path=change["serverPath"],
                      old_server_path=change["oldServerPath"],
                      is_xlink=change["isXlink"],
                      local_info=LocalInfo(
                          modified_time=isoparse(change["localInfo"]["modifiedTime"]),
                          size=change["localInfo"]["size"],
                          is_missing=change["localInfo"]["isMissing"]),
                      revision_info=RevisionInfo(
                          id=change["revisionInfo"]["id"],
                          parent_id=change["revisionInfo"]["parentId"],
                          item_id=change["revisionInfo"]["itemId"],
                          type=change["revisionInfo"]["type"],
                          size=change["revisionInfo"]["size"],
                          hash=change["revisionInfo"]["hash"],
                          branch_id=change["revisionInfo"]["branchId"],
                          changeset_id=change["revisionInfo"]["changesetId"],
                          is_checked_out=change["revisionInfo"]["isCheckedOut"],
                          creation_date=isoparse(change["revisionInfo"]["creationDate"]),
                          rep_id=RepId(id=change["revisionInfo"]["repositoryId"]["id"],
                                       module_id=change["revisionInfo"]["repositoryId"]["moduleId"])
                                 if "repositoryId" in change["revisionInfo"] else None,
                          owner=Owner(name=change["revisionInfo"]["owner"]["name"],
                                      is_group=change["revisionInfo"]["owner"]["isGroup"])
                                if "owner" in change["revisionInfo"] else None))

    # Workspace Update and Switch

    @REST.GET("/wkspaces/{wkspace_name}/update")
    def get_workspace_update_status(self, wkspace_name: str) -> OperationStatus:
        url, action = self.get_workspace_update_status.REST
        url = url.format(wkspace_name=wkspace_name)
        response = action(self.__api_url + url,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return self.__json2OperationStatus(response.json())

    @REST.POST("/wkspaces/{wkspace_name}/update")
    def update_workspace(self, wkspace_name: str) -> OperationStatus:
        url, action = self.update_workspace.REST
        url = url.format(wkspace_name=wkspace_name)
        response = action(self.__api_url + url,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return self.__json2OperationStatus(response.json())

    @REST.GET("/wkspaces/{wkspace_name}/switch")
    def get_workspace_switch_status(self, wkspace_name: str) -> OperationStatus:
        url, action = self.get_workspace_switch_status.REST
        url = url.format(wkspace_name=wkspace_name)
        response = action(self.__api_url + url,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return self.__json2OperationStatus(response.json())

    @REST.POST("/wkspaces/{wkspace_name}/switch")
    def switch_workspace(self, wkspace_name: str,
                         object_type: ObjectType,
                         object: Union[str, int]) -> OperationStatus:
        url, action = self.switch_workspace.REST
        url = url.format(wkspace_name=wkspace_name)
        params = {
            "objectType": object_type.value,
            "object":     str(object),
        }
        response = action(self.__api_url + url, data=params,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return self.__json2OperationStatus(response.json())

    def __json2OperationStatus(self, stat: Dict):
        return OperationStatus(status=stat.get("status"),
                               message=stat.get("message"),
                               total_files=stat.get("totalFiles"),
                               total_bytes=stat.get("totalBytes"),
                               updated_files=stat.get("updatedFiles"),
                               updated_bytes=stat.get("updatedBytes"))

    # Checkin

    @REST.GET("/wkspaces/{wkspace_name}/checkin")
    def get_workspace_checkin_status(self, wkspace_name: str) -> CheckinStatus:
        url, action = self.get_workspace_checkin_status.REST
        url = url.format(wkspace_name=wkspace_name)
        response = action(self.__api_url + url,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return self.__json2CheckinStatus(response.json())

    @REST.POST("/wkspaces/{wkspace_name}/checkin")
    def checkin_workspace(self, wkspace_name: str, *,
                          paths: Optional[List[str]]=None,
                          comment: Optional[str]=None,
                          recurse: bool=True) -> CheckinStatus:
        url, action = self.checkin_workspace.REST
        url = url.format(wkspace_name=wkspace_name)
        params = {
            "recurse": recurse,
        }
        if paths is not None:
            params.update({"paths": paths})
        if comment is not None:
            params.update({"comment": comment})
        response = action(self.__api_url + url, data=params,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return self.__json2CheckinStatus(response.json())

    def __json2CheckinStatus(self, stat: Dict):
        return CheckinStatus(status=stat.get("status"),
                             message=stat.get("message"),
                             total_size=stat.get("totalSize"),
                             transferred_size=stat.get("transferredSize"))

    # Repository contents

    @REST.GET("/repos/{repo_name}/contents/{item_path}")
    def get_item(self, repo_name: str, item_path: str) -> Item:
        url, action = self.get_item.REST
        url = url.format(repo_name=repo_name,
                         item_path=item_path.strip("/"))
        response = action(self.__api_url + url,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return self.__json2Item(response.json())

    @REST.GET("/repos/{repo_name}/branches/{branch_name}/contents/{item_path}")
    def get_item_in_branch(self, repo_name: str, branch_name: str, item_path: str) -> Item:
        url, action = self.get_item_in_branch.REST
        url = url.format(repo_name=repo_name,
                         branch_name=branch_name.strip("/"),
                         item_path=item_path.strip("/"))
        response = action(self.__api_url + url,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return self.__json2Item(response.json())

    @REST.GET("/repos/{repo_name}/changesets/{changeset_id}/contents/{item_path}")
    def get_item_in_changeset(self, repo_name: str, changeset_id: int, item_path: str) -> Item:
        url, action = self.get_item_in_changeset.REST
        url = url.format(repo_name=repo_name,
                         changeset_id=changeset_id,
                         item_path=item_path.strip("/"))
        response = action(self.__api_url + url,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return self.__json2Item(response.json())

    @REST.GET("/repos/{repo_name}/labels/{label_name}/contents/{item_path}")
    def get_item_in_label(self, repo_name: str, label_name: str, item_path: str) -> Item:
        url, action = self.get_item_in_label.REST
        url = url.format(repo_name=repo_name,
                         label_name=label_name,
                         item_path=item_path.strip("/"))
        response = action(self.__api_url + url,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return self.__json2Item(response.json())

    @REST.GET("/repos/{repo_name}/revisions/{revision_spec}")
    def get_item_revision(self, repo_name: str, revision_spec: str) -> Item:
        url, action = self.get_item_revision.REST
        url = url.format(repo_name=repo_name,
                         revision_spec=revision_spec.strip("/"))
        response = action(self.__api_url + url,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return self.__json2Item(response.json())

    @REST.GET("/repos/{repo_name}/branches/{branch_name}/history/{item_path}")
    def get_item_revision_history_in_branch(self, repo_name: str, branch_name: str, item_path: str) -> Tuple[RevisionHistoryItem]:
        url, action = self.get_item_revision_history_in_branch.REST
        url = url.format(repo_name=repo_name,
                         branch_name=branch_name.strip("/"),
                         item_path=item_path.strip("/"))
        response = action(self.__api_url + url,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return tuple(self.__json2RevisionHistoryItem(item) for item in response.json())

    @REST.GET("/repos/{repo_name}/changesets/{changeset_id}/history/{item_path}")
    def get_item_revision_history_in_changeset(self, repo_name: str, changeset_id: int, item_path: str) -> Tuple[RevisionHistoryItem]:
        url, action = self.get_item_revision_history_in_changeset.REST
        url = url.format(repo_name=repo_name,
                         changeset_id=changeset_id,
                         item_path=item_path.strip("/"))
        response = action(self.__api_url + url,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return tuple(self.__json2RevisionHistoryItem(item) for item in response.json())

    @REST.GET("/repos/{repo_name}/labels/{label_name}/history/{item_path}")
    def get_item_revision_history_in_label(self, repo_name: str, label_name: str, item_path: str) -> Tuple[RevisionHistoryItem]:
        url, action = self.get_item_revision_history_in_label.REST
        url = url.format(repo_name=repo_name,
                         label_name=label_name,
                         item_path=item_path.strip("/"))
        response = action(self.__api_url + url,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return tuple(self.__json2RevisionHistoryItem(item) for item in response.json())

    def __json2Item(self, item: Dict):
        return Item(# ???
                    type=next(itype for itype in Item.Type
                              if itype.value == item["type"]),
                    name=item["name"],
                    path=item["path"],
                    revision_id=item.get("revisionId"), # Optional ???
                    size=item["size"],
                    is_under_xlink=item.get("isUnderXlink"),
                    content=item.get("content"),
                    hash=item.get("hash"),
                    items=[self.__json2Item(elem) for elem in item["items"]]
                          if "items" in item else None,
                    xlink_target=XLink(changeset_id=item["xlinkTarget"]["changesetId"],
                                       changeset_guid=item["xlinkTarget"]["changesetGuid"],
                                       repo_name=item["xlinkTarget"]["repository"],
                                       server=item["xlinkTarget"]["server"])
                                 if "xlinkTarget" in item else None,
                    repository=self.__json2Repository(item["repository"])
                               if "repository" in item else None)

    def __json2RevisionHistoryItem(self, rhitem: Dict):
        return RevisionHistoryItem(# ???
                                   type=rhitem["type"],
                                   revision_id=rhitem["revisionId"],
                                   revision_link=rhitem.get("revisionLink"),
                                   changeset_id=rhitem["changesetId"],
                                   changeset_link=rhitem.get("changesetLink"),
                                   branch_name=rhitem["branchName"],
                                   branch_link=rhitem.get("branchLink"),
                                   repo_name=rhitem["repositoryName"],
                                   repo_link=rhitem.get("repositoryLink"),
                                   comment=rhitem.get("comment"),
                                   creation_date=isoparse(rhitem["creationDate"]),
                                   owner=Owner(name=rhitem["owner"]["name"],
                                               is_group=rhitem["owner"]["isGroup"])
                                         if "owner" in rhitem else None)

    # Diff

    @REST.GET("/repos/{repo_name}/changesets/{changeset_id}/diff/{source_changeset_id}")
    def diff_changesets(self, repo_name: str, changeset_id: int, source_changeset_id: int) -> Tuple[Diff]:
        url, action = self.diff_changesets.REST
        url = url.format(repo_name=repo_name,
                         changeset_id=changeset_id,
                         source_changeset_id=source_changeset_id)
        response = action(self.__api_url + url,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return tuple(self.__json2Diff(diff) for diff in response.json())

    @REST.GET("/repos/{repo_name}/changesets/{changeset_id}/diff")
    def diff_changeset(self, repo_name: str, changeset_id: int) -> Tuple[Diff]:
        url, action = self.diff_changeset.REST
        url = url.format(repo_name=repo_name,
                         changeset_id=changeset_id)
        response = action(self.__api_url + url,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return tuple(self.__json2Diff(diff) for diff in response.json())

    @REST.GET("/repos/{repo_name}/branches/{branch_name}/diff")
    def diff_branch(self, repo_name: str, branch_name: str) -> Tuple[Diff]:
        url, action = self.diff_branch.REST
        url = url.format(repo_name=repo_name,
                         branch_name=branch_name.strip("/"))
        response = action(self.__api_url + url,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return tuple(self.__json2Diff(diff) for diff in response.json())

    def __json2Diff(self, diff: Dict):
        return Diff(# ???
                    status=next(item for item in Diff.Status
                                if item.value == diff["status"]),
                    path=diff["path"],
                    source_path=diff.get("srcPath"),
                    revision_id=diff.get("revisionId"),
                    source_revision_id=diff.get("srcRevisionId"),
                    is_directory=diff["isDirectory"],
                    size=diff.get("size"),
                    hash=diff.get("hash"),
                    source_hash=diff.get("srcHash"),
                    is_under_xlink=diff["isUnderXlink"],
                    xlink=XLink(changeset_id=diff["xlink"]["changesetId"], # Optional ???
                                changeset_guid=diff["xlink"]["changesetGuid"],
                                repo_name=diff["xlink"]["repository"],
                                server=diff["xlink"]["server"])
                          if "xlink" in diff else None,
                    base_xlink=XLink(changeset_id=diff["baseXlink"]["changesetId"], # Optional ???
                                     changeset_guid=diff["baseXlink"]["changesetGuid"],
                                     repo_name=diff["baseXlink"]["repository"],
                                     server=diff["baseXlink"]["server"])
                               if "baseXlink" in diff else None,
                    merges=[Merge(merge_type=next(item for item in Merge.Type
                                                  if item.value == merge["mergeType"]),
                                  source_changeset=self.__json2Changeset(merge["sourceChangeset"]))
                            for merge in diff["merges"]] if "merges" in diff else None,
                    is_item_FS_protection_changed=diff["isItemFSProtectionChanged"],
                    item_FS_protection=diff["itemFileSystemProtection"],  # TODO change this to enum if possible
                    repository=self.__json2Repository(diff["repository"]),
                    modified_time=isoparse(diff["modifiedTime"])
                                  if "modifiedTime" in diff else None,
                    created_by=Owner(name=diff["createdBy"]["name"],
                                     is_group=diff["createdBy"]["isGroup"])
                               if "createdBy" in diff else None)

    # Workspace actions

    @REST.POST("/wkspaces/{wkspace_name}/content/{item_path}")
    def add_workspace_item(self, wkspace_name: str, item_path: str, *,
                           add_parents: bool=True, checkout_parent: bool=True,
                           recurse: bool=True) -> AffectedPaths:
        url, action = self.add_workspace_item.REST
        url = url.format(wkspace_name=wkspace_name, item_path=item_path.strip("/"))
        params = {
            "addPrivateParents": add_parents,
            "checkoutParent":    checkout_parent,
            "recurse":           recurse,
        }
        response = action(self.__api_url + url, data=params,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return self.__json2AffectedPaths(response.json())

    @REST.PUT("/wkspaces/{wkspace_name}/content/{item_path}")
    def checkout_workspace_item(self, wkspace_name: str, item_path: str) -> AffectedPaths:
        url, action = self.checkout_workspace_item.REST
        url = url.format(wkspace_name=wkspace_name, item_path=item_path.strip("/"))
        response = action(self.__api_url + url,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return self.__json2AffectedPaths(response.json())

    @REST.PATCH("/wkspaces/{wkspace_name}/content/{item_path}")
    def move_workspace_item(self, wkspace_name: str, item_path: str,
                            dest_item_path: str) -> AffectedPaths:
        url, action = self.move_workspace_item.REST
        url = url.format(wkspace_name=wkspace_name, item_path=item_path.strip("/"))
        params = {
            "destination": dest_item_path,
        }
        response = action(self.__api_url + url, data=params,
                          verify=self.__ssl_verify, timeout=self.__timeout)
        return self.__json2AffectedPaths(response.json())

    def __json2AffectedPaths(self, paths: Dict):
        return AffectedPaths(paths=[Path(path) for path in paths["affectedPaths"]])
