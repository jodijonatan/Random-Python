from time import sleep
import sys

def print_lirik():
    # Lirik dan waktu delay per karakter
    line = [
        ("Aku yang jatuh cinta", 0.10),
        ("haruskah kuberi kesempatan", 0.07),
        ("ingin aku jadi kekasih yang baik", 0.07),
        ("berikan aku kesempatan oh", 0.8),
        ("tahukah dirimu? tahukah hatimu?", 0.06),
        ("berulang terketuk, aku mencinta mu", 0.08),
        ("tapi dirimu tak pernah sadari", 0.05),
        ("aku yang jatuh cinta", 0.10),
    ]
    # Waktu delay antar baris
    delays = [1.2, 3, 2.5, 7.5, 3.5, 4, 3.5, 3.5]

    # Loop untuk menampilkan lirik
    for i, (lirik, char_delay) in enumerate(line):
        for char in lirik:
            print(char, end='', flush=True)
            sleep(char_delay)  # Delay antar karakter
        sleep(delays[i])  # Delay antar baris

# Menjalankan fungsi untuk menampilkan lirik
print_lirik()
