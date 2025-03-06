siswa=[]
while True:
    print("1. Tambah Siswa")
    print("2. Hapus Siswa")
    print("3. Tampilkan Siswa")
    pilihan=int(input("Tentukan Pilihan Anda"))
    if pilihan==1:
        print("1. No Absen")
        print("2. Nama Siswa")
        pilihanTambah=int(input("Tentukan Pilihan Anda"))
        if pilihanTambah==1:
            no_absen=int(input("Tentukan Nomor Absen"))
            siswa.append(no_absen)
        elif pilihanTambah==2:
            nama=str(input("Tentukan Nama Siswa"))
            siswa.append(nama)

    elif pilihan==2:
        print("1. No Absen")
        print("2. Nama Siswa")
        pilihanHapus=int(input("Tentukan Pilihan Anda"))
        if pilihanHapus==1:
            no_absen=int(input("Tentukan Nomor Absen"))
            siswa.remove(no_absen)
        elif pilihanHapus==2:
            nama=str(input("Tentukan Nama Siswa"))
            siswa.remove(nama)

    elif pilihan==3:
        print(siswa)

    else:
        print("Pilihan Tidak Tersedia")
