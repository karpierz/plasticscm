
    {
        # Repositories

        "get_repositories": [ # -> Tuple[Repository]:
            {
                "args": {},
                "expected": {
                    "status": 200, # OK
                    "response": [
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

        "create_repository": [ # -> Repository
            {
                "args": {},
                "expected": {
                    "status": 200, # OK
                    "response": {
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
        ],

        "get_repository": [ # -> Repository
            {
                "args": {"repo_name": "default"},
                "expected": {
                    "status": 200, # OK
                    "response": {
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

        "rename_repository": [ # -> Repository
            {
                "args": {"repo_name": "oldName",
                         "repo_new_name": "newName"},
                "expected": {
                    "status": 200, # OK
                    "response": {
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

        "delete_repository": [ # -> None
            {
                "args": {"repo_name": ""default""},
                "expected": {
                    "status": 204, # No Content
                    "response": None
                }
            },
        ],

        # Workspaces

        "get_workspaces": [ # -> Tuple[Workspace]
            {
                "args": {},
                "expected": {
                    "status": 200, # OK
                    "response": [
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

        "create_workspace": [ # -> Workspace
            {
                "args": {},
                "expected": {
                    "status": 200, # OK
                    "response": {
                        "name": wkspace_name,
                        "guid": "ed3248d2-5591-407a-94e6-84dac0ce015b",
                        "path": "c:\\the\\path\\to\\new_wk",
                        "machineName": "MACHINE"
                    }
                }
            },
        ],

        "get_workspace": [ # -> Workspace
            {
                "args": {"wkspace_name": "my_wk"},
                "expected": {
                    "status": 200, # OK
                    "response": {
                        "name": "my_wk",
                        "guid": "e93518f8-20a6-4534-a7c6-f3d9ebac45cb",
                        "path": "c:\\path\\to\\workspace",
                        "machineName": "MACHINE",
                    }
                }
            },
        ],

        "rename_workspace": [ # -> Workspace
            {
                "args": {"wkspace_name": str,
                         "wkspace_new_name": str},
                "expected": {
                    "status": 200, # OK
                    "response": {
                        "name": "newName",
                        "guid": "ed3248d2-5591-407a-94e6-84dac0ce015b",
                        "path": "c:\\the\\path\\to\\new_wk",
                        "machineName": "MACHINE",
                    }
                }
            },
        ],

        "delete_worskpace": [ # -> None
            {
                "args": {"wkspace_name": "my_wk"},
                "expected": {
                    "status": 204, # No Content
                    "response": None
                }
            },
        ],


        # Branches

        "get_branches": [ # -> Tuple[Branch]
            {
                "args": {},
                "expected": {
                    "status": 200, # OK
                    "response": [
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

        "create_branch": [ # -> Branch
            {
                #{
                #    "name": "newBranch",
                #    "originType": "branch",
                #    "origin": "/main/scm003",
                #    "topLevel": False,
                #}
                "args": {},
                "expected": {
                    "status": 200, # OK
                    "response": {
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
                #{
                #    "name": "newBranch",
                #    "originType": "label",
                #    "origin": "BL000",
                #    "topLevel": True,
                #}
                "args": {},
                "expected": {
                    "status": 200, # OK
                    "response": {
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
                #{
                #    "name": "newBranch",
                #    "originType": "changeset",
                #    "origin": "97",
                #    "topLevel": False,
                #}
                "args": {},
                "expected": {
                    "status": 200, # OK
                    "response": {
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
        ],

        "get_branch": [ # -> Branch
            {
                "args": {"repo_name": "mainrepo",
                         "branch_name": "/main/task001/task002"},
                "expected": {
                    "status": 200, # OK
                    "response": {
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

        "rename_branch": [ # -> Branch
            {
                "args": {"repo_name": str,
                         "branch_name": str,
                         "branch_new_name": str},
                "expected": {
                    "status": 200, # OK
                    "response": {
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

        "delete_branch": [ # -> None
            {
                "args": {"repo_name": str,
                         "branch_name": str},
                "expected": {
                    "status": 204, # No Content
                    "response":  None
                }
            },
        ],

        "": [ #
            {
                "args": {},
                "expected": {
                    "status": 200, # OK
                    "response": 
                }
            },
        ],

        "": [ #
            {
                "args": {},
                "expected": {
                    "status": 200, # OK
                    "response": 
                }
            },
        ],

        "": [ #
            {
                "args": {},
                "expected": {
                    "status": 200, # OK
                    "response": 
                }
            },
        ],
    }


    def create_repository(repo_name: str, *, server: Optional[str]=None):
    def create_workspace(wkspace_name: str, wkspace_path: str, repo_name: Optional[str]=None):

    # Branches

    def get_branches(repo_name: str, query: Optional[str]=None):
    def create_branch(repo_name: str, branch_name: str,
                      origin_type: ObjectType, origin: Union[str, int],
                      top_level: bool=False):

    # Labels

    def get_labels(repo_name: str, query: Optional[str]=None) -> Tuple[Label]:
        """
        Status: 200 OK

        response = [
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
        """

    def create_label(repo_name: str, label_name: str, changeset_id: int,
                     comment: Optional[str]=None, apply_to_xlinks: bool=False) -> Label:
        """
        Examples:

        {
            "name":          label_name,      # required # "BL001"
            "changeset":     changeset_id,    # required # 99
            "comment":       comment,         # optional # "Stable baseline - 1"
            "applyToXlinks": apply_to_xlinks, # optional # False
        }

        Status: 200 OK

        response = {
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
        """

    def get_label(repo_name: str, label_name: str) -> Label:
        """
        Status: 200 OK

        response = {
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
            }
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
        """

    def rename_label(repo_name: str, label_name: str, label_new_name: str) -> Label:
        """
        Status: 200 OK

        response = {
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
        """

    def delete_label(repo_name: str, label_name: str):
        """ """
        url, action = delete_label.rest
        url = url.format(repo_name=repo_name, label_name=label_name)
        response = action(url)

    # Changesets

    def get_changesets(repo_name: str, query: Optional[str]=None) -> Tuple[Changeset]:
        """
        Status: 200 OK

        response = [
            {
                "id": 0,
                "parentId": -1,
                "comment": "Root dir",
                "creationDate": "2015-04-09T07:17:00",
                "guid": "0497ef04-4c81-4090-8458-649885400c84",
                "branch": {
                    "name": "\/main",
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
        """

    def get_changesets_in_branch(repo_name: str, branch_name: str,
                                 query: Optional[str]=None) -> Tuple[Changeset]:
        """
        Status: 200 OK

        response = [
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
        """

    def get_changeset(repo_name: str, changeset_id: int) -> Changeset:
        """
        Status: 200 OK

        response = {
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
        """

    # Changes

    def get_pending_changes(wkspace_name: str,
        change_types: List[Change.Type]=[Change.Type.ALL]) -> Tuple[Change]:
        """
        Status: 200 OK

        response = [
            {
                "changes": [
                    "CH",
                    "MV"
                ],
                "path": "c:\\Users\\scm-user\\wkspaces\\main-wk\\audio-prj\\orchestrated.fspro",
                "oldPath": "c:\\Users\\scm-user\\wkspaces\\main-wk\\audio-prj\\audio-prj.fspro",
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
        """

    def undo_pending_changes(wkspace_name: str, paths: List[Path]) -> AffectedPaths:
        """
        Examples:

        {
            "paths": [
                "c:\\Users\\scm-user\\wkspaces\\main-wk\\audio-prj\\orchestrated.fspro",
            ]
        }

        {
            "paths": [
                "audio-prj/orchestrated.fspro",
            ]
        }

        Status: 200 OK

        response = {
            "affectedPaths": [
                "c:\\Users\\scm-user\\wkspaces\\main-wk\\audio-prj\\orchestrated.fspro",
            ]
        }
        """

    # Workspace Update and Switch

    def get_workspace_update_status(wkspace_name: str) -> OperationStatus:
        """
        Status: 200 OK

        response = {
            "status": "Not running",
        }

        Status: 200 OK

        response = {
            "status": "Failed",
            "message": "No route to host 'localhost:8084'",
        }

        Status: 200 OK

        response = {
            "status": "Calculating",
            "totalFiles": 1356,
            "totalBytes": 3246739,
            "updatedFiles": 0,
            "updatedBytes": 0,
        }

        Status: 200 OK

        response = {
            "status": "Running",
            "totalFiles": 1356,
            "totalBytes": 3246739,
            "updatedFiles": 356,
            "updatedBytes": 894433,
        }

        Status: 200 OK

        response = {
            "status": "Finished",
            "totalFiles": 1356,
            "totalBytes": 3246739,
            "updatedFiles": 1356,
            "updatedBytes": 3246739,
        }
        """

    def update_workspace(wkspace_name: str) -> OperationStatus:
        """
        Status: 200 OK

        response = {
            "status": "Running",
            "totalFiles": 0,
            "totalBytes": 0,
            "updatedFiles": 0,
            "updatedBytes": 0,
        }
        """

    def get_workspace_switch_status(wkspace_name: str) -> OperationStatus:
        """
        Status: 200 OK

        response = {
            "status": "Not running",
        }

        Status: 200 OK

        response = {
            "status": "Failed",
            "message": "No route to host 'localhost:8084'",
        }

        Status: 200 OK

        response = {
            "status": "Calculating",
            "totalFiles": 1356,
            "totalBytes": 3246739,
            "updatedFiles": 0,
            "updatedBytes": 0,
        }

        Status: 200 OK

        response = {
            "status": "Running",
            "totalFiles": 1356,
            "totalBytes": 3246739,
            "updatedFiles": 356,
            "updatedBytes": 894433,
        }

        Status: 200 OK

        response = {
            "status": "Finished",
            "totalFiles": 1356,
            "totalBytes": 3246739,
            "updatedFiles": 1356,
            "updatedBytes": 3246739,
        }
        """

    def switch_workspace(wkspace_name: str,
                         object_type: ObjectType,
                         object: Union[str, int]) -> OperationStatus:
        """
        Examples:

        {
            "objectType": object_type, # required # "branch"
            "object":     object,      # required # "/main/task001"
        }

        {
            "objectType": object_type, # required # "changeset"
            "object":     object,      # required # "1136"
        }

        {
            "objectType": object_type, # required # "label"
            "object":     object,      # required # "BL001"
        }

        Status: 200 OK

        response = {
            "status": "Running",
            "totalFiles": 0,
            "totalBytes": 0,
            "updatedFiles": 0,
            "updatedBytes": 0,
        }
        """

    # Checkin

    def get_workspace_checkin_status(wkspace_name: str) -> CheckinStatus:
        """
        Status: 200 OK

        response = {
            "status": "Not running",
        }

        Status: 200 OK

        response = {
            "status": "Failed",
            "message": "No route to host 'localhost:8084'",
        }

        Status: 200 OK

        response = {
            "status": "Checkin finished",
            "totalSize": 57990,
            "transferredSize": 57990,
        }
        """

    def checkin_workspace(wkspace_name: str,
                          paths: Optional[List[str]]=None,
                          comment: Optional[str]=None,
                          recurse: bool=False) -> CheckinStatus:
        """
        Examples:

        {
        }

        {
            "comment": "Upgrade core engine", # optional
        }

        {
            "paths": [ # optional
                "src/foo.c",
                "src/bar/baz.c",
                "doc",
            ],
            "comment": "Upgrade core engine", # optional
            "recurse": True,                  # optional
        }

        Status: 200 OK

        response = {
            "status": "Checkin operation starting...",
            "totalSize": 0,
            "transferredSize": 0,
        }
        """

    # Repository contents

    def getItemInRepository(repo_name: str, item_path: str) -> Item:
        """
        """

    def get_item_in_branch(repo_name: str, branch_name: str, item_path: str) -> Item:
        """
        Examples:

        GET /api/v1/repos/myrepo/branches/main/scm003/contents/src/lib/foo.c

        Status: 200 OK

        response = {
            "revisionId": 771,
            "type": "file",
            "size": 57913,
            "name": "soundproject.fspro",
            "path": "/fmod/soundproject.fspro",
            "isUnderXlink": False,
            "hash": "/2ygGGfoXDq9bbKZJCzj9g==",
            "content": "http://localhost:9090/api/v1/repos/myrepo/revisions/771/blob",
            "repository": {
                "repId":
                {
                    "id": 1,
                    "moduleId": 0
                },
                "name": "myrepo",
                "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                "owner":
                {
                    "name": "all",
                    "isGroup": False
                },
                "server": "localhost:8084"
            }
        }

        Status: 200 OK

        response = {
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
                "name": "myrepo",
                "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                "owner":
                {
                    "name": "all",
                    "isGroup": False
                },
                "server": "localhost:8084"
            }
        }

        Status: 200 OK

        response = {
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
                    "content": "http://localhost:9090/api/v1/repos/myrepo/revisions/46348/blob"
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
                "name": "myrepo",
                "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                "owner":
                {
                    "name": "all",
                    "isGroup": False
                },
                "server": "localhost:8084"
            }
        }
        """

    def get_item_in_changeset(repo_name: str, changeset_id: int, item_path: str) -> Item:
        """
        Examples:

        GET /api/v1/repos/myrepo/changesets/5378/contents/src/lib/foo.c

        Status: 200 OK

        response = {
            "revisionId": 771,
            "type": "file",
            "size": 57913,
            "name": "soundproject.fspro",
            "path": "/fmod/soundproject.fspro",
            "isUnderXlink": False,
            "hash": "/2ygGGfoXDq9bbKZJCzj9g==",
            "content": "http://localhost:9090/api/v1/repos/myrepo/revisions/771/blob",
            "repository": {
                "repId":
                {
                    "id": 1,
                    "moduleId": 0
                },
                "name": "myrepo",
                "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                "owner":
                {
                    "name": "all",
                    "isGroup": False
                },
                "server": "localhost:8084"
            }
        }

        Status: 200 OK

        response = {
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
                "name": "myrepo",
                "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                "owner":
                {
                    "name": "all",
                    "isGroup": False
                },
                "server": "localhost:8084"
            }
        }

        Status: 200 OK

        response = {
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
                    "content": "http://localhost:9090/api/v1/repos/myrepo/revisions/46348/blob"
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
                "name": "myrepo",
                "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                "owner":
                {
                    "name": "all",
                    "isGroup": False
                },
                "server": "localhost:8084"
            }
        }
        """

    def get_item_in_label(repo_name: str, label_name: str, item_path: str) -> Item:
        """
        Examples:

        GET /api/v1/repos/myrepo/labels/BL001/contents/src/lib/foo.c

        Status: 200 OK

        response = {
            "revisionId": 771,
            "type": "file",
            "size": 57913,
            "name": "soundproject.fspro",
            "path": "/fmod/soundproject.fspro",
            "isUnderXlink": False,
            "hash": "/2ygGGfoXDq9bbKZJCzj9g==",
            "content": "http://localhost:9090/api/v1/repos/myrepo/revisions/771/blob",
            "repository": {
                "repId":
                {
                    "id": 1,
                    "moduleId": 0
                },
                "name": "myrepo",
                "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                "owner":
                {
                    "name": "all",
                    "isGroup": False
                },
                "server": "localhost:8084"
            }
        }

        Status: 200 OK

        response = {
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
                "name": "myrepo",
                "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                "owner":
                {
                    "name": "all",
                    "isGroup": False
                },
                "server": "localhost:8084"
            }
        }

        Status: 200 OK

        response = {
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
                    "content": "http://localhost:9090/api/v1/repos/myrepo/revisions/46348/blob"
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
                "name": "myrepo",
                "guid": "c43e1cf9-50b0-4e0d-aca5-c1814d016425",
                "owner":
                {
                    "name": "all",
                    "isGroup": False
                },
                "server": "localhost:8084"
            }
        }
        """

    def get_item_revision_history_in_branch(repo_name: str, branch_name: str, item_path: str) -> Item:
        """
        Examples:

        GET /api/v1/repos/myrepo/branches/main/scm003/history/src/lib/foo.c

        Status: 200 OK

        response = [
            {
                "revisionId": 104,
                "type": "text",
                "owner": {
                    "name": "tester",
                    "isGroup": False
                },
                "creationDate": "2015-04-09T09:51:20",
                "comment": "Restore method implementation",
                "revisionLink": "http://localhost:9090/api/v1/repos/myrepo/revisions/104",
                "changesetId": 3,
                "changesetLink": "http://localhost:9090/api/v1/repos/myrepo/changesets/3",
                "branchName": "/main",
                "branchLink": "http://localhost:9090/api/v1/repos/myrepo/branches/main",
                "repositoryName": "myrepo",
                "repositoryLink": "http://localhost:9090/api/v1/repos/myrepo"
            },
        ]
        """

    def get_item_revision_history_in_changeset(repo_name: str, changeset_id: int, item_path: str) -> Item:
        """
        Examples:

        GET /api/v1/repos/myrepo/changesets/5378/history/src/lib/foo.c

        Status: 200 OK

        response = [
            {
                "revisionId": 104,
                "type": "text",
                "owner": {
                    "name": "tester",
                    "isGroup": False
                },
                "creationDate": "2015-04-09T09:51:20",
                "comment": "Restore method implementation",
                "revisionLink": "http://localhost:9090/api/v1/repos/myrepo/revisions/104",
                "changesetId": 3,
                "changesetLink": "http://localhost:9090/api/v1/repos/myrepo/changesets/3",
                "branchName": "/main",
                "branchLink": "http://localhost:9090/api/v1/repos/myrepo/branches/main",
                "repositoryName": "myrepo",
                "repositoryLink": "http://localhost:9090/api/v1/repos/myrepo"
            },
        ]
        """

    def get_item_revision_history_in_label(repo_name: str, label_name: str, item_path: str) -> Item:
        """
        Examples:

        GET /api/v1/repos/myrepo/labels/BL001/history/src/lib/foo.c

        Status: 200 OK

        response = [
            {
                "revisionId": 104,
                "type": "text",
                "owner": {
                    "name": "tester",
                    "isGroup": False
                },
                "creationDate": "2015-04-09T09:51:20",
                "comment": "Restore method implementation",
                "revisionLink": "http://localhost:9090/api/v1/repos/myrepo/revisions/104",
                "changesetId": 3,
                "changesetLink": "http://localhost:9090/api/v1/repos/myrepo/changesets/3",
                "branchName": "/main",
                "branchLink": "http://localhost:9090/api/v1/repos/myrepo/branches/main",
                "repositoryName": "myrepo",
                "repositoryLink": "http://localhost:9090/api/v1/repos/myrepo"
            },
        ]
        """

    # Diff

    def diff_changesets(self, repo_name: str, changeset_id: int, source_changeset_id: int) -> Tuple[Diff]:
        return tuple(self.__json2Diff(diff) for diff in response.json())

    def diff_changeset(self, repo_name: str, changeset_id: int) -> Tuple[Diff]:
        return tuple(self.__json2Diff(diff) for diff in response.json())

    def diff_branch(self, repo_name: str, branch_name: str) -> Tuple[Diff]:
        return tuple(self.__json2Diff(diff) for diff in response.json())

        """
        Status: 200 OK

        response = [
            {
                "status": "Changed",
                "path": "/lib/xlink",
                "isDirectory": true,
                "isUnderXlink": false,
                "xlink": {
                    "changesetGuid": "ff92e897-b662-40f1-9a1f-a17349cbc7c6",
                    "repository": "big",
                    "server": "localhost:8084"
                },
                "baseXlink": {
                    "changesetGuid": "c75c04ec-3546-46e4-bbb7-031b523dca7d",
                    "repository": "big",
                    "server": "localhost:8084"
                },
                "isItemFSProtectionChanged": false,
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
                "isDirectory": false,
                "size": 1616,
                "hash": "u0gJQzQnjLNUUHRI1+QQLg==",
                "isUnderXlink": true,
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
                                "name": "\/main\/scm002",
                                "id": 150865,
                                "parentId": 3,
                                "lastChangeset": 3,
                                "comment": "",
                                "creationDate": "2015-07-16T10:01:30",
                                "guid": "764c4842-aab8-451a-b802-29162d2a399f",
                                "owner": {
                                    "name": "tester",
                                    "isGroup": false
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
                                        "isGroup": false
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
                                    "isGroup": false
                                },
                                "server": "localhost:8084"
                            }
                        }
                    }
                ],
                "isItemFSProtectionChanged": false,
                "itemFileSystemProtection": "NOT_DEFINED",
                "modifiedTime": "2015-07-16T10:04:21",
                "createdBy": {
                    "name": "tester",
                    "isGroup": false
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
        """

    # Workspace actions

    def add_workspace_item(wkspace_name: str,
                           item_path: str,
                           add_parents: bool=True,
                           checkout_parent: bool=True,
                           recurse: bool=True) -> AffectedPaths:
        """
        Status: 200 OK

        response = {
            "affectedPaths": [
                "c:\\wkspaces\\mywk\\src\\lib\\descriptor.h",
                "c:\\wkspaces\\mywk\\src\\lib\\code.c",
            ]
        }
        """

    def checkout_workspace_item(wkspace_name: str, item_path: str) -> AffectedPaths:
        """
        Status: 200 OK

        response = {
            "affectedPaths": [
                "c:\\wkspaces\\mywk\\src\\lib\\code.c",
            ]
        }
        """

    def move_workspace_item(wkspace_name: str, item_path: str, dest_item_path: str) -> AffectedPaths:
        request = {
            "destination": dest_item_path,  # required # e.g. "src/bar.c"
        }
        """
        Status: 200 OK

        response = {
            "affectedPaths": [
                "c:\\wkspaces\\mywk\\src\\bar.c",
            ]
        }
        """
