# flake8-in-file-ignores: noqa: E301

# Copyright (c) 2019 Adam Karpierz
# SPDX-License-Identifier: Zlib

from __future__ import annotations

from typing import Protocol
from typing_extensions import Self
from pathlib import Path

from .model import (Repository, Workspace, ObjectType, Branch, Label, Changeset,
                    RevisionHistoryItem, Change, OperationStatus, CheckinStatus,
                    Item, Diff, AffectedPaths)

__all__ = ('APIProtocol',)


class APIProtocol(Protocol):

    #
    # API Interface.
    #

    def __new__(cls,
                url: str = "http://localhost:9090", *,
                http_username: str | None = None,
                http_password: str | None = None,
                ssl_verify: bool | str | None = True,
                timeout: int | float | None = None) -> Self:
        ...

    # Repositories

    def get_repositories(self) -> tuple[Repository, ...]:
        ...
    def create_repository(self, repo_name: str, *, server: str | None = None) -> Repository:
        ...
    def get_repository(self, repo_name: str) -> Repository:
        ...
    def rename_repository(self, repo_name: str, repo_new_name: str) -> Repository:
        ...
    def delete_repository(self, repo_name: str) -> None:
        ...

    # Workspaces

    def get_workspaces(self) -> tuple[Workspace, ...]:
        ...
    def create_workspace(self, wkspace_name: str, wkspace_path: Path, *,
                         repo_name: str | None = None) -> Workspace:
        ...
    def get_workspace(self, wkspace_name: str) -> Workspace:
        ...
    def rename_workspace(self, wkspace_name: str, wkspace_new_name: str) -> Workspace:
        ...
    def delete_workspace(self, wkspace_name: str) -> None:
        ...

    # Branches

    def get_branches(self, repo_name: str, *, query: str | None = None) -> tuple[Branch, ...]:
        ...
    def create_branch(self,
                      repo_name: str,
                      branch_name: str,
                      origin_type: ObjectType,
                      origin: str | int, *,
                      top_level: bool = False) -> Branch:
        ...
    def get_branch(self, repo_name: str, branch_name: str) -> Branch:
        ...
    def rename_branch(self, repo_name: str, branch_name: str, branch_new_name: str) -> Branch:
        ...
    def delete_branch(self, repo_name: str, branch_name: str) -> None:
        ...

    # Labels

    def get_labels(self, repo_name: str, *, query: str | None = None) -> tuple[Label, ...]:
        ...
    def create_label(self, repo_name: str, label_name: str, changeset_id: int, *,
                     comment: str | None = None, apply_to_xlinks: bool = False) -> Label:
        ...
    def get_label(self, repo_name: str, label_name: str) -> Label:
        ...
    def rename_label(self, repo_name: str, label_name: str, label_new_name: str) -> Label:
        ...
    def delete_label(self, repo_name: str, label_name: str) -> None:
        ...

    # Changesets

    def get_changesets(self, repo_name: str, *, query: str | None = None) -> tuple[Changeset, ...]:
        ...
    def get_changesets_in_branch(self, repo_name: str, branch_name: str, *,
                                 query: str | None = None) -> tuple[Changeset, ...]:
        ...
    def get_changeset(self, repo_name: str, changeset_id: int) -> Changeset:
        ...

    # Changes

    def get_pending_changes(self, wkspace_name: str, *,
                            change_types: list[Change.Type] | None = None) -> tuple[Change, ...]:
        ...
    def undo_pending_changes(self, wkspace_name: str,
                             paths: list[str | Path]) -> AffectedPaths:
        ...

    # Workspace Update and Switch

    def get_workspace_update_status(self, wkspace_name: str) -> OperationStatus:
        ...
    def update_workspace(self, wkspace_name: str) -> OperationStatus:
        ...
    def get_workspace_switch_status(self, wkspace_name: str) -> OperationStatus:
        ...
    def switch_workspace(self, wkspace_name: str,
                         object_type: ObjectType,
                         object: str | int) -> OperationStatus:  # noqa A002
        ...

    # Checkin

    def get_workspace_checkin_status(self, wkspace_name: str) -> CheckinStatus:
        ...
    def checkin_workspace(self, wkspace_name: str, *,
                          paths: list[str] | None = None,
                          comment: str | None = None,
                          recurse: bool = True) -> CheckinStatus:
        ...

    # Repository contents

    def get_item(self, repo_name: str, item_path: str) -> Item:
        ...
    def get_item_in_branch(self, repo_name: str, branch_name: str, item_path: str) -> Item:
        ...
    def get_item_in_changeset(self, repo_name: str, changeset_id: int, item_path: str) -> Item:
        ...
    def get_item_in_label(self, repo_name: str, label_name: str, item_path: str) -> Item:
        ...
    def get_item_revision(self, repo_name: str, revision_spec: str) -> Item:
        ...
    def get_item_revision_history_in_branch(self, repo_name: str,
                                            branch_name: str, item_path: str) \
                                            -> tuple[RevisionHistoryItem, ...]:
        ...
    def get_item_revision_history_in_changeset(self, repo_name: str,
                                               changeset_id: int, item_path: str) \
                                               -> tuple[RevisionHistoryItem, ...]:
        ...
    def get_item_revision_history_in_label(self, repo_name: str,
                                           label_name: str, item_path: str) \
                                           -> tuple[RevisionHistoryItem, ...]:
        ...

    # Diff

    def diff_changesets(self, repo_name: str,
                        changeset_id: int, source_changeset_id: int) -> tuple[Diff, ...]:
        ...
    def diff_changeset(self, repo_name: str, changeset_id: int) -> tuple[Diff, ...]:
        ...
    def diff_branch(self, repo_name: str, branch_name: str) -> tuple[Diff, ...]:
        ...

    # Workspace actions

    def add_workspace_item(self, wkspace_name: str, item_path: str, *,
                           add_parents: bool = True, checkout_parent: bool = True,
                           recurse: bool = True) -> AffectedPaths:
        ...
    def checkout_workspace_item(self, wkspace_name: str, item_path: str) -> AffectedPaths:
        ...
    def move_workspace_item(self, wkspace_name: str, item_path: str,
                            dest_item_path: str) -> AffectedPaths:
        ...
