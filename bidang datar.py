print("SELAMAT DATANG DI WEBSITE LUAS BANGUN DATAR")
print("1. Persegi")
print("2. Persegi Panjang")
print("3. Segitiga")
print("4. Lingkaran")
print("5. Jajar Genjang")
print("6. Layang-Layang")
print("7. Trapesium")
print("8. Tabung")
print("9. Kerucut")

pilihan=int(input("Tentukan Pilihan Anda"))

if pilihan==1:
    sisi=int(input("Tentukan Nilai Sisi"))
    luas=sisi*sisi
    print("Luas Persegi=",luas)

elif pilihan==2:
    panjang=int(input("Tentukan Nilai Panjang"))
    lebar=int(input("Tentukan Nilai Lebar"))
    luas=panjang*lebar
    print("Luas Persegi Panjang=",luas)

elif pilihan==3:
    alas=int(input("Tentukan Nilai Alas"))
    tinggi=int(input("Tentukan Nilai Tinggi"))
    luas=alas*tinggi/2
    print("Luas Segitiga=",luas)

elif pilihan==4:
    r=int(input("Tentukan Nilai Jari-Jari"))
    luas=3.14*r*r
    print("Luas Lingkaran=",luas)

elif pilihan==5:
    alas=int(input("Tentukan Nilai Alas"))
    tinggi=int(input("Tentukan Nilai Tinggi"))
    luas=alas*tinggi
    print("Luas Jajar Genjang=",luas)

elif pilihan==6:
    d1=int(input("Tentukan Nilai Diagonal 1"))
    d2=int(input("Tentukan Nilai Diagonal 2"))
    luas=0.5*d1*d2
    print("Luas Layang-Layang=",luas)

elif pilihan==7:
    alasA=int(input("Tentukan Nilai Alas A"))
    alasB=int(input("Tentukan Nilai Alas B"))
    tinggi=int(input("Tentukan Nilai Tinggi"))
    luas=0.5*(alasA+alasB)*tinggi
    print("Luas Trapesium=",luas)

elif pilihan==8:
    r=int(input("Tentukan Nilai Jari-Jari"))
    tinggi=int(input("Tentukan Nilai Tinggi"))
    luas=2*3.14*r*(r+tinggi)
    print("Luas Tabung=",luas)

elif pilihan==9:
    s=int(input("Tentukan Nilai Garis Pelukis"))
    r=int(input("Tentukan Nilai Jari-Jari"))
    luas=3.14*r*(s+r)
    print("Luas Kerucut=",luas)

else:
    print("NOTE= Pilihan Anda Tidak Tersedia")
