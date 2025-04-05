import piexif
from piexif.helper import UserComment
from PIL import Image

class MetadataService:
    def __init__(self):
        # Initialize the service and combine all EXIF tags
        self.all_tags = self._combine_all_tags()

    def _combine_all_tags(self):
        # Combine all EXIF tags into a single dictionary
        all_tags = {}
        for ifd_name in piexif.TAGS:
            for tag_id, tag_info in piexif.TAGS[ifd_name].items():
                all_tags[tag_info["name"]] = (ifd_name, tag_id)
        return all_tags

    def _resolve_tag(self, tag_name: str):
        # Resolve the tag name to its corresponding IFD and tag ID
        result = self.all_tags.get(tag_name)
        if not result:
            raise ValueError(f"Tag '{tag_name}' not found in known EXIF tags")
        return result  # (ifd, tag_id)

    def update_metadata(self, image_path: str, tag_name: str, new_value: str):
        # Update the metadata of an image
        exif_dict = piexif.load(image_path)
        ifd, tag_id = self._resolve_tag(tag_name)
        encoded_value = new_value.encode("utf-8")
        exif_dict[ifd][tag_id] = encoded_value
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, image_path)

    def delete_metadata_tag(self, image_path: str, tag_name: str):
        # Delete a specific metadata tag from an image
        exif_dict = piexif.load(image_path)
        ifd, tag_id = self._resolve_tag(tag_name)
        if tag_id in exif_dict[ifd]:
            del exif_dict[ifd][tag_id]
            exif_bytes = piexif.dump(exif_dict)
            piexif.insert(exif_bytes, image_path)
        else:
            raise ValueError(f"Tag '{tag_name}' not found in image metadata")

    def get_gps_info(self, exif_data):
        # Extract GPS information from EXIF data
        gps_info = {}
        if "GPSInfo" in exif_data:
            for key in exif_data["GPSInfo"].keys():
                decode = piexif.GPSIFD.get(key, key)
                gps_info[decode] = exif_data["GPSInfo"][key]
        return gps_info

