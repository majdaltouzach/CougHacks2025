import piexif
# Remove the unnecessary imports
# from piexif import ImageIFD, ExifIFD, GPSIFD, InteroperabilityIFD, FirstIFD, ThumbnailIFD
from piexif.helper import UserComment
from PIL import Image
import os

# Combine all known tag mappings from piexif
ALL_TAGS = {}
for ifd_name in piexif.TAGS:
    for tag_id, tag_info in piexif.TAGS[ifd_name].items():
        ALL_TAGS[tag_info["name"]] = (ifd_name, tag_id)

# Helper to get tag location and ID
def resolve_tag(tag_name: str):
    result = ALL_TAGS.get(tag_name)
    if not result:
        raise ValueError(f"Tag '{tag_name}' not found in known EXIF tags")
    return result  # (ifd, tag_id)

def update_metadata(image_path: str, tag_name: str, new_value: str):
    exif_dict = piexif.load(image_path)
    ifd, tag_id = resolve_tag(tag_name)

    # Encode string value to bytes
    encoded_value = new_value.encode("utf-8")

    # Assign new tag value
    exif_dict[ifd][tag_id] = encoded_value

    # Dump & reinsert
    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, image_path)

def delete_metadata_tag(image_path: str, tag_name: str):
    exif_dict = piexif.load(image_path)
    ifd, tag_id = resolve_tag(tag_name)

    if tag_id in exif_dict[ifd]:
        del exif_dict[ifd][tag_id]
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, image_path)
    else:
        raise ValueError(f"Tag '{tag_name}' not found in image metadata")

