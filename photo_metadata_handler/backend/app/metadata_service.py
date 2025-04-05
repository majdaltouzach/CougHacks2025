import piexif
from piexif import ImageIFD, ExifIFD, GPSIFD
from piexif.helper import UserComment
from PIL import Image
import os
import json

class MetadataService:
    def __init__(self):
        # Combine all known tag mappings from piexif
        self.ALL_TAGS = {}
        for ifd_name in piexif.TAGS:
            for tag_id, tag_info in piexif.TAGS[ifd_name].items():
                self.ALL_TAGS[tag_info["name"]] = (ifd_name, tag_id)

    # Helper to get tag location and ID
    def resolve_tag(self, tag_name: str):
        result = self.ALL_TAGS.get(tag_name)
        if not result:
            raise ValueError(f"Tag '{tag_name}' not found in known EXIF tags")
        return result  # (ifd, tag_id)

    def update_metadata(self, image_path: str, tag_name: str, new_value: str):
        # Encode string value to bytes
        encoded_value = new_value.encode("utf-8")
        
        exif_dict = piexif.load(image_path)
        ifd, tag_id = self.resolve_tag(tag_name)

        # ALL_TAGS is kinda broken because multiple IFDs (Image, 0th, 1st, etc.), can contain the same tag
        # But it parses with the assumption that each tag name will only exist in one IFD
        # So we only use ALL_TAGS to look up the tag_id for a given tag name, which doesn't change between IFDS.
        for ifd_name in exif_dict:
            if ifd_name == "thumbnail":
                continue
            if tag_id in exif_dict[ifd_name]:
                exif_dict[ifd_name][tag_id] = encoded_value

        # Dump & reinsert
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, image_path)

    def delete_metadata_tag(self, image_path: str, tag_name: str):
        exif_dict = piexif.load(image_path)
        ifd, tag_id = self.resolve_tag(tag_name)

        deleted = False
        # same thing here
        for ifd_name in exif_dict:
            if ifd_name == "thumbnail":
                continue
            if tag_id in exif_dict[ifd_name]:
                del exif_dict[ifd_name][tag_id]
                deleted = True
        if not deleted:
            raise ValueError(f"Tag '{tag_name}' not found in image metadata")
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, image_path)
            
    def get_exif_data(self, path: str):
        exif_data = piexif.load(path)
        return exif_data

    def get_gps_info(self, exif_data_raw):
        gps_info = {}
        for tag_id, value in exif_data_raw.items():
            tag_name = piexif.GPSIFD.get(tag_id, tag_id)
            gps_info[tag_name] = value
        return gps_info if gps_info else None
