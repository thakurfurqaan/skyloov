from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile

from products.models import ProductImage


def process_product_image(image_id):
    try:
        image = ProductImage.objects.get(id=image_id)
        image_data = image.image.read()

        # Generate thumbnails
        sizes = {
            "thumbnail": (150, 150),
            "small": (300, 300),
            "large": (1200, 1200),
        }

        img = Image.open(BytesIO(image_data))

        # Process each size and populate the respective image field
        for size_name, size in sizes.items():
            img_copy = img.copy()
            img_copy.thumbnail(size)

            # Create a BytesIO object to write the processed image to
            output = BytesIO()

            # Write the processed image to the BytesIO object
            img_copy.save(output, format="JPEG")

            # Create an InMemoryUploadedFile object from the BytesIO object
            image_file = InMemoryUploadedFile(
                output,
                "ImageField",
                f"{image.image.name}-{size_name}.jpg",
                "image/jpeg",
                output.getbuffer().nbytes,
                None,
            )

            # Set the processed image to the appropriate image field
            setattr(image, size_name, image_file)

        # Save the ProductImage instance with the processed images
        image.save()

    except ProductImage.DoesNotExist:
        pass
