import os
import wave
import struct
import numpy as np

STOP_MARKER = "<<END>>"

def analyze_audio(file_path):
    if not os.path.exists(file_path):
        print(f"Erreur : {file_path} introuvable.")
        return

    os.system('clear' if os.name == 'posix' else 'cls')
    print("╔══════════════════════════════════════════╗")
    print("║         ANALYSE STEGANO AUDIO (WAV)      ║")
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
            print(f"║ Frequence     : {framerate} Hz")
            print("╠══════════════════════════════════════╣")
            print("║ Extraction LSB audio...              ║")
            
            raw = wav.readframes(min(n_frames, 50000))
        
        samples = struct.unpack(f'<{len(raw)//2}h', raw[:len(raw) - (len(raw) % 2)])
        bits = [s & 1 for s in samples[:80000]]
        
        chars = []
        for i in range(0, len(bits) - 7, 8):
            byte = int("".join(str(b) for b in bits[i:i+8]), 2)
            if 32 <= byte <= 126:
                chars.append(chr(byte))
            else:
                chars.append('.')
                
        result = "".join(chars)
        
        # Check for our marker
        if STOP_MARKER in result:
            msg = result.split(STOP_MARKER)[0]
            print(f"║ 🔐 MESSAGE CACHÉ TROUVÉ !             ║")
            print(f"║ → {msg[:40]}")
        else:
            patterns = ["flag", "ctf", "secret", "key", "{"]
            found = False
            for p in patterns:
                if p in result.lower():
                    print(f"║ 🚩 PATTERN '{p.upper()}' DETECTE !         ║")
                    found = True
            if not found:
                print("║ ℹ️  Aucun pattern classique trouve   ║")
            
        print(f"║ EXTRAIT : {result[:35]}...")
        
        save = input("\n💾 Sauvegarder l'extrait audio LSB ? (o/n) : ").lower()
        if save == 'o':
            out = f"audio_lsb_{os.path.basename(file_path)}.txt"
            with open(out, 'w') as f:
                f.write(result)
            print(f"✅ Sauvegarde dans {out}")
            
    except wave.Error:
        print("║ ❌ Ce fichier n'est pas un WAV valide   ║")
    except Exception as e:
        print(f"║ ❌ Erreur : {str(e)}")
        
    print("╚══════════════════════════════════════════╝")
    input("\nAppuyez sur Entree pour continuer...")


def encode_audio(file_path):
    """Cache un message dans les bits de poids faible d'un fichier WAV."""
    if not os.path.exists(file_path):
        print(f"Erreur : {file_path} introuvable.")
        return

    os.system('clear' if os.name == 'posix' else 'cls')
    print("╔══════════════════════════════════════════╗")
    print("║       ENCODER AUDIO — CACHER MSG         ║")
    print("╠══════════════════════════════════════════╣")
    
    try:
        message = input("Message a cacher dans le WAV : ")
        message += STOP_MARKER
        
        # Convert message to bits
        bits = []
        for char in message:
            b = ord(char)
            for i in range(7, -1, -1):
                bits.append((b >> i) & 1)
        
        with wave.open(file_path, 'rb') as wav:
            params = wav.getparams()
            n_frames = wav.getnframes()
            raw = wav.readframes(n_frames)
        
        if len(bits) > len(raw) // 2:
            print(f"║ ❌ Message trop long pour ce fichier  ║")
            input("\nAppuyez sur Entree pour continuer...")
            return
        
        samples = list(struct.unpack(f'<{len(raw)//2}h', raw[:len(raw) - (len(raw) % 2)]))
        
        print(f"║ 📊 Message    : {len(message)} caracteres")
        print(f"║ 📊 Bits       : {len(bits)}")
        print(f"║ 📊 Capacite   : {len(samples)} samples disponibles")
        print("╠══════════════════════════════════════════╣")
        
        for i, bit in enumerate(bits):
            samples[i] = (samples[i] & ~1) | bit
        
        out_name = f"stego_{os.path.basename(file_path)}"
        with wave.open(out_name, 'wb') as out_wav:
            out_wav.setparams(params)
            out_wav.writeframes(struct.pack(f'<{len(samples)}h', *samples))
        
        print(f"║ ✅ Message cache avec succes !           ║")
        print(f"║ 📁 Fichier : {out_name}")
        print(f"║ 💡 Son identique, message invisible !    ║")
        
    except wave.Error:
        print("║ ❌ Fichier WAV invalide                  ║")
    except Exception as e:
        print(f"║ ❌ Erreur : {str(e)}")
        
    print("╚══════════════════════════════════════════╝")
    input("\nAppuyez sur Entree pour continuer...")
