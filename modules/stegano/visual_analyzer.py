from PIL import Image
import os
import numpy as np
import matplotlib.pyplot as plt

def analyze_visual(file_path):
    if not os.path.exists(file_path):
        print(f"Erreur : {file_path} introuvable.")
        return

    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        print("╔══════════════════════════════════════════╗")
        print("║       AMPLIFICATEUR & ANALYSE VISUELLE   ║")
        print("╠══════════════════════════════════════════╣")
        print("║ [1] Amplificateur LSB (StegSolve)        ║")
        print("║ [2] Isolation Plans R / G / B            ║")
        print("║ [3] Analyse FFT (Fréquences)             ║")
        print("║ [4] Retour                               ║")
        print("╚══════════════════════════════════════════╝")
        
        choice = input("\nChoix : ")
        
        if choice == '4':
            break
            
        try:
            img = Image.open(file_path).convert('RGB')
            arr = np.array(img)
            
            if choice == '1':
                print("║ 🔍 Mode : Amplification LSB...           ║")
                # Create a new image where each pixel is (r&1*255, g&1*255, b&1*255)
                lsb_arr = (arr & 1) * 255
                out_img = Image.fromarray(lsb_arr.astype(np.uint8))
                out_name = f"output_lsb_{os.path.basename(file_path)}.png"
                out_img.save(out_name)
                print(f"╠══════════════════════════════════════════╣")
                print(f"║ ✅ Image amplifiée : {out_name} ")
                print(f"║ 💡 Ouvre-la pour voir l'invisible.       ║")
                
            elif choice == '2':
                print("║ 🔍 Mode : Isolation des plans...         ║")
                modes = ['Rouge', 'Vert', 'Bleu']
                for i, mode in enumerate(modes):
                    plane = np.zeros_like(arr)
                    plane[:,:,i] = arr[:,:,i]
                    out_img = Image.fromarray(plane)
                    out_name = f"{mode.lower()}_plane_{os.path.basename(file_path)}.png"
                    out_img.save(out_name)
                    print(f"║ ✅ Plan {mode} généré : {out_name}")
                print(f"╠══════════════════════════════════════════╣")
                print(f"║ 💡 Vérifie surtout le plan BLEU !        ║")
                
            elif choice == '3':
                print("║ 🔍 Mode : Analyse FFT...                 ║")
                # Convert to grayscale for FFT
                gray = np.array(img.convert('L'))
                f = np.fft.fft2(gray)
                fshift = np.fft.fftshift(f)
                magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1)
                
                out_name = f"fft_spectrum_{os.path.basename(file_path)}.png"
                plt.imsave(out_name, magnitude_spectrum, cmap='gray')
                print(f"╠══════════════════════════════════════════╣")
                print(f"║ ✅ Spectre FFT généré : {out_name} ")
                print(f"║ 📊 Cherche des pics de fréquence anormaux║")
                
            input("\nAppuyez sur Entrée pour continuer...")
            
        except Exception as e:
            print(f"║ ❌ Erreur : {str(e)}")
            input("\nAppuyez sur Entrée pour continuer...")
