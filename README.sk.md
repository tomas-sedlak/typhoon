# Robotické rameno Typhoon

[![en](https://img.shields.io/badge/lang-en-red.svg)](README.md)
[![sk](https://img.shields.io/badge/lang-sk-green.svg)](README.sk.md)

`typhoon-robotic-arm` je Python knižnica, ktorá umožňuje ovládanie robotického ramena Typhoon. Táto knižnica poskytuje rôzne funkcie vrátane výpočtov, komunikácie a pohybu ramena.

## Inštalácia

Potrebný je **Python 3.8+**. Najnovšiu verziu stiahneš týmto príkazom:

```bash
pip install typhoon-robotic-arm
```

## Quickstart

```python
from typhoon import Typhoon

typhoon = Typhoon("COM3", 0, 170, 130, output=True)

typhoon.move_to(100, 0, 0)
typhoon.tool(pw9=255)
typhoon.move_to(0, 0, 0)

typhoon.close()
```

## Referencie

*trieda* **Typhoon**(*port: str, start_x: int, start_y: int, start_z: int, tool_offset_x: int = 0, tool_offset_y: int = 0, tool_offset_z: int = 0, output: bool = False*)

- Ovláda robotickú ruku Typhoon prostredníctvom sériovej komunikácie. Ponúka užívateľsky prívetivé rozhranie pre rôzne operácie s rukou.

- **Parametre:**

    - **port** (*povinné*) - Port, na ktorom je pripojená robotická ruka Typhoon. Môžete si to skontrolovať vo svojom Správcovi zariadení na Windows pod Správcami konektorov USB.
    
    - **start_x** (*povinné*): - Počiatočná pozícia X robotickej ruky.
   
    - **start_y** (*povinné*) - Počiatočná pozícia Y robotickej ruky.
   
    - **start_z** (*povinné*) - Počiatočná pozícia Z robotickej ruky.
   
    - **tool_offset_x** - X posun nástroja.
   
    - **tool_offset_y** - Y posun nástroja.
   
    - **tool_offset_z** - Z posun nástroja.
   
    - **output** - Ak chcete vidieť výstup z Arduino dosky.

- **Metódy:**

    - **move_to**(*x: int, y: int, z: int*):
        - Presunie ruku na zadané súradnice.
        - Vypočíta potrebné uhly a pošle ich do ruky.

    - **move_home**():
        - Presunie ruku do počiatočnej polohy.

    - **tool**(*pw8: int = 0, pw9: int = 0, pw10: int = 0*):

        - Ovláda stav nástroja (napr. otvorenie/zatvorenie grippera, zapnutie/vypnutie sania).
        - Pošle PWM hodnoty do ruky na aktiváciu požadovaných funkcií nástroja.

    - **get_angles**():

        - Vracia aktuálne uhly základne, hornej a dolnej ruky ako n-ticu.

    - **get_coords**():

        - Vracia aktuálne súradnice X, Y a Z špičky ruky ako n-ticu.

    - **send_file**(*file_path: str, separator: str = " "*):

        - Pohybuje rukou podľa súradníc zadaných v textovom súbore.
        - Každá súradnica musí byť napísaná na **novom riadku** vo formáte `x y z`.
        - Keď nastavíte `separator` na `, `, program očakáva na každom riadku dáta vo formáte `x, y, z`

    - **close**():

        - Ukončí sériové spojenie s rukou.