# super_pm.py

import hashlib
import os
from getpass import getpass
from rich import print as printc
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from pyfiglet import figlet_format
from config import get_master_password, checkConfig

import string
import random
import requests
import utils.add
import utils.aesutil
import utils.retrieve
import utils.generate
import utils.delete
from utils.add import computeMasterKey
from utils.dbconfig import dbconfig


# Periksa apakah master password ada
def check_master_password():
    if not checkConfig():
        printc("[red][!] No configuration found! Please configure the application first using 'config.py make'[/red]")
        exit(1)

    master_password = get_master_password()
    if not master_password:
        printc("[red][!] Master password is not set! Please set it first.[/red]")
        exit(1)


# Lakukan pengecekan master password dan konfigurasi saat pertama kali menjalankan aplikasi
check_master_password()


def check_password_pwned(password):
    sha1_password = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1_password[:5], sha1_password[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"

    for _ in range(3):  # Retry up to 3 times if request fails
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                hashes = response.text.splitlines()
                for line in hashes:
                    hash_suffix, count = line.split(":")
                    if hash_suffix == suffix:
                        return int(count)
            break
        except requests.exceptions.RequestException:
            printc("[red][!] Error connecting to HIBP API. Retrying...[/red]")

    return 0


def generatePassword(length=15):
    try:
        length = int(length)
        if length < 8:
            printc("[red][!] Warning: Password length should be at least 8 characters according to NIST standards.[/red]")
            return None
    except ValueError:
        printc("[red][!] Invalid length. Please enter a valid number.[/red]")
        return None

    required_chars = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice(string.punctuation)
    ]

    all_chars = string.ascii_letters + string.digits + string.punctuation
    password = required_chars + [random.choice(all_chars) for _ in range(length - 4)]

    random.shuffle(password)
    password = ''.join(password)

    breach_count = check_password_pwned(password)
    if breach_count > 0:
        printc(f"[red][!] Warning: Generated password has been found {breach_count} time(s) in data breaches! Consider generating a new one.[/red]")

    return password


def inputAndValidateMasterPassword():
    attempts = 3
    db = dbconfig()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM pm.secrets")
    result = cursor.fetchone()

    while attempts > 0:
        mp = getpass("MASTER PASSWORD: ")
        hashed_mp = hashlib.sha256(mp.encode()).hexdigest()

        if hashed_mp == result[0]:
            breach_count = check_password_pwned(mp)
            if breach_count > 0:
                printc(f"[red][!] Warning: Your master password has been found {breach_count} time(s) in data breaches! Consider changing it.[/red]")
            return [mp, result[1]]
        else:
            printc(f"[red][!] WRONG! You have {attempts - 1} attempts left.[/red]")
            attempts -= 1

    printc("[red][!] Too many failed attempts. Exiting...[/red]")
    return None


def show_usage():
    printc("[cyan]" + figlet_format("SUPER PM", font="larry3d") + "[/cyan]")
    printc("[bold]Super PM is a password manager designed to securely store, manage, and protect passwords with ease.[/bold]\n")
    printc("[blue]by Sani, Zho & Riel[/blue]\n")
    printc("[yellow]Tata Cara Penggunaan:[/yellow]")
    printc("[green]  add      : Menambahkan entri password baru[/green]")
    printc("[green]  extract  : Mengambil password berdasarkan filter[/green]")
    printc("[green]  generate : Menghasilkan password acak dengan panjang tertentu[/green]")
    printc("[green]  check    : Mengecek apakah password pernah bocor dalam data breach[/green]")
    printc("[green]  delete   : Menghapus entri password yang sudah ada[/green]")
    printc("[green]  exit     : Keluar dari program[/green]")


def interactive_cli():
    show_usage()
    menu_completer = WordCompleter(['add', 'extract', 'generate', 'check', 'update', 'exit'], ignore_case=True)
    session = PromptSession(completer=menu_completer)

    while True:
        try:
            option = session.prompt('Super PM > ', completer=menu_completer)

            if option in ['add', 'a']:
                name = input('Enter site name: ')
                url = input('Enter site URL: ')
                login = input('Enter site login (username): ')
                email = input('Enter email (optional): ') or ""

                res = inputAndValidateMasterPassword()
                if res is not None:
                    utils.add.addEntry(res[0], res[1], name, url, email, login)
                    printc("[green][+] Entry added successfully![/green]")

            elif option in ['extract', 'e']:
                name = input('Enter site name (optional): ') or None
                url = input('Enter site URL (optional): ') or None
                email = input('Enter email (optional): ') or None
                login = input('Enter username (optional): ') or None

                res = inputAndValidateMasterPassword()
                if res is not None:
                    search = {key: value for key, value in zip(['sitename', 'siteurl', 'email', 'username'], [name, url, email, login]) if value}
                    password = utils.retrieve.retrieveEntries(res[0], res[1], search, decryptPassword=True)
                    if password:
                        printc(f"[green][+] Extracted Password: {password}[/green]")

            elif option in ['generate', 'g']:
                length = input('Enter password length (default 15): ')
                password = generatePassword(length or 15)
                if password:
                    printc(f"[green][+] Generated Password: {password}[/green]")

            elif option in ['check', 'c']:
                password = getpass('Enter password to check: ')
                breach_count = check_password_pwned(password)
                if breach_count > 0:
                    printc(f"[red][!] Warning: This password has been found {breach_count} time(s) in data breaches! Consider changing it.[/red]")
                else:
                    printc("[green][+] This password has not been found in known breaches.[/green]")

            elif option in ['delete', 'd']:
                name = input('Enter site name: ')
                login = input('Enter username: ')

                # Validasi master password
                res = inputAndValidateMasterPassword()
                if res is not None:
                # Panggil fungsi untuk menghapus entri
                  success = utils.delete.deleteEntry(name, login)

            elif option in ['exit', 'quit']:
                printc("[yellow][+] Exiting program...[/yellow]")
                break
            else:
                printc("[red][!] Invalid option. Please try again.[/red]")

        except KeyboardInterrupt:
            printc("\n[yellow][+] Exiting program...[/yellow]")
            break


if __name__ == "__main__":
    interactive_cli()
