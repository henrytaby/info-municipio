import re
#import colorama import Fore
import requests


website = "https://fichacomunidad.ine.gob.bo/"
resultado = requests.get(website)
content = resultado.text
print(content)