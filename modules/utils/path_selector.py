import os
import readline
import glob
import subprocess

def path_completer(text, state):
    """Completer for path names."""
    if text.startswith('~'):
        text = os.path.expanduser(text)
    
    matches = glob.glob(text + '*')
    matches = [m + '/' if os.path.isdir(m) else m for m in matches]
    
    try:
        return matches[state]
    except IndexError:
        return None

def select_file(prompt="Entrez le chemin du fichier"):
    # Setup readline
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(path_completer)
    
    while True:
        cwd = os.getcwd()
        print(f"\n📂 Dossier actuel : {cwd}")
        print("💡 Astuces : 'ls' pour lister, 'cd <dossier>' pour naviguer, 'q' pour annuler")
        
        try:
            line = input(f"{prompt} (ou commande) : ").strip()
            
            if not line:
                continue
                
            if line.lower() == 'q':
                return None
                
            # Handle commands
            if line.startswith('ls'):
                # Simple ls implementation
                files = os.listdir('.')
                for f in sorted(files):
                    prefix = "📁 " if os.path.isdir(f) else "📄 "
                    print(f"  {prefix}{f}")
                continue
                
            if line.startswith('cd '):
                target = line[3:].strip()
                if target.startswith('~'):
                    target = os.path.expanduser(target)
                try:
                    os.chdir(target)
                except Exception as e:
                    print(f"❌ Erreur cd : {e}")
                continue

            if line == 'pwd':
                print(f"📍 {cwd}")
                continue
                
            # Assume it's a file selection
            path = line
            if path.startswith('~'):
                path = os.path.expanduser(path)
            
            if os.path.isfile(path):
                return os.path.abspath(path)
            elif os.path.isdir(path):
                # If they select a dir, just cd into it for convenience
                os.chdir(path)
                continue
            else:
                # Check if it exists at least
                if os.path.exists(path):
                    print(f"⚠️  {path} est présent mais n'est pas un fichier régulier.")
                else:
                    print(f"❌ '{path}' introuvable.")
                    
        except EOFError:
            return None
        except KeyboardInterrupt:
            print("\n")
            return None
        finally:
            pass

    # Clean up (though unreachable here due to infinite loop)
    readline.set_completer(None)
