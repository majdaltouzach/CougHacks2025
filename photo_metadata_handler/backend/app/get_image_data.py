from picarta import Picarta

api_token = "8SU34IGX2WC8KS41WLSB"
localizer = Picarta(api_token)

def get_image_details(path):
    result = localizer.localize(img_path=path)
    return result



print(get_image_details("PXL_20211004_072757661.jpg"))