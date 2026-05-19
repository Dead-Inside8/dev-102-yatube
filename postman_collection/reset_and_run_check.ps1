Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

Write-Output "==> Resetting database and seed data..."
powershell -ExecutionPolicy Bypass -File ".\set_up_data.ps1"

Write-Output "==> Running readiness checks..."
$checkCommand = @'
from django.contrib.auth import get_user_model
from posts.models import Group, Follow

User = get_user_model()
required_users = {"root", "regular_user", "second_user"}
existing_users = set(User.objects.values_list("username", flat=True))
missing_users = sorted(required_users - existing_users)

group_exists = Group.objects.filter(slug="test-group").exists()
follows_count = Follow.objects.count()

print("users_ok", not missing_users)
print("missing_users", missing_users)
print("group_ok", group_exists)
print("follows_count", follows_count)
'@
$checkCommand | python "..\yatube_api\manage.py" shell

Write-Output ""
Write-Output "Ready for Postman run."
Write-Output "Tip: run the full collection from the top."
