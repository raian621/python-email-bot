from image_registry import image_registry, ImageEntry

# create ImageEntry
cat_entry = ImageEntry(
    cid="cat-picture", 
    img_path="./static/images/maine-coon-gf740a0b4e_640.jpg",
    img_type="gif"
)

# register ImageEntry cat_entry to "generic.html" template 
image_registry["bot-email-template.html"] = [cat_entry]
