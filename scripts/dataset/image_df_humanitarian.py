# Creación del dataset de imágenes a partir de archivos TSV
# Se centra en los datos humanitarios
import os
from pathlib import Path
import pandas as pd

# Lista de archivos TSV
tsv_files = [
    "C:\\Users\\isaja\\Documents\\dcc\\e\\CrisisMMD_v2.0\\CrisisMMD_v2.0\\annotations\\california_wildfires_final_data.tsv",
    "C:\\Users\\isaja\\Documents\\dcc\\e\\CrisisMMD_v2.0\\CrisisMMD_v2.0\\annotations\\srilanka_floods_final_data.tsv", 
    "C:\\Users\\isaja\\Documents\\dcc\\e\\CrisisMMD_v2.0\\CrisisMMD_v2.0\\annotations\\hurricane_harvey_final_data.tsv",
    "C:\\Users\\isaja\\Documents\\dcc\\e\\CrisisMMD_v2.0\\CrisisMMD_v2.0\\annotations\\hurricane_irma_final_data.tsv", 
    "C:\\Users\\isaja\\Documents\\dcc\\e\\CrisisMMD_v2.0\\CrisisMMD_v2.0\\annotations\\hurricane_maria_final_data.tsv", 
    "C:\\Users\\isaja\\Documents\\dcc\\e\\CrisisMMD_v2.0\\CrisisMMD_v2.0\\annotations\\iraq_iran_earthquake_final_data.tsv",
    "C:\\Users\\isaja\\Documents\\dcc\\e\\CrisisMMD_v2.0\\CrisisMMD_v2.0\\annotations\\mexico_earthquake_final_data.tsv"
]

remain_columns = ['tweet_id', 'image_id','image_human', 'image_human_conf', 'image_path']
# 'image_url' no es tan importante en este momento

def create_image_df():
    """Crear DataFrame de textos a partir de los archivos TSV"""
    all_images = []
    missing_files = []
    print("=== CREANDO DATASET DE IMAGENES CrisisMMD ===\n")
    
    for file_path in tsv_files:
        if os.path.exists(file_path):
            print(f"Cargando: {Path(file_path).name}")
            try:
                df = pd.read_csv(file_path, sep='\t', encoding='utf-8')
                df_image = df[remain_columns].copy()
                all_images.append(df_image)
                print(f"   - Registros: {len(df_image)}")
            except Exception as e:
                print(f"Error al cargar: {e}")
        else:
            missing_files.append(file_path)
            print(f"No encontrado: {file_path}")

    if all_images:
        image_dataset = pd.concat(all_images, ignore_index=True)
        print(f"\nDATASET DE IMAGENES CARGADO:")
        print(f"   - Total de registros: {len(image_dataset):,}")
        print(f"   - Archivos cargados: {len(tsv_files) - len(missing_files)}/{len(tsv_files)}")
        return image_dataset
    else:
        print("No se pudieron cargar archivos")
        return None
    
# Creamos el DataFrame de imágenes
image_df = create_image_df()

# Eliminamos duplicados basados en 'tweet_id' y 'image_path'
if image_df is not None:
    before_dedup = len(image_df)
    image_df.drop_duplicates(subset=['tweet_id', 'image_path'], inplace=True)
    after_dedup = len(image_df)
    print(f"\nDuplicados eliminados: {before_dedup - after_dedup}")
    print(f"Registros después de eliminar duplicados: {after_dedup:,}")

# Agregamos una columna 'image_name' para facilitar la identificación de las imágenes
# 'data_image/california_wildfires/10_10_2017/917791044158185473_0.jpg' -> '917791044158185473_0'

if image_df is not None:
    image_df['image_name'] = image_df['image_path'].apply(lambda x: os.path.splitext(os.path.basename(x))[0])
    print("\nColumna 'image_name' agregada al DataFrame.")

# Guardar el DataFrame a un archivo CSV para uso futuro
if image_df is not None:
    output_path = "C:\\Users\\isaja\\Documents\\dcc\\e\\crisis\\data\\crisis_images_dataset_humanitarian.csv"
    image_df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"\nDataset de imágenes guardado en: {output_path}")