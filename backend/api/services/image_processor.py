from PIL import Image
import io

class ImageProcessor:
    @staticmethod
    def read_image(image_bytes: bytes) -> Image.Image:
        try:
            return Image.open(io.BytesIO(image_bytes))
        except Exception as e:
            raise ValueError(f"Unable to read image: {str(e)}")

    @staticmethod
    def enhance_medical_image(image: Image.Image) -> Image.Image:
        return image

    @staticmethod
    def validate_medical_format(image: Image.Image) -> bool:
        return image.size[0] >= 224 and image.size[1] >= 224