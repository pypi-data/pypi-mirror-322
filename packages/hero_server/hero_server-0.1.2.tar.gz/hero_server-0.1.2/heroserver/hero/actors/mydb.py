from osis.db import DB
import shutil
import os

reset=False

def rm_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)

if reset:
    rm_dir("/tmp/index")
    rm_dir("/tmp/indexbackup")

db = DB(secret="mysecretkey", index_path="/tmp/index",index_backup_path="/tmp/indexbackup")

db.index_create("user", oid=str, pubkey=str, name=str, ipaddr=str, email=str, mobile=str, time_creation=int)
db.index_create("circle", oid=str, name=str, time_creation=int)

#communication
db.index_create("message", oid=str, subject=str, parent=str, to=str, to_group=str, time=int, msg_type=str, content_type=str, tags=str)

#tfgrid
db.index_create("referral", oid=str, pubkey_existing_user=str, pubkey_new_user=str, time_invited=int, time_installed=int)

#project mgmt
db.index_create("milestone", oid=str, title=str, owners=str, notifications=str, deadline=int, time_creation=int)
db.index_create("project", oid=str, title=str, project_type=str, owners=str, notifications=str, deadline=int, time_creation=int)
db.index_create("swimlane_template", oid=str, name=str, time_creation=int)
db.index_create("story", oid=str, title=str, assignees=str, project=str, swimlane=str, milestone=str, notifications=str, deadline=int, time_creation=int)
db.index_create("requirement", oid=str, requirement_type=str, title=str, content=str, story=str)
db.index_create("issue", oid=str, issue_type=str, title=str, assignees=str, notifications=str, deadline=int, time_creation=int)

def get():
   return db

