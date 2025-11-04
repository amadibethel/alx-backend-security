# ip_tracking/management/commands/block_ip.py
from django.core.management.base import BaseCommand, CommandError
from ip_tracking.models import BlockedIP

class Command(BaseCommand):
    help = "Add an IP address to the BlockedIP list."

    def add_arguments(self, parser):
        parser.add_argument("ip_address", type=str, help="IP address to block")

    def handle(self, *args, **options):
        ip_address = options["ip_address"]
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            self.stdout.write(self.style.WARNING(f"IP {ip_address} is already blocked."))
        else:
            BlockedIP.objects.create(ip_address=ip_address)
            self.stdout.write(self.style.SUCCESS(f"IP {ip_address} successfully blocked."))

