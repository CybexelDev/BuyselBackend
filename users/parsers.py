
from rest_framework.parsers import MultiPartParser, DataAndFiles
from rest_framework.exceptions import ParseError

from .image_compression import compress_image


class ImageCompressionMultiPartParser(MultiPartParser):
    def parse(self, stream, media_type=None, parser_context=None):
        parsed = super().parse(
            stream,
            media_type=media_type,
            parser_context=parser_context,
        )

        data = parsed.data
        files = parsed.files

        try:
            for field_name in ("image", "images","profile_image"):
                compressed_files = []

                for uploaded_file in files.getlist(field_name):
                    compressed_files.append(
                        compress_image(uploaded_file)
                    )

                if compressed_files:
                    files.setlist(field_name, compressed_files)

        except ValueError as exc:
            raise ParseError(str(exc)) from exc

        return DataAndFiles(data, files)