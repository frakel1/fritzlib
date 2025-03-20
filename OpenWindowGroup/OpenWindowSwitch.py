import sys
import os

library_path = os.path.abspath(r"C:\\OngoingWork\\Development\\pythongit\\fritzlib")
sys.path.append(library_path)

from fritzlib import fritzbox

# Nur Module anzeigen, die mit "fritzbox" beginnen
print("Geladene Libraries aus dem Projekt:")
for module_name in sys.modules.keys():
    if module_name.startswith("fritzlib"):
        print(module_name)
        

def main():
    mybox = fritzbox()   

if __name__ == '__main__':
    main()