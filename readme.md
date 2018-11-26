# Script para enviar elementos de una fuente RSS por correo

Note: this readme file is in spanish. If you don't know our language, consider using a translation tool or learning it. It's one of the most spoken languages in the world, apart from English.

Este repositorio contiene un script muy sencillo que envía los nuevos elementos del feed RSS de nvda.es a la lista de correo en Google Groups. Su propósito es sustituir a un aplet de IFTTT que hacía lo mismo, suprimiendo así la dependencia de servicios externos. Aunque está preparado para funcionar sólo desde nuestros servidores, te lo dejamos por aquí para que lo adaptes según tus necesidades.

## Requisitos

* Python 2.7
* html2text
* requests

Puedes instalar estas dos últimas bibliotecas mediante pip, o utilizando el gestor de paquetes de tu distribución Linux.

## Modo de uso

Para utilizar este script, basta con ejecutarlo: `python rss-email.py`
La primera vez que se ejecute, enviará por correo toda la fuente RSS en orden, empezando por el elemento más antiguo. En las siguientes ejecuciones sólo enviará las nuevas entradas, o no enviará nada si no hay nuevo contenido disponible. Los identificadores de las entradas ya publicadas se almacenan en el archivo ids.json, por lo que es importante no borrarlo.
Nota: el algoritmo de detección de nuevo contenido es dependiente de los metadatos ofrecidos por WordPress.
