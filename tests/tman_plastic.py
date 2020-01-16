from pathlib import Path
from pprint import pprint
from plasticscm import Plastic

workspaces_path  = Path(r"C:\Users\gjtrd0\wkspaces")
repository_name  = "00000000_test"
workspace_name   = "00000000_test"
label_name       = "test1"
changeset_id     = 2188

pl = Plastic(timeout=150)

#changesets = pl.get_changesets(repository_name) #, query="id > 0")#"comment = 'rot gemacht'")#"id = 2193")
changesets = pl.get_changesets(repository_name, query="id = 2193")
print("Changesets:", [(chgset.id, chgset.parent_id, chgset.branch.name) for chgset in changesets])
input(">")

labels = pl.get_labels(repository_name, query="changeset between 0 and 2024") # 1024"
print("Labels:", len(labels), [(label.id, label.name, label.changeset_id, label.branch.name) for label in labels])
input(">")

# Utils

cm_location = pl.get_cm_location()
print("Command line executable (cm):", cm_location)
input(">")

# Repositories

repos = pl.get_repositories()
print("Repositories:", [repo.full_name for repo in repos])
input(">")
repo = pl.get_repository(repository_name)
print("Repository:", repo.name, repo.server)
input(">")

# Workspaces

wkspaces = pl.get_workspaces()
print("Workspaces:", [(wkspace.name, wkspace.path, wkspace.machine_name) for wkspace in wkspaces])
input(">")
wkspace = pl.get_workspace(workspace_name)
print("Workspace:", wkspace.name, wkspace.path, wkspace.machine_name)
input(">")
wkspace = pl.create_workspace("AK_new_workspace", workspaces_path/"AK_new_workspace")
print("New workspace:", wkspace.name, wkspace.path, wkspace.machine_name)
input(">")
print("Workspaces:", [(wkspace.name, wkspace.path, wkspace.machine_name) for wkspace in pl.get_workspaces()])
input(">")
wkspace = pl.rename_workspace("AK_new_workspace", "AK_BLABLA")
print("Renamed workspace:", wkspace.name, wkspace.path, wkspace.machine_name)
input(">")
print("Workspaces:", [(wkspace.name, wkspace.path, wkspace.machine_name) for wkspace in pl.get_workspaces()])
input(">")
wkspace = pl.rename_workspace("AK_BLABLA", "AK_new_workspace")
print("Renamed back workspace:", wkspace.name, wkspace.path, wkspace.machine_name)
input(">")
print("Workspaces:", [(wkspace.name, wkspace.path, wkspace.machine_name) for wkspace in pl.get_workspaces()])
input(">")
pl.delete_workspace("AK_new_workspace")
print("Deleted workspace:", wkspace.name, wkspace.path, wkspace.machine_name)
input(">")
print("Workspaces:", [(wkspace.name, wkspace.path, wkspace.machine_name) for wkspace in pl.get_workspaces()])
input(">")

# Branches

branches = pl.get_branches(repository_name)
print("Branches:", [(branch.name, branch.parent_id) for branch in branches])
input(">")
branch = pl.get_branch(repository_name, "/main")
print("Branch:", branch.name, branch.parent_id)
input(">")
branch = pl.create_branch(repository_name, "AK_new_branch", pl.model.ObjectType.BRANCH, "/main")
print("New branch:", branch.name, branch.parent_id)
input(">")
print("Branches:", [(branch.name, branch.parent_id) for branch in pl.get_branches(repository_name)])
input(">")
branch = pl.rename_branch(repository_name, "/main/AK_new_branch", "/main/AK_BLEBLE")
print("Renamed branch:", branch.name, branch.parent_id)
input(">")
print("Branches:", [(branch.name, branch.parent_id) for branch in pl.get_branches(repository_name)])
input(">")
branch = pl.rename_branch(repository_name, "/main/AK_BLEBLE", "/main/AK_new_branch")
print("Renamed back branch:", branch.name, branch.parent_id)
input(">")
print("Branches:", [(branch.name, branch.parent_id) for branch in pl.get_branches(repository_name)])
input(">")
pl.delete_branch(repository_name, "/main/AK_new_branch")
print("Deleted branch:", branch.name, branch.parent_id)
input(">")
print("Branches:", [(branch.name, branch.parent_id) for branch in pl.get_branches(repository_name)])
input(">")

# Labels

#labels = pl.get_labels(repository_name)
#print("Labels:", [(label.name, label.changeset_id, label.branch.name) for label in labels])
#input(">")
label = pl.get_label(repository_name, label_name)
print("Label:", label.name, label.changeset_id, label.branch.name)
input(">")
label = pl.create_label(repository_name, "AK_new_label", changeset_id)
print("New label:", label.name, label.changeset_id, label.branch.name)
input(">")
#print("Labels:", [(label.name, label.changeset_id, label.branch.name) for label in pl.get_labels(repository_name)])
#input(">")
label = pl.rename_label(repository_name, "AK_new_label", "AK_BLUBLU")
print("Renamed label:", label.name, label.changeset_id, label.branch.name)
input(">")
#print("Labels:", [(label.name, label.changeset_id, label.branch.name) for label in pl.get_labels(repository_name)])
#input(">")
label = pl.rename_label(repository_name, "AK_BLUBLU", "AK_new_label")
print("Renamed back label:", label.name, label.changeset_id, label.branch.name)
input(">")
#print("Labels:", [(label.name, label.changeset_id, label.branch.name) for label in pl.get_labels(repository_name)])
#input(">")
pl.delete_label(repository_name, "AK_new_label")
print("Deleted label:", label.name, label.changeset_id, label.branch.name)
input(">")
#print("Labels:", [(label.name, label.changeset_id, label.branch.name) for label in pl.get_labels(repository_name)])
#input(">")

# Changesets

#changesets = pl.get_changesets(repository_name)
#print("Changesets:", [(chgset.id, chgset.parent_id, chgset.branch.name) for chgset in changesets])
#input(">")
changesets = pl.get_changesets_in_branch(repository_name, "/main")
print("Changesets in branch:", "/main", [(chgset.id, chgset.parent_id, chgset.branch.name) for chgset in changesets])
input(">")
changeset = pl.get_changeset(repository_name, changeset_id)
print("Changeset:", changeset.id, changeset.parent_id, changeset.branch.name)
input(">")


changes = pl.get_pending_changes(workspace_name)
pprint([change.changes for change in changes])

status = pl.get_workspace_update_status(workspace_name)
pprint((status.status, status.message))
#status = pl.update_workspace(workspace_name)
#pprint((status.status, status.message))
status = pl.get_workspace_update_status(workspace_name)
pprint((status.status, status.message))

status = pl.get_workspace_checkin_status(workspace_name)
pprint((status.status, status.message))
status = pl.get_workspace_switch_status(workspace_name)
pprint((status.status, status.message))
status = pl.get_workspace_update_status(workspace_name)
pprint((status.status, status.message))

apaths = pl.undo_pending_changes(workspace_name, [
                                 workspaces_path/workspace_name/"README.md",
                                 ])
pprint(apaths.paths)
