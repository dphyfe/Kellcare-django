from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = "Force refresh API token for a user (deletes old token and creates new one)"

    def add_arguments(self, parser):
        parser.add_argument("--username", type=str, help="Username to refresh token for", default="admin")

    def handle(self, *args, **options):
        username = options["username"]

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User "{username}" does not exist.'))
            return

        # Delete existing token
        deleted_count, _ = Token.objects.filter(user=user).delete()
        if deleted_count > 0:
            self.stdout.write(self.style.WARNING(f"Deleted {deleted_count} existing token(s) for {username}"))

        # Create new token
        token = Token.objects.create(user=user)

        self.stdout.write(self.style.SUCCESS(f"Created NEW API token for {username}"))
        self.stdout.write(self.style.WARNING(f"NEW API Token: {token.key}"))
        self.stdout.write("")
        self.stdout.write("Usage examples:")
        self.stdout.write(f'  curl -H "Authorization: Token {token.key}" http://127.0.0.1:8000/api/doctors/')
        self.stdout.write(f'  curl -H "Authorization: Token {token.key}" http://127.0.0.1:8000/api/appointments/')
        self.stdout.write("")
        self.stdout.write("Or add to request headers:")
        self.stdout.write(f"  Authorization: Token {token.key}")
