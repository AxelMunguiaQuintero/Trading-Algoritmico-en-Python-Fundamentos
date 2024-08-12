# Importar librerías
import pandas as pd
import numpy as np

# Indicador RSI
def RSI(df: pd.DataFrame, periodo: int = 14) -> pd.Series:
    
    """
    Indicador RSI - Calcula los niveles de sobrecompra y sobreventa
    """
    
    # Calcular
    Delta = df["Close"].diff(periods=1)
    Ganancia = Delta.where(Delta >= 0, 0)
    Perdida = np.abs(Delta.where(Delta < 0, 0))
    # Valores en la posición del periodo, utilizando una media exponencial ponderada
    ganancia_promedio = Ganancia.ewm(alpha = 1 / periodo, min_periods = periodo).mean()
    perdida_promedio = Perdida.ewm(alpha = 1 / periodo, min_periods = periodo).mean()
    RS = ganancia_promedio / perdida_promedio
    RSI = pd.Series(np.where(RS == 0, 100, 100 - (100 / (1 + RS))), name="RSI", index=df.index)
    
    return RSI

# Indicador SMA
def SMA(df: pd.DataFrame, periodo: int = 9) -> pd.Series:
    
    """
    Promedio Móvil Simple
    """
    
    # Calcular
    MA = df["Close"].rolling(window=periodo, min_periods=periodo).mean()
    MA.name = "MA"
    
    return MA


# Ejemplo
if __name__ == "__main__":
    # Importar librerías adicionales
    import yfinance
    # Obtener datos
    df = yfinance.download("AMZN", start="2023-01-01", end="2024-01-01", interval="1d")
    # RSI
    rsi_calculo = RSI(df, periodo=14)
    print("RSI:")
    print(rsi_calculo)
    # Promedio Móvil
    ma_9 = SMA(df, periodo=9)
    print("SMA:")
    print(ma_9)
