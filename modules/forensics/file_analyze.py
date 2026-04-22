import os
import magic
import subprocess

def extract_hidden_files(file_path):
    print("╠══════════════════════════════════════╣")
    print("║           EXTRACTION                 ║")
    print("╠══════════════════════════════════════╣")
    
    output_dir = f"extracted_{os.path.basename(file_path)}"
    print(f"║ 📂 Sortie : {output_dir}")
    
    try:
        result = subprocess.run(['binwalk', '-e', '--directory', output_dir, file_path], capture_output=True, text=True)
        if os.path.exists(output_dir):
            files = []
            for root, dirs, filenames in os.walk(output_dir):
                for f in filenames:
                    files.append(f)
            
            if files:
                print(f"║ ✅ {len(files)} fichiers extraits")
            else:
                print("║ ⚠️  Aucun fichier trouvé après extraction")
        else:
            print("║ ❌ Dossier d'extraction non créé")
    except Exception as e:
        print(f"║ ❌ Erreur : {str(e)}")

def analyze_file(file_path):
    if not os.path.exists(file_path):
        print(f"Erreur : Le fichier {file_path} n'existe pas.")
        return

    os.system('clear' if os.name == 'posix' else 'cls')
    print("╔══════════════════════════════════════╗")
    print("║       ANALYSE COMPLÈTE               ║")
    print("╠══════════════════════════════════════╣")
    
    file_name = os.path.basename(file_path)
    extension = os.path.splitext(file_name)[1]
    real_type = magic.from_file(file_path)
    size_kb = os.path.getsize(file_path) / 1024
    
    mismatch = "⚠️ MISMATCH" if extension and extension.lower() not in real_type.lower() else ""
    
    print(f"║ Nom          : {file_name}")
    print(f"║ Type réel    : {real_type[:30]}...")
    print(f"║ Status       : {mismatch if mismatch else '✅ OK'}")
    print(f"║ Taille       : {size_kb:.2f} KB")
    
    # Strings améliorés
    print("╠══════════════════════════════════════╣")
    print("║         STRINGS EXTRAITS             ║")
    print("╠══════════════════════════════════════╣")
    
    try:
        result = subprocess.run(['strings', '-n', '6', file_path], capture_output=True, text=True)
        lines = result.stdout.splitlines()
        if lines:
            for line in lines[:8]:
                # Nettoyage minimal pour l'affichage
                clean_line = line.strip()
                if clean_line:
                    print(f"║ 🔤 {clean_line[:35]}...")
            if len(lines) > 8:
                print(f"║ ... ({len(lines)-8} autres)")
                
            save = input("\n💾 Sauvegarder TOUS les strings dans un fichier ? (o/n) : ").lower()
            if save == 'o':
                save_path = f"strings_{file_name}.txt"
                with open(save_path, 'w') as f:
                    f.write(result.stdout)
                print(f"✅ Sauvegardé dans {save_path}")
        else:
            print("║ 🚫 Aucun string lisible trouvé          ")
    except Exception as e:
        print(f"║ ❌ Erreur strings : {str(e)}")

    # Fichiers Cachés
    print("╠══════════════════════════════════════╣")
    print("║         FICHIERS CACHÉS (Binwalk)    ║")
    print("╠══════════════════════════════════════╣")
    
    hidden_detected = False
    try:
        result = subprocess.run(['binwalk', file_path], capture_output=True, text=True)
        lines = result.stdout.splitlines()
        
        for line in lines[3:]:
            if line.strip():
                print(f"║ ⚠️  {line[:35]}...")
                hidden_detected = True
        
        if not hidden_detected:
            print("║ ✅ Aucun fichier caché détecté       ")
    except Exception:
        print("║ ❌ Erreur lors de l'appel à binwalk  ")
        
    print("╚══════════════════════════════════════╝")
    
    if hidden_detected:
        choice = input("\nExtraire les fichiers cachés ? (o/n) : ").lower()
        if choice == 'o':
            extract_hidden_files(file_path)
            
    input("\nAppuyez sur Entrée pour continuer...")
