from django.core.management.base import BaseCommand
from products.models import Product


class Command(BaseCommand):
    help = "Populates the database with sample products"

    def handle(self, *args, **kwargs):
        Product.objects.create(
            name="Emaar Beachfront Apartment",
            description="Beautiful 2-bedroom apartment in Emaar Beachfront with sea view",
            price=1200000,
            quantity=10,
            category="Apartment",
            brand="Emaar Properties",
            rating=4.8,
        )
        Product.objects.create(
            name="Damac Hills Villa",
            description="Luxurious 4-bedroom villa in Damac Hills with private pool and golf course view",
            price=3500000,
            quantity=5,
            category="Villa",
            brand="Damac Properties",
            rating=4.9,
        )
        Product.objects.create(
            name="Dubai Marina Penthouse",
            description="Stunning 3-bedroom penthouse in Dubai Marina with panoramic view of the city",
            price=6500000,
            quantity=2,
            category="Penthouse",
            brand="Emaar Properties",
            rating=4.7,
        )
        Product.objects.create(
            name="Jumeirah Lake Towers Office",
            description="Spacious office space in Jumeirah Lake Towers with beautiful lake view",
            price=2000000,
            quantity=8,
            category="Office",
            brand="DMCC",
            rating=4.5,
        )
        Product.objects.create(
            name="Dubai Creek Harbour Townhouse",
            description="Lovely 3-bedroom townhouse in Dubai Creek Harbour with views of the creek and Burj Khalifa",
            price=2800000,
            quantity=3,
            category="Townhouse",
            brand="Emaar Properties",
            rating=4.6,
        )
        Product.objects.create(
            name="Palm Jumeirah Villa",
            description="Luxury 5-bedroom villa on the Palm Jumeirah with private beach and pool",
            price=12000000,
            quantity=1,
            category="Villa",
            brand="Nakheel",
            rating=4.9,
        )
        Product.objects.create(
            name="Business Bay Office",
            description="Spacious office space in Business Bay with stunning view of the Burj Khalifa",
            price=5000000,
            quantity=4,
            category="Office",
            brand="Emaar Properties",
            rating=4.7,
        )
        Product.objects.create(
            name="The Greens Apartment",
            description="Beautiful 1-bedroom apartment in The Greens with views of the community and pool",
            price=1000000,
            quantity=15,
            category="Apartment",
            brand="Emaar Properties",
            rating=4.5,
        )
        Product.objects.create(
            name="Jumeirah Village Circle Townhouse",
            description="Lovely 3-bedroom townhouse in Jumeirah Village Circle with private garden",
            price=2500000,
            quantity=6,
            category="Townhouse",
            brand="Nakheel",
            rating=4.8,
        )
        Product.objects.create(
            name="Dubai Hills Estate Villa",
            description="Stunning 6-bedroom villa in Dubai Hills Estate with private pool and golf course view",
            price=16000000,
            quantity=1,
            category="Villa",
            brand="Emaar Properties",
            rating=4.9,
        )
        self.stdout.write(
            self.style.SUCCESS(
                "Successfully populated the database with sample products."
            )
        )
