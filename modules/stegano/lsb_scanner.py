from PIL import Image
import os
import numpy as np

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
        pixels = np.array(img).reshape(-1, 3) # Flatten to list of RGB pixels
        
        # Take only the needed pixels
        pixels = pixels[:limit_px]
        
        print(f"║ Pixels analysés   : {len(pixels)}")
        print(f"║ Canaux            : R + G + B            ║")
        print(f"║ Bits extraits     : {len(pixels)*3}                ║")
        print("╠══════════════════════════════════════════╣")
        print("║ 🔍 Recherche de patterns...               ║")
        
        # Extract bits
        extracted_bits = []
        for r, g, b in pixels:
            extracted_bits.append(r & 1)
            extracted_bits.append(g & 1)
            extracted_bits.append(b & 1)
            
        # Group bits into bytes
        extracted_bytes = []
        for i in range(0, len(extracted_bits) - 7, 8):
            byte = 0
            for bit in extracted_bits[i:i+8]:
                byte = (byte << 1) | bit
            extracted_bytes.append(byte)
            
        # Convert to text
        chars = []
        for b in extracted_bytes:
            if 32 <= b <= 126:
                chars.append(chr(b))
            else:
                chars.append('.')
        
        result_text = "".join(chars)
        patterns = ["flag", "ctf", "secret", "key", "{"]
        
        found = False
        for pattern in patterns:
            if pattern in result_text.lower():
                print(f"║ ✅ {pattern.upper()} DÉTECTÉ POTENTIELLEMENT ! ")
                found = True
        
        if not found:
            print("║ ℹ️ Aucun pattern connu détecté        ")
            
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
