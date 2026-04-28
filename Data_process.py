import pandas as pd
import numpy as np
import re


spreadsheet_id = "1w5oJHiU229tzKiveWV9IPGfRL8nnLjzNlsrhIh0L9ak"
gid = "1335454597"

url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={gid}"

df = pd.read_csv(url)

def analizar_tendencias_y_exito(df, nombre_archivo="reporte_tendencias.xlsx"):
    datos = df.copy()

    columnas_necesarias = [
        "track_name",
        "prime_genre",
        "user_rating",
        "rating_count_tot",
        "price",
        "cont_rating"
    ]

    for columna in columnas_necesarias:
        if columna not in datos.columns:
            raise ValueError(f"Falta la columna necesaria: {columna}")

    # Convertir columnas numéricas
    datos["user_rating"] = pd.to_numeric(datos["user_rating"], errors="coerce")
    datos["rating_count_tot"] = pd.to_numeric(datos["rating_count_tot"], errors="coerce")
    datos["price_num"] = pd.to_numeric(datos["price"], errors="coerce")

    # Revisar campos vacíos en cont_rating
    campos_vacios = datos["cont_rating"].isna() | (
        datos["cont_rating"].astype(str).str.strip() == ""
    )

    if campos_vacios.any():
        print(f"Hay {campos_vacios.sum()} campos vacíos en cont_rating.")
    else:
        print("No hay campos vacíos en cont_rating.")

    # Limpiar cont_rating: ejemplo "4+" -> 4, "12+" -> 12, "17+" -> 17
    datos["cont_rating_num"] = (
        datos["cont_rating"]
        .astype(str)
        .str.extract(r"(\d+)")[0]
    )

    datos["cont_rating_num"] = pd.to_numeric(
        datos["cont_rating_num"],
        errors="coerce"
    )

    # Eliminar filas incompletas en columnas críticas
    datos_limpios = datos.dropna(
        subset=[
            "track_name",
            "prime_genre",
            "user_rating",
            "rating_count_tot",
            "price_num"
        ]
    ).copy()

    # Factor de éxito
    datos_limpios["score_exito"] = (
        datos_limpios["user_rating"] * np.log1p(datos_limpios["rating_count_tot"])
    )

    # Resumen por género
    resumen_generos = datos_limpios.groupby("prime_genre").agg(
        Total_Apps=("track_name", "size"),
        Rating_Promedio=("user_rating", "mean"),
        Rating_Maximo=("user_rating", "max"),
        Total_Ratings=("rating_count_tot", "sum"),
        Promedio_Ratings=("rating_count_tot", "mean"),
        Precio_Promedio=("price_num", "mean"),
        Precio_Minimo=("price_num", "min"),
        Precio_Maximo=("price_num", "max")
    ).reset_index()

    resumen_generos = resumen_generos.sort_values(
        by=["Rating_Promedio", "Total_Ratings"],
        ascending=False
    )

    # Mejores apps por género
    mejores_apps = (
        datos_limpios
        .sort_values(
            by=["prime_genre", "score_exito"],
            ascending=[True, False]
        )
        .groupby("prime_genre")
        .head(5)
    )

    mejores_apps = mejores_apps[
        [
            "prime_genre",
            "track_name",
            "user_rating",
            "rating_count_tot",
            "price_num",
            "cont_rating",
            "cont_rating_num",
            "score_exito"
        ]
    ]

    # Guardar reporte en Excel local con varias hojas
    with pd.ExcelWriter(nombre_archivo, engine="openpyxl") as writer:
        datos_limpios.to_excel(writer, sheet_name="Datos_Limpios", index=False)
        resumen_generos.to_excel(writer, sheet_name="Resumen_por_Genero", index=False)
        mejores_apps.to_excel(writer, sheet_name="Mejores_Apps", index=False)

    print(f"Reporte creado correctamente: {nombre_archivo}")

    return datos_limpios, resumen_generos, mejores_apps

datos_limpios, resumen_generos, mejores_apps = analizar_tendencias_y_exito(df)

print("\nResumen por género:")
print(resumen_generos)

print("\nMejores apps por género:")
print(mejores_apps)