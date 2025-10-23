from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = "Create or get API token for a user"

    def add_arguments(self, parser):
        parser.add_argument("--username", type=str, help="Username to create/get token for", default="admin")
        parser.add_argument(
            "--create-user",
            action="store_true",
            help="Create user if it does not exist",
        )

    def handle(self, *args, **options):
        username = options["username"]

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            if options["create_user"]:
                # Create a new user
                user = User.objects.create_user(
                    username=username,
                    email=f"{username}@kellcare.com",
                    password="kellcare123",  # Default password
                )
                self.stdout.write(self.style.SUCCESS(f"Created user: {username} with password: kellcare123"))
            else:
                self.stdout.write(self.style.ERROR(f'User "{username}" does not exist. Use --create-user to create it.'))
                return

        # Get or create token
        token, created = Token.objects.get_or_create(user=user)

        if created:
            self.stdout.write(self.style.SUCCESS(f"Created new API token for {username}"))
        else:
            self.stdout.write(self.style.SUCCESS(f"Retrieved existing API token for {username}"))

        self.stdout.write(self.style.WARNING(f"API Token: {token.key}"))
        self.stdout.write("")
        self.stdout.write("Usage examples:")
        self.stdout.write(f'  curl -H "Authorization: Token {token.key}" http://127.0.0.1:8000/api/doctors/')
        self.stdout.write(f'  curl -H "Authorization: Token {token.key}" http://127.0.0.1:8000/api/appointments/')
        self.stdout.write("")
        self.stdout.write("Or add to request headers:")
        self.stdout.write(f"  Authorization: Token {token.key}")
