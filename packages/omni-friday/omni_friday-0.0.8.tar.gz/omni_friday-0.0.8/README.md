```

███████ ██████  ██ ██████   █████  ██    ██ 
██      ██   ██ ██ ██   ██ ██   ██  ██  ██  
█████   ██████  ██ ██   ██ ███████   ████   
██      ██   ██ ██ ██   ██ ██   ██    ██    
██      ██   ██ ██ ██████  ██   ██    ██    

```

# F.R.I.D.A.Y. - Adobe Commerce Project Tool

**FRIDAY** es una herramienta de consola desarrollada en Python que permite obtener y analizar información clave de proyectos basados en Adobe Commerce (Magento). 

## Características

- **Análisis de configuración**: Extrae y muestra configuraciones clave del proyecto.
- **Verificación de módulos**: Lista módulos habilitados/deshabilitados.
- **Revisión de versiones**: Obtiene la versión actual de Adobe Commerce y sus dependencias.
- **Logs y reportes**: Accede a logs importantes y genera reportes.

## Requisitos

- Python 3.8 o superior
- Acceso al servidor donde está alojado el proyecto Adobe Commerce
- Permisos para leer archivos de configuración y logs

### Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/usuario/friday.git
   cd friday
   ```
2. **Crear un entorno virtual (opcional pero recomendado):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Linux/macOS
   venv\Scripts\activate    # En Windows
   ```
3. **Instalar las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

Ejecuta el script principal `friday.py` desde la terminal. Puedes usar los siguientes comandos:

### Comandos Disponibles

```bash
python friday.py --help
```

| Comando                          | Descripción                                  |
|----------------------------------|----------------------------------------------|
| `--info`                         | Muestra información general del proyecto     |
| `--modules`                      | Lista módulos habilitados y deshabilitados   |
| `--version`                      | Muestra la versión de Adobe Commerce        |
| `--logs [n]`                     | Muestra las últimas `n` líneas del log       |
| `--config`                       | Muestra configuraciones clave del proyecto   |

### Ejemplos de uso

1. Obtener información general del proyecto:
   ```bash
   python friday.py --info
   ```
2. Listar módulos habilitados/deshabilitados:
   ```bash
   python friday.py --modules
   ```
3. Mostrar las últimas 50 líneas del log:
   ```bash
   python friday.py --logs 50
   ```

## Configuración

Si es necesario, puedes definir rutas o configuraciones en un archivo `config.json`:

```json
{
  "project_path": "/var/www/html/magento",
  "log_path": "/var/www/html/magento/var/log/system.log"
}
```

## Contribución

¡Las contribuciones son bienvenidas! Para colaborar:

1. Realiza un fork del repositorio.
2. Crea una rama con la nueva funcionalidad o corrección de errores.
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
3. Envía un Pull Request.

## Licencia

Este proyecto está licenciado bajo la licencia **MIT**. Consulta el archivo [LICENSE](LICENSE) para más detalles.

## Contacto

- **Autor**: Facundo Capua
- **Empresa**: OMNI.PRO
- **Correo**: capua.facundo@omni.pro
