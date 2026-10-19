
from io import BytesIO
from rag.loader import load_brand_guide


class FakeUploadedFile:
    name = "sample_brand_guide.txt"

    def getvalue(self):
        return (
            b"Brand tone: Friendly and simple.\n"
            b"Required keyword: Reusable.\n"
            b"Avoid unsupported claims."
        )


sample_file = FakeUploadedFile()

text = load_brand_guide(sample_file)

print("Brand guide loaded successfully!")
print("\nExtracted content:\n")
print(text)
