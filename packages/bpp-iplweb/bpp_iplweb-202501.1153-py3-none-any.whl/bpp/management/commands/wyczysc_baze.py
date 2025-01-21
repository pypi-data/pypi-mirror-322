import random

from django.core.management import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = (
        "Czyści dane z PBNu oraz dane z bazy BPP (autorzy, źródła, wydawcy, publikacje)"
    )

    @transaction.atomic
    def handle(self, *args, **options):
        challenge = random.sample()
        raise NotImplementedError
