# Preprocesamiento de imágenes

# Redimensionar y normalizar (224x224)
# Normalizar los canales de color con respecto al dataset ImageNet

from PIL import Image

path = "C:\\Users\\isaja\\Downloads\\Clairo_@_Fonda_Theatre_09_08_2024_(54012443778)_(cropped).jpg"

# Open the image
img = Image.open(path)

# Define the new size (width, height)
new_size = (224, 224)
# Resize the image
resized_img = img.resize(new_size)

# Save the resized image
resized_img.save("output_image.jpg")