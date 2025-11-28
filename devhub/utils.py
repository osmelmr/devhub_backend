# utils.py
import cloudinary.uploader

def delete_image(public_id: str):
    if public_id:
        result = cloudinary.uploader.destroy(public_id)
        return result
    return {"result": "no public_id"}
