#!/usr/bin/env python
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    import django

    django.setup()  

    from django.core.management import execute_from_command_line
    from django_tenants.utils import schema_context
    from django.contrib.auth import get_user_model

    args = sys.argv

    # custom command
    if len(args) >= 3 and args[1] == "createsuperuser":

        schema = args[2]

        username = input("Username: ")
        email = input("Email: ")
        password = input("Password: ")

        User = get_user_model()

        with schema_context(schema):
            if User.objects.filter(username=username).exists():
                print("User already exists")
                return

            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )

        print(f"✅ Superuser created in schema: {schema}")
        return

    # fallback to normal django commands
    execute_from_command_line(args)


if __name__ == "__main__":
    main()
