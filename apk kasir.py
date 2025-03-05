print("Coffee Joe")
print("1. Milk Coffee $7")
print("2. Chocolate Coffee $5")
print("3. Americano $10")
print("4. Coffee Latte $9")
harga=0
pilihan=int(input("Tentukan Pilihan"))
if pilihan==1:
    print("Anda membeli milk coffee= $7")
    harga+=5
elif pilihan==2:
    print("Anda membeli chocolate= $5")
    harga+=5
elif pilihan==3:
    print("Anda membeli americano= $10")
    harga+=10
elif pilihan==4:
    print("Anda membeli coffee latte= $9")
    harga+=9
else:
    print("Pilihan tidak tersedia")
bayar=int(input("Tentukan nominal pembayaran= $"))
kembalian:print("Kembalian= $",(bayar-harga))
if bayar>harga:
    print("Terima kasih telah berbelanja")
elif bayar<harga:
    print("Uang anda tidak mencukupi")
