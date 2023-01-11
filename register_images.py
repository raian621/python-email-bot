from image_registry import image_registry, ImageEntry

cat_entry = ImageEntry(
    cid="cat-picture", 
    img_path="./static/images/cat-typing.gif",
    img_type="gif"
)

image_registry["generic.html"] = [cat_entry]

 