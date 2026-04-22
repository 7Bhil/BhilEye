from PIL import Image
import os

def extract_lsb(file_path):
    if not os.path.exists(file_path):
        print(f"Erreur : {file_path} introuvable.")
        return

    print("╔══════════════════════════════════════╗")
    print("║         ANALYSE LSB (Bit Faible)     ║")
    print("╠══════════════════════════════════════╣")
    
    try:
        img = Image.open(file_path).convert('RGB')
        pixels = img.load()
        width, height = img.size
        
        extracted_bin = ""
        # On va extraire les bits de poids faible de chaque canal R, G, B
        # pour les 1000 premiers pixels (ou plus si besoin)
        limit = min(width * height, 5000) 
        
        count = 0
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                extracted_bin += str(r & 1)
                extracted_bin += str(g & 1)
                extracted_bin += str(b & 1)
                count += 1
                if count >= limit:
                    break
            if count >= limit:
                break
        
        # Conversion du binaire en texte
        chars = []
        for i in range(0, len(extracted_bin), 8):
            byte = extracted_bin[i:i+8]
            if len(byte) < 8:
                break
            try:
                char = chr(int(byte, 2))
                # On ne garde que les caractères imprimables
                if 32 <= ord(char) <= 126:
                    chars.append(char)
                else:
                    chars.append('.')
            except:
                chars.append('.')
        
        result_text = "".join(chars)
        print("║ PREMIERS CARACTÈRES EXTRAITS :       ")
        print(f"║ {result_text[:35]}...")
        if len(result_text) > 35:
            print(f"║ {result_text[35:70]}...")
            
        # Recherche de "flag"
        if "flag" in result_text.lower():
            print("╠══════════════════════════════════════╣")
            print("║ 🚩 FLAG POTENTIEL DÉTECTÉ DANS L'LSB! ║")
            print("╠══════════════════════════════════════╣")
            
        save = input("\n💾 Sauvegarder TOUS les bits extraits dans un fichier ? (o/n) : ").lower()
        if save == 'o':
            save_path = f"lsb_extracted_{os.path.basename(file_path)}.txt"
            with open(save_path, 'w') as f:
                f.write(result_text)
            print(f"✅ Sauvegardé dans {save_path}")
            
    except Exception as e:
        print(f"║ ❌ Erreur LSB : {str(e)}")
        
    print("╚══════════════════════════════════════╝")
    input("\nAppuyez sur Entrée pour continuer...")
