from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from clients.models import Client


class Command(BaseCommand):
    help = 'Create a tenant (Client) and optionally a superuser for that tenant'

    def add_arguments(self, parser):
        parser.add_argument('--name', required=True, help='Client name')
        parser.add_argument('--subdomain', required=True, help='Client subdomain (slug)')
        parser.add_argument('--create-superuser', action='store_true', help='Also create a superuser')
        parser.add_argument('--username', help='Superuser username')
        parser.add_argument('--email', help='Superuser email')
        parser.add_argument('--password', help='Superuser password (not secure in CLI)')

    def handle(self, *args, **options):
        name = options['name']
        subdomain = options['subdomain']
        client, created = Client.objects.get_or_create(subdomain=subdomain, defaults={'name': name})
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created client: {client}'))
        else:
            client.name = name
            client.save()
            self.stdout.write(self.style.WARNING(f'Client existed — updated name: {client}'))

        if options['create_superuser']:
            username = options.get('username') or 'admin'
            email = options.get('email') or ''
            password = options.get('password') or None
            User = get_user_model()
            if not User.objects.filter(username=username).exists():
                if password:
                    User.objects.create_superuser(username=username, email=email, password=password)
                    self.stdout.write(self.style.SUCCESS(f'Created superuser `{username}`'))
                else:
                    # fallback: create user without password and prompt to set
                    user = User.objects.create_superuser(username=username, email=email)
                    self.stdout.write(self.style.SUCCESS(f'Created superuser `{username}` (no password set)'))
            else:
                self.stdout.write(self.style.WARNING('Superuser already exists — no action taken'))

        self.stdout.write('Next: add a hosts entry and open the admin at http://<subdomain>.localhost:8000/admin/')
