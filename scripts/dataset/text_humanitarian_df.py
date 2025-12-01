import pandas as pd
import os
from pathlib import Path

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

# Lista de columnas a mantener
remain_columns = ['tweet_id', 'text_human', 'text_human_conf', 'tweet_text']

def create_text_df():
    """Crear DataFrame de textos a partir de los archivos TSV"""
    all_texts = []
    missing_files = []
    print("=== CREANDO DATASET DE TEXTOS CrisisMMD ===\n")
    
    for file_path in tsv_files:
        if os.path.exists(file_path):
            print(f"Cargando: {Path(file_path).name}")
            try:
                df = pd.read_csv(file_path, sep='\t', encoding='utf-8')
                df_text = df[remain_columns].copy()
                all_texts.append(df_text)
                print(f"   - Registros: {len(df_text)}")
            except Exception as e:
                print(f"Error al cargar: {e}")
        else:
            missing_files.append(file_path)
            print(f"No encontrado: {file_path}")

    if all_texts:
        text_dataset = pd.concat(all_texts, ignore_index=True)
        print(f"\nDATASET DE TEXTOS CARGADO:")
        print(f"   - Total de registros: {len(text_dataset):,}")
        print(f"   - Archivos cargados: {len(tsv_files) - len(missing_files)}/{len(tsv_files)}")
        return text_dataset
    else:
        print("No se pudieron cargar archivos")
        return None
    
# Creamos el DataFrame de textos
text_df = create_text_df()

# Eliminamos duplicados basados en 'tweet_id' y 'tweet_text'
if text_df is not None:
    before_dedup = len(text_df)
    text_df.drop_duplicates(subset=['tweet_id', 'tweet_text'], inplace=True)
    after_dedup = len(text_df)
    print(f"\nDuplicados eliminados: {before_dedup - after_dedup}")
    print(f"Registros después de eliminar duplicados: {after_dedup:,}")

# Eliminamos filas que sean de label "not_humanitarian"
if text_df is not None:
    before_filter = len(text_df)
    text_df = text_df[text_df['text_human'] != 'not_humanitarian']
    after_filter = len(text_df)
    print(f"\nRegistros eliminados (not_humanitarian): {before_filter - after_filter}")
    print(f"Registros después de filtrar: {after_filter:,}")

# Guardar el DataFrame a un archivo CSV para uso futuro
if text_df is not None:
    output_path = "C:\\Users\\isaja\\Documents\\dcc\\e\\crisis\\data\\crisis_texts_humanitarian_dataset.csv"
    text_df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"\nDataset de textos guardado en: {output_path}")