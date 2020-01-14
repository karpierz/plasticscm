# Copyright (c) 2019-2020 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/licenses/zlib

_="""
All operations will be performed in the machine hosting the API server.
"""

from typing    import List, Tuple, Optional, Union
from types     import ModuleType
from pathlib   import Path
from importlib import import_module
import shutil

from public import public

from .model import *  # noqa
from . import config


@public
class Plastic:
    """ """

    @classmethod
    def from_config(cls,
                    plastic_id: Optional[str]=None,
                    config_files: Optional[List[str]]=None) -> 'Plastic':
        """Create a new PlasticSCM API wrapper from configuration files.

        Args:
            plastic_id:   ID of the configuration section.
            config_files: List of paths to configuration files.

        Returns:
            A PlasticSCM API wrapper.

        Raises:
            plasticscm.config.PlasticDataError: If the configuration is not correct.
        """
        if config_files is not None:
            config_files = [Path(file) for file in config_files]
        config = config.PlasticConfigParser(plastic_id=plastic_id,
                                            config_files=config_files)
        return cls(config.url,
                   http_username=config.http_username,
                   http_password=config.http_password,
                   ssl_verify=config.ssl_verify,
                   timeout=config.timeout,
                   api_version=config.api_version)

    def __new__(cls,
                url: str="http://localhost:9090", *,
                http_username: Optional[str]=None,
                http_password: Optional[str]=None,
                ssl_verify: bool=True,
                timeout: Union[int, float]=None,
                api_version: Union[str, int, float]="1"):
        """Instantiates a new PlasticSCM API wrapper.

        Args:
            url:         The endpoint of API, in format http://host:port
                         (default: "http://localhost:9090").
            timeout:     Timeout to use for requests to the PlasticSCM server.
            api_version: PlasticSCM API version to use (support for 1 only).

        """
        self = super().__new__(cls)
        self.__api_version = api_version = str(api_version)
        # Headers that will be used in request to PlasticSCM
        #self.headers = {"User-Agent": "%s/%s" % (__title__, __version__)}
        api   = import_module(".v{}.api".format(api_version),   __package__)
        model = import_module(".v{}.model".format(api_version), __package__)
        self.__api = api.API(url,
                             http_username=http_username,
                             http_password=http_password,
                             ssl_verify=ssl_verify,
                             timeout=timeout)
        self.__model = model
        #self.repositories = model.RepositoryManager(self)
        return self

    @property
    def api_version(self) -> str:
        """The API version used (1 only)."""
        return self.__api_version

    @property
    def model(self) -> ModuleType:
        """Classes of objects provided by the API."""
        return self.__model

    # Utils

    def get_cm_location(self) -> Path:
        """Get the path of cm.
        Raises:
            FileNotFoundError: If cm executable was not found.
        """
        path = shutil.which("cm")
        if path is None:
            raise FileNotFoundError("'cm' executable was not found")
        return Path(path)

    # Repositories

    def get_repositories(self) -> Tuple[Repository]:
        """Gets all available repositories of a server, along with their
        information.

        Returns:
            A list of the available repositories.
        """
        return self.__api.get_repositories()

    def create_repository(self, repo_name: str, *, server: Optional[str]=None) -> Repository:
        """Create a repository in a server.

        Args:
            repo_name: The name of the new repository.
            server:    The target server where the repository is to be created.
                       If it is omitted or if it is None, the repository will be
                       created in configured API server.

        Returns:
            The newly created repository will be returned once the operation
            is completed.
        """
        return self.__api.create_repository(repo_name, server=server)

    def get_repository(self, repo_name: str) -> Repository:
        """Gets the information concerning a single repository.

        Args:
            repo_name: The name of the repository.

        Returns:
            The desired repository will be returned once the operation
            is completed.
        """
        return self.__api.get_repository(repo_name)

    def rename_repository(self, repo_name: str,
                          repo_new_name: str) -> Repository:
        """Rename a repository.

        Args:
            repo_name:     The name of the repository to be renamed.
            repo_new_name: The new name of the repository.

        Returns:
            The updated repository will be returned once the operation
            is completed.
        """
        return self.__api.rename_repository(repo_name, repo_new_name)

    def delete_repository(self, repo_name: str) -> None:
        """Remove a repository from a server.

        Args:
            repo_name: The name of the repository to be removed.
        """
        return self.__api.delete_repository(repo_name)

    # Workspaces

    def get_workspaces(self) -> Tuple[Workspace]:
        """Gets all registered workspaces, along with their information.

        Returns:
            A list of the all registered workspaces.
        """
        return self.__api.get_workspaces()

    def create_workspace(self, wkspace_name: str, wkspace_path: Path, *,
                         repo_name: Optional[str]=None) -> Workspace:
        """Create a new workspace.

        Args:
            wkspace_name: The name of the new workspace.
            wkspace_path: The absolute path of the new workspace.
            repo_name:    The repository of the new workspace.

        Returns:
            The newly created workspace will be returned once the operation
            is completed.
        """
        return self.__api.create_workspace(wkspace_name, wkspace_path, repo_name=repo_name)

    def get_workspace(self, wkspace_name: str) -> Workspace:
        """Gets the information concerning a single workspace.

        Args:
            wkspace_name: The name of the workspace.

        Returns:
            The desired workspace will be returned once the operation
            is completed.
        """
        return self.__api.get_workspace(wkspace_name)

    def rename_workspace(self, wkspace_name: str, wkspace_new_name: str) -> Workspace:
        """Rename a workspace.

        Args:
            wkspace_name:     The name of the workspace to be renamed.
            wkspace_new_name: The new name of the workspace.

        Returns:
            The updated workspace will be returned once the operation
            is completed.
        """
        return self.__api.rename_workspace(wkspace_name, wkspace_new_name)

    def delete_workspace(self, wkspace_name: str) -> None:
        """Remove a workspace.

        Args:
            wkspace_name: The name of the workspace to be removed.
        """
        return self.__api.delete_workspace(wkspace_name)

    # Branches

    def get_branches(self, repo_name: str, *, query: Optional[str]=None) -> Tuple[Branch]:
        """Gets branches in a repository, along with their information.

        Args:
            repo_name: The name of the branches's host repository.
            query:     An optional constraints string using the 'cm find'
                       command syntax.

        Returns:
            A list of all branches in a repository.
        """
        return self.__api.get_branches(repo_name, query=query)

    def create_branch(self,
                      repo_name: str,
                      branch_name: str,
                      origin_type: ObjectType,
                      origin: Union[str, int], *,
                      top_level: bool=False) -> Branch:
        """Create a new branch.

        Args:
            repo_name:   The name of the host repository of the new branch.
            branch_name: The name of the new branch.
                         Do NOT use a hierarchical name.
            origin_type: The type of the origin of the branch.
                         It should be ObjectType.CHANGESET, ObjectType.LABEL
                         or ObjectType.BRANCH.
            origin:      The point of origin from which the branch will be
                         created.
            top_level:   Whether or not the branch will be top-level - i.e.
                         it will have no parent (default: False).

        Returns:
            The newly created branch will be returned once the operation
            is completed.
        """
        return self.__api.create_branch(repo_name, branch_name,
                                        origin_type, origin, top_level=top_level)

    def get_branch(self, repo_name: str, branch_name: str) -> Branch:
        """Gets information about a single branch in a repository.

        Args:
            repo_name:   The repository hosting the desired branch.
            branch_name: The name of the desired branch.
                         Please note that branch names are hierarchical
                         (e.g. "main/task001/task002").

        Returns:
            The desired branch will be returned once the operation
            is completed.
        """
        return self.__api.get_branch(repo_name, branch_name)

    def rename_branch(self, repo_name: str, branch_name: str,
                      branch_new_name: str) -> Branch:
        """Rename a branch.

        Args:
            repo_name:       The name of the host repository of the branch.
            branch_name:     The hierarchical name of the branch to be renamed.
                             Please note that branch names are hierarchical
                             (e.g. "main/task001/task002").
            branch_new_name: The new name of the branch.
                             Please have in mind that the hierarchy name
                             can not be changed.

        Returns:
            The updated branch will be returned once the operation
            is completed.
        """
        return self.__api.rename_branch(repo_name, branch_name, branch_new_name)

    def delete_branch(self, repo_name: str, branch_name: str) -> None:
        """Remove a branch.

        Args:
            repo_name:   The name of the host repository of the branch
            branch_name: The name of the branch to be removed.
                         Please note that branch names are hierarchical
                         (e.g. "main/task001/task002").
        """
        return self.__api.delete_branch(repo_name, branch_name)

    # Labels

    def get_labels(self, repo_name: str, *, query: Optional[str]=None) -> Tuple[Label]:
        """Gets labels in a repository, along with their information.

        Args:
            repo_name: The name of the host repository of the labels.
            query:     An optional constraints string using the 'cm find'
                       command syntax.

        Returns:
            A list of all labels in a repository.
        """
        return self.__api.get_labels(repo_name, query=query)

    def create_label(self, repo_name: str, label_name: str, changeset_id: int, *,
                     comment: Optional[str]=None, apply_to_xlinks: bool=False) -> Label:
        """Create a new label and applies it to a given changeset.


        Args:
            repo_name:       The name of the future host repository.
            label_name:      The name of the new label.
            changeset_id:    The changeset to label.
            comment:         The comment to add to the label.
            apply_to_xlinks: If True, all xlinked changesets present in the
                             specified changeset tree will be labelled as well
                             (default: False).

        Returns:
            The newly created label will be returned once the operation
            is completed.
        """
        return self.__api.create_label(repo_name, label_name, changeset_id,
                                       comment=comment, apply_to_xlinks=apply_to_xlinks)

    def get_label(self, repo_name: str, label_name: str) -> Label:
        """Gets information about a single label.

        Args:
            repo_name:  The name of the host repository of the label.
            label_name: The name of the label.

        Returns:
            The desired label will be returned once the operation
            is completed.
        """
        return self.__api.get_label(repo_name, label_name)

    def rename_label(self, repo_name: str, label_name: str, label_new_name: str) -> Label:
        """Rename a label.

        Args:
            repo_name:      The name of the host repository of the label.
            label_name:     The name of the label to be renamed.
            label_new_name: The new name of the label.

        Returns:
            The updated label will be returned once the operation
            is completed.
        """
        return self.__api.rename_label(repo_name, label_name, label_new_name)

    def delete_label(self, repo_name: str, label_name: str) -> None:
        """Remove a label.

        Args:
            repo_name:  The name of the host repository of the label.
            label_name: The name of the label to be removed.
        """
        return self.__api.delete_label(repo_name, label_name)

    # Changesets

    def get_changesets(self, repo_name: str, *, query: Optional[str]=None) -> Tuple[Changeset]:
        """Gets changesets in a repository, along with their information.

        Args:
            repo_name: The name of the host repository of the changesets.
            query:     An optional constraints string using the 'cm find'
                       command syntax.

        Returns:
            A list of all changesets in a repository.
        """
        return self.__api.get_changesets(repo_name, query=query)

    def get_changesets_in_branch(self, repo_name: str, branch_name: str, *,
                                 query: Optional[str]=None) -> Tuple[Changeset]:
        """Gets changesets in a given branch, along with their information.

        Args:
            repo_name:   The name of the host repository of the branch.
            branch_name: The hierarchical name of the host branch.
                         Please note that branch names are hierarchical
                         (e.g. "main/task001/task002").
            query:       An optional constraints string using the 'cm find'
                         command syntax.

        Returns:
            A list of all changesets in a given branch.
        """
        return self.__api.get_changesets_in_branch(repo_name, branch_name, query=query)

    def get_changeset(self, repo_name: str, changeset_id: int) -> Changeset:
        """Gets information about a single changeset.

        Args:
            repo_name:    The name of the host repository of the changeset.
            changeset_id: The id of the changeset.

        Returns:
            The desired changeset will be returned once the operation
            is completed.
        """
        return self.__api.get_changeset(repo_name, changeset_id)

    # Changes

    def get_pending_changes(self, wkspace_name: str, *,
                            change_types: Optional[List[Change.Type]]=None) -> Tuple[Change]:
        """Gets pending changes in a workspace, along with their information.

        Args:
            wkspace_name: The name of the workspace.
            change_types: A list detailing the desired change types.
                          It should be a list of Change.Type's values
                          (default: all change types).

        Returns:
            A list of all penging changes of the desired change types.
        """
        if change_types is None:
            return self.__api.get_pending_changes(wkspace_name)
        else:
            return self.__api.get_pending_changes(wkspace_name, change_types=change_types)

    def undo_pending_changes(self, wkspace_name: str, paths: List[Path]) -> AffectedPaths:
        """Deletes the pending changes in a workspace.
        Paths must be a list of paths representing files with pending changes
        to be undone.

        Args:
            wkspace_name: The name of the workspace.
            paths:        A list of file paths with pending changes to be undone.
                          They can be either full paths or workspace-relative paths.

        Returns:
            The paths that were affected by the undo operation.
        """
        return self.__api.undo_pending_changes(wkspace_name, paths)

    # Workspace Update and Switch

    def get_workspace_update_status(self, wkspace_name: str) -> OperationStatus:
        """Gets the status of the last workspace update operation.

        Args:
            wkspace_name: The name of the workspace.

        Returns:
            The status of the last workspace update operation.
        """
        return self.__api.get_workspace_update_status(wkspace_name)

    def update_workspace(self, wkspace_name: str) -> OperationStatus:
        """Update the workspace and download latest changes.

        Args:
            wkspace_name: The name of the workspace.

        Returns:
            The status of the workspace update operation.
        """
        return self.__api.update_workspace(wkspace_name)

    def get_workspace_switch_status(self, wkspace_name: str) -> OperationStatus:
        """Gets the status of the last workspace switch operation.

        Args:
            wkspace_name: The name of the workspace.

        Returns:
            The status of the last workspace switch operation.
        """
        return self.__api.get_workspace_switch_status(wkspace_name)

    def switch_workspace(self, wkspace_name: str,
                         object_type: ObjectType, object: Union[str, int]) -> OperationStatus:
        """Switch the workspace to a branch, changeset or label.

        Args:
            wkspace_name: The name of the workspace.
            object_type:  The type of switch destination.
                          It should be ObjectType.CHANGESET, ObjectType.LABEL
                          or ObjectType.BRANCH.
            object:       The target point the workspace will be set to.
                          It should be (according to object_type) the changeset
                          id, the label name or the branch name.

        Returns:
            The status of the workspace switch operation.
        """
        return self.__api.switch_workspace(wkspace_name, object_type, object)

    # Checkin

    def get_workspace_checkin_status(self, wkspace_name: str) -> CheckinStatus:
        """Gets the status of the last workspace checkin operation.

        Args:
            wkspace_name: The name of the workspace.

        Returns:
            The status of the last workspace checkin operation.
        """
        return self.__api.get_workspace_checkin_status(wkspace_name)

    def checkin_workspace(self, wkspace_name: str, *,
                          paths: Optional[List[str]]=None,
                          comment: Optional[str]=None,
                          recurse: bool=True) -> CheckinStatus:
        """Stores changes in the repository.

        Args:
            wkspace_name: The name of the workspace.
            paths:        The list of target paths to be checked in.
                          Set to the workspace root if empty or not present.
            comment:      The checkin comment.
            recurse:      If set to True, directories present in the paths
                          parameter will have their children recursively
                          checked in. If paths is empty or not present,
                          its value is overridden to True (default: True).

        Returns:
            The status of the workspace checkin operation.
        """
        return self.__api.checkin_workspace(wkspace_name,
                                            paths=paths, comment=comment, recurse=recurse)

    # Repository contents

    def get_item(self, repo_name: str, item_path: str) -> Item:
        """Gets information about a single item in a repository.

        Args:
            repo_name: The name of the repository.
            item_path: The path of selected item.

        Returns:
            The desired item will be returned once the operation is completed.
        """
        return self.__api.get_item(repo_name, item_path)

    def get_item_in_branch(self, repo_name: str, branch_name: str, item_path: str) -> Item:
        """Gets information about a single item in the desired branch.

        Args:
            repo_name:   The name of the host repository of the branch.
            branch_name: The name of the branch.
                         Please note that branch names are hierarchical
                         (e.g. "main/task001/task002").
            item_path:   The path of selected item.

        Returns:
            The desired item will be returned once the operation is completed.
        """
        return self.__api.get_item_in_branch(repo_name, branch_name, item_path)

    def get_item_in_changeset(self, repo_name: str, changeset_id: int, item_path: str) -> Item:
        """Gets information about a single item in the desired changeset.

        Args:
            repo_name:    The name of the host repository of the changeset.
            changeset_id: The id of the changeset.
            item_path:    The path of selected item.

        Returns:
            The desired item will be returned once the operation is completed.
        """
        return self.__api.get_item_in_changeset(repo_name, changeset_id, item_path)

    def get_item_in_label(self, repo_name: str, label_name: str, item_path: str) -> Item:
        """Gets information about a single item in the desired label.

        Args:
            repo_name:  The name of the host repository of the label.
            label_name: The name of the label.
            item_path:  The path of selected item.

        Returns:
            The desired item will be returned once the operation is completed.
        """
        return self.__api.get_item_in_label(repo_name, label_name, item_path)

    def get_item_revision(self, repo_name: str, revision_spec: str) -> Item:
        """Load a single item's revision in the workspace and gets information
        about it.

        Args:
            repo_name:     The name of the repository.
            revision_spec: Specification of the selected revision.

        Returns:
            The desired item's revision will be returned once the operation
            is completed.
        """
        return self.__api.get_item_revision(repo_name, revision_spec)

    def get_item_revision_history_in_branch(self, repo_name: str, branch_name: str,
                                            item_path: str) -> Tuple[RevisionHistoryItem]:
        """Gets the item's revision history for a given branch.

        Args:
            repo_name:   The name of the host repository of the branch.
            branch_name: The name of the branch.
                         Please note that branch names are hierarchical
                         (e.g. "main/task001/task002").
            item_path:   The path of selected item.

        Returns:
            A list of all item's revision history items for a given branch.
        """
        return self.__api.get_item_revision_history_in_branch(repo_name, branch_name, item_path)

    def get_item_revision_history_in_changeset(self, repo_name: str, changeset_id: int,
                                               item_path: str) -> Tuple[RevisionHistoryItem]:
        """Gets the item's revision history for a given changeset.

        Args:
            repo_name:    The name of the host repository of the changeset.
            changeset_id: The id of the changeset.
            item_path:    The path of selected item.

        Returns:
            A list of all item's revision history items for a given changeset.
        """
        return self.__api.get_item_revision_history_in_changeset(repo_name, changeset_id,
                                                                 item_path)

    def get_item_revision_history_in_label(self, repo_name: str, label_name: str,
                                           item_path: str) -> Tuple[RevisionHistoryItem]:
        """Gets the item's revision history for a given label.

        Args:
            repo_name:  The name of the host repository of the label.
            label_name: The name of the label.
            item_path:  The path of selected item.

        Returns:
            A list of all item's revision history items for a given label.
        """
        return self.__api.get_item_revision_history_in_label(repo_name, label_name, item_path)

    # Diff

    def diff_changesets(self, repo_name: str,
                        changeset_id: int, source_changeset_id: int) -> Tuple[Diff]:
        """Gets the differences between the source changeset and the desired
        changeset.

        Args:
            repo_name:    The name of the host repository of the changesets.
            changeset_id: The id of the changeset.
            source_changeset_id: The id of the source changeset.

        Returns:
            A list of all differences between the source changeset and the
            desired changeset.
        """
        return self.__api.diff_changesets(repo_name, changeset_id, source_changeset_id)

    def diff_changeset(self, repo_name: str, changeset_id: int) -> Tuple[Diff]:
        """Gets the differences between the parent changeset and the desired
        changeset.

        Args:
            repo_name:    The name of the host repository of the changeset.
            changeset_id: The id of the changeset.

        Returns:
            A list of all differences between the parent changeset and the
            desired changeset.
        """
        return self.__api.diff_changeset(repo_name, changeset_id)

    def diff_branch(self, repo_name: str, branch_name: str) -> Tuple[Diff]:
        """Gets the differences between the current branch and the desired
        branch.

        Args:
            repo_name:   The name of the host repository of the branch.
            branch_name: The name of the branch.
                         Please note that branch names are hierarchical
                         (e.g. "main/task001/task002").

        Returns:
            A list of all differences between the current branch and the
            desired branch.
        """
        return self.__api.diff_branch(repo_name, branch_name)

    # Workspace actions

    def add_workspace_item(self, wkspace_name: str, item_path: str, *,
                           add_parents: bool=True, checkout_parent: bool=True,
                           recurse: bool=True) -> AffectedPaths:
        """Add an item to version control.

        Args:
            wkspace_name:    The name of the workspace.
            item_path:       The path of the item to be added. 
            add_parents:     If True, the command will add any parent
                             directories which are not under version control
                             yet (default: True).
            checkout_parent: If True, the parent node of the selected item
                             will be checked out as a result (default: True).
            recurse:         If True, causes all the children items to be
                             recursively added (default: True).

        Returns:
            The paths that were affected by the addition operation.
        """
        return self.__api.add_workspace_item(wkspace_name, item_path,
                                             add_parents=add_parents,
                                             checkout_parent=checkout_parent,
                                             recurse=recurse)

    def checkout_workspace_item(self, wkspace_name: str, item_path: str) -> AffectedPaths:
        """Mark workspace item as ready to modify.

        Args:
            wkspace_name: The name of the workspace.
            item_path:    The path of selected item.

        Returns:
            The paths that were affected by the checkout operation.
        """
        return self.__api.checkout_workspace_item(wkspace_name, item_path)

    def move_workspace_item(self, wkspace_name: str,
                            item_path: str, dest_item_path: str) -> AffectedPaths:
        """Move or rename a file or directory in the workspace.

        Args:
            wkspace_name:   The name of the workspace.
            item_path:      Source path of selected item.
            dest_item_path: Destination path to move the selected item
                            (e.g. "src/bar.c").

        Returns:
            The paths that were affected by the movement operation.
        """
        return self.__api.move_workspace_item(wkspace_name, item_path, dest_item_path)
