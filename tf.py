import pandas as pd
from sqlalchemy import create_engine
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter 
# Configura tu conexión a la base de datos
usuario = 'postgres'
contraseña = 'postgres'
host = '192.168.191.230'
puerto = '5434'
nombre_base_datos = 'water_quality'

# Usando SQLAlchemy para crear la conexión
engine = create_engine(f'postgresql+psycopg2://{usuario}:{contraseña}@{host}:{puerto}/{nombre_base_datos}')

# Consulta para obtener los datos (simplificada para prueba)
query = "SELECT * from vistaconjunto"
try:
    df = pd.read_sql(query, engine)
    print(df.head())
except Exception as e:
    print(f"Error: {e}")

print(df.info())

print('VALORES UNICOS: ', df['id_registro'].unique())

# Crear DataFrame base sin duplicados en id_registro y demás columnas no cambiantes
base_columns = ['id_registro', 'condicion_termica', 'fecha', 'codigo_perfil', 
                'descripcion_estratificacion', 'sitio', 'mix_criteria']
df_base = df[base_columns].drop_duplicates()

# Pivotar los datos
df_pivot = df.pivot_table(index='id_registro', columns='parametro', values='valor_parametro', aggfunc='first').reset_index()

# Verificar los datos pivotados
#print(df_pivot.head(20))

# Unir el DataFrame base con el DataFrame pivotado
df_final = pd.merge(df_base, df_pivot, on='id_registro', how='left')

# Ajustar las opciones de visualización para ver todas las filas y columnas
pd.set_option('display.max_columns', None) # Mostrar todas las columnas
 
# Mostrar el DataFrame resultante
print(df_final)

#print(df_final.sample())

print(df_final.info())

df_final['N-NH4 (µg/l)'] = df_final['N-NH4 (µg/l)'].fillna(0)
df_final['N-NO2 (µg/l)'] = df_final['N-NO2 (µg/l)'].fillna(0)
df_final['N-NO3 (mg/l)'] = df_final['N-NO3 (mg/l)'].fillna(0)

# Crear una nueva columna basada en otras columnas
df_final['Nitrato Total'] = df_final['N-NH4 (µg/l)'] + df_final['N-NO2 (µg/l)'] + (df_final['N-NO3 (mg/l)'] * 1000)
df_final['Cianobacterias Total'] = df_final['Anabaena'] + df_final['Anabaenopsis'] 
+ df_final['Aphanizomenon'] + df_final['Aphanocapsa']
+ df_final['Aphanothece'] + df_final['Geitlerinema']
+ df_final['Merismopedia'] + df_final['Chroococcus']
+ df_final['Nostoc'] + df_final['Microcystis']
+ df_final['Oscillatoria'] + df_final['Phormidium']
+ df_final['Planktothrix'] + df_final['Pseudoanabaena']                     
+ df_final['Raphydiopsis'] + df_final['Romeria'] + df_final['Spirulina']    
+ df_final['Dolichospermum'] + df_final['Leptolyngbya'] + df_final['Synechococcus']                         
                        
df_final.drop(columns=['N-NH4 (µg/l)', 'N-NO2 (µg/l)', 'N-NO3 (mg/l)', 'Anabaena', 'Anabaenopsis', 'Aphanizomenon', 
'Aphanocapsa', 'Aphanothece', 'Chroococcus', 'Geitlerinema', 'Merismopedia', 'Microcystis', 'Nostoc', 'Oscillatoria',
'Phormidium', 'Planktothrix', 'Pseudoanabaena', 'Raphydiopsis', 'Romeria', 'Spirulina', 'Dolichospermum', 'Leptolyngbya', 'Synechococcus' ], inplace=True)       

print(df_final.sample())
print(df_final.info())

#print('VALORES UNICOS: ', df_final['id_registro'].unique())

# Obtener valores únicos de la columna 'Registro'
#unique_values = df_final['id_registro'].unique()

# Convertir a lista para asegurarse de que se imprimen todos los valores
#unique_values_list = list(unique_values)

# Imprimir todos los valores únicos
#print("VALORES UNICOS:", unique_values_list)

# Contabilizar la cantidad de valores únicos
#cantidad_valores_unicos = len(unique_values)
#print("CANTIDAD DE VALORES UNICOS:", cantidad_valores_unicos)

# Diagrama de pares para una muestra de 100 filas
#sns.pairplot(df_final.sample(100))  
#plt.show()
plt.figure(figsize=(12, 8))
sns.heatmap(df_final.isnull(), cbar=False, cmap='viridis')
#plt.show()

numeric_df = df_final.select_dtypes(include=[np.number])

plt.figure(figsize=(12, 10))
correlation_matrix = numeric_df.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
#plt.show()

# Crear un gráfico separado por cada columna numérica
# Especificar la columna a graficar
columna = 'Total Algas Sumatoria (Cel/L)'

# Obtener los valores mínimo y máximo de la columna
min_value = df_final[columna].min()
max_value = df_final[columna].max()

# Crear un gráfico de líneas para la columna especificada
plt.figure(figsize=(10, 6))
plt.plot(df_final.index, df_final[columna], marker='o', linestyle='-', color='blue', label=columna)

# Agregar etiquetas con los valores numéricos
plt.annotate(f'Mín: {min_value}', xy=(0, min_value), xytext=(10, 10), textcoords='offset points', fontsize=10,
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="blue", lw=1))
plt.annotate(f'Máx: {max_value}', xy=(len(df_final)-1, max_value), xytext=(-100, 10), textcoords='offset points', fontsize=10,
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="red", lw=1))

# Personalizar el gráfico
plt.title(f'Valores Mínimos y Máximos de {columna}')
plt.xlabel('Índice')
plt.ylabel('Valores')
plt.grid(True)
plt.legend()
plt.xticks(rotation=90)
plt.tight_layout()
#plt.show()
columna = 'Cianobacterias Total'

# Obtener los valores mínimo y máximo de la columna
min_value = df_final[columna].min()
max_value = df_final[columna].max()

# Crear un gráfico de líneas para la columna especificada
plt.figure(figsize=(10, 6))
plt.plot(df_final.index, df_final[columna], marker='o', linestyle='-', color='blue', label=columna)

# Agregar etiquetas con los valores numéricos
plt.annotate(f'Mín: {min_value}', xy=(0, min_value), xytext=(10, 10), textcoords='offset points', fontsize=10,
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="blue", lw=1))
plt.annotate(f'Máx: {max_value}', xy=(len(df_final)-1, max_value), xytext=(-100, 10), textcoords='offset points', fontsize=10,
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="red", lw=1))

# Personalizar el gráfico
plt.title(f'Valores Mínimos y Máximos de {columna}')
plt.xlabel('Índice')
plt.ylabel('Valores')
plt.grid(True)
plt.legend()
plt.xticks(rotation=90)
plt.tight_layout()
#plt.show()

columna = 'Nitrato Total'

# Obtener los valores mínimo y máximo de la columna
min_value = df_final[columna].min()
max_value = df_final[columna].max()

# Crear un gráfico de líneas para la columna especificada
plt.figure(figsize=(10, 6))
plt.plot(df_final.index, df_final[columna], marker='o', linestyle='-', color='blue', label=columna)

# Agregar etiquetas con los valores numéricos
plt.annotate(f'Mín: {min_value}', xy=(0, min_value), xytext=(10, 10), textcoords='offset points', fontsize=10,
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="blue", lw=1))
plt.annotate(f'Máx: {max_value}', xy=(len(df_final)-1, max_value), xytext=(-100, 10), textcoords='offset points', fontsize=10,
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="red", lw=1))

# Personalizar el gráfico
plt.title(f'Valores Mínimos y Máximos de {columna}')
plt.xlabel('Índice')
plt.ylabel('Valores')
plt.grid(True)
plt.legend()
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
#numeric_df = df_final.select_dtypes(include=[np.number])

#plt.figure(figsize=(12, 10))
#correlation_matrix = numeric_df.corr()
#sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
#plt.show()
 