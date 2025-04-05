import piexif
from piexif import TAGS
from PIL import Image
import copy
from PIL.ExifTags import GPSTAGS

class MetadataService:
    def __init__(self):
        self.ALL_TAGS = {}
        for ifd_name in piexif.TAGS:
            for tag_id, tag_info in piexif.TAGS[ifd_name].items():
                self.ALL_TAGS[tag_info["name"]] = (ifd_name, tag_id)

    def resolve_tag(self, tag_name: str):
        result = self.ALL_TAGS.get(tag_name)
        if not result:
            raise ValueError(f"Tag '{tag_name}' not found in known EXIF tags")
        return result

    def update_metadata(self, image_path: str, tag_name: str, new_value: str):
        encoded_value = new_value.encode("utf-8")
        exif_dict = piexif.load(image_path)
        ifd, tag_id = self.resolve_tag(tag_name)
        for ifd_name in exif_dict:
            if ifd_name == "thumbnail":
                continue
            if tag_id in exif_dict[ifd_name]:
                exif_dict[ifd_name][tag_id] = encoded_value
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, image_path)

    def delete_metadata_tag(self, image_path: str, tag_name: str):
        exif_dict = piexif.load(image_path)
        ifd, tag_id = self.resolve_tag(tag_name)
        deleted = False
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

    def delete_everything(self, image_path: str):
        exif_dict = piexif.load(image_path)
        exif_dict_ref = copy.deepcopy(exif_dict)
        for ifd_name in exif_dict_ref:
            if ifd_name == "thumbnail":
                continue
            for tag_id in exif_dict_ref[ifd_name]:
                del exif_dict[ifd_name][tag_id]
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, image_path)

    def get_exif_data(self, path: str):
        return piexif.load(path)

    def get_gps_info(self, exif_data_raw):
        gps_info = {}
        for tag_id, value in exif_data_raw.items():
            tag_name = GPSTAGS.get(tag_id, tag_id)
            gps_info[tag_name] = value
        return gps_info if gps_info else None