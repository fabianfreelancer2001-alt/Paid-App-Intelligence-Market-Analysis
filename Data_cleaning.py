import pandas as pd
import re

spreadsheet_id = "1-PQtPtSU-Vw0cvm5NVhCD7PAezcTkd3VZtBxqv3VuwU"
gid = "1329089383"

url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={gid}"

df = pd.read_csv(url)



# Convertir price a número
df["price_num"] = pd.to_numeric(df["price"], errors="coerce")

# Filtrar solo apps gratis
free = df["price_num"] == 0

apps_gratis = df[free]

def free_apps(df):
    # Convertir price a número
    df["price_num"] = pd.to_numeric(df["price"], errors="coerce")

    # Filtrar solo apps gratis
    apps_gratis = df[df["price_num"] == 0]

    # Contar apps gratis
    cantidad_gratis = apps_gratis["track_name"].count()

    print("Primeros precios:")
    print(df["price"].head(20))

    print("\nTipo de dato de price:")
    print(df["price"].dtype)

    print("\nValores únicos de price:")
    print(df["price"].unique()[:20])

    print(f"\nTotal de apps gratis: {cantidad_gratis}")

    resumen_gratis = apps_gratis.groupby("price_num").agg(
        Total=("track_name", "size"),
        Apps=("track_name", lambda nombres: ", ".join(nombres.astype(str)))
    ).reset_index()

    print("\nResumen de apps gratis:")
    print(resumen_gratis)

    return resumen_gratis


resumen = free_apps(df)

def clasificar_nombre_app(nombre):
    texto = str(nombre).strip()

    if texto == "" or texto.lower() == "nan":
        return "vacio"

    # Detecta si el nombre es solo números, espacios o símbolos básicos
    if re.fullmatch(r"[0-9\s\.\-_/]+", texto):
        return "formato_numerico"

    # Detectar alfabetos/escrituras no latinas
    patrones_otro_idioma = {
        "coreano": r"[\uAC00-\uD7AF]",
        "japones": r"[\u3040-\u30FF]",
        "chino": r"[\u4E00-\u9FFF]",
        "arabe": r"[\u0600-\u06FF]",
        "cirilico": r"[\u0400-\u04FF]",
        "hebreo": r"[\u0590-\u05FF]",
        "tailandes": r"[\u0E00-\u0E7F]",
    }

    for idioma, patron in patrones_otro_idioma.items():
        if re.search(patron, texto):
            return idioma

    return "posible_ingles"


df["Clasificacion_Idioma"] = df["track_name"].apply(clasificar_nombre_app)

apps_otro_idioma = df[
    df["Clasificacion_Idioma"].isin([
        "coreano",
        "japones",
        "chino",
        "arabe",
        "cirilico",
        "hebreo",
        "tailandes",
        "formato_numerico"
    ])
].copy()

apps_otro_idioma.insert(0, "Numero", range(1, len(apps_otro_idioma) + 1))

print(f"Total de apps que no parecen estar en inglés: {len(apps_otro_idioma)}")

print(apps_otro_idioma[["Numero", "track_name", "Clasificacion_Idioma"]])

def eliminar_apps_no_deseadas(df):
    datos = df.copy()

    # Convertir precio a número
    datos["price_num"] = pd.to_numeric(datos["price"], errors="coerce")

    # Clasificar idioma del nombre de la app
    datos["Clasificacion_Idioma"] = datos["track_name"].apply(clasificar_nombre_app)

    # Condición 1: apps gratis
    apps_gratis = datos["price_num"] == 0

    # Condición 2: apps que no parecen estar en inglés
    apps_no_ingles = datos["Clasificacion_Idioma"].isin([
        "coreano",
        "japones",
        "chino",
        "arabe",
        "cirilico",
        "hebreo",
        "tailandes",
        "formato_numerico"
    ])

    # Filas que se van a eliminar
    eliminar = apps_gratis | apps_no_ingles

    # Datos eliminados
    datos_eliminados = datos[eliminar]

    # Datos limpios
    datos_limpios = datos[~eliminar]

    print(f"Filas originales: {len(datos)}")
    print(f"Apps eliminadas: {len(datos_eliminados)}")
    print(f"Apps limpias restantes: {len(datos_limpios)}")

    return datos_limpios, datos_eliminados

datos_limpios, datos_eliminados = eliminar_apps_no_deseadas(df)

datos_limpios.to_csv("apps_limpias.csv", index=False)
datos_eliminados.to_csv("apps_eliminadas.csv", index=False)

print("Se creó el archivo apps_limpias.csv")
print("Se creó el archivo apps_eliminadas.csv")