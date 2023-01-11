from image_registry import image_registry, ImageEntry

# create ImageEntry
cat_entry = ImageEntry(
    cid="cat-picture", 
    img_path="./static/images/cat-typing.gif",
    img_type="gif"
)

# register ImageEntry cat_entry to "generic.html" template 
image_registry["generic.html"] = [cat_entry]
