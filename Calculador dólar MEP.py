import requests
import json
import pandas
import getpass

def pedir_token(data):
    url_token = "https://api.invertironline.com/token"
    respuesta = requests.post(url = url_token, data = data)
    return json.loads(respuesta.text)

# Ingresa por consola el nombre y clave del broker (en este caso IOL)
usuario = input("Ingresar el usuario: ")
password = getpass.getpass("Ingresar la clave: ")
data = {
    "username": usuario,
    "password": password,
    "grant_type": "password"
}

# Llamo a la funcion que hace login y devuelve el token
datos_token = pedir_token(data)
access_token = datos_token['access_token']      # Token para acceder
refresh_token = datos_token['refresh_token']    # Token para refrescar, no lo uso en este script

# Lista de ticker de bonos o acciones que quiero consultar
tickers = ['A2E7','AA25','AA37','AC17','AO20','AY24', 'AF20','DICA','DICY','PARA','PARY']

# Defino listas que voy a utilizar para la salida en formato .csv
listaNombre = []
listaValor = []
preplanilla = {}

# Para cada ticker de la lista pido su cotizacion
for simbolo in tickers:
    # Consulto el ticker en pesos
    url_pedido = "https://api.invertironline.com/api/v2/bCBA/Titulos/" + simbolo + "/Cotizacion"
    datos = requests.get(url = url_pedido, headers = {
        "Authorization": "Bearer " + access_token
    }).json()
    
    # Me da las 5 puntas, solo voy a consultar la primera
    puntas = datos['puntas']
    if len(puntas) == 0:
        continue
    precioP = puntas[0]['precioVenta']  # Precio de venta en pesos
    
    # Consulto el tiker en dolares + D
    url_pedido = "https://api.invertironline.com/api/v2/bCBA/Titulos/" + simbolo + "D/Cotizacion"
    datos = requests.get(url = url_pedido, headers = {
        "Authorization":"Bearer " + access_token
    }).json()
    puntas = datos['puntas']
    if len(puntas) == 0:
        continue
    precioD = puntas[0]['precioCompra']  # Precio de compra en dolares
    
    # Nunca dividir por cero!
    if precioD > 0:
        dolar = round(float(precioP / precioD), 2)   # Redondeo y muestro la cotizacion con dos decimales
    else:
        dolar = 0
    print(str(simbolo + 'D') + ': ' + str(dolar))
    listaNombre.append(simbolo + 'D')
    listaValor.append(dolar)
    
# Armo la estructura que uso para el csv
#preplanilla["TICKER"] = listaNombre
#preplanilla["VALOR"] = listaValor
#planilla = pandas.DataFrame(preplanilla, columns=["TICKER","VALOR"])
#planilla.to_csv('arbitrajes.csv', index=False)