from PIL import Image
import os

def analyze_planes(file_path):
    if not os.path.exists(file_path):
        print(f"Erreur : {file_path} introuvable.")
        return

    print("╔══════════════════════════════════════╗")
    print("║         ANALYSE DES PLANS (RGB)      ║")
    print("╠══════════════════════════════════════╣")
    print("║ [1] Plan Rouge (R)                   ║")
    print("║ [2] Plan Vert (G)                    ║")
    print("║ [3] Plan Bleu (B)                    ║")
    print("║ [4] Bits de poids faible (R0, G0, B0)║")
    print("╚══════════════════════════════════════╝")
    
    choice = input("\nChoix du plan : ")
    
    try:
        img = Image.open(file_path).convert('RGB')
        pixels = img.load()
        width, height = img.size
        
        new_img = Image.new('RGB', (width, height))
        new_pixels = new_img.load()
        
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                if choice == '1':
                    new_pixels[x, y] = (r, 0, 0)
                elif choice == '2':
                    new_pixels[x, y] = (0, g, 0)
                elif choice == '3':
                    new_pixels[x, y] = (0, 0, b)
                elif choice == '4':
                    # On amplifie les bits de poids faible pour les rendre visibles
                    r0 = 255 if (r & 1) else 0
                    g0 = 255 if (g & 1) else 0
                    b0 = 255 if (b & 1) else 0
                    new_pixels[x, y] = (r0, g0, b0)
        
        save_path = f"plane_analysis_{choice}_{os.path.basename(file_path)}.png"
        new_img.save(save_path)
        print(f"\n✅ Analyse terminée. Image générée : {save_path}")
        print("💡 Ouvre cette image pour voir si des motifs cachés apparaissent !")
        
    except Exception as e:
        print(f"❌ Erreur analyse plans : {str(e)}")
        
    input("\nAppuyez sur Entrée pour continuer...")
