import os
import exifread
from PIL import Image
import magic
import subprocess
import shutil

def extract_hidden_files(file_path):
    print("╠══════════════════════════════════════╣")
    print("║           EXTRACTION                 ║")
    print("╠══════════════════════════════════════╣")
    
    output_dir = f"extracted_{os.path.basename(file_path)}"
    print(f"║ 📂 Sortie : {output_dir}")
    
    try:
        # On utilise binwalk -e pour extraire
        # Note: --run-as=root peut être nécessaire dans certains environnements mais on tente sans d'abord
        result = subprocess.run(['binwalk', '-e', '--directory', output_dir, file_path], capture_output=True, text=True)
        
        if os.path.exists(output_dir):
            files = []
            for root, dirs, filenames in os.walk(output_dir):
                for f in filenames:
                    files.append(f)
            
            if files:
                print(f"║ ✅ {len(files)} fichiers extraits avec succès")
                for f in files[:5]:
                    print(f"║    -> {f}")
                if len(files) > 5:
                    print(f"║    ... et {len(files)-5} autres.")
            else:
                print("║ ⚠️  Extraction terminée mais aucun fichier trouvé")
        else:
            print("║ ❌ Échec de la création du dossier d'extraction")
            
    except Exception as e:
        print(f"║ ❌ Erreur d'extraction : {str(e)}")

def analyze_image(file_path):
    if not os.path.exists(file_path):
        print(f"Erreur : Le fichier {file_path} n'existe pas.")
        return

    os.system('clear' if os.name == 'posix' else 'cls')
    print("╔══════════════════════════════════════╗")
    print("║         ANALYSE IMAGE                ║")
    print("╠══════════════════════════════════════╣")
    
    size_mb = os.path.getsize(file_path) / (1024 * 1024)
    file_type = magic.from_file(file_path)
    
    print(f"║ 📄 Fichier      : {os.path.basename(file_path)}")
    print(f"║ 🔍 Type réel    : {file_type[:30]}...")
    
    try:
        with Image.open(file_path) as img:
            print(f"║ 📐 Dimensions   : {img.width} x {img.height} px")
            print(f"║ 🎨 Mode         : {img.mode}")
    except Exception:
        pass
        
    print(f"║ 📦 Taille       : {size_mb:.2f} MB")
    
    # Métadonnées EXIF améliorées
    print("╠══════════════════════════════════════╣")
    print("║              MÉTADONNÉES EXIF        ║")
    print("╠══════════════════════════════════════╣")
    
    hidden_detected = False
    try:
        with open(file_path, 'rb') as f:
            tags = exifread.process_file(f)
            
            if not tags:
                print("║ 🚫 Aucune donnée EXIF trouvée        ")
            else:
                important_tags = {
                    'Image Model': '📷 Modèle',
                    'Image Make': '🏭 Marque',
                    'Image DateTime': '📅 Date',
                    'Image Software': '🛠️ Logiciel',
                    'EXIF ExposureTime': '⏱️ Expo',
                    'EXIF ISOSpeedRatings': '🎞️ ISO'
                }
                
                for tag, label in important_tags.items():
                    if tag in tags:
                        print(f"║ {label.ljust(10)}: {tags[tag]}")
                
                if 'GPS GPSLatitude' in tags:
                    print("║ 📍 GPS       : DÉTECTÉ 🌍")
    except Exception as e:
        print(f"║ ❌ Erreur EXIF  : {str(e)}")

    # Fichiers cachés (Binwalk)
    print("╠══════════════════════════════════════╣")
    print("║           FICHIERS CACHÉS            ║")
    print("╠══════════════════════════════════════╣")
    
    try:
        result = subprocess.run(['binwalk', file_path], capture_output=True, text=True)
        lines = result.stdout.splitlines()
        
        hidden_items = []
        for line in lines[3:]:
            if line.strip():
                hidden_items.append(line)
                hidden_detected = True
        
        if not hidden_detected:
            print("║ ✅ Aucun fichier caché détecté       ")
        else:
            for item in hidden_items[:8]:
                print(f"║ ⚠️  {item[:35]}...")
            if len(hidden_items) > 8:
                print(f"║ ... (+ {len(hidden_items)-8} autres)")
    except Exception:
        print("║ ❌ Erreur Binwalk                    ")
        
    print("╚══════════════════════════════════════╝")
    
    if hidden_detected:
        choice = input("\nExtraire les fichiers cachés ? (o/n) : ").lower()
        if choice == 'o':
            extract_hidden_files(file_path)
    
    input("\nAppuyez sur Entrée pour continuer...")
