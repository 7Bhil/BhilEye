import os
import re

# Common invisible/zero-width Unicode characters used in text steganography
ZERO_WIDTH = {
    '\u200b': '0',    # Zero-width space
    '\u200c': '1',    # Zero-width non-joiner
    '\u200d': '1',    # Zero-width joiner
    '\ufeff': '0',    # BOM / Zero-width no-break space
}

def analyze_text(file_path):
    if not os.path.exists(file_path):
        print(f"Erreur : {file_path} introuvable.")
        return

    os.system('clear' if os.name == 'posix' else 'cls')
    print("╔══════════════════════════════════════════╗")
    print("║       ANALYSE STÉGANO TEXTE              ║")
    print("╠══════════════════════════════════════════╣")
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        print(f"║ Taille texte  : {len(content)} caractères")
        print("╠══════════════════════════════════════╣")
        
        # 1. Detect invisible Unicode chars
        print("║ 🔍 Recherche caractères invisibles... ║")
        
        bits = ""
        for char in content:
            if char in ZERO_WIDTH:
                bits += ZERO_WIDTH[char]
                
        detected = any(c in content for c in ZERO_WIDTH)
        
        if detected:
            print(f"║ ⚠️  Caractères invisibles DÉTECTÉS ! {bits[:20]}")
            if len(bits) >= 8:
                chars = []
                for i in range(0, len(bits) - 7, 8):
                    b = int(bits[i:i+8], 2)
                    if 32 <= b <= 126:
                        chars.append(chr(b))
                decoded = "".join(chars)
                print(f"║ Décodé : {decoded[:40]}")
        else:
            print("║ ✅ Aucun caractère invisible trouvé   ║")
            
        # 2. Detect unusual whitespace (trailing spaces for binary encoding)
        print("╠══════════════════════════════════════╣")
        print("║ 🔍 Analyse espaces suspects...        ║")
        trailing_lines = [line for line in content.splitlines() if line.endswith('  ')]
        if trailing_lines:
            print(f"║ ⚠️  {len(trailing_lines)} lignes suspectes (double espace en fin)")
            
            # Try to decode whitespace steganography (each space=0, tab=1)
            ws_bits = ""
            for char in content:
                if char == ' ':
                    ws_bits += '0'
                elif char == '\t':
                    ws_bits += '1'
                    
            if len(ws_bits) >= 8:
                ws_chars = []
                for i in range(0, len(ws_bits) - 7, 8):
                    b = int(ws_bits[i:i+8], 2)
                    if 32 <= b <= 126:
                        ws_chars.append(chr(b))
                ws_decoded = "".join(ws_chars)
                print(f"║ Espace/Tab décodé : {ws_decoded[:30]}...")
        else:
            print("║ ✅ Aucune anomalie d'espacement       ║")
            
        # 3. Search for flags in content
        flags = re.findall(r'flag\{[^}]+\}|CTF\{[^}]+\}', content, re.IGNORECASE)
        if flags:
            print("╠══════════════════════════════════════╣")
            for flag in flags:
                print(f"║ 🚩 FLAG TROUVÉ : {flag[:35]}  ║")
                
    except Exception as e:
        print(f"║ ❌ Erreur : {str(e)}")
        
    print("╚══════════════════════════════════════════╝")
    input("\nAppuyez sur Entrée pour continuer...")
