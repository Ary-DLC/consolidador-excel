import random
from pathlib import Path
import pandas as pd

CARPETA = Path(__file__).parent / "entrada"
CARPETA.mkdir(exist_ok=True)

sucursales = ["Centro", "Jalapa", "Palenque", "Villahermosa", "Tacotalpa"]
productos = ["Laptop", "Mouse", "Teclado", "Monitor", "Audifonos"]

for sucursal in sucursales:
    filas = []
    for _ in range(40):
        filas.append({
            "Fecha": f"2026-{random.randint(1, 9):02d}-{random.randint(1, 28):02d}",
            "Producto": random.choice(productos),
            "Cantidad": random.randint(1, 10),
            "Precio": random.choice([250, 400, 900, 3500, 12000]),
        })
    df = pd.DataFrame(filas)
    # Errores a propósito: filas duplicadas y celdas vacías
    df = pd.concat([df, df.sample(3)])
    df.loc[df.sample(2).index, "Cantidad"] = None
    df.to_excel(CARPETA / f"ventas_{sucursal}.xlsx", index=False)

print("Listo: archivos creados en", CARPETA)