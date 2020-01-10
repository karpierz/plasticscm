# Copyright (c) 2019-2020 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/licenses/zlib

from typing    import List, Tuple, Optional, Union
from pathlib   import Path
from importlib import import_module

from public import public

from .model import *  # noqa
from . import config


@public
class Plastic:

    @classmethod
    def from_config(cls,
                    plastic_id: Optional[str]=None,
                    config_files: Optional[List[str]]=None) -> 'Plastic':
        """Create a PlasticSCM connection from configuration files.

        Args:
            plastic_id:   ID of the configuration section.
            config_files: List of paths to configuration files.

        Returns:
            A PlasticSCM connection.

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
                timeout=None,
                api_version="1"):
        """Instantiates a new PlasticSCM API wrapper.

        Args:
            url: The endpoint of your API, in format _http://dir:port_
                 (default "http://localhost:9090")
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

    api_version = property(lambda self: self.__api_version,
                           doc="The API version used (1 only).")
    model       = property(lambda self: self.__model,
                           doc="The API version used (1 only).")

    # Repositories

    def get_repositories(self) -> Tuple[Repository]:
        """Gets from the API a list of the available repositories,
        along with their information.

        Returns:
            A list of the available repositories.
        """
        return self.__api.get_repositories()

    def create_repository(self, repo_name: str, *,
                          server: Optional[str]=None) -> Repository:
        """Creates a repository.

        Args:
            repo_name: The name of the new repository.
            server:    The target server where the repository is to be created
                       If it is omitted or if it is None, the repository will be
                       created in configured API server.

        Returns:
            The newly created repository will be returned once the operation
            is completed.
        """
        return self.__api.create_repository(repo_name, server)

    def get_repository(self, repo_name: str) -> Repository:
        """Gets from the API the information concerning a single repository,
        specified by name.

        Args:
            repo_name: The name of the repository.

        Returns:
            The desired repository will be returned once the operation
            is completed.
        """
        return self.__api.get_repository(repo_name)

    def rename_repository(self, repo_name: str,
                          repo_new_name: str) -> Repository:
        """Renames a repository.

        Args:
            repo_name:     The name of the repository to be renamed.
            repo_new_name: The new name of the repository.

        Returns:
            ???.
        """
        return self.__api.rename_repository(repo_name, repo_new_name)

    def delete_repository(self, repo_name: str) -> None:
        """Deletes a repository.

        Args:
            repo_name: The name of the repository to be deleted.
        """
        return self.__api.delete_repository(repo_name)

    # Workspaces

    def get_workspaces(self) -> Tuple[Workspace]:
        """Gets from the API a list of all the available workspaces,
        along with their information.

        Returns:
            A list of the available workspaces.
        """
        return self.__api.get_workspaces()

    def create_workspace(self, wkspace_name: str, wkspace_path: Path, *,
                         repo_name: Optional[str]=None) -> Workspace:
        """Creates a new workspace in the machine hosting the API server.

        Args:
            wkspace_name: The name of the new workspace.
            wkspace_path: The absolute path of the new workspace.
            repo_name:    The repository of the new workspace.

        Returns:
            The newly created workspace will be returned once the operation
            is completed.
        """
        return self.__api.create_workspace(wkspace_name, wkspace_path, repo_name)

    def get_workspace(self, wkspace_name: str) -> Workspace:
        """Gets from the API the information concerning a single workspace.

        Args:
            wkspace_name: The name of the workspace.

        Returns:
            The desired workspace will be returned once the operation
            is completed.
        """
        return self.__api.get_workspace(wkspace_name)

    def rename_workspace(self, wkspace_name: str,
                         wkspace_new_name: str) -> Workspace:
        """Renames a workspace in the machine hosting the API server.

        Args:
            wkspace_name:     The name of the workspace to be renamed.
            wkspace_new_name: The new name of the workspace.

        Returns:
            ???.
        """
        return self.__api.rename_workspace(wkspace_name, wkspace_new_name)

    def delete_workspace(self, wkspace_name: str) -> None:
        """Deletes a workspace.

        Args:
            wkspace_name: The name of the workspace to be deleted.
        """
        return self.__api.delete_workspace(wkspace_name)

    # Branches

    def get_branches(self, repo_name: str,
                     query: Optional[str]=None) -> Tuple[Branch]:
        """Returns the information about all the branches in a repository.

        Args:
            repo_name: The name of the branches's host repository.
            query:     Query ???.

        Returns:
            A list of all the branches in a repository.
        """
        return self.__api.get_branches(repo_name, query)

    def create_branch(self,
                      repo_name: str,
                      branch_name: str,
                      origin_type: ObjectType,
                      origin: Union[str, int],
                      top_level: bool=False) -> Branch:
        """Creates a branch.

        Args:
            repo_name:   The name of the host repository of the new branch.
            branch_name: The name of the new branch.
                         Do NOT use a hierarchical name.
            origin_type: The type of the origin of the branch.
                         It should be ObjectType.CHANGESET, ObjectType.LABEL or
                         ObjectType.BRANCH.
            origin:      ???
            top_level:   ???

        Returns:
            The newly created branch will be returned once the operation
            is completed.
        """
        return self.__api.create_branch(repo_name, branch_name,
                                        origin_type, origin, top_level)

    def get_branch(self, repo_name: str, branch_name: str) -> Branch:
        """Returns the information about a single branch in a repository.

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

    def rename_branch(self, repo_name: str,
                      branch_name: str, branch_new_name: str) -> Branch:
        """Renames a branch.

        Args:
            repo_name:       The name of the host repository of the branch.
            branch_name:     The hierarchical name of the branch to be renamed.
                             Please note that branch names are hierarchical
                             (e.g. "main/task001/task002").
            branch_new_name: The new name of the branch.
                             Please have in mind that the hierarchy name
                             can not be changed.

        Returns:
            ???.
        """
        return self.__api.rename_branch(repo_name,
                                        branch_name, branch_new_name)

    def delete_branch(self, repo_name: str, branch_name: str) -> None:
        """Deletes a branch.

        Args:
            repo_name:   The name of the host repository of the branch
            branch_name: The name of the branch to be deleted.
                         Please note that branch names are hierarchical
                         (e.g. "main/task001/task002").
        """
        return self.__api.delete_branch(repo_name, branch_name)

    # Labels

    def get_labels(self, repo_name: str,
                   query: Optional[str]=None) -> Tuple[Label]:
        """Gets a list of all the labels in a repository along with their
        information.

        Args:
            repo_name: The name of the host repository of the labels.
            query:     Query ???.

        Returns:
            A list of all the labels in a repository.
        """
        return self.__api.get_labels(repo_name, query)

    def create_label(self, repo_name: str, label_name: str, changeset_id: int, *,
                     comment: Optional[str]=None, apply_to_xlinks: bool=False) -> Label:
        """Creates a label in a repository.

        Args:
            repo_name:       The name of the future host repository.
            label_name:      The name of the new label.
            changeset_id:    ???
            comment:         ???
            apply_to_xlinks: ???

        Returns:
            The newly created label will be returned once the operation
            is completed.
        """
        return self.__api.create_label(repo_name, label_name, changeset_id,
                                       comment, apply_to_xlinks)

    def get_label(self, repo_name: str, label_name: str) -> Label:
        """Gets the information about a single label.

        Args:
            repo_name:  The name of the host repository of the label.
            label_name: The name of the label.

        Returns:
            The desired label will be returned once the operation
            is completed.
        """
        return self.__api.get_label(repo_name, label_name)

    def rename_label(self, repo_name: str,
                     label_name: str, label_new_name: str) -> Label:
        """Renames a label.

        Args:
            repo_name:      The name of the host repository of the label.
            label_name:     The name of the label to be renamed.
            label_new_name: The new name of the label.

        Returns:
            ???.
        """
        return self.__api.rename_label(repo_name, label_name, label_new_name)

    def delete_label(self, repo_name: str, label_name: str) -> None:
        """Deletes a label.

        Args:
            repo_name:  The name of the host repository of the label.
            label_name: The name of the label to be deleted.
        """
        return self.__api.delete_label(repo_name, label_name)

    # Changesets

    def get_changesets(self, repo_name: str,
                       query: Optional[str]=None) -> Tuple[Changeset]:
        """Gets the information about all the changesets in a repository.

        Args:
            repo_name: The name of the host repository of the changesets.
            query:     Query ???.

        Returns:
            A list of all the changesets in a repository.
        """
        return self.__api.get_changesets(repo_name, query)

    def get_changesets_in_branch(self, repo_name: str, branch_name: str,
                                 query: Optional[str]=None) -> Tuple[Changeset]:
        """Gets the information about all the changesets in a given branch.

        Args:
            repo_name:   The name of the host repository of the branch.
            branch_name: The hierarchical name of the host branch.
                         Please note that branch names are hierarchical
                         (e.g. "main/task001/task002").
            query:       Query ???.

        Returns:
            A list of all the changesets in a given branch.
        """
        return self.__api.get_changesets_in_branch(repo_name, branch_name,
                                                   query)

    def get_changeset(self, repo_name: str, changeset_id: int) -> Changeset:
        """Gets the information about a single changeset.

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
        """Gets the pending changes in a workspace.

        Args:
            wkspace_name: The name of the workspace.
            change_types: A list detailing the desired change types.
                          It should be a list of Change.Type's values.

        Returns:
            ???.
        """
        if change_types is None:
            return self.__api.get_pending_changes(wkspace_name)
        else:
            return self.__api.get_pending_changes(wkspace_name, change_types)

    def undo_pending_changes(self, wkspace_name: str,
                             paths: List[Path]) -> AffectedPaths:
        """Deletes the pending changes in a wkspace.
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
        """???.

        Args:
            wkspace_name: The name of the workspace.

        Returns:
            ???.
        """
        return self.__api.get_workspace_update_status(wkspace_name)

    def update_workspace(self, wkspace_name: str) -> OperationStatus:
        """???.

        Args:
            wkspace_name: The name of the workspace.

        Returns:
            ???.
        """
        return self.__api.update_workspace(wkspace_name)

    def get_workspace_switch_status(self, wkspace_name: str) -> OperationStatus:
        """???.

        Args:
            wkspace_name: The name of the workspace.

        Returns:
            ???.
        """
        return self.__api.get_workspace_switch_status(wkspace_name)

    def switch_workspace(self, wkspace_name: str,
                         object_type: ObjectType,
                         object: Union[str, int]) -> OperationStatus:
        """???.

        Args:
            wkspace_name: The name of the workspace.
            object_type:  The type of switch destination.
                          It should be ObjectType.CHANGESET, ObjectType.LABEL or
                          ObjectType.BRANCH.
            object:       The target point the workspace will be set to.
                          It should be (according to object_type) the changeset id,
                          the label name or the branch name.

        Returns:
            ???.
        """
        return self.__api.switch_workspace(wkspace_name, object_type, object)

    # Checkin

    def get_workspace_checkin_status(self, wkspace_name: str) -> CheckinStatus:
        """???.

        Args:
            wkspace_name: The name of the workspace.

        Returns:
            ???.
        """
        return self.__api.get_workspace_checkin_status(wkspace_name)

    def checkin_workspace(self, wkspace_name: str, *,
                          paths: Optional[List[str]]=None,
                          comment: Optional[str]=None,
                          recurse: bool=False) -> CheckinStatus:
        """???.

        Args:
            wkspace_name: The name of the workspace.
            paths:        ???
            comment:      The checkin comment.
            recurse:      ???

        Returns:
            ???.
        """
        return self.__api.checkin_workspace(wkspace_name,
                                            paths, comment, recurse)

    # Repository contents

    def getItemInRepository(self, repo_name: str, item_path: str) -> Item:
        """???.

        Args:
            repo_name: The name of the repository.
            item_path: The path of selected item.

        Returns:
            ???.
        """
        return self.__api.getItemInRepository(repo_name, item_path)

    def get_item_in_branch(self, repo_name: str, branch_name: str,
                           item_path: str) -> Item:
        """???.

        Args:
            repo_name:   The name of the host repository of the branch.
            branch_name: The name of the branch.
                         Please note that branch names are hierarchical
                         (e.g. "main/task001/task002").
            item_path:   The path of selected item.

        Returns:
            The desired item will be returned once the operation
            is completed.
        """
        return self.__api.get_item_in_branch(repo_name, branch_name, item_path)

    def get_item_in_changeset(self, repo_name: str, changeset_id: int,
                              item_path: str) -> Item:
        """???.

        Args:
            repo_name:    The name of the host repository of the changeset.
            changeset_id: The id of the changeset.
            item_path:    The path of selected item.

        Returns:
            The desired item will be returned once the operation
            is completed.
        """
        return self.__api.get_item_in_changeset(repo_name, changeset_id, item_path)

    def get_item_in_label(self, repo_name: str, label_name: str,
                          item_path: str) -> Item:
        """???.

        Args:
            repo_name:  The name of the host repository of the label.
            label_name: The name of the label.
            item_path:  The path of selected item.

        Returns:
            The desired item will be returned once the operation
            is completed.
        """
        return self.__api.get_item_in_label(repo_name, label_name, item_path)

    def get_item_revision_history_in_branch(self, repo_name: str, branch_name: str,
                                            item_path: str) -> Tuple[RevisionHistoryItem]:
        """???.

        Args:
            repo_name:   The name of the host repository of the branch.
            branch_name: The name of the branch.
                         Please note that branch names are hierarchical
                         (e.g. "main/task001/task002").
            item_path:   The path of selected item.

        Returns:
            ???.
        """
        return self.__api.get_item_revision_history_in_branch(repo_name, branch_name,
                                                              item_path)

    def get_item_revision_history_in_changeset(self, repo_name: str, changeset_id: int,
                                               item_path: str) -> Tuple[RevisionHistoryItem]:
        """???.

        Args:
            repo_name:    The name of the host repository of the changeset.
            changeset_id: The id of the changeset.
            item_path:    The path of selected item.

        Returns:
            ???.
        """
        return self.__api.get_item_revision_history_in_changeset(repo_name, changeset_id,
                                                                 item_path)

    def get_item_revision_history_in_label(self, repo_name: str, label_name: str,
                                           item_path: str) -> Tuple[RevisionHistoryItem]:
        """???.

        Args:
            repo_name:  The name of the host repository of the label.
            label_name: The name of the label.
            item_path:  The path of selected item.

        Returns:
            ???.
        """
        return self.__api.get_item_revision_history_in_label(repo_name, label_name,
                                                             item_path)

    # Diff

    def diff_changesets(self, repo_name: str,
                        changeset_id: int, source_changeset_id: int) -> Tuple[Diff]:
        """???.

        Args:
            repo_name:           The name of the host repository of the changesets.
            changeset_id:        ???
            source_changeset_id: ???

        Returns:
            ???.
        """
        return self.__api.diff_changesets(repo_name, changeset_id, source_changeset_id)

    def diff_changeset(self, repo_name: str, changeset_id: int) -> Tuple[Diff]:
        """???.

        Args:
            repo_name:    The name of the host repository of the changeset.
            changeset_id: The id of the changeset.

        Returns:
            ???.
        """
        return self.__api.diff_changeset(repo_name, changeset_id)

    def diff_branch(self, repo_name: str, branch_name: str) -> Tuple[Diff]:
        """???.

        Args:
            repo_name:   The name of the host repository of the branch.
            branch_name: The name of the branch.
                         Please note that branch names are hierarchical
                         (e.g. "main/task001/task002").

        Returns:
            ???.
        """
        return self.__api.diff_branch(repo_name, branch_name)

    # Workspace actions

    def add_workspace_item(self, wkspace_name: str, item_path: str, *,
                           add_parents: bool=True, checkout_parent: bool=True,
                           recurse: bool=True) -> AffectedPaths:
        """???.

        Args:
            wkspace_name:    The name of the workspace.
            item_path:       The path of the item to be added. 
            add_parents:     ???
            checkout_parent: ???
            recurse:         ???

        Returns:
            The paths that were affected by the addition operation.
        """
        return self.__api.add_workspace_item(wkspace_name, item_path,
                                             add_parents, checkout_parent, recurse)

    def checkout_workspace_item(self, wkspace_name: str, item_path: str) -> AffectedPaths:
        """???.

        Args:
            wkspace_name: The name of the workspace.
            item_path:    The path of selected item.

        Returns:
            The paths that were affected by the checkout operation.
        """
        return self.__api.checkout_workspace_item(wkspace_name, item_path)

    def move_workspace_item(self, wkspace_name: str, item_path: str,
                            dest_item_path: str) -> AffectedPaths:
        """???.

        Args:
            wkspace_name:   The name of the workspace.
            item_path:      Source path of selected item.
            dest_item_path: Destination path to move the selected item
                            (e.g. "src/bar.c").

        Returns:
            The paths that were affected by the movement operation.
        """
        return self.__api.move_workspace_item(wkspace_name, item_path, dest_item_path)
