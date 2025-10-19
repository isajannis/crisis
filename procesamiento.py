import os
import pandas as pd


def inspect_file(file_path):
    print(f"\n=== Inspeccionando: {file_path} ===")
    
    # Ver tamaño
    file_size = os.path.getsize(file_path)
    print(f"Tamaño: {file_size} bytes")
    
    # Intentar diferentes encodings
    encodings = ['utf-8', 'latin-1', 'cp1252', 'utf-16']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                first_line = f.readline()
                if first_line and len(first_line.strip()) > 0:
                    print(f"Encoding {encoding}: {first_line[:100]}...")
                    return True
        except Exception as e:
            print(f"Encoding {encoding} falló: {e}")
    
    # Si todo falla, leer como binario
    with open(file_path, 'rb') as f:
        first_bytes = f.read(100)
        print(f"Primeros bytes (hex): {first_bytes.hex()}")
        print(f"Primeros bytes (ascii): {first_bytes}")
    
    return False

# Probar con un archivo
inspect_file("C:\\Users\\isaja\\Documents\\dcc\\e\\CrisisMMD_v2.0\\CrisisMMD_v2.0\\annotations\\hurricane_irma_final_data.tsv")


# Cargar un archivo específico para explorar
file_path = "C:\\Users\\isaja\\Documents\\dcc\\e\\CrisisMMD_v2.0\\CrisisMMD_v2.0\\annotations\\hurricane_irma_final_data.tsv"
df = pd.read_csv(file_path, sep='\t', encoding='utf-8')

print("\n=== INFORMACIÓN BÁSICA ===")
print(f"Dimensiones: {df.shape} (filas, columnas)")
print(f"Columnas: {list(df.columns)}")
print(f"Total de registros: {len(df):,}")

print("\n=== PRIMERAS FILAS ===")
# Mostrar primeras filas con todas las columnas
pd.set_option('display.max_columns', None)  # Mostrar todas las columnas
pd.set_option('display.width', 1000)        # Ancho máximo
pd.set_option('display.max_colwidth', 50)   # Ancho máximo por columna

print(df.head(10))