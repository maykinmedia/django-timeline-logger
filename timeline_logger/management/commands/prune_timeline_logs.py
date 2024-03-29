from textwrap import dedent

from django.core.management.base import BaseCommand

from timeline_logger.service import prune_timeline_logs


class Command(BaseCommand):
    help = "Removes timeline logs objects older than the specified date."

    def add_arguments(self, parser):
        parser.add_argument(
            "--noinput",
            "--no-input",
            action="store_false",
            dest="interactive",
            help="Tells Django to NOT prompt the user for input of any kind.",
        )
        exclusive_group = parser.add_mutually_exclusive_group(required=True)

        exclusive_group.add_argument(
            "--all",
            action="store_true",
            help="Whether to delete all log records.",
        )

        exclusive_group.add_argument(
            "--keep-days",
            type=int,
            help="Only delete records older than the specified number of days.",
        )

    def handle(self, *args, **options):
        all = options["all"]
        keep_days = options["keep_days"]
        interactive = options["interactive"]

        if all and interactive:
            confirm = input(
                dedent(
                    """You have specified "--all", meaning all timeline logs will be deleted.
                Are you sure you want to do this?

                Type 'yes' to continue, or 'no' to cancel: """
                )
            )
        else:
            confirm = "yes"

        if confirm == "yes":
            number = prune_timeline_logs(keep_days=0 if all else keep_days)
            self.stdout.write(f"Successfully deleted {number} timeline logs.")
        else:
            self.stdout.write("Flush cancelled.")
