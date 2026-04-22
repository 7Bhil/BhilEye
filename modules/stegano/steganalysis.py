import os
import numpy as np
from PIL import Image
from scipy.stats import chisquare

def chi_square_attack(file_path):
    if not os.path.exists(file_path):
        print(f"Erreur : {file_path} introuvable.")
        return

    os.system('clear' if os.name == 'posix' else 'cls')
    print("╔══════════════════════════════════════════╗")
    print("║         CHI-SQUARE ATTACK (Stat)         ║")
    print("╠══════════════════════════════════════════╣")
    
    try:
        img = Image.open(file_path).convert('RGB')
        arr = np.array(img).flatten()
        
        limit_px = min(len(arr), 30000)
        pixels = arr[:limit_px]
        
        print(f"║ Échantillons analysés : {limit_px} octets    ║")
        
        # In a natural image, adjacent pixels/colors have some variance.
        # Steganography LSB tends to make the distribution of "Pairs of Values" (PoVs) more uniform.
        # We calculate the distribution of values 2i and 2i+1.
        
        obs_counts = []
        exp_counts = []
        
        for i in range(0, 256, 2):
            count2i = np.sum(pixels == i)
            count2iplus1 = np.sum(pixels == i + 1)
            
            # The Chi-square attack on PoVs expects (count2i + count2i+1) / 2 for each
            avg = (count2i + count2iplus1) / 2
            
            if avg > 0:
                obs_counts.extend([count2i, count2iplus1])
                exp_counts.extend([avg, avg])
        
        if not obs_counts:
            print("║ ⚠️ Pas assez de données pour l'analyse  ║")
        else:
            chi_stat, p_value = chisquare(obs_counts, f_exp=exp_counts)
            
            # Note: For Chi-square attack, a p-value close to 1 means the distribution
            # is UNIFORM between PoVs, which is a strong indicator of LSB stego.
            # In scipy, p_value is the probability of seeing a more extreme result.
            # Here, if p-value is > 0.9, it's very likely steganographic.
            
            print(f"║ 📊 Score Chi-Square : {chi_stat:.4f}           ║")
            print(f"║ 🎯 P-Value (Uniformité) : {p_value:.4f}       ║")
            
            if p_value > 0.9:
                print("╠══════════════════════════════════════════╣")
                print("║ ✅ Image TRÈS PROBABLEMENT modifiée !    ║")
                print("║ 🎯 Probabilité stégano : > 90%           ║")
            elif p_value > 0.5:
                print("╠══════════════════════════════════════════╣")
                print("║ ⚠️  Anomalies statistiques détectées.    ║")
                print("║ 🎯 Probabilité stégano : Moyenne         ║")
            else:
                print("╠══════════════════════════════════════════╣")
                print("║ ✅ Distribution Naturelle                ║")
                print("║ 🎯 Probabilité stégano : Faible          ║")
                
    except Exception as e:
        print(f"║ ❌ Erreur : {str(e)}")
        
    print("╚══════════════════════════════════════════╝")
    input("\nAppuyez sur Entrée pour continuer...")
