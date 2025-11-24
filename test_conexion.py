from modelo.conexionbd import ConexionBD

def test_conexion():
    bd = ConexionBD()
    if bd.establecerConexionBD():
        print("✅ Conexión exitosa - BD funciona correctamente")
        bd.cerrarConexionBD()
    else:
        print("❌ Falló la conexión - Revisa credenciales")

if __name__ == "__main__":
    test_conexion()