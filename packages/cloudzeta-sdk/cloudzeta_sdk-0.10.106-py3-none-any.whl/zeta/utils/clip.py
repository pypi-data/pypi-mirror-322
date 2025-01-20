from PIL import Image
from sentence_transformers import SentenceTransformer
import io

CLIP_MODEL = 'clip-ViT-B-32'

def compute_image_embeddings(path: str):
    model = SentenceTransformer(CLIP_MODEL)
    return model.encode(Image.open(path)).tolist() # Convert ndarray to list

def compute_text_embeddings(text: str):
    model = SentenceTransformer(CLIP_MODEL)
    return model.encode(text).tolist() # Convert ndarray to list

def compute_image_embeddings_from_bytes(image_bytes: bytes):
    model = SentenceTransformer(CLIP_MODEL)
    image = Image.open(io.BytesIO(image_bytes))
    return model.encode(image).tolist()  # Convert ndarray to list
