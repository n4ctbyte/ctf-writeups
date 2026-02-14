from scipy.io.wavfile import read
import numpy as np

rate, data = read("./main.wav")

print("[*] Menganalisis gelombang suara...")

hex_results = []

for sample in data:
    digit_val = int((sample - 1000) / 500)
    
    if 0 <= digit_val <= 15:
        hex_char = format(digit_val, 'x')
        hex_results.append(hex_char)

full_hex = "".join(hex_results)

try:
    source_code = bytes.fromhex(full_hex).decode('utf-8')
    
    if "pico" in source_code:
        print("FLAG:")
        for line in source_code.splitlines():
            if "pico" in line:
                print(f"\n   >>> {line.strip()} <<<\n")
    else:
        print("No "pico"")

    with open("flag_source.py", "w") as f:
        f.write(source_code)
    print(f"Full source code: flag_source.py")

except Exception as e:
    print(f"Error: {e}")
