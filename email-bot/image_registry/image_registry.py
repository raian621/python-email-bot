from collections.abc import MutableMapping
from os import path

supported_image_types = (
    "apng", "avif", "gif", "jpeg", "svg+xml", "webp", "bmp", "ico", "tiff"
)

class ImageEntry:
    def __init__(self, cid, img_path, img_type=None):
        if (img_type == 'jpg'):
            img_type = 'jpeg'
        else:
            if (img_type not in supported_image_types):
                raise ValueError(f"Image type {img_type} currently not supported/")
        self.img_type = img_type
        self.cid = cid
        self.img_path = path.abspath(img_path)
    
    def __str__(self):
        return f"img_type: {self.img_type}, cid: {self.cid}, img_path{self.img_path}"

class TemplateImageRegistry(MutableMapping):
    def __init__(self, *args, **kwargs):
        self.__dict__.update(*args, **kwargs)

    def __setitem__(self, key, value):
        if (type(value) != list):
            raise ValueError("Registry entry must be a 'ImageEntry' array")

        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]

    def __delitem__(self, key):
        del self.__dict__[key]

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return '{}, TemplateImageRegistry({})'.format(super(TemplateImageRegistry,
             self).__repr__(), self.__dict__)

"""
Global image registry

Stores ImageEntry objects that store data necessary to embed an image
in a MIME text/html type
"""
image_registry = TemplateImageRegistry()
