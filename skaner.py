import subprocess
import sys
import re


def scan_installed_programs():
    try:
        # Uruchomienie polecenia dpkg -l, które wyświetla zainstalowane pakiety w systemie.
        result = subprocess.run(['dpkg', '-l'], capture_output=True, text=True)
        if result.returncode == 0:
            installed_programs = {}
            lines = result.stdout.split('\n')
            for line in lines[5:]:
                # Pomijanie pierwszych 5 linii, ponieważ są to nagłówki.
                parts = line.split()
                if len(parts) >= 3:
                    package_name = parts[1]
                    package_version = parts[2]
                    installed_programs[package_name] = package_version
            return installed_programs
        else:
            print("Błąd podczas skanowania zainstalowanych programów.")
            return None
    except Exception as e:
        print("Wystąpił błąd:", e)
        return None
    
def scan_with_nmap(ip):
    try:
        # Wywołanie polecenia Nmap i przechwycenie wyników
        result = subprocess.run(['nmap', '-p-', '-sV', '--open', ip], capture_output=True, text=True, timeout=300)
        
        # Sprawdzenie, czy nie wystąpiły błędy podczas wywoływania polecenia
        if result.returncode != 0:
            print("Błąd podczas skanowania:", result.stderr)
            return None
        
        # Analiza wyników skanowania
        services = {}
        lines = result.stdout.split('\n')
        for line in lines:
            # Szukanie linii zawierających informacje o usługach na portach
            match = re.match(r'(\d+)/(\w+)\s+open\s+(\S+)', line)
            if match:
                port = int(match.group(1))
                protocol = match.group(2)
                service_version = match.group(3)
                services[(port, protocol)] = service_version
        
        return services
    
    except subprocess.TimeoutExpired:
        print("Skanowanie zbyt długo trwało.")
        return None

def main():
    if len(sys.argv) == 1:
        pass
    else:
        installed_programs = scan_installed_programs()
        if installed_programs:
            print("Zainstalowane programy i ich wersje:")
            for program, version in installed_programs.items():
                print(program, "-", version)
        else:
            print("Nie znaleziono zainstalowanych programów.")

if __name__ == "__main__":
    main()