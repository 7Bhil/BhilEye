from PIL import Image
import os
import numpy as np

STOP_MARKER = "<<END>>"

def scan_lsb(file_path):
    if not os.path.exists(file_path):
        print(f"Erreur : {file_path} introuvable.")
        return

    os.system('clear' if os.name == 'posix' else 'cls')
    print("╔══════════════════════════════════════════╗")
    print("║         SCANNER LSB INTELLIGENT          ║")
    print("╠══════════════════════════════════════════╣")
    
    try:
        limit_px = int(input("Combien de pixels analyser ? (défaut 5000) : ") or 5000)
        img = Image.open(file_path).convert('RGB')
        pixels = np.array(img).reshape(-1, 3)
        pixels = pixels[:limit_px]
        
        print(f"║ Pixels analysés   : {len(pixels)}")
        print(f"║ Canaux            : R + G + B            ║")
        print(f"║ Bits extraits     : {len(pixels)*3}                ║")
        print("╠══════════════════════════════════════════╣")
        print("║ 🔍 Recherche de patterns...               ║")
        
        extracted_bits = []
        for r, g, b in pixels:
            extracted_bits.append(int(r) & 1)
            extracted_bits.append(int(g) & 1)
            extracted_bits.append(int(b) & 1)
            
        extracted_bytes = []
        for i in range(0, len(extracted_bits) - 7, 8):
            byte = 0
            for bit in extracted_bits[i:i+8]:
                byte = (byte << 1) | bit
            extracted_bytes.append(byte)
            
        chars = []
        for b in extracted_bytes:
            if 32 <= b <= 126:
                chars.append(chr(b))
            else:
                chars.append('.')
        
        result_text = "".join(chars)
        
        # Stop at STOP_MARKER if found (message encoded by our tool)
        if STOP_MARKER in result_text:
            msg = result_text.split(STOP_MARKER)[0]
            print(f"║ 🔐 MESSAGE CACHÉ TROUVÉ !                ║")
            print(f"║ → {msg[:40]}")
        else:
            patterns = ["flag", "ctf", "secret", "key", "{"]
            found = False
            for pattern in patterns:
                if pattern in result_text.lower():
                    print(f"║ ✅ {pattern.upper()} DÉTECTÉ POTENTIELLEMENT !")
                    found = True
            if not found:
                print("║ ℹ️  Aucun pattern connu détecté       ║")
            
        print("╠══════════════════════════════════════════╣")
        print(f"║ EXTRAIT : {result_text[:40]}...")
        if len(result_text) > 40:
            print(f"║           {result_text[40:80]}...")
            
        save = input("\n💾 Sauvegarder l'extrait complet ? (o/n) : ").lower()
        if save == 'o':
            save_path = f"lsb_scan_{os.path.basename(file_path)}.txt"
            with open(save_path, 'w') as f:
                f.write(result_text)
            print(f"✅ Sauvegardé dans {save_path}")
            
    except Exception as e:
        print(f"║ ❌ Erreur : {str(e)}")
        
    print("╚══════════════════════════════════════════╝")
    input("\nAppuyez sur Entrée pour continuer...")


def encode_lsb(file_path):
    """Cache un message texte dans les bits de poids faible d'une image."""
    if not os.path.exists(file_path):
        print(f"Erreur : {file_path} introuvable.")
        return

    os.system('clear' if os.name == 'posix' else 'cls')
    print("╔══════════════════════════════════════════╗")
    print("║          ENCODER LSB — CACHER MSG        ║")
    print("╠══════════════════════════════════════════╣")
    
    try:
        message = input("Message à cacher : ")
        message += STOP_MARKER  # marqueur de fin pour le décodeur
        
        img = Image.open(file_path).convert('RGB')
        arr = np.array(img, dtype=np.uint8)
        flat = arr.flatten().copy()
        
        # Convertir message en bits
        bits = []
        for char in message:
            b = ord(char)
            for i in range(7, -1, -1):
                bits.append((b >> i) & 1)
        
        if len(bits) > len(flat):
            print(f"║ ❌ Message trop long ! ({len(bits)} bits > {len(flat)} disponibles)")
            input("\nAppuyez sur Entrée pour continuer...")
            return
        
        print(f"║ 📊 Message    : {len(message)} caractères")
        print(f"║ 📊 Bits à écrire : {len(bits)}")
        print(f"║ 📊 Capacité image : {len(flat)} disponibles")
        print("╠══════════════════════════════════════════╣")
        
        # Écrire les bits dans les LSB de chaque canal
        for i, bit in enumerate(bits):
            flat[i] = (flat[i] & 0xFE) | bit
        
        out_arr = flat.reshape(arr.shape)
        out_img = Image.fromarray(out_arr.astype(np.uint8))
        
        # Toujours sauvegarder en PNG pour ne pas perdre les LSB
        base = os.path.splitext(os.path.basename(file_path))[0]
        out_name = f"stego_{base}.png"
        out_img.save(out_name, 'PNG')
        
        print(f"║ ✅ Message caché avec succès !            ║")
        print(f"║ 📁 Fichier : {out_name}")
        print(f"║ 💡 Visuellement identique à l'original   ║")
        print(f"║    Seul un Scanner LSB peut le trouver   ║")
        
    except Exception as e:
        print(f"║ ❌ Erreur : {str(e)}")
        
    print("╚══════════════════════════════════════════╝")
    input("\nAppuyez sur Entrée pour continuer...")
