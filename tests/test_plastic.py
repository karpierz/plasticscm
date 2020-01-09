# Copyright (c) 2019-2019 Adam Karpierz
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

    @staticmethod
    def response(test):
        return {"status_code": test["expected"]["status_code"],
                "content":     test["expected"]["content"]}

    @staticmethod
    @all_requests
    def request_mock(url, request, test=None):
        return TestPlastic.response(test)

    def do_test(self, func_name, mock, test):
        func = getattr(self.pl, func_name)
        with HTTMock(partial(mock, test=test)):
            ret = func(*test.get("args", ()), **test.get("kwargs", {}))
        if "rtype" in test:
            rtype = test["rtype"]
            if rtype is None:
                self.assertIsNone(ret)
            else:
                self.assertIsInstance(ret, rtype)
        return ret

    @classmethod
    def setUpClass(cls):
        cls.url = url = "http://localhost:9090"
        cls.pl  = pl  = Plastic(url, api_version="1")
        cls.test_table = {

            # Repositories

            "get_repositories": [
                {
                    "args": (),
                    "rtype": Tuple,#[pl.model.Repository],
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
            ],

            "create_repository": [
                {
                    "args": ("repName",),
                    "rtype": pl.model.Repository,
                    "expected": {
                        "status_code": 200, # OK
                        "content": {
                            "repId": {
                                "id": 2,
                                "moduleId": 0
                            },
                            "name": "repName",
                            "guid": "c45b8af3-1a10-d31f-baca-c00590d12456",
                            "owner": {
                                "name": "all",
                                "isGroup": False
                            },
                            "server": "myserver:8084"
                        }
                    }
                },
                {
                    "args": ("repName",),
                    "kwargs": dict(server="otherserver:8084"),
                    "rtype": pl.model.Repository,
                    "expected": {
                        "status_code": 200, # OK
                        "content": {
                            "repId": {
                                "id": 2,
                                "moduleId": 0
                            },
                            "name": "repName",
                            "guid": "c45b8af3-1a10-d31f-baca-c00590d12456",
                            "owner": {
                                "name": "all",
                                "isGroup": False
                            },
                            "server": "otherserver:8084"
                        }
                    }
                },
            ],

            "get_repository": [
                {
                    "args": ("default",),
                    "rtype": pl.model.Repository,
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
            ],

            "rename_repository": [
                {
                    "args": ("oldName", "newName"),
                    "rtype": pl.model.Repository,
                    "expected": {
                        "status_code": 200, # OK
                        "content": {
                            "repId": {
                                "id": 2,
                                "moduleId": 0
                            },
                            "name": "newName",
                            "guid": "c45b8af3-1a10-d31f-baca-c00590d12456",
                            "owner": {
                                "name": "all",
                                "isGroup": False
                            },
                            "server": "myserver:8084"
                        }
                    }
                },
            ],

            "delete_repository": [
                {
                    "args": ("default",),
                    "rtype": None,
                    "expected": {
                        "status_code": 204, # No Content
                        "content": None
                    }
                },
            ],

            # Workspaces

            "get_workspaces": [
                {
                    "args": (),
                    "rtype": Tuple,#[pl.model.Workspace],
                    "expected": {
                        "status_code": 200, # OK
                        "content": [
                            {
                                "name": "my_wk",
                                "guid": "e93518f8-20a6-4534-a7c6-f3d9ebac45cb",
                                "path": "c:\\path\\to\\workspace",
                                "machineName": "MACHINE",
                            },
                        ]
                    }
                },
            ],

            "create_workspace": [
                {
                    "args": ("my_wk", Path("c:\\the\\path\\to\\new_wk")),
                    "rtype": pl.model.Workspace,
                    "expected": {
                        "status_code": 200, # OK
                        "content": {
                            "name": "my_wk",
                            "guid": "ed3248d2-5591-407a-94e6-84dac0ce015b",
                            "path": "c:\\the\\path\\to\\new_wk",
                            "machineName": "MACHINE"
                        }
                    }
                },
                {
                    "args": ("my_wk", Path("c:\\the\\path\\to\\new_wk")),
                    "kwargs": dict(repo_name="default"),
                    "rtype": pl.model.Workspace,
                    "expected": {
                        "status_code": 200, # OK
                        "content": {
                            "name": "my_wk",
                            "guid": "ed3248d2-5591-407a-94e6-84dac0ce015b",
                            "path": "c:\\the\\path\\to\\new_wk",
                            "machineName": "MACHINE"
                        }
                    }
                },
            ],

            "get_workspace": [
                {
                    "args": ("my_wk",),
                    "rtype": pl.model.Workspace,
                    "expected": {
                        "status_code": 200, # OK
                        "content": {
                            "name": "my_wk",
                            "guid": "e93518f8-20a6-4534-a7c6-f3d9ebac45cb",
                            "path": "c:\\path\\to\\workspace",
                            "machineName": "MACHINE",
                        }
                    }
                },
            ],

            "rename_workspace": [
                {
                    "args": ("oldName", "newName"),
                    "rtype": pl.model.Workspace,
                    "expected": {
                        "status_code": 200, # OK
                        "content": {
                            "name": "newName",
                            "guid": "ed3248d2-5591-407a-94e6-84dac0ce015b",
                            "path": "c:\\the\\path\\to\\new_wk",
                            "machineName": "MACHINE",
                        }
                    }
                },
            ],

            "delete_workspace": [
                {
                    "args": ("my_wk",),
                    "rtype": None,
                    "expected": {
                        "status_code": 204, # No Content
                        "content": None
                    }
                },
            ],

            # Branches

            "get_branches": [
                {
                    "args": ("mainrepo",),
                    "rtype": Tuple,#[pl.model.Branch],
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
                                    "name": "mainrepo",
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
                    "args": ("mainrepo",),
                    "kwargs": dict(query="id > 50"),
                    "rtype": Tuple,#[pl.model.Repository],
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
                                    "name": "mainrepo",
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
            ],

            "create_branch": [
                {
                    "args": ("default", "newBranch", pl.model.ObjectType.BRANCH, "/main/scm003"),
                    "rtype": pl.model.Branch,
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
                    "args": ("default", "newBranch", pl.model.ObjectType.LABEL, "BL000"),
                    "kwargs": dict(top_level=True),
                    "rtype": pl.model.Branch,
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
                    "args": ("default", "newBranch", pl.model.ObjectType.CHANGESET, 97),
                    "kwargs": dict(top_level=False),
                    "rtype": pl.model.Branch,
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
            ],

            "get_branch": [
                {
                    "args": ("mainrepo", "/main/task001/task002"),
                    "rtype": pl.model.Branch,
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
                                "name": "mainrepo",
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
            ],

            "rename_branch": [
                {
                    "args": ("mainrepo", "/main/task001/task002", "/main/task001/task003"),
                    "rtype": pl.model.Branch,
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
                                "name": "mainrepo",
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
            ],

            "delete_branch": [
                {
                    "args": ("mainrepo", "/main/task001/task002"),
                    "rtype": None,
                    "expected": {
                        "status_code": 204, # No Content
                        "content":  None
                    }
                },
            ],

            # Labels

            "get_labels": [
                {
                    "args": ("default",),
                    "rtype": Tuple,#[pl.model.Label],
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
                    "args": ("default",),
                    "kwargs": dict(query="date > '2015-07-01'"),
                    "rtype": Tuple,#[pl.model.Label],
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
            ],

            "create_label": [
                {
                    "args": ("default", "BL001", 99),
                    "kwargs": dict(comment="Stable baseline - 1"),
                    "rtype": pl.model.Label,
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
            ],

            "get_label": [
                {
                    "args": ("default", "BL000"),
                    "rtype": pl.model.Label,
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
            ],

            "rename_label": [
                {
                    "args": ("default", "BL000", "v1.0.0"),
                    "rtype": pl.model.Label,
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
            ],

            "delete_label": [
                {
                    "args": ("default", "BL000"),
                    "rtype": None,
                    "expected": {
                        "status_code": 200, # OK
                        "content": None
                    }
                },
            ],
        }

    @classmethod
    def tearDownClass(cls):
        cls.pl = None

    def test(self):
        repository_name  = "10031411_2021MY_ADCAM10_MID_ECU"
        workspace_name   = "10031411_2021MY_ADCAM10_MID_ECU"
        repository1_name = "repo_new"

        test_table = self.test_table.copy()
        # del test_table["get_repositories"]
        # del test_table["create_repository"]
        # del test_table["get_repository"]
        # del test_table["rename_repository"]
        # del test_table["delete_repository"]

        # del test_table["get_workspaces"]
        # del test_table["create_workspace"]
        # del test_table["get_workspace"]
        # del test_table["rename_workspace"]
        # del test_table["delete_workspace"]

        # del test_table["get_branches"]
        # del test_table["create_branch"]
        # del test_table["get_branch"]
        # del test_table["rename_branch"]
        # del test_table["delete_branch"]

        # del test_table["get_labels"]
        # del test_table["create_label"]
        # del test_table["get_label"]
        # del test_table["rename_label"]
        # del test_table["delete_label"]

        for func_name, tests in test_table.items():
            print(func_name)
            for test in tests:
                ret = self.do_test(func_name, self.request_mock, test)
                #print(ret)
                #r = requests.get('http://google.com/')
                #print(r.status_code)
                #print(r.content)  # 'Oh hai'
                #print(r.json())  # 'Oh hai'

    # Repositories

    @staticmethod
    @urlmatch(scheme="http", netloc="localhost:9090", path=r"^/api/v1/repos$", method="get")
    def mock_get_repositories(url, request, test=None):
        return TestPlastic.response(test)

    def test_get_repositories(self):
        func_name = "get_repositories"
        for test in self.test_table[func_name]:
            ret = self.do_test(func_name, self.mock_get_repositories, test)

    @staticmethod
    @urlmatch(scheme="http", netloc="localhost:9090", path=r"^/api/v1/repos$", method="post")
    def mock_create_repository(url, request, test=None):
        return TestPlastic.response(test)

    def test_create_repository(self):
        func_name = "create_repository"
        for test in self.test_table[func_name]:
            ret = self.do_test(func_name, self.mock_create_repository, test)

    @staticmethod
    @urlmatch(scheme="http", netloc="localhost:9090", path=r"^/api/v1/repos/\w+$", method="get")
    def mock_get_repository(url, request, test=None):
        return TestPlastic.response(test)

    def test_get_repository(self):
        func_name = "get_repository"
        for test in self.test_table[func_name]:
            ret = self.do_test(func_name, self.mock_get_repository, test)

    @staticmethod
    @urlmatch(scheme="http", netloc="localhost:9090", path=r"^/api/v1/repos/\w+$", method="put")
    def mock_rename_repository(url, request, test=None):
        return TestPlastic.response(test)

    def test_rename_repository(self):
        func_name = "rename_repository"
        for test in self.test_table[func_name]:
            ret = self.do_test(func_name, self.mock_rename_repository, test)

    @staticmethod
    @urlmatch(scheme="http", netloc="localhost:9090", path=r"^/api/v1/repos/\w+$", method="delete")
    def mock_delete_repository(url, request, test=None):
        return TestPlastic.response(test)

    def test_delete_repository(self):
        func_name = "delete_repository"
        for test in self.test_table[func_name]:
            ret = self.do_test(func_name, self.mock_delete_repository, test)

    # Workspaces

    @staticmethod
    @urlmatch(scheme="http", netloc="localhost:9090", path=r"^/api/v1/wkspaces$", method="get")
    def mock_get_workspaces(url, request, test=None):
        return TestPlastic.response(test)

    def test_get_workspaces(self):
        func_name = "get_workspaces"
        for test in self.test_table[func_name]:
            ret = self.do_test(func_name, self.mock_get_workspaces, test)

    @staticmethod
    @urlmatch(scheme="http", netloc="localhost:9090", path=r"^/api/v1/wkspaces$", method="post")
    def mock_create_workspace(url, request, test=None):
        return TestPlastic.response(test)

    def test_create_workspace(self):
        func_name = "create_workspace"
        for test in self.test_table[func_name]:
            ret = self.do_test(func_name, self.mock_create_workspace, test)

    @staticmethod
    @urlmatch(scheme="http", netloc="localhost:9090", path=r"^/api/v1/wkspaces/\w+$", method="get")
    def mock_get_workspace(url, request, test=None):
        return TestPlastic.response(test)

    def test_get_workspace(self):
        func_name = "get_workspace"
        for test in self.test_table[func_name]:
            ret = self.do_test(func_name, self.mock_get_workspace, test)

    @staticmethod
    @urlmatch(scheme="http", netloc="localhost:9090", path=r"^/api/v1/wkspaces/\w+$", method="patch")
    def mock_rename_workspace(url, request, test=None):
        return TestPlastic.response(test)

    def test_rename_workspace(self):
        func_name = "rename_workspace"
        for test in self.test_table[func_name]:
            ret = self.do_test(func_name, self.mock_rename_workspace, test)

    @staticmethod
    @urlmatch(scheme="http", netloc="localhost:9090", path=r"^/api/v1/wkspaces/\w+$", method="delete")
    def mock_delete_workspace(url, request, test=None):
        return TestPlastic.response(test)

    def test_delete_workspace(self):
        func_name = "delete_workspace"
        for test in self.test_table[func_name]:
            ret = self.do_test(func_name, self.mock_delete_workspace, test)

    # Branches

    @staticmethod
    @urlmatch(scheme="http", netloc="localhost:9090", path=r"^/api/v1/repos/\w+/branches$", method="get")
    def mock_get_branches(url, request, test=None):
        return TestPlastic.response(test)

    def test_get_branches(self):
        func_name = "get_branches"
        for test in self.test_table[func_name]:
            ret = self.do_test(func_name, self.mock_get_branches, test)

    @staticmethod
    @urlmatch(scheme="http", netloc="localhost:9090", path=r"^/api/v1/repos/\w+/branches$", method="post")
    def mock_create_branch(url, request, test=None):
        return TestPlastic.response(test)

    def test_create_branch(self):
        func_name = "create_branch"
        for test in self.test_table[func_name]:
            ret = self.do_test(func_name, self.mock_create_branch, test)

    @staticmethod
    @urlmatch(scheme="http", netloc="localhost:9090", path=r"^/api/v1/repos/\w+/branches(/\w+)+$", method="get")
    def mock_get_branch(url, request, test=None):
        return TestPlastic.response(test)

    def test_get_branch(self):
        func_name = "get_branch"
        for test in self.test_table[func_name]:
            ret = self.do_test(func_name, self.mock_get_branch, test)

    @staticmethod
    @urlmatch(scheme="http", netloc="localhost:9090", path=r"^/api/v1/repos/\w+/branches(/\w+)+$", method="patch")
    def mock_rename_branch(url, request, test=None):
        return TestPlastic.response(test)

    def test_rename_branch(self):
        func_name = "rename_branch"
        for test in self.test_table[func_name]:
            ret = self.do_test(func_name, self.mock_rename_branch, test)

    @staticmethod
    @urlmatch(scheme="http", netloc="localhost:9090", path=r"^/api/v1/repos/\w+/branches(/\w+)+$", method="delete")
    def mock_delete_branch(url, request, test=None):
        return TestPlastic.response(test)

    def test_delete_branch(self):
        func_name = "delete_branch"
        for test in self.test_table[func_name]:
            ret = self.do_test(func_name, self.mock_delete_branch, test)

    # Labels

    @staticmethod
    @urlmatch(scheme="http", netloc="localhost:9090", path=r"^/api/v1/repos/\w+/labels$", method="get")
    def mock_get_labels(url, request, test=None):
        return TestPlastic.response(test)

    def test_get_labels(self):
        func_name = "get_labels"
        for test in self.test_table[func_name]:
            ret = self.do_test(func_name, self.mock_get_labels, test)

    @staticmethod
    @urlmatch(scheme="http", netloc="localhost:9090", path=r"^/api/v1/repos/\w+/labels$", method="post")
    def mock_create_label(url, request, test=None):
        return TestPlastic.response(test)

    def test_create_label(self):
        func_name = "create_label"
        for test in self.test_table[func_name]:
            ret = self.do_test(func_name, self.mock_create_label, test)

    @staticmethod
    @urlmatch(scheme="http", netloc="localhost:9090", path=r"^/api/v1/repos/\w+/labels/\w+$", method="get")
    def mock_get_label(url, request, test=None):
        return TestPlastic.response(test)

    def test_get_label(self):
        func_name = "get_label"
        for test in self.test_table[func_name]:
            ret = self.do_test(func_name, self.mock_get_label, test)

    @staticmethod
    @urlmatch(scheme="http", netloc="localhost:9090", path=r"^/api/v1/repos/\w+/labels/\w+$", method="patch")
    def mock_rename_label(url, request, test=None):
        return TestPlastic.response(test)

    def test_rename_label(self):
        func_name = "rename_label"
        for test in self.test_table[func_name]:
            ret = self.do_test(func_name, self.mock_rename_label, test)

    @staticmethod
    @urlmatch(scheme="http", netloc="localhost:9090", path=r"^/api/v1/repos/\w+/labels/\w+$", method="delete")
    def mock_delete_label(url, request, test=None):
        return TestPlastic.response(test)

    def test_delete_label(self):
        func_name = "delete_label"
        for test in self.test_table[func_name]:
            ret = self.do_test(func_name, self.mock_delete_label, test)
