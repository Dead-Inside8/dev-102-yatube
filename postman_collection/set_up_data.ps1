Set-Location "..\yatube_api"

python manage.py migrate
python manage.py flush --no-input

$setupCommand = @"
from django.contrib.auth import get_user_model
from posts.models import Group

User = get_user_model()

u, _ = User.objects.get_or_create(username='root')
u.is_superuser = True
u.is_staff = True
u.email = 'root@admin.ru'
u.set_password('5eCretPaSsw0rD')
u.save()

u, _ = User.objects.get_or_create(username='regular_user')
u.is_superuser = False
u.is_staff = False
u.email = 'user@not-admin.ru'
u.set_password('iWannaBeAdmin')
u.save()

u, _ = User.objects.get_or_create(username='second_user')
u.is_superuser = False
u.is_staff = False
u.email = 'second@not-admin.ru'
u.set_password('5eCretPaSsw0rD')
u.save()

Group.objects.get_or_create(
    title='TestGroup',
    slug='test-group',
    description='Some text.',
)
"@

$setupCommand | python manage.py shell *> $null
Write-Output "Setup done."
