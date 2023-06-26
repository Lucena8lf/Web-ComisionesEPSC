# Aplicación web para la gestión de comisiones en la EPSC

## Introducción

Este proyecto es mi Trabajo Fin de Grado (TFG) realizado para la Universidad de Córdoba en el curso 22/23.

## Idea principal y objetivos

Anteriormente la Escuela Politécnica Superior de Córdoba (EPSC) trabaja con su registro de comisiones de todos los profesores de manera local mediante una hoja de cálculo, lo que presenta dificultades de rendimiento, accesibilidad, etc. Lo que agrava un poco más este problema es que no solo debe mantener las comisiones de los profesores operativos, sino que este registro debe ser activo recogiendo a todos los miembros que han participado.

Debido a todo ello, este proyecto fue realizado con el objetivo de crear una aplicación web que permita la gestión de las comisiones de la EPSC. Esta aplicación web tendrá el fin de dar una solución más óptima a la forma de trabajar de la EPSC actualmente que es operar en local mediante una hoja de cálculo.

El foco principal de la aplicación será la gestión de comisiones, generación de
certificados y gestión de los miembros de estas comisiones que serán los miembros
de la EPSC. Es decir, una nueva comisión puede ser creada en cualquier momento
por el administrativo, al igual que un nuevo miembro. Cabe recalcar que aunque se
gestionan miembros como son los profesores, el público objetivo de la aplicación es
el administrativo designado a este sector por parte de la Universidad de Córdoba,
por lo que solo se tiene en cuenta un tipo de usuario.

Se plantea también la posibilidad de generar los certificados en dos tipos de
formatos y, además exportar los datos que contenga la aplicación a formato
CSV.

## 🔨Funcionalidades del proyecto

La aplicación a desarrollar tendrá las siguientes características:

- Acceso al sistema mediante correo y contraseña.
- Gestión de las diferentes comisiones (dar de alta, editar y cerrarlas).
- Gestión de los miembros de las comisiones (dar de alta, modificar y dar de baja).
- Gestión de la composición de las comisiones.
- Generación de certificados de participación en comisiones.
- Creación y recuperación de copias de seguridad.
- Migración de la información del sistema anterior.
- La aplicación debe adaptarse al tamaño de la pantalla del dispositivo que se esté utilizando (diseño responsive).

## Tecnologías utilizadas

Se han utilizado las siguientes tecnologías para su desarrollo:

- Flask
- Jinja2
- SQLite3
- Bootstrap
- HTML5
- CSS3
- Javascript

## Instalación

### Descarga del proyecto

Para llevar a cabo la instalación primero se debe descargar el proyecto y para ello se clonará el repositorio:

```sh
git clone https://github.com/Lucena8lf/Web-ComisionesEPSC.git
```

Esto dejara una carpeta llamada ’Web-ComisionesEPSC’ que es la que contiene el proyecto.

### Variables de entorno

Para que la aplicación funcione deben ser creadas variables de entorno. Para ello será
necesario abrir una terminal, situarse dentro del directorio generado al clonar el repositorio
y ejecutar los siguientes comandos dependiendo del sistema operativo:

#### Linux/Mac

```sh
export FLASK_APP="entrypoint"
export FLASK_ENV="production"
export APP_SETTINGS_MODULE="config.local"
```

#### Windows

```sh
set FLASK_APP="entrypoint"
set FLASK_ENV="production"
set APP_SETTINGS_MODULE="config.local"
```

> Nota: si se está usando virtualenv es recomendable añadir esas variables
> al fichero que activa el entorno virtual. Dependiendo del sistema operativo
> éste puede ser “activate“, “activate.bat“, “activate.ps1“, etc.

### Instalación de dependencias

Por último, se instalarán las dependencias. Para ello el proyecto cuenta con el fichero
“requirements.txt“ que contiene la lista de dependencias requeridas por la aplicación. Para
instalarlas se deberá ejecutar:

```sh
pip install -r requirements.txt
```

### Ejecución de la aplicación

Una vez completados todos los pasos ya se tendría todo lo necesario para ejecutar la
aplicación. Por lo tanto para arrancar el proyecto se ejecutará el siguiente comando:

```sh
flask run
```

Tras ello ya se encontraría la aplicación ejecutada y se podrá acceder a ella a través de
un navegador web accediendo a la dirección http://localhost:5000/.
