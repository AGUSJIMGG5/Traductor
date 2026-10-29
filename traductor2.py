
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import random
import os


duration = 5
sample_rate = 44100

recognizer = sr.Recognizer()
translator = Translator()


palabras = {
    "facil": [
        "casa", "perro", "gato", "agua", "libro",
        "sol", "pan", "mesa", "rojo", "mano"
    ],
    "medio": [
        "ventana", "escuela", "amigo", "comida",
        "familia", "ciudad", "trabajo", "pelota"
    ],
    "dificil": [
        "mariposa", "computadora", "biblioteca",
        "desayuno", "conocimiento", "medioambiente"
    ]
}

print("=" * 40)
print("  TRADUCTOR RETO")
print("=" * 40)
print("Traduce las palabras del español al ingles.")
print("Di la traducción en voz alta.")
print("Gana puntos por cada respuesta correcta.")
print("Escribe 'salir' cuando quieras terminar.")

print("\nSelecciona la dificultad:")
print("1. facil")
print("2. medio")
print("3. dificil")

opcion = input("Elige 1, 2 o 3: ").strip()

while opcion not in ["1", "2", "3"]:
    opcion = input("Opción inválida. Elige 1, 2 o 3: ").strip()

if opcion == "1":
    dificultad = "facil"
    puntos_por_acierto = 1
elif opcion == "2":
    dificultad = "medio"
    puntos_por_acierto = 2
else:
    dificultad = "dificil"
    puntos_por_acierto = 3

puntos = 0
aciertos = 0
errores = 0
rondas = 0

racha = 0
racha_maxima = 0

total_rondas = min(5, len(palabras[dificultad]))

preguntas = random.sample(
    palabras[dificultad],
    total_rondas
)

print("\nComienza la partida!")
print("Escribe 'salir' antes de cada ronda para terminar.")

for palabra_espanol in preguntas:

    print("\n" + "-" * 35)
    print("🇪🇸 Traduce esta palabra:", palabra_espanol)

    respuesta = input(
        "Presiona ENTER para grabar o escribe 'salir': "
    ).strip().lower()

    if respuesta == "salir":
        break

    print("\nHabla ahora. Di la traducción en ingles...")

    try:
        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="int16"
        )

        sd.wait()

        wav.write("output.wav", sample_rate, recording)

        print("Reconociendo tu voz...")

        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)

        texto = recognizer.recognize_google(
            audio,
            language="en-US"
        ).strip().lower()

        print("Dijiste:", texto)

        traduccion = translator.translate(
            palabra_espanol,
            src="es",
            dest="en"
        ).text.strip().lower()

        print("Traduccion correcta:", traduccion)

        if texto == traduccion:
            print("correcto")
            puntos += puntos_por_acierto
            aciertos += 1

            racha += 1
            print("Racha actual:", racha)

            if racha > racha_maxima:
                racha_maxima = racha

            if racha % 3 == 0:
                puntos += 2
                print("3 aciertos seguidos")

        else:
            print("No es correcto.")
            errores += 1

            racha = 0
            print("Racha perdida")

        rondas += 1
        print("Puntos:", puntos)

    except sr.UnknownValueError:
        print("No entendí lo que dijiste.")
        print("Inténtalo de nuevo en la próxima ronda.")

    except sr.RequestError as e:
        print("Error en el reconocimiento de voz:", e)
        break

    except Exception as e:
        print("Ocurrió un error:", e)
        break

print("\n" + "=" * 40)
print("FIN")
print("=" * 40)
print("Dificultad:", dificultad)
print("rondas completadas:", rondas)
print("aciertos:", aciertos)
print("Errores:", errores)
print("puntuación final:", puntos)
print("racha actual:", racha)
print("racha máxima:", racha_maxima)

if rondas > 0:
    porcentaje = (aciertos / rondas) * 100
    print(f"Precisión: {porcentaje:.1f}%")

if aciertos == rondas and rondas > 0:
    print("¡Excelente! ¡Todas correctas!")
elif aciertos > 0:
    print("¡Buen trabajo! Sigue practicando.")
else:
    print("¡No te rindas! Puedes volver a intentarlo.")

if os.path.exists("output.wav"):
    os.remove("output.wav")

print("\nGracias por jugar")
