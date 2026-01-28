# Copyright (c) 2019 Adam Karpierz
# SPDX-License-Identifier: Zlib

from __future__ import annotations

import enum

__all__ = ('RepId', 'Owner', 'Repository', 'Workspace', 'ObjectType',
           'Branch', 'Label', 'Changeset', 'LocalInfo', 'RevisionInfo',
           'RevisionHistoryItem', 'Change', 'OperationStatus', 'CheckinStatus',
           'XLink', 'Item', 'Merge', 'Diff', 'AffectedPaths')


class RepId:
    """PlasticSCM's repository ID."""


class Owner:
    """PlasticSCM's object owner."""


class Repository:
    """PlasticSCM's repository."""


class Workspace:
    """PlasticSCM's workspace."""


@enum.unique
class ObjectType(enum.Enum):
    """PlasticSCM's object type."""


class Branch:
    """PlasticSCM's branch."""


class Label:
    """PlasticSCM's label."""


class Changeset:
    """PlasticSCM's changeset."""


class LocalInfo:
    """PlasticSCM's local info."""


class RevisionInfo:
    """PlasticSCM's revision info."""


class RevisionHistoryItem:
    """PlasticSCM's revision history item."""


class Change:
    """PlasticSCM's changes in workspace."""

    @enum.unique
    class Type(enum.Enum):
        """PlasticSCM's changes type."""


class OperationStatus:
    """PlasticSCM's operation status."""


class CheckinStatus:
    """PlasticSCM's checkin status."""


class XLink:
    """PlasticSCM's XLink target."""


class Item:
    """PlasticSCM's item."""

    @enum.unique
    class Type(enum.Enum):
        """PlasticSCM's item type."""


class Merge:
    """PlasticSCM's merge."""

    @enum.unique
    class Type(enum.Enum):
        """PlasticSCM's merge type."""


class Diff:
    """PlasticSCM's diff."""

    @enum.unique
    class Status(enum.Enum):
        """PlasticSCM's diff status."""


class AffectedPaths:
    """PlasticSCM's affected paths.

    Represents the paths that were affected by a undo operation.
    """
