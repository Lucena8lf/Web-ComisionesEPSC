# Web Comisiones EPSC

## Introducción

Este proyecto es mi Trabajo Fin de Grado (TFG) realizado para la Universidad de Córdoba en el curso 22/23.

## Idea principal y objetivos

Anteriormente la EPSC trabaja con su registro de comisiones de todos los profesores de manera local mediante una hoja de cálculo, lo que presenta dificultades de rendimiento, accesibilidad, etc. Lo que agrava un poco más este problema es que no solo debe mantener las comisiones de los profesores operativos, sino que este registro debe ser activo recogiendo a todos los miembros que han participado.

Debido a todo ello, este proyecto fue realizado con el objetivo de crear una aplicación web que permita la gestión de las comisiones de la EPSC. Esta aplicación web tendrá el fin de dar una solución más óptima a la forma de trabajar de la EPSC actualmente que es operar en local mediante una hoja de cálculo.

El foco principal de la aplicación será la gestión de comisiones, generación de
certificados y gestión de los miembros de estas comisiones que serán los miembros
de la EPSC. Es decir, una nueva comisión puede ser creada en cualquier momento
por el administrativo, al igual que un nuevo miembro. Cabe recalcar que aunque se
gestionan miembros como son los profesores, el público objetivo de la aplicación es
el administrativo designado a este sector por parte de la Universidad de Córdoba,
por lo que solo se tiene en cuenta un tipo de usuario.

Se plantea también la posibilidad de generar los certificados en dos tipos de
formatos y, además exportar los datos actuales que contenga la aplicación a formato
CSV.

## 🔨Funcionalidades del proyecto

La aplicación a desarrollar tendrá las siguientes características:

- Acceso al sistema mediante usuario y contraseña.
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

<!--
## Descarga e instalación del proyecto
    ### Variables de entorno
    ### Instalación de dependencias

## Ejecución con el servidor nativo de Flask

In process...
-->
