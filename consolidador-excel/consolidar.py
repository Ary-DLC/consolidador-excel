from pathlib import Path
import pandas as pd

BASE = Path(__file__).parent
ENTRADA = BASE / "entrada"
SALIDA = BASE / "salida"
SALIDA.mkdir(exist_ok=True)

# 1. Leer todos los Excel para luego  agregar la columna de Sucursal
tablas = []
for archivo in ENTRADA.glob("*.xlsx"):
    df = pd.read_excel(archivo)
    df["Sucursal"] = archivo.stem.replace("ventas_", "")
    tablas.append(df)

datos = pd.concat(tablas, ignore_index=True)
filas_originales = len(datos)

# 2. Limpiar quitando duplicados y filas sin cantidad
datos = datos.drop_duplicates()
duplicados = filas_originales - len(datos)

vacias = datos["Cantidad"].isna().sum()
datos = datos.dropna(subset=["Cantidad"])

# 3. Calcular totales
datos["Fecha"] = pd.to_datetime(datos["Fecha"])
datos["Mes"] = datos["Fecha"].dt.strftime("%Y-%m")
datos["Total"] = datos["Cantidad"] * datos["Precio"]

por_sucursal = datos.groupby("Sucursal")["Total"].sum().sort_values(ascending=False).reset_index()
por_mes = datos.groupby("Mes")["Total"].sum().reset_index()
por_producto = datos.groupby("Producto")["Cantidad"].sum().sort_values(ascending=False).reset_index()

# 4. Guardar el reporte con varias hojas
reporte = SALIDA / "reporte_consolidado.xlsx"
with pd.ExcelWriter(reporte) as writer:
    datos.sort_values("Fecha").to_excel(writer, sheet_name="Datos limpios", index=False)
    por_sucursal.to_excel(writer, sheet_name="Por sucursal", index=False)
    por_mes.to_excel(writer, sheet_name="Por mes", index=False)
    por_producto.to_excel(writer, sheet_name="Por producto", index=False)

# 5. Resumen en la terminal
print(f"Archivos leídos: {len(tablas)}")
print(f"Filas originales: {filas_originales}")
print(f"Duplicados eliminados: {duplicados}")
print(f"Filas sin cantidad eliminadas: {vacias}")
print(f"Ventas totales: ${datos['Total'].sum():,.2f}")
print(f"Reporte guardado en: {reporte}")