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
        print("\n=== Forensics & Métadonnées ===")
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

def main():
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        print_banner()
        print("=== CTF TOOLKIT ===")
        print("[1] Forensics & Métadonnées")
        print("[2] Stéganographie (À venir)")
        print("[3] Cryptographie (À venir)")
        print("[4] Hash Cracker (À venir)")
        print("[5] Réseau / PCAP (À venir)")
        print("[6] Fichiers & Repair (À venir)")
        print("[7] Quitter")
        
        choice = input("\nChoix : ")
        
        if choice == '1':
            forensics_menu()
        elif choice == '7':
            print("Au revoir !")
            sys.exit()
        else:
            print("Fonctionnalité non encore implémentée ou choix invalide.")
            input("Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()
