from PIL import Image
import numpy as np
import os
import pandas as pd
import time

time_start = time.time()

def preprocess_and_save_final(image_path, output_dir="./preprocessed_images"):
    """
    Aplica preprocesamiento a una imagen:
    1. Redimensiona la imagen a 224x224 píxeles
    2. Normaliza los valores de los píxeles a un rango de 0 a 1
    3. Normaliza cada canal de color (R, G, B) usando los valores de media y desviación estándar del dataset ImageNet
    Guarda la imagen preprocesada en formato .npy
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Cargar imagen original
    img = Image.open(image_path).convert('RGB')
    
    # 2. Redimensionar a 224x224
    img_resized = img.resize((224, 224))
    
    # 3. Convertir a array numpy y escalar a 0-1
    img_array = np.array(img_resized, dtype=np.float32)
    img_scaled = img_array / 255.0
    
    # 4. Normalizar cada canal con valores de ImageNet
    mean = [0.485, 0.456, 0.406]  # Media de ImageNet
    std = [0.229, 0.224, 0.225]   # Desviación estándar de ImageNet
    
    img_normalized = np.zeros_like(img_scaled)
    for channel in range(3):  # Para cada canal R, G, B
        img_normalized[:, :, channel] = (img_scaled[:, :, channel] - mean[channel]) / std[channel]
    
    # 5. Guardar la imagen preprocesada final
    original_name = os.path.basename(image_path)
    name, _ = os.path.splitext(original_name)
    output_path = os.path.join(output_dir, f"{name}.npy")
    np.save(output_path, img_normalized)
    
    print(f"Imagen preprocesada guardada en: {output_path}")
    print(f"Estadísticas de la imagen preprocesada:")
    print(f"    - Shape: {img_normalized.shape}")
    print(f"    - Rango: [{img_normalized.min():.3f}, {img_normalized.max():.3f}]")
    print(f"    - Media: [{img_normalized[:,:,0].mean():.3f}, {img_normalized[:,:,1].mean():.3f}, {img_normalized[:,:,2].mean():.3f}]")
    
    return img_normalized, output_path

path = "C:\\Users\\isaja\\Downloads\\Clairo_@_Fonda_Theatre_09_08_2024_(54012443778)_(cropped).jpg"
output_dir = "./data/preprocessed_images"

csv_path = "C:\\Users\\isaja\\Documents\\dcc\\e\\crisis\\data\\crisis_images_dataset.csv"
default_path = "C:/Users/isaja/Documents/dcc/e/CrisisMMD_v2.0/CrisisMMD_v2.0/"
df = pd.read_csv(csv_path)
for idx, row in df.iterrows():
    image_path = default_path + row['image_path']
    try:
        preprocess_and_save_final(image_path, output_dir)
    except Exception as e:
        print(f"Error al procesar la imagen {image_path}: {e}")

time_end = time.time()
# Tiempo en minutos
print(f"Tiempo total de preprocesamiento: {(time_end - time_start) / 60:.2f} minutos")
print("Preprocesamiento de todas las imágenes completado.")
print(f"Las imágenes preprocesadas se han guardado en el directorio: {output_dir}")