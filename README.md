# web3-python-practices
Web3 Python Practices

Para poder usar este código te recomiendo instales las siguientes herramientas.

- Python 3.8 o superior.
- Windows 10 (20H1, 20H2 o 21H1)
- Windows Subsystem Linux (WSL) usando como distribución Ubuntu 20.04 (o usar GNU/Linux Ubuntu 20.04)
- Visual Studio Code (con el plugin de Python)
- Windows Terminal
- Instalar Web3 Python

## Procedimiento:

Si usas Windows 10, te recomiendo instalar WSL junto con Ubuntu 20.04. Este procedimiento puedes realizarlo siguiendo las instrucciones descritas en este enlace (https://docs.microsoft.com/en-us/windows/wsl/install-win10). Una vez instalado WSL, procede a instalar Ubuntu 20.04 desde la Windows Store y continua con el procedimiento mostrado. 

Esto te permitirá contar con una instalación de Ubuntu 20.40 accesible desde Windows sin mayores contratiempos, útil si por ejemplo, no conoces como funciona GNU/Linux.

En segundo lugar, comienza a instalar Python y Visual Studio Code. Las webs oficiales de ambos softwares son las siguientes

- Python: https://www.python.org/
- Visual Studio Code: https://code.visualstudio.com/

Ambos son softwares gratuitos, seguros y podrás instalarlos sin mayores problemas (no requieres de permisos administrativos para instalarlos).

**TIP:** Cuando instales Python, recuerda seleccionar la opción "Add Path", esto te permitirá ejecutar Python sin mayores problemas desde la consola de Windows. 

Una vez instalado todo esto, procede a instalar el plugin de Python en Visual Studio, podrás verlo en el listado de plugins disponible dentro de este editor. 

Seguidamente, instala Windows Terminal. Esto puedes hacerlo desde la Windows Store o desde su web oficial (https://github.com/microsoft/terminal). Esta terminal hará más fácil que puedas interactuar con la instalación de Ubuntu 20.04 en WSL.

Finalmente, ejecuta la Windows Terminal, y abre una pestaña con Ubuntu 20.04. Una vez allí, ejecuta este comando:

<pre>pip install web3</pre>

Con ello comenzarás a instalar todo lo que necesitas para usar Web3 Python. Asegúrate de ejecutar este comando sobre el WSL de Ubuntu 20.04, porque de otra forma fallará la instalación debido a dependencias no cumplidas. 

Al terminar la instalación, podrás copiar el código de cada uno de los archivos acá dispuestos y podrás ejecutarlos usando Visual Studio Code o directamente Python desde el WSL de Ubuntu 20.04.
