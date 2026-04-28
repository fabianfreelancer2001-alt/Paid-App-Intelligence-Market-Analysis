import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def cargar_reporte(nombre_archivo="reporte_tendencias.xlsx"):
    resumen_generos = pd.read_excel(nombre_archivo, sheet_name="Resumen_por_Genero")
    mejores_apps = pd.read_excel(nombre_archivo, sheet_name="Mejores_Apps")

    return resumen_generos, mejores_apps


def crear_carpeta_graficos(nombre_carpeta="graficos_reporte"):
    carpeta = Path(nombre_carpeta)
    carpeta.mkdir(exist_ok=True)

    return carpeta


def grafico_total_apps_por_genero(resumen_generos, carpeta):
    datos = resumen_generos.sort_values("Total_Apps", ascending=False).head(10)

    plt.figure(figsize=(10, 6))
    plt.barh(datos["prime_genre"], datos["Total_Apps"])
    plt.title("Top 10 géneros por cantidad de apps")
    plt.xlabel("Cantidad de apps")
    plt.ylabel("Género")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(carpeta / "01_total_apps_por_genero.png", dpi=300)
    plt.close()


def grafico_rating_promedio_por_genero(resumen_generos, carpeta):
    datos = resumen_generos.sort_values("Rating_Promedio", ascending=False).head(10)

    plt.figure(figsize=(10, 6))
    plt.barh(datos["prime_genre"], datos["Rating_Promedio"])
    plt.title("Top 10 géneros por rating promedio")
    plt.xlabel("Rating promedio")
    plt.ylabel("Género")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(carpeta / "02_rating_promedio_por_genero.png", dpi=300)
    plt.close()


def grafico_total_ratings_por_genero(resumen_generos, carpeta):
    datos = resumen_generos.sort_values("Total_Ratings", ascending=False).head(10)

    plt.figure(figsize=(10, 6))
    plt.barh(datos["prime_genre"], datos["Total_Ratings"])
    plt.title("Top 10 géneros por cantidad total de ratings")
    plt.xlabel("Total de ratings")
    plt.ylabel("Género")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(carpeta / "03_total_ratings_por_genero.png", dpi=300)
    plt.close()


def grafico_precio_promedio_por_genero(resumen_generos, carpeta):
    datos = resumen_generos.sort_values("Precio_Promedio", ascending=False).head(10)

    plt.figure(figsize=(10, 6))
    plt.barh(datos["prime_genre"], datos["Precio_Promedio"])
    plt.title("Top 10 géneros por precio promedio")
    plt.xlabel("Precio promedio")
    plt.ylabel("Género")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(carpeta / "04_precio_promedio_por_genero.png", dpi=300)
    plt.close()


def grafico_mejores_apps_por_score(mejores_apps, carpeta):
    datos = mejores_apps.sort_values("score_exito", ascending=False).head(15)

    plt.figure(figsize=(12, 7))
    plt.barh(datos["track_name"], datos["score_exito"])
    plt.title("Top 15 apps por score de éxito")
    plt.xlabel("Score de éxito")
    plt.ylabel("App")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(carpeta / "05_mejores_apps_por_score.png", dpi=300)
    plt.close()


def grafico_rating_vs_precio(mejores_apps, carpeta):
    plt.figure(figsize=(10, 6))
    plt.scatter(mejores_apps["price_num"], mejores_apps["user_rating"])
    plt.title("Relación entre precio y rating de usuario")
    plt.xlabel("Precio")
    plt.ylabel("Rating de usuario")
    plt.tight_layout()
    plt.savefig(carpeta / "06_rating_vs_precio.png", dpi=300)
    plt.close()


def generar_graficos_reporte(nombre_archivo="reporte_tendencias.xlsx"):
    resumen_generos, mejores_apps = cargar_reporte(nombre_archivo)
    carpeta = crear_carpeta_graficos()

    grafico_total_apps_por_genero(resumen_generos, carpeta)
    grafico_rating_promedio_por_genero(resumen_generos, carpeta)
    grafico_total_ratings_por_genero(resumen_generos, carpeta)
    grafico_precio_promedio_por_genero(resumen_generos, carpeta)
    grafico_mejores_apps_por_score(mejores_apps, carpeta)
    grafico_rating_vs_precio(mejores_apps, carpeta)

    print("Gráficos generados correctamente.")
    print(f"Carpeta creada: {carpeta}")


generar_graficos_reporte()