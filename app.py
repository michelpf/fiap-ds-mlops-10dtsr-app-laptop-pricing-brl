import streamlit as st
import requests
import json
import locale


def get_prediction(payload):
    endpoint = st.secrets["API-ENDPOINT"]
    headers = {
        "Content-Type": "application/json",
        "x-api-key": st.secrets["API-KEY"]
    }

    response = requests.post(endpoint, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        result = response.json()

        """
        ### Preço estimado para compra

        De acordo com os dados fornecidos, seu laptop poderá ser comprado pelo seguinte valor abaixo.
        """

        locale.setlocale(locale.LC_ALL, 'pt_BR')

        predicted_value_formatted = locale.format_string("%d", result["prediction"], grouping=True)

        st.markdown("Valor para compra: **"+ predicted_value_formatted + " BRL (Brazilian Reais)**")
    else:
        st.markdown("Erro ao obter a previsão. Por favor, tente novamente mais tarde ou revise seus dados.")



"""
# Machine Learning Engineering

## Predição de Preço de Laptop em BRL

Este modelo é capaz de prever o preço de um laptop dada algumas características.

A aplicação é para ser utilizada em uma loja eletrônica que avalia laptops usados como parte do pagamento de um novo, 
por tal razão a avaliação não é tão exaustiva e se baseia em caracteríticas comuns, como marca, processador, memória etc.
sem nenhuma outra avaliação visual, pelo menos por enquanto.

### Características do laptop
"""

brand_option = st.selectbox(
    "Qual é a marca?",
    ("Asus", "Dell", "HP", "Lenovo", "Outro"))

touchscreen = st.radio(
    "Possui touchscreen (tela sensível ao toque)?",
    ["Não", "Sim"])

processor_brand = st.radio(
    "Qual a marca do processor?",
    ["AMD", "Intel", "M1"])

warranty = st.number_input("Quantos anos de garantia?", step=1, placeholder="Coloque 0 se não houver garantia.")

brand_option = st.selectbox(
    "Qual é o nome do processador?",
    ("Core i3", "Core i5 ", "Core i7", "Ryzen 5", "Ryzen 7", "Outro"),)

os_bit = st.radio(
    "Qual a arquitetura do sistema operacional?",
    ["32 bits", "64 bits"])

os_brand = st.radio(
    "Qual o sistema operacional?",
    ["Windows", "Outro"])

weight = st.radio(
    "Qual o peso estimado?",
    ["Casual", "Gaming", "Thinlight"],
    captions = ["Peso padrão", "Pesado", "Leve"])

ram_type = st.radio(
    "Qual o tipo da memória RAM?",
    ["DDR4", "Outro"])

ram_size = st.number_input("Qual é o tamanho da memória RAM em GB?", step=4)
graphic_card_option = st.number_input("Qual é o tamanho da memória gráfica (vídeo) em GB?", step=4)
hdd_size = st.number_input("Qual é o tamanho do armazenamento em disco estado sólido (HDD) em GB?", step=512, placeholder="Coloque 0 se houver apenas SSD.")
ssd_size = st.number_input("Qual é o tamanho do armazenamento em disco estado sólido (SSD) em GB?", step=128, placeholder="Coloque 0 se houver apenas HDD.")

if brand_option == "Outro":
    brand_option = "other"

if os_brand == "Outro":
    os_brand = "other"

if ram_type == "Outro":
    ram_type = "other"

if touchscreen == "Sim":
    touchscreen = "1"
else:
    touchscreen = "0"

os_bit = os_bit.replace(" bits", "")

payload = { "data" : {
        "brand": brand_option.lower(),
        "processor_brand": processor_brand.lower(),
        "processor_name": brand_option.lower(),
        "os": os_brand.lower(),
        "weight": weight.lower(),
        "warranty": warranty,
        "touchscreen": touchscreen,
        "ram_gb": ram_size,
        "hdd": hdd_size,
        "ssd": ssd_size,
        "graphic_card": graphic_card_option,
        "ram_type": ram_type.lower(),
        "os_bit": os_bit
    }
}

if st.button("Estimar Preço"):
    with st.spinner("Calculando..."):
        get_prediction(payload)