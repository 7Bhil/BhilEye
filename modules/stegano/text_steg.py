import os
import re

# Zero-width Unicode characters for encoding (space=0, non-joiner=1)
ZW_ZERO = '\u200b'  # Zero-width space = bit 0
ZW_ONE  = '\u200c'  # Zero-width non-joiner = bit 1

ZERO_WIDTH = {
    '\u200b': '0',
    '\u200c': '1',
    '\u200d': '1',
    '\ufeff': '0',
}


def analyze_text(file_path):
    if not os.path.exists(file_path):
        print(f"Erreur : {file_path} introuvable.")
        return

    os.system('clear' if os.name == 'posix' else 'cls')
    print("╔══════════════════════════════════════════╗")
    print("║       ANALYSE STEGANO TEXTE              ║")
    print("╠══════════════════════════════════════════╣")
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        print(f"║ Taille texte  : {len(content)} caracteres")
        print("╠══════════════════════════════════════╣")
        
        # 1. Detect invisible Unicode chars
        print("║ Recherche de caracteres invisibles... ║")
        
        bits = ""
        for char in content:
            if char in ZERO_WIDTH:
                bits += ZERO_WIDTH[char]
                
        detected = any(c in content for c in ZERO_WIDTH)
        
        if detected:
            print(f"║ ⚠️  Caracteres invisibles DETECTES !  ║")
            if len(bits) >= 8:
                chars = []
                for i in range(0, len(bits) - 7, 8):
                    b = int(bits[i:i+8], 2)
                    if 32 <= b <= 126:
                        chars.append(chr(b))
                decoded = "".join(chars)
                print(f"║ Decode : {decoded[:40]}")
        else:
            print("║ ✅ Aucun caractere invisible trouve   ║")
            
        # 2. Detect whitespace steganography
        print("╠══════════════════════════════════════╣")
        print("║ Analyse espaces suspects...           ║")
        trailing_lines = [line for line in content.splitlines() if line.endswith('  ')]
        if trailing_lines:
            print(f"║ ⚠️  {len(trailing_lines)} lignes suspectes (double espace)")
        else:
            print("║ ✅ Aucune anomalie d'espacement       ║")
            
        # 3. Search for flags
        flags = re.findall(r'flag\{[^}]+\}|CTF\{[^}]+\}', content, re.IGNORECASE)
        if flags:
            print("╠══════════════════════════════════════╣")
            for flag in flags:
                print(f"║ 🚩 FLAG TROUVE : {flag[:35]}  ║")
                
    except Exception as e:
        print(f"║ ❌ Erreur : {str(e)}")
        
    print("╚══════════════════════════════════════════╝")
    input("\nAppuyez sur Entree pour continuer...")


def encode_text(file_path):
    """Cache un message dans un fichier texte en utilisant des caracteres Unicode invisibles."""
    if not os.path.exists(file_path):
        print(f"Erreur : {file_path} introuvable.")
        return

    os.system('clear' if os.name == 'posix' else 'cls')
    print("╔══════════════════════════════════════════╗")
    print("║       ENCODER TEXTE — CACHER MSG         ║")
    print("╠══════════════════════════════════════════╣")
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        message = input("Message a cacher dans le fichier texte : ")
        
        # Convert message to invisible chars (zero-width)
        hidden_chars = ""
        for char in message:
            b = ord(char)
            for i in range(7, -1, -1):
                bit = (b >> i) & 1
                hidden_chars += ZW_ONE if bit else ZW_ZERO
        
        # Inject at the beginning (after first line ideally)
        lines = content.split('\n')
        if len(lines) > 1:
            lines[0] = lines[0] + hidden_chars
            out_content = '\n'.join(lines)
        else:
            out_content = content + hidden_chars
        
        out_name = f"stego_{os.path.basename(file_path)}"
        with open(out_name, 'w', encoding='utf-8') as f:
            f.write(out_content)
        
        print(f"║ 📊 Message     : {len(message)} caracteres")
        print(f"║ 📊 Bits caches : {len(message)*8} zero-width chars")
        print("╠══════════════════════════════════════════╣")
        print(f"║ ✅ Message cache avec succes !           ║")
        print(f"║ 📁 Fichier : {out_name}")
        print(f"║ 💡 Lisible normalement, invisible en     ║")
        print(f"║    copiant dans un editeur standard.     ║")
        
    except Exception as e:
        print(f"║ ❌ Erreur : {str(e)}")
        
    print("╚══════════════════════════════════════════╝")
    input("\nAppuyez sur Entree pour continuer...")
