# Copyright (c) 2019-2020 Adam Karpierz
# Licensed under the zlib/libpng License
# https://opensource.org/licenses/zlib

import unittest
from typing import List, Tuple, Optional, Union
from functools import partial
from pathlib import Path
from pprint import pprint

from httmock import all_requests, urlmatch, response, HTTMock
from plasticscm import Plastic


class TestPlastic(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.url = url = "http://localhost:9090"
        scheme, _, netloc = url.partition("://")
        cls.pl  = pl = Plastic(url, api_version="1")
        cls.test_table = [

            # Repositories

            {
                "method": "get_repositories",
                "args": (),
                "rtype": Tuple,#[pl.model.Repository],
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/repos$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": [
                        {
                            "repId":
                            {
                                "id": 1,
                                "moduleId": 0
                            },
                            "name": "default",
                            "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                            "owner":
                            {
                                "name": "all",
                                "isGroup": False
                            },
                            "server": "localhost:8084"
                        },
                    ]
                }
            },

            {
                "method": "create_repository",
                "args": ("main_repo",),
                "rtype": pl.model.Repository,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="post",
                                     path=r"^/api/v1/repos$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "repId": {
                            "id": 2,
                            "moduleId": 0
                        },
                        "name": "main_repo",
                        "guid": "c45b8af3-1a10-d31f-baca-c00590d12456",
                        "owner": {
                            "name": "all",
                            "isGroup": False
                        },
                        "server": "my_server:8084"
                    }
                }
            },
            {
                "method": "create_repository",
                "args": ("main_repo",),
                "kwargs": dict(server="otherserver:8084"),
                "rtype": pl.model.Repository,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="post",
                                     path=r"^/api/v1/repos$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "repId": {
                            "id": 2,
                            "moduleId": 0
                        },
                        "name": "main_repo",
                        "guid": "c45b8af3-1a10-d31f-baca-c00590d12456",
                        "owner": {
                            "name": "all",
                            "isGroup": False
                        },
                        "server": "otherserver:8084"
                    }
                }
            },

            {
                "method": "get_repository",
                "args": ("default",),
                "rtype": pl.model.Repository,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/repos/\w+$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "repId": {
                            "id": 1,
                            "moduleId": 0
                        },
                        "name": "default",
                        "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                        "owner": {
                            "name": "all",
                            "isGroup": False
                        },
                        "server": "localhost:8084"
                    }
                }
            },

            {
                "method": "rename_repository",
                "args": ("old_name", "new_name"),
                "rtype": pl.model.Repository,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="put",
                                     path=r"^/api/v1/repos/\w+$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "repId": {
                            "id": 2,
                            "moduleId": 0
                        },
                        "name": "new_name",
                        "guid": "c45b8af3-1a10-d31f-baca-c00590d12456",
                        "owner": {
                            "name": "all",
                            "isGroup": False
                        },
                        "server": "my_server:8084"
                    }
                }
            },

            {
                "method": "delete_repository",
                "args": ("default",),
                "rtype": None,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="delete",
                                     path=r"^/api/v1/repos/\w+$"),
                "expected": {
                    "status_code": 204, # No Content
                    "content": None
                }
            },

            # Workspaces

            {
                "method": "get_workspaces",
                "args": (),
                "rtype": Tuple,#[pl.model.Workspace],
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/wkspaces$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": [
                        {
                            "name": "my_wkspace",
                            "guid": "e93518f8-20a6-4534-a7c6-f3d9ebac45cb",
                            "path": "c:\\path\\to\\workspace",
                            "machineName": "MACHINE",
                        },
                    ]
                }
            },

            {
                "method": "create_workspace",
                "args": ("my_wkspace", Path("c:\\the\\path\\to\\new_wkspace")),
                "rtype": pl.model.Workspace,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="post",
                                     path=r"^/api/v1/wkspaces$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "name": "my_wkspace",
                        "guid": "ed3248d2-5591-407a-94e6-84dac0ce015b",
                        "path": "c:\\the\\path\\to\\new_wkspace",
                        "machineName": "MACHINE"
                    }
                }
            },
            {
                "method": "create_workspace",
                "args": ("my_wkspace", Path("c:\\the\\path\\to\\new_wkspace")),
                "kwargs": dict(repo_name="default"),
                "rtype": pl.model.Workspace,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="post",
                                     path=r"^/api/v1/wkspaces$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "name": "my_wkspace",
                        "guid": "ed3248d2-5591-407a-94e6-84dac0ce015b",
                        "path": "c:\\the\\path\\to\\new_wkspace",
                        "machineName": "MACHINE"
                    }
                }
            },

            {
                "method": "get_workspace",
                "args": ("my_wkspace",),
                "rtype": pl.model.Workspace,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/wkspaces/\w+$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "name": "my_wkspace",
                        "guid": "e93518f8-20a6-4534-a7c6-f3d9ebac45cb",
                        "path": "c:\\path\\to\\workspace",
                        "machineName": "MACHINE",
                    }
                }
            },

            {
                "method": "rename_workspace",
                "args": ("old_name", "new_name"),
                "rtype": pl.model.Workspace,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="patch",
                                     path=r"^/api/v1/wkspaces/\w+$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "name": "new_name",
                        "guid": "ed3248d2-5591-407a-94e6-84dac0ce015b",
                        "path": "c:\\the\\path\\to\\new_wkspace",
                        "machineName": "MACHINE",
                    }
                }
            },

            {
                "method": "delete_workspace",
                "args": ("my_wkspace",),
                "rtype": None,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="delete",
                                     path=r"^/api/v1/wkspaces/\w+$"),
                "expected": {
                    "status_code": 204, # No Content
                    "content": None
                }
            },

            # Branches

            {
                "method": "get_branches",
                "args": ("main_repo",),
                "rtype": Tuple,#[pl.model.Branch],
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/repos/\w+/branches$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": [
                        {
                            "name": "/main/task001/task002",
                            "id": 1388,
                            "parentId": 1067,
                            "lastChangeset": 1383,
                            "comment": "Testing: implement new smoke tests.",
                            "creationDate": "2015-06-30T15:18:08",
                            "guid": "0ced86fe-37cb-4801-8f6d-0081edb46d39",
                            "owner": {
                                "name": "codice-master",
                                "isGroup": False
                            },
                            "repository": {
                                "name": "main_repo",
                                "repId": {
                                    "id": 1,
                                    "moduleId": 0
                                },
                                "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                                "owner": {
                                    "name": "all",
                                    "isGroup": False
                                },
                                "server": "localhost:8084"
                            }
                        },
                    ]
                }
            },
            {
                "method": "get_branches",
                "args": ("main_repo",),
                "kwargs": dict(query="id > 50"),
                "rtype": Tuple,#[pl.model.Branch],
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/repos/\w+/branches$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": [
                        {
                            "name": "/main/task001/task002",
                            "id": 1388,
                            "parentId": 1067,
                            "lastChangeset": 1383,
                            "comment": "Testing: implement new smoke tests.",
                            "creationDate": "2015-06-30T15:18:08",
                            "guid": "0ced86fe-37cb-4801-8f6d-0081edb46d39",
                            "owner": {
                                "name": "codice-master",
                                "isGroup": False
                            },
                            "repository": {
                                "name": "main_repo",
                                "repId": {
                                    "id": 1,
                                    "moduleId": 0
                                },
                                "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                                "owner": {
                                    "name": "all",
                                    "isGroup": False
                                },
                                "server": "localhost:8084"
                            }
                        },
                    ]
                }
            },

            {
                "method": "create_branch",
                "args": ("default", "newBranch", pl.model.ObjectType.BRANCH, "/main/scm003"),
                "rtype": pl.model.Branch,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="post",
                                     path=r"^/api/v1/repos/\w+/branches$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "name": "/main/scm003/newBranch",
                        "id": 1395,
                        "parentId": 1067,
                        "lastChangeset": 1383,
                        "creationDate": "2015-07-01T09:01:08",
                        "guid": "3416a2b4-f88a-43b1-8319-3424bc23c77b",
                        "owner": {
                            "name": "tester",
                            "isGroup": False
                        },
                        "repository": {
                            "name": "default",
                            "repId": {
                                "id": 1,
                                "moduleId": 0
                            },
                            "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                            "owner": {
                                "name": "all",
                                "isGroup": False
                            },
                            "server": "localhost:8084"
                        }
                    }
                }
            },
            {
                "method": "create_branch",
                "args": ("default", "newBranch", pl.model.ObjectType.LABEL, "BL000"),
                "kwargs": dict(top_level=True),
                "rtype": pl.model.Branch,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="post",
                                     path=r"^/api/v1/repos/\w+/branches$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "name": "/main/newBranch",
                        "id": 1395,
                        "parentId": 1067,
                        "lastChangeset": 1383,
                        "creationDate": "2015-07-01T09:01:08",
                        "guid": "3416a2b4-f88a-43b1-8319-3424bc23c77b",
                        "owner": {
                            "name": "tester",
                            "isGroup": False
                        },
                        "repository": {
                            "name": "default",
                            "repId": {
                                "id": 1,
                                "moduleId": 0
                            },
                            "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                            "owner": {
                                "name": "all",
                                "isGroup": False
                            },
                            "server": "localhost:8084"
                        }
                    }
                }
            },
            {
                "method": "create_branch",
                "args": ("default", "newBranch", pl.model.ObjectType.CHANGESET, 97),
                "kwargs": dict(top_level=False),
                "rtype": pl.model.Branch,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="post",
                                     path=r"^/api/v1/repos/\w+/branches$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "name": "/main/newBranch",
                        "id": 1395,
                        "parentId": 1067,
                        "lastChangeset": 1383,
                        "creationDate": "2015-07-01T09:01:08",
                        "guid": "3416a2b4-f88a-43b1-8319-3424bc23c77b",
                        "owner": {
                            "name": "tester",
                            "isGroup": False
                        },
                        "repository": {
                            "name": "default",
                            "repId": {
                                "id": 1,
                                "moduleId": 0
                            },
                            "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                            "owner": {
                                "name": "all",
                                "isGroup": False
                            },
                            "server": "localhost:8084"
                        }
                    }
                }
            },

            {
                "method": "get_branch",
                "args": ("main_repo", "/main/task001/task002"),
                "rtype": pl.model.Branch,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/repos/\w+/branches(/\w+)+$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "name": "/main/task001/task002",
                        "id": 1388,
                        "parentId": 1067,
                        "lastChangeset": 1383,
                        "comment": "Testing: implement new smoke tests.",
                        "creationDate": "2015-06-30T15:18:08",
                        "guid": "0ced86fe-37cb-4801-8f6d-0081edb46d39",
                        "owner": {
                            "name": "codice-master",
                            "isGroup": False
                        },
                        "repository": {
                            "name": "main_repo",
                            "repId": {
                                "id": 1,
                                "moduleId": 0
                            },
                            "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                            "owner": {
                                "name": "all",
                                "isGroup": False
                            },
                            "server": "localhost:8084"
                        }
                    }
                }
            },

            {
                "method": "rename_branch",
                "args": ("main_repo", "/main/task001/task002", "/main/task001/task003"),
                "rtype": pl.model.Branch,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="patch",
                                     path=r"^/api/v1/repos/\w+/branches(/\w+)+$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "name": "/main/task001/task003",
                        "id": 1388,
                        "parentId": 1067,
                        "lastChangeset": 1383,
                        "comment": "Testing: implement new smoke tests.",
                        "creationDate": "2015-06-30T15:18:08",
                        "guid": "0ced86fe-37cb-4801-8f6d-0081edb46d39",
                        "owner": {
                            "name": "codice-master",
                            "isGroup": False
                        },
                        "repository": {
                            "name": "main_repo",
                            "repId": {
                                "id": 1,
                                "moduleId": 0
                            },
                            "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                            "owner": {
                                "name": "all",
                                "isGroup": False
                            },
                            "server": "localhost:8084"
                        }
                    }
                }
            },

            {
                "method": "delete_branch",
                "args": ("main_repo", "/main/task001/task002"),
                "rtype": None,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="delete",
                                     path=r"^/api/v1/repos/\w+/branches(/\w+)+$"),
                "expected": {
                    "status_code": 204, # No Content
                    "content":  None
                }
            },

            # Labels

            {
                "method": "get_labels",
                "args": ("default",),
                "rtype": Tuple,#[pl.model.Label],
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/repos/\w+/labels$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": [
                        {
                            "name": "BL000",
                            "id": 1391,
                            "changeset": 100,
                            "comment": "",
                            "creationDate": "2015-07-01T07:45:56",
                            "branch": {
                                "name": "/main",
                                "id": 3,
                                "parentId": -1,
                                "lastChangeset": 101,
                                "comment": "main branch",
                                "creationDate": "2015-04-09T07:17:00",
                                "guid": "5fc2d7c8-05e1-4987-9dd9-74eaec7c27eb",
                                "owner": {
                                    "name": "all",
                                    "isGroup": False
                                },
                                "repository": {
                                    "name": "default",
                                    "repId": {
                                        "id": 1,
                                        "moduleId": 0
                                    },
                                    "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                                    "owner": {
                                        "name": "all",
                                        "isGroup": False
                                    },
                                    "server": "localhost:8084"
                                }
                            },
                            "owner": {
                                "name": "tester",
                                "isGroup": False
                            },
                            "repository": {
                                "name": "default",
                                "repId": {
                                    "id": 1,
                                    "moduleId": 0
                                },
                                "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                                "owner": {
                                    "name": "all",
                                    "isGroup": False
                                },
                                "server": "localhost:8084"
                            }
                        },
                    ]
                }
            },
            {
                "method": "get_labels",
                "args": ("default",),
                "kwargs": dict(query="date >= '2015-07-01'"),
                "rtype": Tuple,#[pl.model.Label],
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/repos/\w+/labels$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": [
                        {
                            "name": "BL000",
                            "id": 1391,
                            "changeset": 100,
                            "comment": "",
                            "creationDate": "2015-07-01T07:45:56",
                            "branch": {
                                "name": "/main",
                                "id": 3,
                                "parentId": -1,
                                "lastChangeset": 101,
                                "comment": "main branch",
                                "creationDate": "2015-04-09T07:17:00",
                                "guid": "5fc2d7c8-05e1-4987-9dd9-74eaec7c27eb",
                                "owner": {
                                    "name": "all",
                                    "isGroup": False
                                },
                                "repository": {
                                    "name": "default",
                                    "repId": {
                                        "id": 1,
                                        "moduleId": 0
                                    },
                                    "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                                    "owner": {
                                        "name": "all",
                                        "isGroup": False
                                    },
                                    "server": "localhost:8084"
                                }
                            },
                            "owner": {
                                "name": "tester",
                                "isGroup": False
                            },
                            "repository": {
                                "name": "default",
                                "repId": {
                                    "id": 1,
                                    "moduleId": 0
                                },
                                "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                                "owner": {
                                    "name": "all",
                                    "isGroup": False
                                },
                                "server": "localhost:8084"
                            }
                        },
                    ]
                }
            },

            {
                "method": "create_label",
                "args": ("default", "BL001", 99),
                "kwargs": dict(comment="Stable baseline - 1"),
                "rtype": pl.model.Label,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="post",
                                     path=r"^/api/v1/repos/\w+/labels$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "name": "BL001",
                        "id": 1401,
                        "changeset": 99,
                        "comment": "Stable baseline - 1",
                        "creationDate": "2015-07-01T10:19:14",
                        "branch": {
                            "name": "/main",
                            "id": 3,
                            "parentId": -1,
                            "lastChangeset": 101,
                            "comment": "main branch",
                            "creationDate": "2015-04-09T07:17:00",
                            "guid": "5fc2d7c8-05e1-4987-9dd9-74eaec7c27eb",
                            "owner": {
                                "name": "all",
                                "isGroup": False
                            },
                            "repository": {
                                "name": "default",
                                "repId": {
                                    "id": 1,
                                    "moduleId": 0
                                },
                                "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                                "owner": {
                                    "name": "all",
                                    "isGroup": False
                                },
                                "server": "localhost:8084"
                            }
                        },
                        "owner": {
                            "name": "tester",
                            "isGroup": False
                        },
                        "repository": {
                            "name": "default",
                            "repId": {
                                "id": 1,
                                "moduleId": 0
                            },
                            "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                            "owner": {
                                "name": "all",
                                "isGroup": False
                            },
                            "server": "localhost:8084"
                        }
                    }
                }
            },

            {
                "method": "get_label",
                "args": ("default", "BL000"),
                "rtype": pl.model.Label,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/repos/\w+/labels/\w+$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "name": "BL000",
                        "id": 1391,
                        "changeset": 100,
                        "branch": {
                            "name": "/main",
                            "id": 3,
                            "parentId": -1,
                            "lastChangeset": 101,
                            "comment": "main branch",
                            "creationDate": "2015-04-09T07:17:00",
                            "guid": "5fc2d7c8-05e1-4987-9dd9-74eaec7c27eb",
                            "owner": {
                                "name": "all",
                                "isGroup": False
                            },
                            "repository": {
                                "name": "default",
                                "repId": {
                                    "id": 1,
                                    "moduleId": 0
                                },
                                "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                                "owner": {
                                    "name": "all",
                                    "isGroup": False
                                },
                                "server": "localhost:8084"
                            }
                        },
                        "comment": "",
                        "creationDate": "2015-07-01T07:45:56",
                        "owner": {
                            "name": "tester",
                            "isGroup": False
                        },
                        "repository": {
                            "name": "default",
                            "repId": {
                                "id": 1,
                                "moduleId": 0
                            },
                            "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                            "owner": {
                                "name": "all",
                                "isGroup": False
                            },
                            "server": "localhost:8084"
                        }
                    }
                }
            },

            {
                "method": "rename_label",
                "args": ("default", "BL000", "v1.0.0"),
                "rtype": pl.model.Label,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="patch",
                                     path=r"^/api/v1/repos/\w+/labels/\w+$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "name": "v1.0.0",
                        "id": 1401,
                        "changeset": 99,
                        "comment": "Stable baseline - 1",
                        "creationDate": "2015-07-01T10:19:14",
                        "branch": {
                            "name": "/main",
                            "id": 3,
                            "parentId": -1,
                            "lastChangeset": 101,
                            "comment": "main branch",
                            "creationDate": "2015-04-09T07:17:00",
                            "guid": "5fc2d7c8-05e1-4987-9dd9-74eaec7c27eb",
                            "owner": {
                                "name": "all",
                                "isGroup": False
                            },
                            "repository": {
                                "name": "default",
                                "repId": {
                                    "id": 1,
                                    "moduleId": 0
                                },
                                "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                                "owner": {
                                    "name": "all",
                                    "isGroup": False
                                },
                                "server": "localhost:8084"
                            }
                        },
                        "owner": {
                            "name": "tester",
                            "isGroup": False
                        },
                        "repository": {
                            "name": "default",
                            "repId": {
                                "id": 1,
                                "moduleId": 0
                            },
                            "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                            "owner": {
                                "name": "all",
                                "isGroup": False
                            },
                            "server": "localhost:8084"
                        }
                    }
                }
            },

            {
                "method": "delete_label",
                "args": ("default", "BL000"),
                "rtype": None,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="delete",
                                     path=r"^/api/v1/repos/\w+/labels/\w+$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": None
                }
            },

            # Changesets

            {
                "method": "get_changesets",
                "args": ("default",),
                "rtype": Tuple,#[pl.model.Changeset],
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/repos/\w+/changesets$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": [
                        {
                            "id": 0,
                            "parentId": -1,
                            "comment": "Root dir",
                            "creationDate": "2015-04-09T07:17:00",
                            "guid": "0497ef04-4c81-4090-8458-649885400c84",
                            "branch": {
                                "name": "/main",
                                "id": 3,
                                "parentId": -1,
                                "lastChangeset": 101,
                                "comment": "main branch",
                                "creationDate": "2015-04-09T07:17:00",
                                "guid": "5fc2d7c8-05e1-4987-9dd9-74eaec7c27eb",
                                "owner": {
                                    "name": "all",
                                    "isGroup": False
                                },
                                "repository": {
                                    "name": "default",
                                    "repId": {
                                        "id": 1,
                                        "moduleId": 0
                                    },
                                    "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                                    "owner": {
                                        "name": "all",
                                        "isGroup": False
                                    },
                                    "server": "localhost:8084"
                                }
                            },
                            "owner": {
                                "name": "all",
                                "isGroup": False
                            },
                            "repository": {
                                "name": "default",
                                "repId": {
                                    "id": 1,
                                    "moduleId": 0
                                },
                                "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                                "owner": {
                                    "name": "all",
                                    "isGroup": False
                                },
                                "server": "localhost:8084"
                            }
                        },
                    ]
                }
            },
            {
                "method": "get_changesets",
                "args": ("default",),
                "kwargs": dict(query="date > '2015-04-09'"),
                "rtype": Tuple,#[pl.model.Changeset],
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/repos/\w+/changesets$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": [
                        {
                            "id": 0,
                            "parentId": -1,
                            "comment": "Root dir",
                            "creationDate": "2015-04-09T07:17:00",
                            "guid": "0497ef04-4c81-4090-8458-649885400c84",
                            "branch": {
                                "name": "/main",
                                "id": 3,
                                "parentId": -1,
                                "lastChangeset": 101,
                                "comment": "main branch",
                                "creationDate": "2015-04-09T07:17:00",
                                "guid": "5fc2d7c8-05e1-4987-9dd9-74eaec7c27eb",
                                "owner": {
                                    "name": "all",
                                    "isGroup": False
                                },
                                "repository": {
                                    "name": "default",
                                    "repId": {
                                        "id": 1,
                                        "moduleId": 0
                                    },
                                    "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                                    "owner": {
                                        "name": "all",
                                        "isGroup": False
                                    },
                                    "server": "localhost:8084"
                                }
                            },
                            "owner": {
                                "name": "all",
                                "isGroup": False
                            },
                            "repository": {
                                "name": "default",
                                "repId": {
                                    "id": 1,
                                    "moduleId": 0
                                },
                                "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                                "owner": {
                                    "name": "all",
                                    "isGroup": False
                                },
                                "server": "localhost:8084"
                            }
                        },
                    ]
                }
            },

            {
                "method": "get_changesets_in_branch",
                "args": ("default", "/main/scm003"),
                "rtype": Tuple,#[pl.model.Changeset],
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/repos/\w+/branches(/\w+)+/changesets$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": [
                        {
                            "id": 77,
                            "parentId": 76,
                            "comment": "checkin TaskOnBranch test",
                            "creationDate": "2015-06-02T08:59:12",
                            "guid": "799e4fd3-1161-4f8f-be4f-067dbe98ed89",
                            "branch": {
                                "name": "/main/scm003",
                                "id": 1067,
                                "parentId": 3,
                                "lastChangeset": 1383,
                                "comment": "text\r\n",
                                "creationDate": "2015-06-02T08:46:11",
                                "guid": "e99e8843-9bd9-43eb-ad67-c170b516a032",
                                "owner": {
                                    "name": "testing01",
                                    "isGroup": False
                                },
                                "repository": {
                                    "name": "default",
                                    "repId": {
                                        "id": 1,
                                        "moduleId": 0
                                    },
                                    "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                                    "owner": {
                                        "name": "all",
                                        "isGroup": False
                                    },
                                    "server": "localhost:8084"
                                }
                            },
                            "owner": {
                                "name": "testing01",
                                "isGroup": False
                            },
                            "repository": {
                                "name": "default",
                                "repId": {
                                    "id": 1,
                                    "moduleId": 0
                                },
                                "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                                "owner": {
                                    "name": "all",
                                    "isGroup": False
                                },
                                "server": "localhost:8084"
                            }
                        },
                    ]
                }
            },
            {
                "method": "get_changesets_in_branch",
                "args": ("default", "/main/scm003"),
                "kwargs": dict(query="changesetid > 50"),
                "rtype": Tuple,#[pl.model.Changeset],
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/repos/\w+/branches(/\w+)+/changesets$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": [
                        {
                            "id": 77,
                            "parentId": 76,
                            "comment": "checkin TaskOnBranch test",
                            "creationDate": "2015-06-02T08:59:12",
                            "guid": "799e4fd3-1161-4f8f-be4f-067dbe98ed89",
                            "branch": {
                                "name": "/main/scm003",
                                "id": 1067,
                                "parentId": 3,
                                "lastChangeset": 1383,
                                "comment": "text\r\n",
                                "creationDate": "2015-06-02T08:46:11",
                                "guid": "e99e8843-9bd9-43eb-ad67-c170b516a032",
                                "owner": {
                                    "name": "testing01",
                                    "isGroup": False
                                },
                                "repository": {
                                    "name": "default",
                                    "repId": {
                                        "id": 1,
                                        "moduleId": 0
                                    },
                                    "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                                    "owner": {
                                        "name": "all",
                                        "isGroup": False
                                    },
                                    "server": "localhost:8084"
                                }
                            },
                            "owner": {
                                "name": "testing01",
                                "isGroup": False
                            },
                            "repository": {
                                "name": "default",
                                "repId": {
                                    "id": 1,
                                    "moduleId": 0
                                },
                                "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                                "owner": {
                                    "name": "all",
                                    "isGroup": False
                                },
                                "server": "localhost:8084"
                            }
                        },
                    ]
                }
            },

            {
                "method": "get_changeset",
                "args": ("default", 1383),
                "rtype": pl.model.Changeset,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/repos/\w+/changesets/\d+$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "id": 77,
                        "parentId": 76,
                        "comment": "checkin TaskOnBranch test",
                        "creationDate": "2015-06-02T08:59:12",
                        "guid": "799e4fd3-1161-4f8f-be4f-067dbe98ed89",
                        "branch": {
                            "name": "/main/scm003",
                            "id": 1067,
                            "parentId": 3,
                            "lastChangeset": 1383,
                            "comment": "text\r\n",
                            "creationDate": "2015-06-02T08:46:11",
                            "guid": "e99e8843-9bd9-43eb-ad67-c170b516a032",
                            "owner": {
                                "name": "testing01",
                                "isGroup": False
                            },
                            "repository": {
                                "name": "default",
                                "repId": {
                                    "id": 1,
                                    "moduleId": 0
                                },
                                "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                                "owner": {
                                    "name": "all",
                                    "isGroup": False
                                },
                                "server": "localhost:8084"
                            }
                        },
                        "owner": {
                            "name": "testing01",
                            "isGroup": False
                        },
                        "repository": {
                            "name": "default",
                            "repId": {
                                "id": 1,
                                "moduleId": 0
                            },
                            "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                            "owner": {
                                "name": "all",
                                "isGroup": False
                            },
                            "server": "localhost:8084"
                        }
                    }
                }
            },

            # Changes

            {
                "method": "get_pending_changes",
                "args": ("main_wkspace",),
                "rtype": Tuple,#[pl.model.Change],
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/wkspaces/\w+/changes$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": [
                        {
                            "changes": [
                                "CH",
                                "MV"
                            ],
                            "path": "c:\\Users\\scm-user\\wkspaces\\main_wkspace\\audio-prj\\orchestrated.fspro",
                            "oldPath": "c:\\Users\\scm-user\\wkspaces\\main_wkspace\\audio-prj\\audio-prj.fspro",
                            "serverPath": "/audio-prj/orchestrated.fspro",
                            "oldServerPath": "/audio-prj/audio-prj.fspro",
                            "isXlink": False,
                            "localInfo": {
                                "modifiedTime": "2015-07-02T11:16:07.0042908Z",
                                "size": 57906,
                                "isMissing": False
                            },
                            "revisionInfo": {
                                "id": 65,
                                "parentId": -1,
                                "itemId": 187,
                                "type": "text",
                                "size": 57896,
                                "hash": "tLq1aWZ24MGupAHKZAgYFA==",
                                "branchId": 3,
                                "changesetId": 3,
                                "isCheckedOut": False,
                                "creationDate": "2015-04-09T09:51:20",
                                "repositoryId": {
                                    "id": 1,
                                    "moduleId": 0
                                },
                                "owner": {
                                    "name": "scm-user",
                                    "isGroup": False
                                }
                            }
                        },
                    ]
                }
            },
            {
                "method": "get_pending_changes",
                "args": ("main_wkspace",),
                "kwargs": dict(change_types=[pl.model.Change.Type.ALL]),
                "rtype": Tuple,#[pl.model.Change],
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/wkspaces/\w+/changes$"),
                "expected": {
                    "status_code": 200, # OK

                    "content": [
                        {
                            "changes": [
                                "CH",
                                "MV"
                            ],
                            "path": "c:\\Users\\scm-user\\wkspaces\\main_wkspace\\audio-prj\\orchestrated.fspro",
                            "oldPath": "c:\\Users\\scm-user\\wkspaces\\main_wkspace\\audio-prj\\audio-prj.fspro",
                            "serverPath": "/audio-prj/orchestrated.fspro",
                            "oldServerPath": "/audio-prj/audio-prj.fspro",
                            "isXlink": False,
                            "localInfo": {
                                "modifiedTime": "2015-07-02T11:16:07.0042908Z",
                                "size": 57906,
                                "isMissing": False
                            },
                            "revisionInfo": {
                                "id": 65,
                                "parentId": -1,
                                "itemId": 187,
                                "type": "text",
                                "size": 57896,
                                "hash": "tLq1aWZ24MGupAHKZAgYFA==",
                                "branchId": 3,
                                "changesetId": 3,
                                "isCheckedOut": False,
                                "creationDate": "2015-04-09T09:51:20",
                                "repositoryId": {
                                    "id": 1,
                                    "moduleId": 0
                                },
                                "owner": {
                                    "name": "scm-user",
                                    "isGroup": False
                                }
                            }
                        },
                    ]
                }
            },
            {
                "method": "get_pending_changes",
                "args": ("main_wkspace",),
                "kwargs": dict(change_types=[pl.model.Change.Type.ADDED,
                                             pl.model.Change.Type.CHANGED]),
                "rtype": Tuple,#[pl.model.Change],
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/wkspaces/\w+/changes$"),
                "expected": {
                    "status_code": 200, # OK

                    "content": [
                        {
                            "changes": [
                                "CH",
                                "MV"
                            ],
                            "path": "c:\\Users\\scm-user\\wkspaces\\main_wkspace\\audio-prj\\orchestrated.fspro",
                            "oldPath": "c:\\Users\\scm-user\\wkspaces\\main_wkspace\\audio-prj\\audio-prj.fspro",
                            "serverPath": "/audio-prj/orchestrated.fspro",
                            "oldServerPath": "/audio-prj/audio-prj.fspro",
                            "isXlink": False,
                            "localInfo": {
                                "modifiedTime": "2015-07-02T11:16:07.0042908Z",
                                "size": 57906,
                                "isMissing": False
                            },
                            "revisionInfo": {
                                "id": 65,
                                "parentId": -1,
                                "itemId": 187,
                                "type": "text",
                                "size": 57896,
                                "hash": "tLq1aWZ24MGupAHKZAgYFA==",
                                "branchId": 3,
                                "changesetId": 3,
                                "isCheckedOut": False,
                                "creationDate": "2015-04-09T09:51:20",
                                "repositoryId": {
                                    "id": 1,
                                    "moduleId": 0
                                },
                                "owner": {
                                    "name": "scm-user",
                                    "isGroup": False
                                }
                            }
                        },
                    ]
                }
            },
            {
                "method": "get_pending_changes",
                "args": ("main_wkspace",),
                "kwargs": dict(change_types=[pl.model.Change.Type.MOVED,
                                             pl.model.Change.Type.DELETED]),
                "rtype": Tuple,#[pl.model.Change],
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/wkspaces/\w+/changes$"),
                "expected": {
                    "status_code": 200, # OK

                    "content": [
                        {
                            "changes": [
                                "CH",
                                "MV"
                            ],
                            "path": "c:\\Users\\scm-user\\wkspaces\\main_wkspace\\audio-prj\\orchestrated.fspro",
                            "oldPath": "c:\\Users\\scm-user\\wkspaces\\main_wkspace\\audio-prj\\audio-prj.fspro",
                            "serverPath": "/audio-prj/orchestrated.fspro",
                            "oldServerPath": "/audio-prj/audio-prj.fspro",
                            "isXlink": False,
                            "localInfo": {
                                "modifiedTime": "2015-07-02T11:16:07.0042908Z",
                                "size": 57906,
                                "isMissing": False
                            },
                            "revisionInfo": {
                                "id": 65,
                                "parentId": -1,
                                "itemId": 187,
                                "type": "text",
                                "size": 57896,
                                "hash": "tLq1aWZ24MGupAHKZAgYFA==",
                                "branchId": 3,
                                "changesetId": 3,
                                "isCheckedOut": False,
                                "creationDate": "2015-04-09T09:51:20",
                                "repositoryId": {
                                    "id": 1,
                                    "moduleId": 0
                                },
                                "owner": {
                                    "name": "scm-user",
                                    "isGroup": False
                                }
                            }
                        },
                    ]
                }
            },

            {
                "method": "undo_pending_changes",
                "args": ("main_wkspace",
                         [Path("c:\\Users\\scm-user\\wkspaces\\main_wkspace\\audio-prj\\orchestrated.fspro")]),
                "rtype": pl.model.AffectedPaths,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="delete",
                                     path=r"^/api/v1/wkspaces/\w+/changes$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "affectedPaths": [
                            "c:\\Users\\scm-user\\wkspaces\\main_wkspace\\audio-prj\\orchestrated.fspro",
                        ]
                    }
                }
            },
            {
                "method": "undo_pending_changes",
                "args": ("main_wkspace", [Path("audio-prj/orchestrated.fspro")]),
                "rtype": pl.model.AffectedPaths,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="delete",
                                     path=r"^/api/v1/wkspaces/\w+/changes$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "affectedPaths": [
                            "c:\\Users\\scm-user\\wkspaces\\main_wkspace\\audio-prj\\orchestrated.fspro",
                        ]
                    }
                }
            },

            # Workspace Update and Switch

            {
                "method": "get_workspace_update_status",
                "args": ("main_wkspace",),
                "rtype": pl.model.OperationStatus,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/wkspaces/\w+/update$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "status": "Not running",
                    }
                }
            },
            {
                "method": "get_workspace_update_status",
                "args": ("main_wkspace",),
                "rtype": pl.model.OperationStatus,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/wkspaces/\w+/update$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "status": "Failed",
                        "message": "No route to host 'localhost:8084'",
                    }
                }
            },
            {
                "method": "get_workspace_update_status",
                "args": ("main_wkspace",),
                "rtype": pl.model.OperationStatus,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/wkspaces/\w+/update$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "status": "Calculating",
                        "totalFiles": 1356,
                        "totalBytes": 3246739,
                        "updatedFiles": 0,
                        "updatedBytes": 0,
                    }
                }
            },
            {
                "method": "get_workspace_update_status",
                "args": ("main_wkspace",),
                "rtype": pl.model.OperationStatus,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/wkspaces/\w+/update$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "status": "Running",
                        "totalFiles": 1356,
                        "totalBytes": 3246739,
                        "updatedFiles": 356,
                        "updatedBytes": 894433,
                    }
                }
            },
            {
                "method": "get_workspace_update_status",
                "args": ("main_wkspace",),
                "rtype": pl.model.OperationStatus,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/wkspaces/\w+/update$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "status": "Finished",
                        "totalFiles": 1356,
                        "totalBytes": 3246739,
                        "updatedFiles": 1356,
                        "updatedBytes": 3246739,
                    }
                }
            },

            {
                "method": "update_workspace",
                "args": ("main_wkspace",),
                "rtype": pl.model.OperationStatus,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="post",
                                     path=r"^/api/v1/wkspaces/\w+/update$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "status": "Running",
                        "totalFiles": 0,
                        "totalBytes": 0,
                        "updatedFiles": 0,
                        "updatedBytes": 0,
                    }
                }
            },

            {
                "method": "get_workspace_switch_status",
                "args": ("main_wkspace",),
                "rtype": pl.model.OperationStatus,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/wkspaces/\w+/switch$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "status": "Not running",
                    }
                }
            },
            {
                "method": "get_workspace_switch_status",
                "args": ("main_wkspace",),
                "rtype": pl.model.OperationStatus,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/wkspaces/\w+/switch$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "status": "Failed",
                        "message": "No route to host 'localhost:8084'",
                    }
                }
            },
            {
                "method": "get_workspace_switch_status",
                "args": ("main_wkspace",),
                "rtype": pl.model.OperationStatus,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/wkspaces/\w+/switch$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "status": "Calculating",
                        "totalFiles": 1356,
                        "totalBytes": 3246739,
                        "updatedFiles": 0,
                        "updatedBytes": 0,
                    }
                }
            },
            {
                "method": "get_workspace_switch_status",
                "args": ("main_wkspace",),
                "rtype": pl.model.OperationStatus,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/wkspaces/\w+/switch$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "status": "Running",
                        "totalFiles": 1356,
                        "totalBytes": 3246739,
                        "updatedFiles": 356,
                        "updatedBytes": 894433,
                    }
                }
            },
            {
                "method": "get_workspace_switch_status",
                "args": ("main_wkspace",),
                "rtype": pl.model.OperationStatus,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/wkspaces/\w+/switch$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "status": "Finished",
                        "totalFiles": 1356,
                        "totalBytes": 3246739,
                        "updatedFiles": 1356,
                        "updatedBytes": 3246739,
                    }
                }
            },

            {
                "method": "switch_workspace",
                "args": ("main_wkspace", pl.model.ObjectType.BRANCH, "/main/task001"),
                "rtype": pl.model.OperationStatus,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="post",
                                     path=r"^/api/v1/wkspaces/\w+/switch$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "status": "Running",
                        "totalFiles": 0,
                        "totalBytes": 0,
                        "updatedFiles": 0,
                        "updatedBytes": 0,
                    }
                }
            },
            {
                "method": "switch_workspace",
                "args": ("main_wkspace", pl.model.ObjectType.CHANGESET, 1136),
                "rtype": pl.model.OperationStatus,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="post",
                                     path=r"^/api/v1/wkspaces/\w+/switch$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "status": "Running",
                        "totalFiles": 0,
                        "totalBytes": 0,
                        "updatedFiles": 0,
                        "updatedBytes": 0,
                    }
                }
            },
            {
                "method": "switch_workspace",
                "args": ("main_wkspace", pl.model.ObjectType.LABEL, "BL001"),
                "rtype": pl.model.OperationStatus,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="post",
                                     path=r"^/api/v1/wkspaces/\w+/switch$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "status": "Running",
                        "totalFiles": 0,
                        "totalBytes": 0,
                        "updatedFiles": 0,
                        "updatedBytes": 0,
                    }
                }
            },

            # Checkin

            {
                "method": "get_workspace_checkin_status",
                "args": ("main_wkspace",),
                "rtype": pl.model.CheckinStatus,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/wkspaces/\w+/checkin$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "status": "Not running",
                    }
                }
            },
            {
                "method": "get_workspace_checkin_status",
                "args": ("main_wkspace",),
                "rtype": pl.model.CheckinStatus,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/wkspaces/\w+/checkin$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "status": "Failed",
                        "message": "No route to host 'localhost:8084'",
                    }
                }
            },
            {
                "method": "get_workspace_checkin_status",
                "args": ("main_wkspace",),
                "rtype": pl.model.CheckinStatus,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/wkspaces/\w+/checkin$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "status": "Checkin finished",
                        "totalSize": 57990,
                        "transferredSize": 57990,
                    }
                }
            },

            {
                "method": "checkin_workspace",
                "args": ("main_wkspace",),
                "rtype": pl.model.CheckinStatus,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="post",
                                     path=r"^/api/v1/wkspaces/\w+/checkin$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "status": "Checkin operation starting...",
                        "totalSize": 0,
                        "transferredSize": 0,
                    }
                }
            },
            {
                "method": "checkin_workspace",
                "args": ("main_wkspace",),
                "kwargs": dict(comment="Upgrade core engine"),
                "rtype": pl.model.CheckinStatus,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="post",
                                     path=r"^/api/v1/wkspaces/\w+/checkin$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "status": "Checkin operation starting...",
                        "totalSize": 0,
                        "transferredSize": 0,
                    }
                }
            },
            {
                "method": "checkin_workspace",
                "args": ("main_wkspace",),
                "kwargs": dict(paths=["src/foo.c",
                                      "src/bar/baz.c",
                                      "doc"],
                               comment="Upgrade core engine"),
                "rtype": pl.model.CheckinStatus,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="post",
                                     path=r"^/api/v1/wkspaces/\w+/checkin$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "status": "Checkin operation starting...",
                        "totalSize": 0,
                        "transferredSize": 0,
                    }
                }
            },
            {
                "method": "checkin_workspace",
                "args": ("main_wkspace",),
                "kwargs": dict(paths=["src/foo.c",
                                      "src/bar/baz.c",
                                      "doc"],
                               comment="Upgrade core engine",
                               recurse=False),
                "rtype": pl.model.CheckinStatus,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="post",
                                     path=r"^/api/v1/wkspaces/\w+/checkin$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "status": "Checkin operation starting...",
                        "totalSize": 0,
                        "transferredSize": 0,
                    }
                }
            },

            # Repository contents

            {
                "method": "get_item",
                "args": ("my_repo", "src/lib/foo.c"),
                "rtype": pl.model.Item,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/repos/\w+/contents/[^/]+(/[^/]+)*$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "revisionId": 771,
                        "type": "file",
                        "size": 57913,
                        "name": "soundproject.fspro",
                        "path": "/fmod/soundproject.fspro",
                        "isUnderXlink": False,
                        "hash": "/2ygGGfoXDq9bbKZJCzj9g==",
                        "content": "http://localhost:9090/api/v1/repos/my_repo/revisions/771/blob",
                        "repository": {
                            "repId":
                            {
                                "id": 1,
                                "moduleId": 0
                            },
                            "name": "my_repo",
                            "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                            "owner":
                            {
                                "name": "all",
                                "isGroup": False
                            },
                            "server": "localhost:8084"
                        }
                    }
                }
            },
            {
                "method": "get_item",
                "args": ("my_repo", "src/lib/foo.c"),
                "rtype": pl.model.Item,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/repos/\w+/contents/[^/]+(/[^/]+)*$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "revisionId": 3648,
                        "type": "directory",
                        "size": 0,
                        "name": "lib",
                        "path": "/lib",
                        "isUnderXlink": False,
                        "items": [
                            {
                                "revisionId": 6878,
                                "type": "xlink",
                                "size": 0,
                                "name": "xlink",
                                "path": "/lib/xlink",
                                "xlinkTarget": {
                                    "changesetGuid": "41acf2bd-1484-4679-a634-2570d9a7801b",
                                    "changesetId": 2,
                                    "repository": "big",
                                    "server": "localhost:8084"
                                }
                            },
                        ],
                        "repository": {
                            "repId":
                            {
                                "id": 1,
                                "moduleId": 0
                            },
                            "name": "my_repo",
                            "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                            "owner":
                            {
                                "name": "all",
                                "isGroup": False
                            },
                            "server": "localhost:8084"
                        }
                    }
                }
            },
            {
                "method": "get_item",
                "args": ("my_repo", "src/lib/foo.c"),
                "rtype": pl.model.Item,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/repos/\w+/contents/[^/]+(/[^/]+)*$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "revisionId": 2427,
                        "type": "directory",
                        "size": 0,
                        "name": "mono",
                        "path": "/lib/xlink/mono",
                        "isUnderXlink": True,
                        "items": [
                            {
                                "revisionId": 46348,
                                "type": "file",
                                "size": 26383,
                                "name": "COPYING.LIB",
                                "path": "/lib/xlink/mono/COPYING.LIB",
                                "hash": "uFbSL8ON1UNln1XUYeAc7w==",
                                "content": "http://localhost:9090/api/v1/repos/my_repo/revisions/46348/blob"
                            },
                            {
                                "type": "directory",
                                "size": 0,
                                "name": "data",
                                "path": "/lib/xlink/mono/data"
                            },
                        ],
                        "repository": {
                            "repId":
                            {
                                "id": 1,
                                "moduleId": 0
                            },
                            "name": "my_repo",
                            "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                            "owner":
                            {
                                "name": "all",
                                "isGroup": False
                            },
                            "server": "localhost:8084"
                        }
                    }
                }
            },

            {
                "method": "get_item_in_branch",
                "args": ("my_repo", "main/scm003", "src/lib/foo.c"),
                "rtype": pl.model.Item,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/repos/\w+/branches(/\w+)+/contents/[^/]+(/[^/]+)*$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "revisionId": 771,
                        "type": "file",
                        "size": 57913,
                        "name": "soundproject.fspro",
                        "path": "/fmod/soundproject.fspro",
                        "isUnderXlink": False,
                        "hash": "/2ygGGfoXDq9bbKZJCzj9g==",
                        "content": "http://localhost:9090/api/v1/repos/my_repo/revisions/771/blob",
                        "repository": {
                            "repId":
                            {
                                "id": 1,
                                "moduleId": 0
                            },
                            "name": "my_repo",
                            "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                            "owner":
                            {
                                "name": "all",
                                "isGroup": False
                            },
                            "server": "localhost:8084"
                        }
                    }
                }
            },
            {
                "method": "get_item_in_branch",
                "args": ("my_repo", "main/scm003", "src/lib/foo.c"),
                "rtype": pl.model.Item,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/repos/\w+/branches(/\w+)+/contents/[^/]+(/[^/]+)*$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "revisionId": 3648,
                        "type": "directory",
                        "size": 0,
                        "name": "lib",
                        "path": "/lib",
                        "isUnderXlink": False,
                        "items": [
                            {
                                "revisionId": 6878,
                                "type": "xlink",
                                "size": 0,
                                "name": "xlink",
                                "path": "/lib/xlink",
                                "xlinkTarget": {
                                    "changesetGuid": "41acf2bd-1484-4679-a634-2570d9a7801b",
                                    "changesetId": 2,
                                    "repository": "big",
                                    "server": "localhost:8084"
                                }
                            },
                        ],
                        "repository": {
                            "repId":
                            {
                                "id": 1,
                                "moduleId": 0
                            },
                            "name": "my_repo",
                            "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                            "owner":
                            {
                                "name": "all",
                                "isGroup": False
                            },
                            "server": "localhost:8084"
                        }
                    }
                }
            },
            {
                "method": "get_item_in_branch",
                "args": ("my_repo", "main/scm003", "src/lib/foo.c"),
                "rtype": pl.model.Item,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/repos/\w+/branches(/\w+)+/contents/[^/]+(/[^/]+)*$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "revisionId": 2427,
                        "type": "directory",
                        "size": 0,
                        "name": "mono",
                        "path": "/lib/xlink/mono",
                        "isUnderXlink": True,
                        "items": [
                            {
                                "revisionId": 46348,
                                "type": "file",
                                "size": 26383,
                                "name": "COPYING.LIB",
                                "path": "/lib/xlink/mono/COPYING.LIB",
                                "hash": "uFbSL8ON1UNln1XUYeAc7w==",
                                "content": "http://localhost:9090/api/v1/repos/my_repo/revisions/46348/blob"
                            },
                            {
                                "type": "directory",
                                "size": 0,
                                "name": "data",
                                "path": "/lib/xlink/mono/data"
                            },
                        ],
                        "repository": {
                            "repId":
                            {
                                "id": 1,
                                "moduleId": 0
                            },
                            "name": "my_repo",
                            "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                            "owner":
                            {
                                "name": "all",
                                "isGroup": False
                            },
                            "server": "localhost:8084"
                        }
                    }
                }
            },

            {
                "method": "get_item_in_changeset",
                "args": ("my_repo", 5378, "src/lib/foo.c"),
                "rtype": pl.model.Item,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/repos/\w+/changesets/\d+/contents/[^/]+(/[^/]+)*$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "revisionId": 771,
                        "type": "file",
                        "size": 57913,
                        "name": "soundproject.fspro",
                        "path": "/fmod/soundproject.fspro",
                        "isUnderXlink": False,
                        "hash": "/2ygGGfoXDq9bbKZJCzj9g==",
                        "content": "http://localhost:9090/api/v1/repos/my_repo/revisions/771/blob",
                        "repository": {
                            "repId":
                            {
                                "id": 1,
                                "moduleId": 0
                            },
                            "name": "my_repo",
                            "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                            "owner":
                            {
                                "name": "all",
                                "isGroup": False
                            },
                            "server": "localhost:8084"
                        }
                    }
                }
            },
            {
                "method": "get_item_in_changeset",
                "args": ("my_repo", 5378, "src/lib/foo.c"),
                "rtype": pl.model.Item,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/repos/\w+/changesets/\d+/contents/[^/]+(/[^/]+)*$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "revisionId": 3648,
                        "type": "directory",
                        "size": 0,
                        "name": "lib",
                        "path": "/lib",
                        "isUnderXlink": False,
                        "items": [
                            {
                                "revisionId": 6878,
                                "type": "xlink",
                                "size": 0,
                                "name": "xlink",
                                "path": "/lib/xlink",
                                "xlinkTarget": {
                                    "changesetGuid": "41acf2bd-1484-4679-a634-2570d9a7801b",
                                    "changesetId": 2,
                                    "repository": "big",
                                    "server": "localhost:8084"
                                }
                            },
                        ],
                        "repository": {
                            "repId":
                            {
                                "id": 1,
                                "moduleId": 0
                            },
                            "name": "my_repo",
                            "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                            "owner":
                            {
                                "name": "all",
                                "isGroup": False
                            },
                            "server": "localhost:8084"
                        }
                    }
                }
            },
            {
                "method": "get_item_in_changeset",
                "args": ("my_repo", 5378, "src/lib/foo.c"),
                "rtype": pl.model.Item,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/repos/\w+/changesets/\d+/contents/[^/]+(/[^/]+)*$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "revisionId": 2427,
                        "type": "directory",
                        "size": 0,
                        "name": "mono",
                        "path": "/lib/xlink/mono",
                        "isUnderXlink": True,
                        "items": [
                            {
                                "revisionId": 46348,
                                "type": "file",
                                "size": 26383,
                                "name": "COPYING.LIB",
                                "path": "/lib/xlink/mono/COPYING.LIB",
                                "hash": "uFbSL8ON1UNln1XUYeAc7w==",
                                "content": "http://localhost:9090/api/v1/repos/my_repo/revisions/46348/blob"
                            },
                            {
                                "type": "directory",
                                "size": 0,
                                "name": "data",
                                "path": "/lib/xlink/mono/data"
                            },
                        ],
                        "repository": {
                            "repId":
                            {
                                "id": 1,
                                "moduleId": 0
                            },
                            "name": "my_repo",
                            "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                            "owner":
                            {
                                "name": "all",
                                "isGroup": False
                            },
                            "server": "localhost:8084"
                        }
                    }
                }
            },

            {
                "method": "get_item_in_label",
                "args": ("my_repo", "BL001", "src/lib/foo.c"),
                "rtype": pl.model.Item,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/repos/\w+/labels/\w+/contents/[^/]+(/[^/]+)*$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "revisionId": 771,
                        "type": "file",
                        "size": 57913,
                        "name": "soundproject.fspro",
                        "path": "/fmod/soundproject.fspro",
                        "isUnderXlink": False,
                        "hash": "/2ygGGfoXDq9bbKZJCzj9g==",
                        "content": "http://localhost:9090/api/v1/repos/my_repo/revisions/771/blob",
                        "repository": {
                            "repId":
                            {
                                "id": 1,
                                "moduleId": 0
                            },
                            "name": "my_repo",
                            "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                            "owner":
                            {
                                "name": "all",
                                "isGroup": False
                            },
                            "server": "localhost:8084"
                        }
                    }
                }
            },
            {
                "method": "get_item_in_label",
                "args": ("my_repo", "BL001", "src/lib/foo.c"),
                "rtype": pl.model.Item,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/repos/\w+/labels/\w+/contents/[^/]+(/[^/]+)*$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "revisionId": 3648,
                        "type": "directory",
                        "size": 0,
                        "name": "lib",
                        "path": "/lib",
                        "isUnderXlink": False,
                        "items": [
                            {
                                "revisionId": 6878,
                                "type": "xlink",
                                "size": 0,
                                "name": "xlink",
                                "path": "/lib/xlink",
                                "xlinkTarget": {
                                    "changesetGuid": "41acf2bd-1484-4679-a634-2570d9a7801b",
                                    "changesetId": 2,
                                    "repository": "big",
                                    "server": "localhost:8084"
                                }
                            },
                        ],
                        "repository": {
                            "repId":
                            {
                                "id": 1,
                                "moduleId": 0
                            },
                            "name": "my_repo",
                            "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                            "owner":
                            {
                                "name": "all",
                                "isGroup": False
                            },
                            "server": "localhost:8084"
                        }
                    }
                }
            },
            {
                "method": "get_item_in_label",
                "args": ("my_repo", "BL001", "src/lib/foo.c"),
                "rtype": pl.model.Item,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/repos/\w+/labels/\w+/contents/[^/]+(/[^/]+)*$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "revisionId": 2427,
                        "type": "directory",
                        "size": 0,
                        "name": "mono",
                        "path": "/lib/xlink/mono",
                        "isUnderXlink": True,
                        "items": [
                            {
                                "revisionId": 46348,
                                "type": "file",
                                "size": 26383,
                                "name": "COPYING.LIB",
                                "path": "/lib/xlink/mono/COPYING.LIB",
                                "hash": "uFbSL8ON1UNln1XUYeAc7w==",
                                "content": "http://localhost:9090/api/v1/repos/my_repo/revisions/46348/blob"
                            },
                            {
                                "type": "directory",
                                "size": 0,
                                "name": "data",
                                "path": "/lib/xlink/mono/data"
                            },
                        ],
                        "repository": {
                            "repId":
                            {
                                "id": 1,
                                "moduleId": 0
                            },
                            "name": "my_repo",
                            "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                            "owner":
                            {
                                "name": "all",
                                "isGroup": False
                            },
                            "server": "localhost:8084"
                        }
                    }
                }
            },

            {
                "method": "get_item_revision",
                "args": ("my_repo", "src/lib/foo.c#cs:3"),
                "rtype": pl.model.Item,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/repos/\w+/revisions/[^/]+(/[^/]+)*$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "revisionId": 3526,
                        "type": "file",
                        "size": 71,
                        "name": "foo.c",
                        "path": "/src/lib/foo.c",
                        "changeset": 1406,
                        "branch": "br:/main/scm003",
                        "hash": "tNYiUA4VyMJxJrK0kic7mg==",
                        "contents": "http://localhost:9090/api/v1/repos/my_repo/revisions/3526/blob",
                        "repository": {
                            "repId":
                            {
                                "id": 1,
                                "moduleId": 0
                            },
                            "name": "my_repo",
                            "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                            "owner":
                            {
                                "name": "all",
                                "isGroup": False
                            },
                            "server": "localhost:8084"
                        }
                    }
                }
            },
            {
                "method": "get_item_revision",
                "args": ("my_repo", "src/lib#cs:3"),
                "rtype": pl.model.Item,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/repos/\w+/revisions/[^/]+(/[^/]+)*$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "revisionId": 5355,
                        "type": "directory",
                        "size": 0,
                        "name": "lib",
                        "path": "/src/lib",
                        "changeset": 1406,
                        "branch": "br:/main/scm003",
                        "repository": {
                            "repId":
                            {
                                "id": 1,
                                "moduleId": 0
                            },
                            "name": "my_repo",
                            "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                            "owner":
                            {
                                "name": "all",
                                "isGroup": False
                            },
                            "server": "localhost:8084"
                        }
                    }
                }
            },

            {
                "method": "get_item_revision_history_in_branch",
                "args": ("my_repo", "main/scm003", "src/lib/foo.c"),
                "rtype": Tuple,#pl.model.RevisionHistoryItem,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/repos/\w+/branches(/\w+)+/history/[^/]+(/[^/]+)*$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": [
                        {
                            "revisionId": 104,
                            "type": "text",
                            "owner": {
                                "name": "tester",
                                "isGroup": False
                            },
                            "creationDate": "2015-04-09T09:51:20",
                            "comment": "Restore method implementation",
                            "revisionLink": "http://localhost:9090/api/v1/repos/my_repo/revisions/104",
                            "changesetId": 3,
                            "changesetLink": "http://localhost:9090/api/v1/repos/my_repo/changesets/3",
                            "branchName": "/main",
                            "branchLink": "http://localhost:9090/api/v1/repos/my_repo/branches/main",
                            "repositoryName": "my_repo",
                            "repositoryLink": "http://localhost:9090/api/v1/repos/my_repo"
                        },
                    ]
                }
            },

            {
                "method": "get_item_revision_history_in_changeset",
                "args": ("my_repo", 5378, "src/lib/foo.c"),
                "rtype": Tuple,#pl.model.RevisionHistoryItem,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/repos/\w+/changesets/\d+/history/[^/]+(/[^/]+)*$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": [
                        {
                            "revisionId": 104,
                            "type": "text",
                            "owner": {
                                "name": "tester",
                                "isGroup": False
                            },
                            "creationDate": "2015-04-09T09:51:20",
                            "comment": "Restore method implementation",
                            "revisionLink": "http://localhost:9090/api/v1/repos/my_repo/revisions/104",
                            "changesetId": 3,
                            "changesetLink": "http://localhost:9090/api/v1/repos/my_repo/changesets/3",
                            "branchName": "/main",
                            "branchLink": "http://localhost:9090/api/v1/repos/my_repo/branches/main",
                            "repositoryName": "my_repo",
                            "repositoryLink": "http://localhost:9090/api/v1/repos/my_repo"
                        },
                    ]
                }
            },

            {
                "method": "get_item_revision_history_in_label",
                "args": ("my_repo", "BL001", "src/lib/foo.c"),
                "rtype": Tuple,#pl.model.RevisionHistoryItem,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/repos/\w+/labels/\w+/history/[^/]+(/[^/]+)*$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": [
                        {
                            "revisionId": 104,
                            "type": "text",
                            "owner": {
                                "name": "tester",
                                "isGroup": False
                            },
                            "creationDate": "2015-04-09T09:51:20",
                            "comment": "Restore method implementation",
                            "revisionLink": "http://localhost:9090/api/v1/repos/my_repo/revisions/104",
                            "changesetId": 3,
                            "changesetLink": "http://localhost:9090/api/v1/repos/my_repo/changesets/3",
                            "branchName": "/main",
                            "branchLink": "http://localhost:9090/api/v1/repos/my_repo/branches/main",
                            "repositoryName": "my_repo",
                            "repositoryLink": "http://localhost:9090/api/v1/repos/my_repo"
                        },
                    ]
                }
            },

            # Diff

            {
                "method": "diff_changesets",
                "args": ("default", 3, 2),
                "rtype": Tuple,#[pl.model.Diff],
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/repos/\w+/changesets/\d+/diff/\d+$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": [
                        {
                            "status": "Changed",
                            "path": "/lib/xlink",
                            "isDirectory": True,
                            "isUnderXlink": False,
                            "xlink": {
                                "changesetGuid": "ff92e897-b662-40f1-9a1f-a17349cbc7c6",
                                "changesetId": 3,
                                "repository": "big",
                                "server": "localhost:8084"
                            },
                            "baseXlink": {
                                "changesetGuid": "c75c04ec-3546-46e4-bbb7-031b523dca7d",
                                "changesetId": 2,
                                "repository": "big",
                                "server": "localhost:8084"
                            },
                            "isItemFSProtectionChanged": False,
                            "itemFileSystemProtection": "NOT_DEFINED",
                            "repository": {
                                "name": "default",
                                "server": "localhost:8084"
                            }
                        },
                        {
                            "status": "Changed",
                            "path": "/lib/xlink/mono/.gitignore",
                            "revisionId": 150892,
                            "isDirectory": False,
                            "size": 1616,
                            "hash": "u0gJQzQnjLNUUHRI1+QQLg==",
                            "isUnderXlink": True,
                            "merges": [
                                {
                                    "mergeType": "Merged",
                                    "sourceChangeset": {
                                        "id": 3,
                                        "parentId": 2,
                                        "comment": "multiple changes",
                                        "creationDate": "2015-07-16T10:01:32",
                                        "guid": "4d064ea0-4694-41b2-adec-15c3df243dd7",
                                        "branch": {
                                            "name": "/main/scm002",
                                            "id": 150865,
                                            "parentId": 3,
                                            "lastChangeset": 3,
                                            "comment": "",
                                            "creationDate": "2015-07-16T10:01:30",
                                            "guid": "764c4842-aab8-451a-b802-29162d2a399f",
                                            "owner": {
                                                "name": "tester",
                                                "isGroup": False
                                            },
                                            "repository": {
                                                "name": "big",
                                                "repId": {
                                                    "id": 4,
                                                    "moduleId": 0
                                                },
                                                "guid": "301b269c-6d24-4347-afc1-f095da43f3f2",
                                                "owner": {
                                                    "name": "testing01",
                                                    "isGroup": False
                                                },
                                                "server": "localhost:8084"
                                            }
                                        },
                                        "repository": {
                                            "name": "big",
                                            "repId": {
                                                "id": 4,
                                                "moduleId": 0
                                            },
                                            "guid": "301b269c-6d24-4347-afc1-f095da43f3f2",
                                            "owner": {
                                                "name": "testing01",
                                                "isGroup": False
                                            },
                                            "server": "localhost:8084"
                                        }
                                    }
                                }
                            ],
                            "isItemFSProtectionChanged": False,
                            "itemFileSystemProtection": "NOT_DEFINED",
                            "modifiedTime": "2015-07-16T10:04:21",
                            "createdBy": {
                                "name": "tester",
                                "isGroup": False
                            },
                            "repository": {
                                "name": "big",
                                "repId": {
                                    "id": 4,
                                    "moduleId": 0
                                },
                                "server": "localhost:8084"
                            }
                        }
                    ]
                }
            },

            {
                "method": "diff_changeset",
                "args": ("default", 3),
                "rtype": Tuple,#[pl.model.Diff],
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/repos/\w+/changesets/\d+/diff$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": [
                        {
                            "status": "Changed",
                            "path": "/lib/xlink",
                            "isDirectory": True,
                            "isUnderXlink": False,
                            "xlink": {
                                "changesetGuid": "ff92e897-b662-40f1-9a1f-a17349cbc7c6",
                                "changesetId": 3,
                                "repository": "big",
                                "server": "localhost:8084"
                            },
                            "baseXlink": {
                                "changesetGuid": "c75c04ec-3546-46e4-bbb7-031b523dca7d",
                                "changesetId": 2,
                                "repository": "big",
                                "server": "localhost:8084"
                            },
                            "isItemFSProtectionChanged": False,
                            "itemFileSystemProtection": "NOT_DEFINED",
                            "repository": {
                                "name": "default",
                                "server": "localhost:8084"
                            }
                        },
                        {
                            "status": "Changed",
                            "path": "/lib/xlink/mono/.gitignore",
                            "revisionId": 150892,
                            "isDirectory": False,
                            "size": 1616,
                            "hash": "u0gJQzQnjLNUUHRI1+QQLg==",
                            "isUnderXlink": True,
                            "merges": [
                                {
                                    "mergeType": "Merged",
                                    "sourceChangeset": {
                                        "id": 3,
                                        "parentId": 2,
                                        "comment": "multiple changes",
                                        "creationDate": "2015-07-16T10:01:32",
                                        "guid": "4d064ea0-4694-41b2-adec-15c3df243dd7",
                                        "branch": {
                                            "name": "/main/scm002",
                                            "id": 150865,
                                            "parentId": 3,
                                            "lastChangeset": 3,
                                            "comment": "",
                                            "creationDate": "2015-07-16T10:01:30",
                                            "guid": "764c4842-aab8-451a-b802-29162d2a399f",
                                            "owner": {
                                                "name": "tester",
                                                "isGroup": False
                                            },
                                            "repository": {
                                                "name": "big",
                                                "repId": {
                                                    "id": 4,
                                                    "moduleId": 0
                                                },
                                                "guid": "301b269c-6d24-4347-afc1-f095da43f3f2",
                                                "owner": {
                                                    "name": "testing01",
                                                    "isGroup": False
                                                },
                                                "server": "localhost:8084"
                                            }
                                        },
                                        "repository": {
                                            "name": "big",
                                            "repId": {
                                                "id": 4,
                                                "moduleId": 0
                                            },
                                            "guid": "301b269c-6d24-4347-afc1-f095da43f3f2",
                                            "owner": {
                                                "name": "testing01",
                                                "isGroup": False
                                            },
                                            "server": "localhost:8084"
                                        }
                                    }
                                }
                            ],
                            "isItemFSProtectionChanged": False,
                            "itemFileSystemProtection": "NOT_DEFINED",
                            "modifiedTime": "2015-07-16T10:04:21",
                            "createdBy": {
                                "name": "tester",
                                "isGroup": False
                            },
                            "repository": {
                                "name": "big",
                                "repId": {
                                    "id": 4,
                                    "moduleId": 0
                                },
                                "server": "localhost:8084"
                            }
                        }
                    ]
                }
            },

            {
                "method": "diff_branch",
                "args": ("default", "/main/scm003"),
                "rtype": Tuple,#[pl.model.Diff],
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="get",
                                     path=r"^/api/v1/repos/\w+/branches(/\w+)+/diff$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": [
                        {
                            "status": "Changed",
                            "path": "/lib/xlink",
                            "isDirectory": True,
                            "isUnderXlink": False,
                            "xlink": {
                                "changesetGuid": "ff92e897-b662-40f1-9a1f-a17349cbc7c6",
                                "changesetId": 3,
                                "repository": "big",
                                "server": "localhost:8084"
                            },
                            "baseXlink": {
                                "changesetGuid": "c75c04ec-3546-46e4-bbb7-031b523dca7d",
                                "changesetId": 2,
                                "repository": "big",
                                "server": "localhost:8084"
                            },
                            "isItemFSProtectionChanged": False,
                            "itemFileSystemProtection": "NOT_DEFINED",
                            "repository": {
                                "name": "default",
                                "server": "localhost:8084"
                            }
                        },
                        {
                            "status": "Changed",
                            "path": "/lib/xlink/mono/.gitignore",
                            "revisionId": 150892,
                            "isDirectory": False,
                            "size": 1616,
                            "hash": "u0gJQzQnjLNUUHRI1+QQLg==",
                            "isUnderXlink": True,
                            "merges": [
                                {
                                    "mergeType": "Merged",
                                    "sourceChangeset": {
                                        "id": 3,
                                        "parentId": 2,
                                        "comment": "multiple changes",
                                        "creationDate": "2015-07-16T10:01:32",
                                        "guid": "4d064ea0-4694-41b2-adec-15c3df243dd7",
                                        "branch": {
                                            "name": "/main/scm002",
                                            "id": 150865,
                                            "parentId": 3,
                                            "lastChangeset": 3,
                                            "comment": "",
                                            "creationDate": "2015-07-16T10:01:30",
                                            "guid": "764c4842-aab8-451a-b802-29162d2a399f",
                                            "owner": {
                                                "name": "tester",
                                                "isGroup": False
                                            },
                                            "repository": {
                                                "name": "big",
                                                "repId": {
                                                    "id": 4,
                                                    "moduleId": 0
                                                },
                                                "guid": "301b269c-6d24-4347-afc1-f095da43f3f2",
                                                "owner": {
                                                    "name": "testing01",
                                                    "isGroup": False
                                                },
                                                "server": "localhost:8084"
                                            }
                                        },
                                        "repository": {
                                            "name": "big",
                                            "repId": {
                                                "id": 4,
                                                "moduleId": 0
                                            },
                                            "guid": "301b269c-6d24-4347-afc1-f095da43f3f2",
                                            "owner": {
                                                "name": "testing01",
                                                "isGroup": False
                                            },
                                            "server": "localhost:8084"
                                        }
                                    }
                                }
                            ],
                            "isItemFSProtectionChanged": False,
                            "itemFileSystemProtection": "NOT_DEFINED",
                            "modifiedTime": "2015-07-16T10:04:21",
                            "createdBy": {
                                "name": "tester",
                                "isGroup": False
                            },
                            "repository": {
                                "name": "big",
                                "repId": {
                                    "id": 4,
                                    "moduleId": 0
                                },
                                "server": "localhost:8084"
                            }
                        }
                    ]
                }
            },

            # Workspace actions

            {
                "method": "add_workspace_item",
                "args": ("my_wkspace", "src/lib"),
                "kwargs": dict(add_parents=True,
                               checkout_parent=False,
                               recurse=True),
                "rtype": pl.model.AffectedPaths,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="post",
                                     path=r"^/api/v1/wkspaces/\w+/content/[^/]+(/[^/]+)*$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "affectedPaths": [
                            "c:\\wkspaces\\my_wkspace\\src\\lib\\descriptor.h",
                            "c:\\wkspaces\\my_wkspace\\src\\lib\\code.c",
                        ]
                    }
                }
            },
            {
                "method": "add_workspace_item",
                "args": ("my_wkspace", "src/lib"),
                "rtype": pl.model.AffectedPaths,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="post",
                                     path=r"^/api/v1/wkspaces/\w+/content/[^/]+(/[^/]+)*$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "affectedPaths": [
                            "c:\\wkspaces\\my_wkspace\\src\\lib\\descriptor.h",
                            "c:\\wkspaces\\my_wkspace\\src\\lib\\code.c",
                        ]
                    }
                }
            },
            {
                "method": "add_workspace_item",
                "args": ("my_wkspace", "src/lib/code.c"),
                "kwargs": dict(recurse=False),
                "rtype": pl.model.AffectedPaths,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="post",
                                     path=r"^/api/v1/wkspaces/\w+/content/[^/]+(/[^/]+)*$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "affectedPaths": [
                            "c:\\wkspaces\\my_wkspace\\src\\lib\\code.c",
                        ]
                    }
                }
            },

            {
                "method": "checkout_workspace_item",
                "args": ("my_wkspace", "src/lib/code.c"),
                "rtype": pl.model.AffectedPaths,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="put",
                                     path=r"^/api/v1/wkspaces/\w+/content/[^/]+(/[^/]+)*$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "affectedPaths": [
                            "c:\\wkspaces\\my_wkspace\\src\\lib\\code.c",
                        ]
                    }
                }
            },

            {
                "method": "move_workspace_item",
                "args": ("my_wkspace", "src/lib/foo.c", "src/bar.c"),
                "rtype": pl.model.AffectedPaths,
                "urlmatch": urlmatch(scheme=scheme, netloc=netloc, method="patch",
                                     path=r"^/api/v1/wkspaces/\w+/content/[^/]+(/[^/]+)*$"),
                "expected": {
                    "status_code": 200, # OK
                    "content": {
                        "affectedPaths": [
                            "c:\\wkspaces\\my_wkspace\\src\\bar.c",
                        ]
                    }
                }
            },

        ]

    @classmethod
    def tearDownClass(cls):
        cls.pl = None

    @staticmethod
    def response(test):
        return {"status_code": test["expected"]["status_code"],
                "content":     test["expected"]["content"]}

    @staticmethod
    @all_requests
    def request_mock(url, request, test=None):
        return TestPlastic.response(test)

    @classmethod
    def select_tests_for_tag(cls, tag, test_table=None):
        return (test for test in test_table or cls.test_table
                if test.get("tag") == tag)

    @classmethod
    def select_tests_for_method(cls, method_name, test_table=None):
        return (test for test in test_table or cls.test_table
                if test["method"] == method_name)

    def do_test(self, test, mock=None):
        func = getattr(self.pl, test["method"])
        if mock is None:
            mock = test["urlmatch"](lambda url, request, test=None:
                                    TestPlastic.response(test))
        with HTTMock(partial(mock, test=test)):
            ret = func(*test.get("args", ()), **test.get("kwargs", {}))
        if "rtype" in test:
            rtype = test["rtype"]
            if rtype is None:
                self.assertIsNone(ret)
            else:
                self.assertIsInstance(ret, rtype)
        return ret

    def test(self):
        repository_name  = "10031411_2021MY_ADCAM10_MID_ECU"
        workspace_name   = "10031411_2021MY_ADCAM10_MID_ECU"
        repository1_name = "repo_new"
        for test in self.test_table:
            #print(test["method"])
            ret = self.do_test(test, mock=self.request_mock)
            #print(ret)
            #r = requests.get('http://google.com/')
            #print(r.status_code)
            #print(r.content) # 'Oh hai'
            #print(r.json())  # 'Oh hai'

    # Repositories

    def test_get_repositories(self):
        method_name = "get_repositories"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    def test_create_repository(self):
        method_name = "create_repository"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    def test_get_repository(self):
        method_name = "get_repository"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    def test_rename_repository(self):
        method_name = "rename_repository"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    def test_delete_repository(self):
        method_name = "delete_repository"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    # Workspaces

    def test_get_workspaces(self):
        method_name = "get_workspaces"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    def test_create_workspace(self):
        method_name = "create_workspace"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    def test_get_workspace(self):
        method_name = "get_workspace"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    def test_rename_workspace(self):
        method_name = "rename_workspace"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    def test_delete_workspace(self):
        method_name = "delete_workspace"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    # Branches

    def test_get_branches(self):
        method_name = "get_branches"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    def test_create_branch(self):
        method_name = "create_branch"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    def test_get_branch(self):
        method_name = "get_branch"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    def test_rename_branch(self):
        method_name = "rename_branch"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    def test_delete_branch(self):
        method_name = "delete_branch"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    # Labels

    def test_get_labels(self):
        method_name = "get_labels"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    def test_create_label(self):
        method_name = "create_label"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    def test_get_label(self):
        method_name = "get_label"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    def test_rename_label(self):
        method_name = "rename_label"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    def test_delete_label(self):
        method_name = "delete_label"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    # Changesets

    def test_get_changesets(self):
        method_name = "get_changesets"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    def test_get_changesets_in_branch(self):
        method_name = "get_changesets_in_branch"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    def test_get_changeset(self):
        method_name = "get_changeset"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    # Changes

    def test_get_pending_changes(self):
        method_name = "get_pending_changes"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    # @staticmethod
    # @urlmatch(scheme="http", netloc="localhost:9090",
    #           path=r"^/api/v1/wkspaces/\w+/changes$", method="delete")
    # def mock_undo_pending_changes(url, request, test=None):
    #     return TestPlastic.response(test)

    def test_undo_pending_changes(self):
        method_name = "undo_pending_changes"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)#, mock=self.mock_undo_pending_changes)

    # Workspace Update and Switch

    def test_get_workspace_update_status(self):
        method_name = "get_workspace_update_status"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    def test_update_workspace(self):
        method_name = "update_workspace"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    def test_get_workspace_switch_status(self):
        method_name = "get_workspace_switch_status"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    def test_switch_workspace(self):
        method_name = "switch_workspace"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    # Checkin

    def test_get_workspace_checkin_status(self):
        method_name = "get_workspace_checkin_status"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    def test_checkin_workspace(self):
        method_name = "checkin_workspace"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    # Repository contents

    def test_get_item(self):
        method_name = "get_item"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    def test_get_item_in_branch(self):
        method_name = "get_item_in_branch"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    def test_get_item_in_changeset(self):
        method_name = "get_item_in_changeset"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    def test_get_item_in_label(self):
        method_name = "get_item_in_label"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    def test_get_item_revision(self):
        method_name = "get_item_revision"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    def test_get_item_revision_history_in_branch(self):
        method_name = "get_item_revision_history_in_branch"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    def test_get_item_revision_history_in_changeset(self):
        method_name = "get_item_revision_history_in_changeset"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    def test_get_item_revision_history_in_label(self):
        method_name = "get_item_revision_history_in_label"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    # Diff

    def test_diff_changesets(self):
        method_name = "diff_changesets"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    def test_diff_changeset(self):
        method_name = "diff_changeset"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    def test_diff_branch(self):
        method_name = "diff_branch"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    # Workspace actions

    def test_add_workspace_item(self):
        method_name = "add_workspace_item"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    def test_checkout_workspace_item(self):
        method_name = "checkout_workspace_item"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)

    def test_move_workspace_item(self):
        method_name = "move_workspace_item"
        for test in self.select_tests_for_method(method_name):
            ret = self.do_test(test)
