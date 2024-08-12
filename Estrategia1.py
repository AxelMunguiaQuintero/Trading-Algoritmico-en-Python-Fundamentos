# Librerías Estándar
import pandas as pd
import numpy as np
import mplfinance as mpf
# Librerías Propias
from IndicadoresTecnicos import RSI, SMA


# Clase Estrategia
class Estrategia1:
    
    """ 
    Estrategia 1: Estrategia de Cruce de Promedios Móviles y RSI: 
    
        Descripción:
            
            Esta estrategia combina cruces de promedios móviles simples (SMA) con el Índice de Fuerza Relativa (RSI) para 
            generar señales de compra y venta. La estrategia busca identificar cambios en la tendencia y validar estos
            cambios con condiciones de sobrecompra y sobreventa.
    
    Estrategia Para:
        
        - Acciones
        - Divisas
        - Materias Primas
        - Criptomonedas
        
    Frecuencias (Ventanas de Tiempo):
        
        - 1 minuto
        - 1 hora
        - 1 día
        
    Periodo de Retención:
        
        - Corto Plazo (Variable)
        - Mediano Plazo (Variable)
        - Largo Plazo (Variable)
    
    Análisis Usado: 
        
        - Análisis Técnico:
            * Promedios Móviles
            * RSI
    
    Descripción Detallada de la Estrategia:    
        
        La estrategia se basa en dos componentes principales: Cruces de Promedios Móviles y el RSI.
       
        1. **Cruces de Promedios Móviles Simples (SMA):**
           - Se utilizan dos SMAs, uno de corto plazo (por ejemplo, 9 periodos) y otro de largo plazo (por ejemplo, 21 periodos).
           - Una señal de compra se genera cuando el SMA de corto plazo cruza por encima del SMA de largo plazo.
           - Una señal de venta se genera cuando el SMA de corto plazo cruza por debajo del SMA de largo plazo.
           
        2. **Índice de Fuerza Relativa (RSI):**
           - El RSI se calcula usando un periodo de 14 días.
           - Se definen niveles de sobrecompra (RSI > 50) y sobreventa (RSI < 50).
           
        **Señales de Compra y Venta:**
           - Señal de Compra: Se genera cuando el SMA de corto plazo cruza por encima del SMA de largo plazo y el RSI está en 
             nivel de sobreventa (RSI < 50).
           - Señal de Venta: Se genera cuando el SMA de corto plazo cruza por debajo del SMA de largo plazo y el RSI está en
             nivel de sobrecompra (RSI > 50).
                        
        Descripción de Stop Loss y Take Profit:
            
            Take Profit:
                
                - El objetivo de beneficios se mantiene hasta que se genere una señal contraria.
               
            Stop Loss:
               
               - El stop loss se mantiene hasta que se genere una señal contraria.
           
        Co-Integración (Si se usan múltiples Indicadores):
           
            Señales:
               
                - Las señales se confirman cuando tanto el cruce de SMA como las condiciones de RSI coinciden en 
                  indicar una entrada.
               
           Salida del Trade:
               
                - La salida se realiza cuando se genera una señal contraria.
               
    Supuestos Generales:
        
        - Los costos de transacción y el deslizamiento no se consideran en esta estrategia.
        
    Notas:
        
        - Esta estrategia maximiza la utilidad en tendencias definidas. 
    """
    
    __version__ = 1.0
    
    # __init__
    def __init__(self, df: pd.DataFrame) -> None:
        
        """
        Constructor.
        
        Parámetros
        ----------
        param : pd.DataFrame : df : Datos históricos del activo.
                
        
        Salida
        -------
        return: NoneType: None.
        """
        
        # Atributos
        self.df = df
        self.periodo_rsi = 14
        self.periodo_ma_rapido = 9
        self.periodo_ma_lento = 21
        self.sobrecompra_sobreventa = 50
        
    
    # __repr__
    def __repr__(self) -> str:
        return self.__class__.__name__ + ".class"
    
    
    # Backtest
    def backtest(self):
        
        """
        Método que obtiene el rendimiento generado por la estrategia a lo largo del tiempo
        

        Salida
        -------
        return: pd.Series: Rendimientos de la estrategia a lo largo del tiempo.
        """
        
        # Calcular
        calculo_est = self.estrategia_calculo.copy()
        # Rellenar señales hacia adelante para conocer la posición actual en todo momento
        calculo_est["posicion_mercado"] = calculo_est["Señales"].ffill()
        # Calcular rendimiento
        calculo_est["Rendimientos"] = self.df["Close"].pct_change()
        rendimiento = (1 + calculo_est["posicion_mercado"].shift(periods=1) * calculo_est["Rendimientos"]).cumprod()
        
        return rendimiento
    
    
    # Calcular
    def calcular(self):
        
        """
        Este método calculará la estrategia
        
        Salida
        -------
        return: dict: Devuelve un diccionario si se generó una señal en la última vela, o False si no se generó nada.
        """
        
        # Calcular indicadores
        datos = pd.DataFrame(index=self.df.index)
        datos[f"SMA_{self.periodo_ma_rapido}"] = SMA(self.df, periodo=self.periodo_ma_rapido)
        datos[f"SMA_{self.periodo_ma_lento}"] = SMA(self.df, periodo=self.periodo_ma_lento)
        datos["RSI"] = RSI(self.df, periodo=self.periodo_rsi)
        
        # Generar cruces
        datos["Cruces_MAs"] = np.where(datos[f"SMA_{self.periodo_ma_rapido}"] > datos[f"SMA_{self.periodo_ma_lento}"], 1, -1)
        # Detectar niveles sobrecompra y sobreventa
        datos["RSI_Señal"] = np.where(datos["RSI"] > self.sobrecompra_sobreventa, -1,
                                      np.where(datos["RSI"] < self.sobrecompra_sobreventa, 1, np.nan))
        
        # Detectar señales
        datos["Señales"] = np.nan
        datos.loc[(datos["Cruces_MAs"] == 1) & (datos["RSI_Señal"] == 1), "Señales"] = 1
        datos.loc[(datos["Cruces_MAs"] == -1) & (datos["RSI_Señal"] == -1), "Señales"] = -1
        
        # Guardar
        self.estrategia_calculo = datos
        
        # Revisar si hay una señal en la última vela
        if datos["Señales"].iloc[-1] == 1:
            valor = {"tendencia": "alcista"}
        elif datos["Señales"].iloc[-1] == -1:
            valor = {"tendencia": "bajista"}
        else:
            valor = False

        return valor
    
    
    # Optimizar
    def optimizar(self, combinaciones: list):
        
        """
        Optimiza la estrategia encontrando los mejores parámetros.
        
        Parámetros
        ----------
        param : list : combinaciones : Conjunto de parámetros que se probarán en la estrategia.
                
        Salida
        -------
        return: pd.DataFrame: Rendimiento para cada estrategia probada.
        """
        
        # Optimizar
        
        # Guardar los parámetros originales
        params_originales = [self.periodo_ma_rapido, self.periodo_ma_lento, self.periodo_rsi]
        
        # Almacenar resultados
        resultados = []
        # Iterar en cada combinación
        for parametro in combinaciones:
            # Modificar parámetros de la estrategia
            self.periodo_ma_rapido = parametro[0]
            self.periodo_ma_lento = parametro[1]
            self.periodo_rsi = parametro[2]
            # Calcular estrategia
            _ = self.calcular()
            # Backtest
            retorno_final = self.backtest().iloc[-1]
            # Almacenar los resultados
            resultados.append([self.periodo_ma_rapido, self.periodo_ma_lento, self.periodo_rsi, retorno_final])
            
        # Dar estructura y ordenar
        resultados = pd.DataFrame(data=resultados, columns=["MA Rap Param", "MA Len Param", "RSI Param", "Retorno"])
        resultados.sort_values(by="Retorno", ascending=False, inplace=True)
        
        # Devolver los parámetros originales
        self.periodo_ma_rapido = params_originales[0]
        self.periodo_ma_lento = params_originales[1]
        self.periodo_rsi = params_originales[2]
        # Devolver calculos con parámetros originales
        self.calcular()
        
        return resultados
    
    
    # Plot
    def plot(self):
        
        """
        Este método realiza el gráfico de nuestros datos
        
        
        Salida
        -------
        return: NoneType: None
        """
        
        # Graficar
        rsi_data = self.estrategia_calculo["RSI"]
        nivel_sobrecompra = self.sobrecompra_sobreventa
        nivel_sobreventa = self.sobrecompra_sobreventa
        
        # Crear plot adicional para el RSI
        rsi_plot = [mpf.make_addplot(rsi_data, panel=2, color="blue", ylabel="RSI")]
        
        # Añadir las líneas divisorias 
        rsi_plot.append(mpf.make_addplot([nivel_sobrecompra] * len(rsi_data), panel=2, color="black", linestyle="dashed"))
        
        # Añadir las áreas coloreadas
        rsi_plot.append(mpf.make_addplot(rsi_data, panel=2, color="blue",
                                         fill_between=dict(y1=nivel_sobrecompra, y2=rsi_data, where=rsi_data >= nivel_sobrecompra, alpha=0.5,
                                                          color="green")))
        rsi_plot.append(mpf.make_addplot(rsi_data, panel=2, color="blue",
                                         fill_between=dict(y1=nivel_sobreventa, y2=rsi_data, where=rsi_data < nivel_sobreventa, alpha=0.5,
                                                          color="red")))
        
        mpf.plot(self.df, type="candle", style="yahoo", title="Gráfico de Velas", ylabel="Precio", volume=True, figsize=(20,10),
                 figscale=3.0, addplot=rsi_plot, tight_layout=True,
                 mav=(int(self.periodo_ma_rapido), int(self.periodo_ma_lento)), warn_too_much_data=self.df.shape[0],
                 savefig="estrategia1.png")
    
    
# Ejemplo
if __name__ == "__main__":
    # Importar librerías adicionales
    import yfinance as yf
    from itertools import product
    # Obtener datos
    df = yf.download("AMZN", start="2014-01-01", end="2024-01-01", interval="1d")
    # Generar una instancia de nuestra clase
    est1 = Estrategia1(df)
    # Calcular Estrategia
    calculo_señal = est1.calcular()
    print(calculo_señal)
    print(est1.estrategia_calculo)    
    print(est1.estrategia_calculo["Señales"].dropna())
    # Backtest
    backtest = est1.backtest()
    print(backtest)    
    # Optimizar
    periodos_rapidos = np.arange(5, 14)
    periodos_lentos = np.arange(14, 51)
    rsi_periodos = np.arange(9, 22)
    combinaciones_parametros = list(product(periodos_rapidos, periodos_lentos, rsi_periodos))
    print("Total de Estrategias por Correr son:", len(combinaciones_parametros))
    resultados = est1.optimizar(combinaciones_parametros)
    print(resultados.head(10))

    # Tomar mejores parámetros
    ma_rapida = resultados["MA Rap Param"].iloc[0]
    ma_lenta = resultados["MA Len Param"].iloc[0]
    rsi_valor = resultados["RSI Param"].iloc[0]
    # Definir nuevamente estrategia 
    est1 = Estrategia1(df)
    est1.periodo_ma_rapido = ma_rapida
    est1.periodo_ma_lento = ma_lenta
    est1.periodo_rsi = rsi_valor
    # Calcular
    calculo_señal = est1.calcular()
    # Backtest
    print("Rendimiento Final:", est1.backtest().iloc[-1])
    # Graficar
    est1.plot()
    
    
    
    
    
    
    
    
    
    
    
    
    
