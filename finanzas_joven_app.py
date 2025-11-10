#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 10:30:20 2025

@author: anandaramirez
"""

import streamlit as st
from openai import OpenAI
import os
import re

# ----------------------------------------------------------
# CONFIGURACIÓN DEL CLIENTE
# ----------------------------------------------------------

# Asegúrate de tener tu clave de API guardada como variable de entorno


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ----------------------------------------------------------
# FUNCIONES FINANCIERAS
# ----------------------------------------------------------

def interes_simple(capital, tasa, tiempo):
    """Calcula el interés simple"""
    return capital * (tasa / 100) * tiempo

def interes_compuesto(capital, tasa, tiempo):
    """Calcula el monto final con interés compuesto"""
    return capital * (1 + tasa / 100) ** tiempo

def presupuesto_mensual(ingreso, gastos):
    """Calcula cuánto puedes ahorrar en un mes"""
    ahorro = ingreso - gastos
    if ahorro < 0:
        return f"⚠️ Estás gastando más de lo que ganas. Te faltan ${abs(ahorro):,.2f}."
    return f"💪 Podrías ahorrar aproximadamente ${ahorro:,.2f} este mes."

# ----------------------------------------------------------
# DETECTOR DE CÁLCULOS AUTOMÁTICOS
# ----------------------------------------------------------

def detectar_calculo(pregunta):
    """
    Detecta si la pregunta pide un cálculo financiero
    y ejecuta la función correspondiente.
    """

    numeros = [float(x) for x in re.findall(r"\d+\.?\d*", pregunta)]

    if "interés simple" in pregunta.lower() and len(numeros) >= 3:
        capital, tasa, tiempo = numeros[:3]
        resultado = interes_simple(capital, tasa, tiempo)
        return f"💰 El interés simple sería de ${resultado:,.2f} después de {tiempo} años."

    elif "interés compuesto" in pregunta.lower() and len(numeros) >= 3:
        capital, tasa, tiempo = numeros[:3]
        resultado = interes_compuesto(capital, tasa, tiempo)
        return f"📈 El monto final con interés compuesto sería de ${resultado:,.2f} después de {tiempo} años."

    elif "presupuesto" in pregunta.lower() and len(numeros) >= 2:
        ingreso, gastos = numeros[:2]
        return presupuesto_mensual(ingreso, gastos)

    return None

# ----------------------------------------------------------
# FUNCIÓN DE RESPUESTA CON GPT
# ----------------------------------------------------------

def responder(pregunta):
    """Si no hay cálculo automático, responde con IA (GPT)."""
    respuesta_calculo = detectar_calculo(pregunta)
    if respuesta_calculo:
        return respuesta_calculo

    respuesta = client.chat.completions.create(
        model="gpt-4o-mini",  # o "gpt-5" si tienes acceso
        messages=[
            {
                "role": "system",
                "content": (
                    "Eres un asesor financiero juvenil, amable y motivador. "
                    "Respondes con lenguaje claro, ejemplos sencillos y consejos responsables. "
                    "Evita jerga técnica y promueve hábitos financieros saludables."
                ),
            },
            {"role": "user", "content": pregunta},
        ],
    )
    return respuesta.choices[0].message.content

# ----------------------------------------------------------
# INTERFAZ WEB CON STREAMLIT
# ----------------------------------------------------------

st.set_page_config(page_title="Finatic IA", page_icon="💸")

st.title("💸 Finatic")
st.write("Fintor tu asesor virtual para aprender a manejar el dinero de forma fácil y divertida.")
st.markdown("---")

pregunta = st.text_input("💬 Escribe tu pregunta o cálculo financiero:")

if pregunta:
    with st.spinner("Pensando... 💭"):
        respuesta = responder(pregunta)
    st.success("✅ Resultado:")
    st.write(respuesta)

# ----------------------------------------------------------
# SECCIÓN DE CÁLCULOS DIRECTOS
# ----------------------------------------------------------

st.markdown("---")
st.header("🧮 Calculadora financiera rápida")

opcion = st.selectbox(
    "Selecciona el tipo de cálculo:",
    ["Interés Simple", "Interés Compuesto", "Presupuesto Mensual"]
)

if opcion == "Interés Simple":
    capital = st.number_input("💵 Capital inicial:", min_value=0.0, step=100.0)
    tasa = st.number_input("📊 Tasa de interés (% anual):", min_value=0.0, step=0.1)
    tiempo = st.number_input("📆 Tiempo (años):", min_value=0.0, step=0.5)
    if st.button("Calcular Interés Simple"):
        resultado = interes_simple(capital, tasa, tiempo)
        st.success(f"El interés simple sería de ${resultado:,.2f} después de {tiempo} años.")

elif opcion == "Interés Compuesto":
    capital = st.number_input("💵 Capital inicial:", min_value=0.0, step=100.0)
    tasa = st.number_input("📊 Tasa de interés (% anual):", min_value=0.0, step=0.1)
    tiempo = st.number_input("📆 Tiempo (años):", min_value=0.0, step=0.5)
    if st.button("Calcular Interés Compuesto"):
        resultado = interes_compuesto(capital, tasa, tiempo)
        st.success(f"El monto final sería de ${resultado:,.2f} después de {tiempo} años.")

elif opcion == "Presupuesto Mensual":
    ingreso = st.number_input("💰 Ingreso mensual:", min_value=0.0, step=100.0)
    gastos = st.number_input("💸 Gastos mensuales:", min_value=0.0, step=100.0)
    if st.button("Calcular Presupuesto"):
        st.success(presupuesto_mensual(ingreso, gastos))

st.markdown("---")
st.caption("💡 Consejo: ahorrar incluso pequeñas cantidades cada mes puede tener un gran impacto a largo plazo.")