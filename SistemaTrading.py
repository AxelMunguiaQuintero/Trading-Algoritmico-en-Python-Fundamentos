# Importar librerías
import yfinance as yf
import time
# Librerías Propias
from Estrategia1 import Estrategia1

# Definir lista de activos y marco de tiempo
activos = [
    
    "EURUSD=X", "GBPUSD=X", "USDJPY=X", "USDCAD=X",
    "GC=F", "CL=F", "SI=F", "NG=F",
    "AAPL", "MSFT", "GOOGL", "AMZN",
    "BTC-USD", "ETH-USD", "ADA-USD", "SOL-USD"
    
    ]
marco_tiempo = "1h"

# Función para ejecutar la estrategia en diferentes activos y marcos de tiempo
def ejecutar_estrategia(activos: list, marco_tiempo: str, parametros_optimizados: list):
    
    """
    Ejecuta nuestra clase de Estrategia 1 para detectar oportunidades de inversión (señales)
    """
    
    while True:
        for activo in activos:
            # Descargar datos
            df = yf.download(activo, period="1y", interval=marco_tiempo)
            # Crear instancia de la estrategia
            estrategia = Estrategia1(df)
            estrategia.periodo_ma_rapido = parametros_optimizados[0]
            estrategia.periodo_ma_lento = parametros_optimizados[1]
            estrategia.periodo_rsi = parametros_optimizados[2]
            # Calcular la estrategia
            calculo_señal = estrategia.calcular()
            if calculo_señal is not False:
                # Imprimir señal generada
                print(f"Activo: {activo}, Marco de Tiempo: {marco_tiempo}, Señal Generada: {calculo_señal}")
        # Esperar a volver a ejecutar
        print("\nEsperando...\n")
        time.sleep(60 * 60)
        
# Ejecutar la estrategia en diferentes activos
parametros_optimizados = [12, 27, 14]
ejecutar_estrategia(activos=activos, marco_tiempo=marco_tiempo, parametros_optimizados=parametros_optimizados) 
