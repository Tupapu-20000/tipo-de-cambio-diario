import requests
import pandas as pd
from pathlib import Path
from datetime import date, datetime
import matplotlib.pyplot as plt

url = "https://api.frankfurter.dev/v2/rates"
parametros = {"base": "USD", "quotes": "EUR,BRL,GBP"}
RUTA_LOG = Path(__file__).parent / "bitacora.txt"
print(RUTA_LOG)
ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
try:
    respuesta = requests.get(url, params=parametros, timeout=10)
    respuesta.raise_for_status()
    print(respuesta.status_code)   
    print(respuesta.url)           
    datos = respuesta.json()
    tabla = pd.DataFrame(datos)
    print(tabla)       
    print(len(datos))
    print(datos)
    hoy = date.today()
    tabla = tabla[["date", "quote", "rate"]]
    tabla = tabla.rename(columns={"date": "fecha", "quote": "moneda", "rate" : "valor"})
    RUTA = Path(__file__).parent / "tasas.csv"
    print(RUTA)
    if RUTA.exists():
        anterior = pd.read_csv(RUTA)
        tabla = pd.concat([anterior, tabla], ignore_index=True)

    tabla = tabla.drop_duplicates(subset=["fecha", "moneda"], keep="last")
    tabla =  tabla.sort_values(["fecha", "moneda"], ignore_index=True)
    tabla.to_csv(RUTA, index=False)
    leida = pd.read_csv(RUTA)
    print(leida)
    print(len(leida))
    leida["fecha"] = pd.to_datetime(leida["fecha"])
    print(tabla["fecha"].min())
    print(tabla["fecha"].max())
    monedas = ["EUR","BRL","GBP"]
    fig, ejes = plt.subplots(len(monedas), 1, sharex=True, figsize=(8, 9))
    for i in range(len(monedas)):
        moneda = monedas[i]
        sub = leida[leida["moneda"] == moneda] 
        ejes[i].plot(sub["fecha"], sub["valor"], marker="o")
        ejes[i].set_title(f"USD a {moneda}")
    fig.autofmt_xdate()
    fig.savefig(Path(__file__).parent / "grafico_tasas.png")
    plt.close(fig)
    print(f"Hoy Segun tu Pc: {hoy}")
    print(leida["moneda"].value_counts())
    resultado = f"{ahora} OK filas en el CSV: {len(leida)}"
except Exception as error:
    resultado = f"{ahora} ERROR {error}"

with open(RUTA_LOG, "a", encoding="utf-8") as archivo:
    archivo.write(resultado + "\n")
print(resultado)
