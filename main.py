import os
import sys

def print_banner():
    banner = r"""
╔══════════════════════════╗
║      PhantomEye 👁️       ║
║    "See what others can't"║
╚══════════════════════════╝
"""
    print(banner)

from modules.utils.path_selector import select_file

def forensics_menu():
    while True:
        print("\n=== Forensics & Metadonnees ===")
        print("[1] Analyser une image")
        print("[2] Analyser un PDF")
        print("[3] Analyser un fichier quelconque")
        print("[4] Retour")
        
        choice = input("\nChoix : ")
        
        if choice == '1':
            from modules.forensics.image_meta import analyze_image
            path = select_file("Chemin de l'image")
            if path: analyze_image(path)
        elif choice == '2':
            from modules.forensics.pdf_meta import analyze_pdf
            path = select_file("Chemin du PDF")
            if path: analyze_pdf(path)
        elif choice == '3':
            from modules.forensics.file_analyze import analyze_file
            path = select_file("Chemin du fichier")
            if path: analyze_file(path)
        elif choice == '4':
            break
        else:
            print("Choix invalide.")

def stega_menu():
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        print_banner()
        print("=== Steganographie V2 🔥 ===")
        print("")
        print("──── ANALYSE (Trouver) ────")
        print("[1] Scanner LSB Intelligent")
        print("[2] Amplificateur / Plans RGB / FFT")
        print("[3] Chi-Square Attack (Detection Statistique)")
        print("[4] Analyse Audio WAV")
        print("[5] Analyse Texte Invisible")
        print("")
        print("──── ENCODER (Cacher) ────")
        print("[6] Cacher message dans une image (LSB)")
        print("[7] Cacher message dans un WAV (LSB Audio)")
        print("[8] Cacher message dans un fichier texte")
        print("")
        print("[9] Retour")
        
        choice = input("\nChoix : ")
        
        if choice == '1':
            from modules.stegano.lsb_scanner import scan_lsb
            path = select_file("Chemin de l'image")
            if path: scan_lsb(path)
        elif choice == '2':
            from modules.stegano.visual_analyzer import analyze_visual
            path = select_file("Chemin de l'image")
            if path: analyze_visual(path)
        elif choice == '3':
            from modules.stegano.steganalysis import chi_square_attack
            path = select_file("Chemin de l'image")
            if path: chi_square_attack(path)
        elif choice == '4':
            from modules.stegano.audio_steg import analyze_audio
            path = select_file("Chemin du fichier WAV")
            if path: analyze_audio(path)
        elif choice == '5':
            from modules.stegano.text_steg import analyze_text
            path = select_file("Chemin du fichier texte")
            if path: analyze_text(path)
        elif choice == '6':
            from modules.stegano.lsb_scanner import encode_lsb
            path = select_file("Image de couverture")
            if path: encode_lsb(path)
        elif choice == '7':
            from modules.stegano.audio_steg import encode_audio
            path = select_file("Fichier WAV de couverture")
            if path: encode_audio(path)
        elif choice == '8':
            from modules.stegano.text_steg import encode_text
            path = select_file("Fichier texte de couverture")
            if path: encode_text(path)
        elif choice == '9':
            break
        else:
            print("Choix invalide.")

def main():
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        print_banner()
        print("=== CTF TOOLKIT ===")
        print("[1] Forensics & Metadonnees")
        print("[2] Steganographie V2 🔥 (Analyse + Cache)")
        print("[3] Cryptographie (A venir)")
        print("[4] Hash Cracker (A venir)")
        print("[5] Reseau / PCAP (A venir)")
        print("[6] Fichiers & Repair (A venir)")
        print("[7] Quitter")
        
        choice = input("\nChoix : ")
        
        if choice == '1':
            forensics_menu()
        elif choice == '2':
            stega_menu()
        elif choice == '7':
            print("Au revoir !")
            sys.exit()
        else:
            print("Fonctionnalite non encore implementee ou choix invalide.")
            input("Appuyez sur Entree pour continuer...")

if __name__ == "__main__":
    main()
