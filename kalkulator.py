from tkinter import*

root=Tk()

def tampil(angka):
    current_text = E1.get()
    E1.delete(0, END)  
    E1.insert(0, current_text + str(angka))

def hapus():
    E1.delete(0, END)

def tambah():
    angka_awal=E1.get()
    global angka_sekarang
    global operator
    operator="tambah"
    angka_sekarang=int(E1.get())
    E1.delete(0, END)

def kurang():
    angka_awal=E1.get()
    global angka_sekarang
    global operator
    operator="kurang"
    angka_sekarang=int(E1.get())
    E1.delete(0, END)

def bagi():
    angka_awal=E1.get()
    global angka_sekarang
    global operator
    operator="bagi"
    angka_sekarang=int(E1.get())
    E1.delete(0, END)

def kali():
    angka_awal=E1.get()
    global angka_sekarang
    global operator
    operator="kali"
    angka_sekarang=int(E1.get())
    E1.delete(0, END)

def sama_dengan():
    angka_kedua = int(E1.get())
    if operator == "tambah":
        hasil = angka_sekarang + angka_kedua
        E1.delete(0, END)
        E1.insert(0, hasil)
    elif operator == "kurang":
        hasil = angka_sekarang - angka_kedua
        E1.delete(0, END)
        E1.insert(0, hasil)
    elif operator == "bagi":
        hasil = angka_sekarang / angka_kedua
        E1.delete(0, END)
        E1.insert(0, hasil)
    elif operator == "kali":
        hasil = angka_sekarang * angka_kedua
        E1.delete(0, END)
        E1.insert(0, hasil)
                                                                                                      

                                                                                                      
E1=Entry(root)
E1.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

B1=Button(root, text="1", command=lambda:tampil(1))
B1.grid(row=1, column=0, padx=10, pady=10)

B2=Button(root, text="2", command=lambda:tampil(2))
B2.grid(row=1, column=1, padx=10, pady=10)

B3=Button(root, text="3", command=lambda:tampil(3))
B3.grid(row=1, column=2, padx=10, pady=10)

B4=Button(root, text="4", command=lambda:tampil(4))
B4.grid(row=2, column=0, padx=10, pady=10)

B5=Button(root, text="5", command=lambda:tampil(5))
B5.grid(row=2, column=1, padx=10, pady=10)

B6=Button(root, text="6", command=lambda:tampil(6))
B6.grid(row=2, column=2, padx=10, pady=10)

B7=Button(root, text="7", command=lambda:tampil(7))
B7.grid(row=3, column=0, padx=10, pady=10)

B8=Button(root, text="8", command=lambda:tampil(8))
B8.grid(row=3, column=1, padx=10, pady=10)

B9=Button(root, text="9", command=lambda:tampil(9))
B9.grid(row=3, column=2, padx=10, pady=10)

B10=Button(root, text="0", command=lambda:tampil(0))
B10.grid(row=4, column=1, padx=10, pady=10)

B11=Button(root, text="-", command=kurang)
B11.grid(row=1, column=3, padx=10, pady=10)

B12=Button(root, text="+", command=tambah)
B12.grid(row=2, column=3, padx=10, pady=10)

B13=Button(root, text="*", command=kali)
B13.grid(row=3, column=3, padx=10, pady=10)

B14=Button(root, text="/", command=bagi)
B14.grid(row=4, column=3, padx=10, pady=10)

B15=Button(root, text="=", command=sama_dengan)
B15.grid(row=4, column=2, padx=10, pady=10)

B16=Button(root, text="C", command=hapus)
B16.grid(row=4, column=0, padx=10, pady=10)

root.mainloop()