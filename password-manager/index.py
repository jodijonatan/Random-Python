# ─── Import Library ────────────────────────────────────────────────────────────
import os
import json
import time
import uuid
import random
import string
import hashlib
import getpass
import base64
from datetime import datetime

# Rich: library tampilan terminal yang modern dan berwarna
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint
from rich.text import Text
from rich.columns import Columns
from rich.align import Align

# Pyperclip: copy ke clipboard (opsional, handle jika tidak ada)
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

# ─── Konfigurasi Global ────────────────────────────────────────────────────────
console = Console()
DATA_FILE = "passwords.json"          # File penyimpanan data
SALT = "SecureVault_2024_Salt_Key"    # Salt untuk hashing (bisa diganti)
MIN_PASSWORD_LENGTH = 6               # Minimal panjang master password

# ─── Enkripsi Sederhana (Base64 XOR) ──────────────────────────────────────────
def simple_encrypt(text: str, key: str) -> str:
    """
    Enkripsi sederhana menggunakan XOR + Base64.
    Tidak sekuat AES, tapi cukup untuk pemula.
    
    Args:
        text: Teks yang akan dienkripsi
        key: Kunci enkripsi (master password)
    
    Returns:
        String terenkripsi dalam format Base64
    """
    # Buat key stream berulang sepanjang text
    key_stream = (key * (len(text) // len(key) + 1))[:len(text)]
    
    # XOR setiap karakter dengan key stream
    encrypted_bytes = bytes(ord(c) ^ ord(k) for c, k in zip(text, key_stream))
    
    # Encode ke Base64 agar aman disimpan sebagai string
    return base64.b64encode(encrypted_bytes).decode('utf-8')


def simple_decrypt(encrypted_text: str, key: str) -> str:
    """
    Dekripsi teks yang sudah dienkripsi dengan simple_encrypt.
    
    Args:
        encrypted_text: Teks terenkripsi dalam format Base64
        key: Kunci dekripsi (harus sama dengan kunci enkripsi)
    
    Returns:
        Teks asli yang sudah didekripsi
    """
    # Decode dari Base64
    encrypted_bytes = base64.b64decode(encrypted_text.encode('utf-8'))
    
    # Buat key stream yang sama
    key_stream = (key * (len(encrypted_bytes) // len(key) + 1))[:len(encrypted_bytes)]
    
    # XOR kembali untuk mendapatkan teks asli
    decrypted = ''.join(chr(b ^ ord(k)) for b, k in zip(encrypted_bytes, key_stream))
    
    return decrypted


def hash_password(password: str) -> str:
    """
    Hash password menggunakan SHA-256 dengan salt.
    Digunakan untuk menyimpan master password dengan aman.
    
    Args:
        password: Password yang akan di-hash
    
    Returns:
        String hash dalam format hex
    """
    salted = f"{SALT}{password}{SALT}"
    return hashlib.sha256(salted.encode()).hexdigest()


# ─── Manajemen File JSON ───────────────────────────────────────────────────────
def load_data() -> dict:
    """
    Muat data dari file JSON.
    Jika file belum ada, kembalikan struktur data kosong.
    
    Returns:
        Dictionary berisi master_hash dan list passwords
    """
    if not os.path.exists(DATA_FILE):
        # Kembalikan struktur data default jika file belum ada
        return {
            "master_hash": None,
            "passwords": []
        }
    
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Jika file rusak, kembalikan data kosong
        console.print("[red]⚠ File data rusak! Membuat data baru...[/red]")
        return {
            "master_hash": None,
            "passwords": []
        }


def save_data(data: dict) -> bool:
    """
    Simpan data ke file JSON dengan format yang rapi.
    
    Args:
        data: Dictionary data yang akan disimpan
    
    Returns:
        True jika berhasil, False jika gagal
    """
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except IOError as e:
        console.print(f"[red]✗ Gagal menyimpan data: {e}[/red]")
        return False


# ─── Tampilan UI ───────────────────────────────────────────────────────────────
def clear_screen():
    """Bersihkan layar terminal (support Windows & Unix/Linux/Mac)."""
    os.system('cls' if os.name == 'nt' else 'clear')


def show_banner():
    """Tampilkan banner ASCII art aplikasi."""
    banner_text = """
 ██████╗ █████╗  ██████╗██╗   ██╗██████╗ ███████╗
██╔════╝██╔══██╗██╔════╝██║   ██║██╔══██╗██╔════╝
╚█████╗ ███████║██║     ██║   ██║██████╔╝█████╗  
 ╚═══██╗██╔══██║██║     ██║   ██║██╔══██╗██╔══╝  
██████╔╝██║  ██║╚██████╗╚██████╔╝██║  ██║███████╗
╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
       ██╗   ██╗ █████╗ ██╗   ██╗██╗  ████████╗
       ██║   ██║██╔══██╗██║   ██║██║  ╚══██╔══╝
       ██║   ██║███████║██║   ██║██║     ██║   
       ╚██╗ ██╔╝██╔══██║██║   ██║██║     ██║   
        ╚████╔╝ ██║  ██║╚██████╔╝███████╗██║   
         ╚═══╝  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝   
"""
    console.print(Panel(
        Align.center(
            Text(banner_text, style="bold cyan") +
            Text("\n🔐 Password Manager Modern  v1.0.0\n", style="bold yellow") +
            Text("Kelola password Anda dengan aman & mudah", style="dim white")
        ),
        border_style="cyan",
        padding=(0, 2)
    ))


def show_loading(message: str, duration: float = 1.5):
    """
    Tampilkan animasi loading sederhana.
    
    Args:
        message: Pesan yang ditampilkan saat loading
        duration: Durasi loading dalam detik
    """
    with Progress(
        SpinnerColumn(style="cyan"),
        TextColumn(f"[cyan]{message}...[/cyan]"),
        console=console,
        transient=True  # Hapus progress bar setelah selesai
    ) as progress:
        task = progress.add_task("", total=100)
        steps = int(duration * 20)  # 20 langkah per detik
        for _ in range(steps):
            progress.update(task, advance=100 / steps)
            time.sleep(duration / steps)


def show_menu():
    """Tampilkan menu utama interaktif."""
    menu_items = [
        ("1", "👁  Lihat Semua Password", "cyan"),
        ("2", "➕  Tambah Password Baru", "green"),
        ("3", "🔍  Cari Password", "yellow"),
        ("4", "🗑  Hapus Password", "red"),
        ("5", "🎲  Generate Password Acak", "magenta"),
        ("6", "📊  Statistik", "blue"),
        ("0", "🚪  Keluar", "white"),
    ]
    
    # Buat grid menu dengan dua kolom
    menu_text = Text()
    for number, label, color in menu_items:
        menu_text.append(f"  [{number}]", style=f"bold {color}")
        menu_text.append(f"  {label}\n", style="white")
    
    console.print(Panel(
        menu_text,
        title="[bold cyan]📋 MENU UTAMA[/bold cyan]",
        border_style="cyan",
        padding=(1, 3)
    ))


# ─── Autentikasi Master Password ──────────────────────────────────────────────
def setup_master_password(data: dict) -> str:
    """
    Setup master password pertama kali.
    
    Args:
        data: Dictionary data aplikasi
    
    Returns:
        Master password yang dibuat
    """
    console.print(Panel(
        "[yellow]⚠ Belum ada master password!\n[/yellow]"
        "[white]Buat master password yang kuat untuk melindungi data Anda.[/white]\n"
        f"[dim]Minimal {MIN_PASSWORD_LENGTH} karakter[/dim]",
        title="[bold yellow]SETUP PERTAMA KALI[/bold yellow]",
        border_style="yellow"
    ))
    
    while True:
        # Gunakan getpass agar password tidak terlihat saat diketik
        password = getpass.getpass("  🔑 Buat Master Password: ")
        
        # Validasi panjang password
        if len(password) < MIN_PASSWORD_LENGTH:
            console.print(f"[red]  ✗ Password minimal {MIN_PASSWORD_LENGTH} karakter![/red]")
            continue
        
        # Konfirmasi password
        confirm = getpass.getpass("  🔑 Konfirmasi Master Password: ")
        
        if password != confirm:
            console.print("[red]  ✗ Password tidak cocok! Coba lagi.[/red]")
            continue
        
        # Simpan hash master password
        data["master_hash"] = hash_password(password)
        save_data(data)
        
        console.print("[green]  ✓ Master password berhasil dibuat![/green]")
        show_loading("Menyimpan konfigurasi", 1.0)
        return password


def login(data: dict) -> str | None:
    """
    Proses login dengan master password.
    Berikan 3 kesempatan percobaan.
    
    Args:
        data: Dictionary data aplikasi
    
    Returns:
        Master password jika berhasil, None jika gagal
    """
    max_attempts = 3
    
    for attempt in range(1, max_attempts + 1):
        # Gunakan getpass agar password tidak terlihat
        password = getpass.getpass(f"  🔑 Master Password [{attempt}/{max_attempts}]: ")
        
        # Verifikasi dengan membandingkan hash
        if hash_password(password) == data["master_hash"]:
            console.print("[green]  ✓ Login berhasil! Selamat datang.[/green]")
            show_loading("Memuat data", 1.0)
            return password
        else:
            remaining = max_attempts - attempt
            if remaining > 0:
                console.print(f"[red]  ✗ Password salah! {remaining} percobaan tersisa.[/red]")
            else:
                console.print("[red]  ✗ Terlalu banyak percobaan gagal! Keluar.[/red]")
    
    return None


# ─── Fungsi Utama Password Manager ────────────────────────────────────────────
def view_all_passwords(data: dict, master_password: str):
    """
    Tampilkan semua password tersimpan dalam tabel yang rapi.
    Password ditampilkan dalam bentuk terenkripsi (bintang).
    
    Args:
        data: Dictionary data aplikasi
        master_password: Master password untuk dekripsi
    """
    clear_screen()
    passwords = data.get("passwords", [])
    
    if not passwords:
        console.print(Panel(
            Align.center("[yellow]📭 Belum ada password tersimpan.\nGunakan menu [2] untuk menambah password.[/yellow]"),
            title="[bold cyan]SEMUA PASSWORD[/bold cyan]",
            border_style="cyan"
        ))
        input("\n  Tekan Enter untuk kembali...")
        return
    
    # Buat tabel dengan kolom yang menarik
    table = Table(
        title=f"🔐 Semua Password ({len(passwords)} entri)",
        border_style="cyan",
        header_style="bold cyan",
        show_lines=True,
        min_width=70
    )
    
    # Definisi kolom tabel
    table.add_column("#", style="dim", width=4, justify="center")
    table.add_column("🌐 Website/App", style="bold white", min_width=20)
    table.add_column("👤 Username/Email", style="cyan", min_width=25)
    table.add_column("🔑 Password", style="green", min_width=15)
    table.add_column("📅 Ditambahkan", style="dim", min_width=18)
    
    # Isi tabel dengan data password
    for i, entry in enumerate(passwords, 1):
        # Dekripsi password untuk ditampilkan (sembunyikan dengan bintang)
        try:
            decrypted_pass = simple_decrypt(entry["password"], master_password)
            # Sembunyikan password: tampilkan 2 karakter pertama + bintang
            masked = decrypted_pass[:2] + "●" * (len(decrypted_pass) - 2) if len(decrypted_pass) > 2 else "●●●●●●"
        except Exception:
            masked = "[red]Error dekripsi[/red]"
        
        table.add_row(
            str(i),
            entry.get("website", "-"),
            entry.get("username", "-"),
            masked,
            entry.get("created_at", "-")
        )
    
    console.print(table)
    
    # Opsi untuk melihat password asli
    console.print("\n[dim]Ketik nomor untuk melihat detail, atau tekan Enter untuk kembali:[/dim]")
    choice = input("  → ").strip()
    
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(passwords):
            show_password_detail(passwords[idx], master_password)


def show_password_detail(entry: dict, master_password: str):
    """
    Tampilkan detail lengkap satu entri password.
    
    Args:
        entry: Dictionary satu entri password
        master_password: Master password untuk dekripsi
    """
    try:
        decrypted_pass = simple_decrypt(entry["password"], master_password)
    except Exception:
        decrypted_pass = "[Error dekripsi]"
    
    # Panel detail yang menarik
    detail_text = Text()
    detail_text.append("  🌐 Website   : ", style="dim")
    detail_text.append(f"{entry.get('website', '-')}\n", style="bold cyan")
    detail_text.append("  👤 Username  : ", style="dim")
    detail_text.append(f"{entry.get('username', '-')}\n", style="bold white")
    detail_text.append("  🔑 Password  : ", style="dim")
    detail_text.append(f"{decrypted_pass}\n", style="bold green")
    detail_text.append("  📅 Dibuat    : ", style="dim")
    detail_text.append(f"{entry.get('created_at', '-')}\n", style="white")
    detail_text.append("  🔄 Diperbarui: ", style="dim")
    detail_text.append(f"{entry.get('updated_at', '-')}", style="white")
    
    console.print(Panel(
        detail_text,
        title=f"[bold cyan]Detail: {entry.get('website', '')}[/bold cyan]",
        border_style="green",
        padding=(1, 2)
    ))
    
    # Opsi copy ke clipboard
    if CLIPBOARD_AVAILABLE:
        if Confirm.ask("  📋 Copy password ke clipboard?", default=False):
            pyperclip.copy(decrypted_pass)
            console.print("[green]  ✓ Password berhasil disalin ke clipboard![/green]")
    
    input("\n  Tekan Enter untuk kembali...")


def add_password(data: dict, master_password: str):
    """
    Tambah entri password baru.
    
    Args:
        data: Dictionary data aplikasi (akan dimodifikasi)
        master_password: Master password untuk enkripsi
    """
    clear_screen()
    console.print(Panel(
        "[white]Isi informasi password baru di bawah ini.\n[dim]Ketik 'batal' untuk membatalkan.[/dim][/white]",
        title="[bold green]➕ TAMBAH PASSWORD BARU[/bold green]",
        border_style="green"
    ))
    
    # Input website/aplikasi dengan validasi
    while True:
        website = Prompt.ask("  🌐 Nama Website/Aplikasi").strip()
        if website.lower() == 'batal':
            console.print("[yellow]  ↩ Dibatalkan.[/yellow]")
            return
        if not website:
            console.print("[red]  ✗ Nama tidak boleh kosong![/red]")
            continue
        break
    
    # Cek duplikat website
    existing = [p for p in data["passwords"] if p["website"].lower() == website.lower()]
    if existing:
        console.print(f"[yellow]  ⚠ Website '{website}' sudah ada ({len(existing)} entri).[/yellow]")
        if not Confirm.ask("  Tetap tambahkan?", default=True):
            return
    
    # Input username/email
    while True:
        username = Prompt.ask("  👤 Username/Email").strip()
        if username.lower() == 'batal':
            console.print("[yellow]  ↩ Dibatalkan.[/yellow]")
            return
        if not username:
            console.print("[red]  ✗ Username tidak boleh kosong![/red]")
            continue
        break
    
    # Input atau generate password
    console.print("\n  [dim]Pilih cara mengisi password:[/dim]")
    console.print("  [cyan][1][/cyan] Ketik password sendiri")
    console.print("  [cyan][2][/cyan] Generate password otomatis")
    
    while True:
        pass_choice = input("\n  Pilihan (1/2): ").strip()
        if pass_choice == '1':
            # Input manual dengan getpass (tersembunyi)
            while True:
                password = getpass.getpass("  🔑 Password: ")
                if not password:
                    console.print("[red]  ✗ Password tidak boleh kosong![/red]")
                    continue
                confirm = getpass.getpass("  🔑 Konfirmasi Password: ")
                if password != confirm:
                    console.print("[red]  ✗ Password tidak cocok![/red]")
                    continue
                break
            break
        elif pass_choice == '2':
            password = generate_strong_password()
            console.print(f"  [green]✓ Password generated: [bold]{password}[/bold][/green]")
            break
        else:
            console.print("[red]  ✗ Pilih 1 atau 2![/red]")
    
    # Enkripsi password sebelum disimpan
    encrypted_password = simple_encrypt(password, master_password)
    
    # Buat entri baru
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_entry = {
        "id": str(uuid.uuid4()),           # ID unik untuk setiap entri
        "website": website,
        "username": username,
        "password": encrypted_password,    # Disimpan dalam bentuk terenkripsi
        "created_at": now,
        "updated_at": now
    }
    
    # Tambahkan ke data dan simpan
    data["passwords"].append(new_entry)
    
    show_loading("Menyimpan password")
    if save_data(data):
        console.print(Panel(
            f"[green]✓ Password untuk [bold]{website}[/bold] berhasil disimpan![/green]",
            border_style="green"
        ))
    
    # Tawarkan copy ke clipboard
    if CLIPBOARD_AVAILABLE and Confirm.ask("  📋 Copy password ke clipboard?", default=False):
        pyperclip.copy(password)
        console.print("[green]  ✓ Password disalin ke clipboard![/green]")
    
    input("\n  Tekan Enter untuk kembali...")


def search_password(data: dict, master_password: str):
    """
    Cari password berdasarkan nama website atau username.
    
    Args:
        data: Dictionary data aplikasi
        master_password: Master password untuk dekripsi
    """
    clear_screen()
    console.print(Panel(
        "[white]Cari password berdasarkan nama website atau username.[/white]",
        title="[bold yellow]🔍 CARI PASSWORD[/bold yellow]",
        border_style="yellow"
    ))
    
    query = Prompt.ask("  🔎 Kata kunci pencarian").strip().lower()
    
    if not query:
        console.print("[red]  ✗ Kata kunci tidak boleh kosong![/red]")
        input("\n  Tekan Enter untuk kembali...")
        return
    
    # Filter password yang cocok dengan kata kunci
    results = [
        p for p in data["passwords"]
        if query in p.get("website", "").lower() or 
           query in p.get("username", "").lower()
    ]
    
    if not results:
        console.print(Panel(
            f"[yellow]📭 Tidak ditemukan password dengan kata kunci '[bold]{query}[/bold]'[/yellow]",
            border_style="yellow"
        ))
        input("\n  Tekan Enter untuk kembali...")
        return
    
    # Tampilkan hasil pencarian
    table = Table(
        title=f"🔍 Hasil pencarian: '{query}' ({len(results)} ditemukan)",
        border_style="yellow",
        header_style="bold yellow",
        show_lines=True
    )
    
    table.add_column("#", width=4, justify="center")
    table.add_column("🌐 Website/App", style="bold white", min_width=20)
    table.add_column("👤 Username/Email", style="cyan", min_width=25)
    table.add_column("📅 Ditambahkan", style="dim", min_width=18)
    
    for i, entry in enumerate(results, 1):
        table.add_row(
            str(i),
            entry.get("website", "-"),
            entry.get("username", "-"),
            entry.get("created_at", "-")
        )
    
    console.print(table)
    
    # Pilih untuk lihat detail
    console.print("\n[dim]Ketik nomor untuk melihat detail, atau tekan Enter untuk kembali:[/dim]")
    choice = input("  → ").strip()
    
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(results):
            show_password_detail(results[idx], master_password)


def delete_password(data: dict):
    """
    Hapus entri password berdasarkan pilihan pengguna.
    
    Args:
        data: Dictionary data aplikasi (akan dimodifikasi)
    """
    clear_screen()
    passwords = data.get("passwords", [])
    
    if not passwords:
        console.print(Panel(
            "[yellow]📭 Tidak ada password untuk dihapus.[/yellow]",
            title="[bold red]🗑 HAPUS PASSWORD[/bold red]",
            border_style="red"
        ))
        input("\n  Tekan Enter untuk kembali...")
        return
    
    console.print(Panel(
        "[white]Pilih password yang ingin dihapus.[/white]",
        title="[bold red]🗑 HAPUS PASSWORD[/bold red]",
        border_style="red"
    ))
    
    # Tampilkan daftar password
    table = Table(border_style="red", header_style="bold red", show_lines=True)
    table.add_column("#", width=4, justify="center")
    table.add_column("🌐 Website/App", style="bold white", min_width=20)
    table.add_column("👤 Username/Email", style="cyan", min_width=25)
    
    for i, entry in enumerate(passwords, 1):
        table.add_row(str(i), entry.get("website", "-"), entry.get("username", "-"))
    
    console.print(table)
    
    # Input nomor yang akan dihapus
    while True:
        choice = input(f"\n  Nomor yang dihapus (1-{len(passwords)}, atau 0 untuk batal): ").strip()
        
        if choice == '0':
            console.print("[yellow]  ↩ Dibatalkan.[/yellow]")
            input("\n  Tekan Enter untuk kembali...")
            return
        
        if not choice.isdigit():
            console.print("[red]  ✗ Masukkan angka yang valid![/red]")
            continue
        
        idx = int(choice) - 1
        if not (0 <= idx < len(passwords)):
            console.print(f"[red]  ✗ Nomor harus antara 1 dan {len(passwords)}![/red]")
            continue
        
        break
    
    # Konfirmasi penghapusan
    target = passwords[idx]
    console.print(f"\n  [yellow]⚠ Anda akan menghapus:[/yellow]")
    console.print(f"  Website : [bold]{target.get('website')}[/bold]")
    console.print(f"  Username: [bold]{target.get('username')}[/bold]")
    
    if Confirm.ask("\n  [red]Yakin ingin menghapus? (tidak bisa dikembalikan)[/red]", default=False):
        deleted_website = passwords.pop(idx)["website"]
        
        show_loading("Menghapus data")
        if save_data(data):
            console.print(f"[green]  ✓ Password untuk '{deleted_website}' berhasil dihapus![/green]")
    else:
        console.print("[yellow]  ↩ Penghapusan dibatalkan.[/yellow]")
    
    input("\n  Tekan Enter untuk kembali...")


def generate_strong_password(length: int = 16) -> str:
    """
    Generate password acak yang kuat.
    Mengandung huruf besar, huruf kecil, angka, dan simbol.
    
    Args:
        length: Panjang password yang diinginkan (default: 16)
    
    Returns:
        String password yang kuat dan acak
    """
    # Definisi karakter yang digunakan
    lowercase = string.ascii_lowercase    # a-z
    uppercase = string.ascii_uppercase    # A-Z
    digits = string.digits                # 0-9
    symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"  # Simbol umum
    
    # Gabungkan semua karakter
    all_chars = lowercase + uppercase + digits + symbols
    
    # Pastikan minimal 1 karakter dari setiap kategori (password lebih kuat)
    password_chars = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(symbols),
    ]
    
    # Isi sisa panjang dengan karakter acak
    for _ in range(length - 4):
        password_chars.append(random.choice(all_chars))
    
    # Acak urutan karakter agar tidak terprediksi
    random.shuffle(password_chars)
    
    return ''.join(password_chars)


def show_password_generator():
    """
    Menu interaktif untuk generate password acak.
    Pengguna bisa memilih panjang dan meng-generate ulang.
    """
    clear_screen()
    console.print(Panel(
        "[white]Generate password acak yang kuat untuk digunakan.[/white]",
        title="[bold magenta]🎲 PASSWORD GENERATOR[/bold magenta]",
        border_style="magenta"
    ))
    
    # Input panjang password
    while True:
        length_str = Prompt.ask("  📏 Panjang password", default="16")
        if length_str.isdigit() and 8 <= int(length_str) <= 64:
            length = int(length_str)
            break
        console.print("[red]  ✗ Panjang harus antara 8-64![/red]")
    
    # Loop generate password
    while True:
        password = generate_strong_password(length)
        
        # Hitung kekuatan password
        strength = calculate_password_strength(password)
        strength_color = "green" if strength >= 80 else "yellow" if strength >= 50 else "red"
        
        console.print(Panel(
            Align.center(
                Text(f"\n{password}\n", style="bold white") +
                Text(f"\nKekuatan: ", style="white") +
                Text(f"{'█' * (strength // 10)}{'░' * (10 - strength // 10)} {strength}%\n", style=strength_color) +
                Text(f"\nPanjang: {len(password)} karakter", style="dim")
            ),
            title="[bold magenta]Password Generated[/bold magenta]",
            border_style="magenta",
            padding=(1, 4)
        ))
        
        # Opsi setelah generate
        console.print("  [cyan][1][/cyan] Generate ulang")
        console.print("  [cyan][2][/cyan] Copy ke clipboard")
        console.print("  [cyan][0][/cyan] Kembali ke menu")
        
        choice = input("\n  Pilihan: ").strip()
        
        if choice == '1':
            clear_screen()
            continue
        elif choice == '2':
            if CLIPBOARD_AVAILABLE:
                pyperclip.copy(password)
                console.print("[green]  ✓ Password disalin ke clipboard![/green]")
            else:
                console.print("[yellow]  ⚠ Clipboard tidak tersedia. Install: pip install pyperclip[/yellow]")
            input("\n  Tekan Enter untuk kembali...")
            break
        elif choice == '0':
            break


def calculate_password_strength(password: str) -> int:
    """
    Hitung skor kekuatan password (0-100).
    
    Args:
        password: Password yang akan dinilai
    
    Returns:
        Skor antara 0-100
    """
    score = 0
    
    # Panjang password
    if len(password) >= 8:  score += 15
    if len(password) >= 12: score += 15
    if len(password) >= 16: score += 10
    
    # Variasi karakter
    if any(c.islower() for c in password):  score += 15
    if any(c.isupper() for c in password):  score += 15
    if any(c.isdigit() for c in password):  score += 15
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password): score += 15
    
    return min(score, 100)


def show_statistics(data: dict):
    """
    Tampilkan statistik singkat tentang password tersimpan.
    
    Args:
        data: Dictionary data aplikasi
    """
    clear_screen()
    passwords = data.get("passwords", [])
    total = len(passwords)
    
    if total == 0:
        console.print(Panel(
            "[yellow]📭 Belum ada data password.[/yellow]",
            title="[bold blue]📊 STATISTIK[/bold blue]",
            border_style="blue"
        ))
        input("\n  Tekan Enter untuk kembali...")
        return
    
    # Hitung statistik
    websites = set(p.get("website", "") for p in passwords)
    
    stats_text = Text()
    stats_text.append(f"\n  📦 Total Password   : ", style="dim")
    stats_text.append(f"{total}\n", style="bold cyan")
    stats_text.append(f"  🌐 Website Unik     : ", style="dim")
    stats_text.append(f"{len(websites)}\n", style="bold cyan")
    stats_text.append(f"  📁 File Data        : ", style="dim")
    stats_text.append(f"{DATA_FILE}\n", style="bold white")
    
    if passwords:
        latest = max(passwords, key=lambda p: p.get("created_at", ""))
        stats_text.append(f"\n  🕐 Password Terakhir: ", style="dim")
        stats_text.append(f"{latest.get('website', '-')} ({latest.get('created_at', '-')})\n", style="white")
    
    # Cek ketersediaan fitur
    stats_text.append(f"\n  📋 Clipboard        : ", style="dim")
    stats_text.append(
        "✓ Tersedia\n" if CLIPBOARD_AVAILABLE else "✗ Tidak tersedia (pip install pyperclip)\n",
        style="green" if CLIPBOARD_AVAILABLE else "red"
    )
    
    console.print(Panel(
        stats_text,
        title="[bold blue]📊 STATISTIK SECUREVAULT[/bold blue]",
        border_style="blue",
        padding=(1, 2)
    ))
    
    input("\n  Tekan Enter untuk kembali...")


# ─── Main Program ──────────────────────────────────────────────────────────────
def main():
    """
    Fungsi utama program.
    Mengelola alur aplikasi dari login hingga menu interaktif.
    """
    clear_screen()
    show_banner()
    
    # Muat data dari file
    data = load_data()
    
    # Cek apakah sudah ada master password
    if data["master_hash"] is None:
        # Setup pertama kali
        master_password = setup_master_password(data)
    else:
        # Login dengan master password yang sudah ada
        master_password = login(data)
        if master_password is None:
            console.print("\n[red]Program dihentikan karena autentikasi gagal.[/red]\n")
            return
    
    # Loop menu utama
    while True:
        clear_screen()
        show_banner()
        
        # Tampilkan info singkat
        total_pass = len(data.get("passwords", []))
        console.print(f"  [dim]📦 {total_pass} password tersimpan  |  📁 {DATA_FILE}[/dim]\n")
        
        show_menu()
        
        # Input pilihan menu
        choice = input("\n  → Pilih menu: ").strip()
        
        # Routing menu
        if choice == '1':
            view_all_passwords(data, master_password)
        elif choice == '2':
            add_password(data, master_password)
        elif choice == '3':
            search_password(data, master_password)
        elif choice == '4':
            delete_password(data)
        elif choice == '5':
            show_password_generator()
        elif choice == '6':
            show_statistics(data)
        elif choice == '0':
            # Konfirmasi keluar
            if Confirm.ask("\n  🚪 Yakin ingin keluar?", default=True):
                clear_screen()
                console.print(Panel(
                    Align.center(
                        "[bold cyan]Terima kasih telah menggunakan SecureVault! 🔐[/bold cyan]\n"
                        "[dim]Password Anda tetap aman.[/dim]"
                    ),
                    border_style="cyan",
                    padding=(1, 4)
                ))
                break
        else:
            console.print("[red]  ✗ Pilihan tidak valid! Masukkan angka 0-6.[/red]")
            time.sleep(1)


# ─── Entry Point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Handle Ctrl+C dengan elegan
        console.print("\n\n[yellow]  ⚠ Program dihentikan oleh pengguna (Ctrl+C).[/yellow]\n")