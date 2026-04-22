import os
import fitz  # PyMuPDF
from pdfminer.high_level import extract_text
import re

def analyze_pdf(file_path):
    if not os.path.exists(file_path):
        print(f"Erreur : Le fichier {file_path} n'existe pas.")
        return

    print("╔══════════════════════════════════════╗")
    print("║         ANALYSE PDF                  ║")
    print("╠══════════════════════════════════════╣")
    
    try:
        doc = fitz.open(file_path)
        meta = doc.metadata
        
        print(f"║ Auteur       : {meta.get('author', 'Inconnu')}")
        print(f"║ Créé le      : {meta.get('creationDate', 'Inconnu')}")
        print(f"║ Modifié le   : {meta.get('modDate', 'Inconnu')}")
        print(f"║ Logiciel     : {meta.get('producer', 'Inconnu')}")
        print(f"║ Pages        : {doc.page_count}")
        
        # Extraction d'images
        image_count = 0
        for page_index in range(len(doc)):
            page = doc[page_index]
            image_count += len(page.get_images())
            
        print("╠══════════════════════════════════════╣")
        print("║           CONTENU SUSPECT            ║")
        print("╠══════════════════════════════════════╣")
        
        # Texte invisible (simplifié : on cherche du texte très petit ou de la même couleur que le fond)
        # Ici on va juste utiliser pdfminer pour voir si on extrait plus de texte que PyMuPDF ou des motifs suspects
        full_text = extract_text(file_path)
        suspicious_patterns = [r'flag\{.*\}', r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+']
        found_patterns = []
        for pattern in suspicious_patterns:
            found = re.findall(pattern, full_text)
            if found:
                found_patterns.extend(found)
        
        if found_patterns:
            print(f"║ ⚠️  Patterns suspects trouvés : {len(found_patterns)}")
            for p in found_patterns[:3]:
                print(f"║    -> {p[:30]}...")
        else:
            print("║ ✅ Aucun texte suspect évident       ")
            
        print(f"║ 📎 {image_count} images embarquées détectées")
        doc.close()
        
    except Exception as e:
        print(f"║ Erreur PDF   : {str(e)}")
        
    print("╚══════════════════════════════════════╝")
    input("\nAppuyez sur Entrée pour continuer...")
