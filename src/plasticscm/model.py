# Copyright (c) 2019-2020 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/licenses/zlib

import enum

from public import public


@public
class RepId:
    """PlasticSCM's repository ID"""


@public
class Owner:
    """PlasticSCM's object owner"""


@public
class Repository:
    """PlasticSCM's repository"""


@public
class Workspace:
    """PlasticSCM's workspace"""


@public
@enum.unique
class ObjectType(enum.Enum):
    """PlasticSCM's object type"""


@public
class Branch:
    """PlasticSCM's branch"""


@public
class Label:
    """PlasticSCM's label"""


@public
class Changeset:
    """PlasticSCM's changeset"""


@public
class LocalInfo:
    """PlasticSCM's local info"""


@public
class RevisionInfo:
    """PlasticSCM's revision info"""


@public
class RevisionHistoryItem:
    """PlasticSCM's revision history item"""


@public
class Change:
    """PlasticSCM's changes in workspace"""

    @enum.unique
    class Type(enum.Enum):
        """PlasticSCM's changes type"""


@public
class OperationStatus:
    """PlasticSCM's operation status"""


@public
class CheckinStatus:
    """PlasticSCM's checkin status"""


@public
class XLink:
    """PlasticSCM's XLink target"""


@public
class Item:
    """PlasticSCM's item"""

    @enum.unique
    class Type(enum.Enum):
        """PlasticSCM's item type"""


@public
class Merge:
    """PlasticSCM's merge"""

    @enum.unique
    class Type(enum.Enum):
        """PlasticSCM's merge type"""


@public
class Diff:
    """PlasticSCM's diff"""

    @enum.unique
    class Status(enum.Enum):
        """PlasticSCM's diff status"""


@public
class AffectedPaths:
    """PlasticSCM's affected paths.
    Represents the paths that were affected by a undo operation."""
