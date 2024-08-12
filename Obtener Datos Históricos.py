# Importar librerías
import yfinance as yf # pip install yfinance
import os
import time

# Listas de símbolos para diferentes categorías

# Divisas: Representan pares de monedas
divisas = [
    "EURUSD=X",   # Euro vs Dólar estadounidense
    "GBPUSD=X",   # Libra esternila vs Dólar estadounidense
    "USDJPY=X",   # Dólar estadounidense vs Yen Japónes
    "USDCAD=X"    # Dólar estadounidense vs Dólar canadiense
    ]

# Materias Primas: Incluyen productos básicos como metales y energéticos
materias_primas = [
    "GC=F",       # Oro (Gold)
    "CL=F",       # Petróleo Cruco (Crude Oil)
    "SI=F",       # Plata (Silver)
    "NG=F"        # Gas Natural (Natural Gas)
    ]

# Acciones: Empresas que cotizan en bolsa
acciones = [
    "AAPL",       # Apple Inc.
    "MSFT",       # Microsoft Corp.
    "GOOGL",      # Alphabet Inc. (Google)
    "AMZN"        # Amazon.com Inc.
    ]

# Criptomonedas: Monedas digitales y sus valores expresados en dólares estadounidenses
criptomonedas = [
    "BTC-USD",    # Bitcoin
    "ETH-USD",    # Ethereum
    "ADA-USD",    # Cardano
    "SOL-USD"     # Solana
    ]

# Intervalos de tiempo para los datos históricos
intervalos = ["1m", "1h", "1d"]

# Fecha de inicio y fecha final para los datos históricos
fecha_inicio = "2023-01-01"
fecha_final = "2024-08-01"

# Función para obtener datos históricos
def obtener_datos(simbolos: list, fecha_inicio: str, fecha_final: str, intervalos: list) -> dict:
    
    """
    Método que descarga datos históricos para un conjunto de instrumentos financieros.
    """
    
    datos = {}
    for simbolo in simbolos:
        datos[simbolo] = {}
        for intervalo in intervalos:
            print(f"Descargando datos para {simbolo} con intervalo {intervalo}...")
            if intervalo == "1m":
                df = yf.download(tickers=simbolo, interval=intervalo)
            else:
                df = yf.download(tickers=simbolo, start=fecha_inicio, end=fecha_final, interval=intervalo)
            datos[f"{simbolo}"][f"{intervalo}"] = df
        time.sleep(0.25)
        
    return datos

# Obtener datos históricos para cada categoría
datos_divisas = obtener_datos(simbolos=divisas, fecha_inicio=fecha_inicio, fecha_final=fecha_final, intervalos=intervalos)
datos_materias_primas = obtener_datos(simbolos=materias_primas, fecha_inicio=fecha_inicio, fecha_final=fecha_final, intervalos=intervalos)
datos_acciones = obtener_datos(simbolos=acciones, fecha_inicio=fecha_inicio, fecha_final=fecha_final, intervalos=intervalos)
datos_criptomonedas = obtener_datos(simbolos=criptomonedas, fecha_inicio=fecha_inicio, fecha_final=fecha_final, intervalos=intervalos)

# Guardar los datos en archivos csv
if not os.path.isdir("datos"):
    os.mkdir("datos")

datos_conjutnos = {"acciones": datos_acciones, "divisas": datos_divisas, "materias_primas": datos_materias_primas,
                   "criptomonedas": datos_criptomonedas}
# Iterar en cada conjunto de datos
for tipo_activo, conjunto_datos in datos_conjutnos.items():
    # Iterar en cada instrumento
    for ticker, datos_dict in conjunto_datos.items():
        # Iterar en cada intervalo de tiempo
        for intervalo, datos_df in datos_dict.items():
            # Revisar si existe subcarpeta para este tipo de activo
            if not os.path.isdir(f"datos/{tipo_activo}"):
                os.mkdir(f"datos/{tipo_activo}")
            # Revisar si este activo ya existe dentro de esta categoría
            if not os.path.isdir(f"datos/{tipo_activo}/{ticker}"):
                os.mkdir(f"datos/{tipo_activo}/{ticker}")
            datos_df.to_csv(f"datos/{tipo_activo}/{ticker}/{intervalo}.csv")

# Recordatorio:
#   - Los datos históricos son fundamentales para desarrollar estrategias de trading efectivas y tomar decisiones informadas.
