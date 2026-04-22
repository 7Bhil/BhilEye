import os
import wave
import struct
import numpy as np

def analyze_audio(file_path):
    if not os.path.exists(file_path):
        print(f"Erreur : {file_path} introuvable.")
        return

    os.system('clear' if os.name == 'posix' else 'cls')
    print("╔══════════════════════════════════════════╗")
    print("║         ANALYSE STÉGANO AUDIO (WAV)      ║")
    print("╠══════════════════════════════════════════╣")
    
    try:
        with wave.open(file_path, 'rb') as wav:
            n_channels = wav.getnchannels()
            samp_width = wav.getsampwidth()
            n_frames = wav.getnframes()
            framerate = wav.getframerate()
            
            print(f"║ Canaux        : {n_channels}")
            print(f"║ Profondeur    : {samp_width * 8} bits")
            print(f"║ Frames        : {n_frames}")
            print(f"║ Fréquence     : {framerate} Hz")
            print("╠══════════════════════════════════════╣")
            print("║ 🔍 Extraction LSB audio...           ║")
            
            # Only process the first 10000 frames to stay fast
            raw = wav.readframes(min(n_frames, 50000))
        
        # Each sample in 16-bit audio is 2 bytes (little endian)
        samples = struct.unpack(f'<{len(raw)//2}h', raw[:len(raw) - (len(raw) % 2)])
        
        # Extract LSB from each sample
        bits = [s & 1 for s in samples[:80000]]
        
        chars = []
        for i in range(0, len(bits) - 7, 8):
            byte = int("".join(str(b) for b in bits[i:i+8]), 2)
            if 32 <= byte <= 126:
                chars.append(chr(byte))
            else:
                chars.append('.')
                
        result = "".join(chars)
        
        patterns = ["flag", "ctf", "secret", "key", "{"]
        found = False
        for p in patterns:
            if p in result.lower():
                print(f"║ 🚩 PATTERN '{p.upper()}' DÉTECTÉ !          ║")
                found = True
        if not found:
            print("║ ℹ️  Aucun pattern classique trouvé   ║")
            
        print(f"║ EXTRAIT : {result[:35]}...")
        
        save = input("\n💾 Sauvegarder l'extrait audio LSB ? (o/n) : ").lower()
        if save == 'o':
            out = f"audio_lsb_{os.path.basename(file_path)}.txt"
            with open(out, 'w') as f:
                f.write(result)
            print(f"✅ Sauvegardé dans {out}")
            
    except wave.Error:
        print("║ ❌ Ce fichier n'est pas un WAV valide   ║")
    except Exception as e:
        print(f"║ ❌ Erreur : {str(e)}")
        
    print("╚══════════════════════════════════════════╝")
    input("\nAppuyez sur Entrée pour continuer...")
