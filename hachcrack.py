#!/usr/bin/env python3
import os
import subprocess
import argparse
from datetime import datetime

def show_banner():
    print("""
    ██╗  ██╗ █████╗ ███████╗██╗  ██╗ ██████╗██████╗  █████╗  ██████╗██╗  ██╗
    ██║  ██║██╔══██╗██╔════╝██║  ██║██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝
    ███████║███████║███████╗███████║██║     ██████╔╝███████║██║     █████╔╝ 
    ██╔══██║██╔══██║╚════██║██╔══██║██║     ██╔══██╗██╔══██║██║     ██╔═██╗ 
    ██║  ██║██║  ██║███████║██║  ██║╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗
    ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
    Advanced Hash Cracking Tool with Hashcat (Supports GPU Acceleration)
    """)

def get_hash_types():
    """Return common hash types with their codes"""
    return {
        "MD5": 0,
        "SHA1": 100,
        "SHA256": 1400,
        "SHA512": 1700,
        "NTLM": 1000,
        "WPA/WPA2": 22000,
        "NetNTLMv1": 5500,
        "NetNTLMv2": 5600,
        "Kerberos 5 AS-REQ Pre-Auth": 7500,
        "Adobe PDF": 10500,
        "WordPress": 400,
        "Joomla": 400,
        "Drupal": 7900,
        "MySQL 4.1+": 300,
        "Oracle 11g": 112,
        "PostgreSQL": 111,
        "Cisco Type 7": 7,
        "Cisco $9$": 9200,
        "VeraCrypt": 13721,
        "Bitcoin/Litecoin": 11300,
        "Android PIN": 101,
        "GPG": 17010,
        "Zip/RAR": 13600,
        "7-Zip": 11600,
        "iTunes Backup": 14700
    }

def detect_hash_type(hash_sample):
    """Try to automatically detect hash type"""
    # This is a simplified version - hashcat has better detection
    length = len(hash_sample)
    
    if hash_sample.startswith('$2a$') or hash_sample.startswith('$2b$') or hash_sample.startswith('$2y$'):
        return 3200  # bcrypt
    elif hash_sample.startswith('$5$'):
        return 7400  # SHA-256 Crypt
    elif hash_sample.startswith('$6$'):
        return 1800  # SHA-512 Crypt
    elif hash_sample.startswith('$DCC2$'):
        return 2100  # Domain Cached Credentials 2
    elif length == 32 and all(c in '0123456789abcdef' for c in hash_sample.lower()):
        return 0  # MD5
    elif length == 40 and all(c in '0123456789abcdef' for c in hash_sample.lower()):
        return 100  # SHA1
    elif length == 64 and all(c in '0123456789abcdef' for c in hash_sample.lower()):
        return 1400  # SHA256
    elif length == 128 and all(c in '0123456789abcdef' for c in hash_sample.lower()):
        return 1700  # SHA512
    else:
        return None  # Unknown

def run_hashcat(hash_file, wordlist, hash_type, attack_mode, rules_file=None, mask=None, workload=4, gpu=True):
    """Execute hashcat with given parameters"""
    cmd = [
        "hashcat",
        "-m", str(hash_type),
        "-a", str(attack_mode),
        "-w", str(workload),
        "--status",
        "--status-timer=10",
        "--potfile-disable",
        hash_file,
        wordlist
    ]
    
    if gpu:
        cmd.append("--force")
        cmd.append("--opencl-device-types=1,2")  # Use both CPU and GPU
    
    if rules_file:
        cmd.extend(["-r", rules_file])
    
    if mask:
        cmd.extend([mask])
    
    try:
        print("\n[+] Starting Hashcat...")
        print(f"[+] Command: {' '.join(cmd)}")
        
        start_time = datetime.now()
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        print("\n[+] Cracking completed!")
        print(f"[+] Time elapsed: {duration}")
        
        # Show results
        show_results_cmd = ["hashcat", "--show", hash_file]
        subprocess.run(show_results_cmd)
        
    except Exception as e:
        print(f"[!] Error: {str(e)}")

def show_advanced_options():
    """Display advanced options for power users"""
    print("\nAdvanced Options:")
    print("1. Rules Attack (Custom rules file)")
    print("2. Mask Attack (Custom mask)")
    print("3. Hybrid Attack (Wordlist + Mask)")
    print("4. Toggle GPU/CPU (Current: GPU)")
    print("5. Set Workload Profile (Current: 4)")
    print("6. Back to main menu")

def main():
    show_banner()
    
    # Check if hashcat is installed
    try:
        subprocess.run(["hashcat", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except:
        print("[!] Hashcat is not installed. Please install it first.")
        print("[!] On Kali Linux: sudo apt install hashcat")
        return
    
    hash_types = get_hash_types()
    attack_modes = {
        "0": "Straight (Dictionary)",
        "1": "Combination",
        "3": "Brute-Force",
        "6": "Hybrid Wordlist + Mask",
        "7": "Hybrid Mask + Wordlist"
    }
    
    # Default settings
    settings = {
        "workload": 4,
        "gpu": True,
        "rules_file": None,
        "mask": None
    }
    
    while True:
        print("\nMain Menu:")
        print("1. Quick Crack (Auto-detect hash type)")
        print("2. Advanced Crack (Manual settings)")
        print("3. Advanced Options")
        print("4. Show Supported Hash Types")
        print("5. Exit")
        
        choice = input("\n[?] Select an option (1-5): ").strip()
        
        if choice == "1":
            print("\n[+] Quick Crack Mode")
            hash_file = input("[?] Path to hash file: ").strip()
            wordlist = input("[?] Path to wordlist: ").strip()
            
            # Read first hash to detect type
            try:
                with open(hash_file, 'r') as f:
                    first_hash = f.readline().strip()
                
                hash_type = detect_hash_type(first_hash)
                
                if hash_type is None:
                    print("[!] Could not automatically detect hash type")
                    print("[!] Please use Advanced Mode and specify hash type manually")
                    continue
                
                print(f"[+] Detected hash type: {hash_type}")
                run_hashcat(hash_file, wordlist, hash_type, 0, 
                          settings['rules_file'], settings['mask'], 
                          settings['workload'], settings['gpu'])
                
            except Exception as e:
                print(f"[!] Error: {str(e)}")
        
        elif choice == "2":
            print("\n[+] Advanced Crack Mode")
            
            # Hash file
            hash_file = input("[?] Path to hash file: ").strip()
            if not os.path.isfile(hash_file):
                print("[!] Hash file not found!")
                continue
            
            # Wordlist
            wordlist = input("[?] Path to wordlist: ").strip()
            if not os.path.isfile(wordlist):
                print("[!] Wordlist file not found!")
                continue
            
            # Hash type
            print("\nCommon Hash Types:")
            for name, code in hash_types.items():
                print(f"{code}: {name}")
            
            hash_type = input("\n[?] Hash type code (e.g., 22000 for WPA): ").strip()
            try:
                hash_type = int(hash_type)
            except:
                print("[!] Invalid hash type code")
                continue
            
            # Attack mode
            print("\nAttack Modes:")
            for code, desc in attack_modes.items():
                print(f"{code}: {desc}")
            
            attack_mode = input("\n[?] Attack mode (0-7): ").strip()
            if attack_mode not in attack_modes:
                print("[!] Invalid attack mode")
                continue
            
            run_hashcat(hash_file, wordlist, hash_type, int(attack_mode), 
                      settings['rules_file'], settings['mask'], 
                      settings['workload'], settings['gpu'])
        
        elif choice == "3":
            while True:
                show_advanced_options()
                adv_choice = input("\n[?] Select advanced option (1-6): ").strip()
                
                if adv_choice == "1":
                    rules_file = input("[?] Path to rules file: ").strip()
                    if os.path.isfile(rules_file):
                        settings['rules_file'] = rules_file
                        print("[+] Rules file set successfully")
                    else:
                        print("[!] Rules file not found")
                
                elif adv_choice == "2":
                    print("\nCommon Masks:")
                    print("?l = lowercase [a-z]")
                    print("?u = uppercase [A-Z]")
                    print("?d = digit [0-9]")
                    print("?s = special character [!@#$%^&*()]")
                    print("?a = all characters")
                    print("\nExample: ?l?l?l?l?d?d?d (4 letters + 3 digits)")
                    
                    mask = input("\n[?] Enter mask pattern: ").strip()
                    if mask:
                        settings['mask'] = mask
                        print("[+] Mask pattern set successfully")
                
                elif adv_choice == "3":
                    print("\n[+] Hybrid Attack Setup")
                    wordlist = input("[?] Path to wordlist: ").strip()
                    mask = input("[?] Mask pattern (appended to words): ").strip()
                    
                    if os.path.isfile(wordlist) and mask:
                        run_hashcat(hash_file, wordlist, hash_type, 6, 
                                  settings['rules_file'], mask, 
                                  settings['workload'], settings['gpu'])
                    else:
                        print("[!] Invalid wordlist or mask")
                
                elif adv_choice == "4":
                    settings['gpu'] = not settings['gpu']
                    print(f"[+] GPU acceleration {'enabled' if settings['gpu'] else 'disabled'}")
                
                elif adv_choice == "5":
                    print("\nWorkload Profiles:")
                    print("1 = Low (Reduces performance impact on other processes)")
                    print("2 = Default")
                    print("3 = Medium")
                    print("4 = High (Best for dedicated cracking machines)")
                    
                    workload = input("\n[?] Select workload profile (1-4): ").strip()
                    if workload in ['1', '2', '3', '4']:
                        settings['workload'] = int(workload)
                        print(f"[+] Workload profile set to {workload}")
                    else:
                        print("[!] Invalid selection")
                
                elif adv_choice == "6":
                    break
                
                else:
                    print("[!] Invalid option")
        
        elif choice == "4":
            print("\nSupported Hash Types:")
            for name, code in hash_types.items():
                print(f"{code}: {name}")
            input("\nPress Enter to continue...")
        
        elif choice == "5":
            print("\n[+] Exiting HashCrack...")
            break
        
        else:
            print("[!] Invalid option")

if __name__ == "__main__":
    main()
