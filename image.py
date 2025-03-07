import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageViewer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Keren Image Viewer")
        self.geometry("800x600")

        # Variabel untuk gambar dan zoom level
        self.image = None
        self.tk_image = None
        self.zoom_level = 1.0

        # Frame utama
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas untuk menampilkan gambar
        self.canvas = tk.Canvas(self.main_frame, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar untuk canvas
        self.scrollbar_y = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        # Menambahkan tombol untuk membuka gambar
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.open_button = tk.Button(self.button_frame, text="Open Image", command=self.open_image)
        self.open_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.zoom_in_button = tk.Button(self.button_frame, text="Zoom In", command=self.zoom_in)
        self.zoom_in_button.pack(side=tk.LEFT, padx=10)

        self.zoom_out_button = tk.Button(self.button_frame, text="Zoom Out", command=self.zoom_out)
        self.zoom_out_button.pack(side=tk.LEFT, padx=10)

    def open_image(self):
        # Pilih file gambar
        filepath = filedialog.askopenfilename(
            title="Open an Image",
            filetypes=[("Image Files", ".png .jpg .jpeg .gif .bmp")]
        )
        
        if filepath:
            self.image = Image.open(filepath)
            self.zoom_level = 1.0
            self.display_image()

    def display_image(self):
        # Resize image sesuai dengan zoom level
        if self.image:
            width, height = self.image.size
            new_size = (int(width * self.zoom_level), int(height * self.zoom_level))
            
            # Coba gunakan alternatif untuk LANCZOS jika error
            try:
                resized_image = self.image.resize(new_size, Image.Resampling.LANCZOS)
            except AttributeError:
                resized_image = self.image.resize(new_size, Image.LANCZOS)

            # Convert to ImageTk untuk ditampilkan di canvas
            self.tk_image = ImageTk.PhotoImage(resized_image)

            # gambar di canvas
            self.canvas.delete("all")  # Hapus gambar sebelumnya
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
            self.canvas.image = self.tk_image  # Simpan referensi agar gambar tetap tampil

            # Update ukuran canvas sesuai dengan gambar
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def zoom_in(self):
        self.zoom_level *= 1.1
        self.display_image()

    def zoom_out(self):
        self.zoom_level /= 1.1
        self.display_image()

if __name__ == "__main__":
    app = ImageViewer()
    app.mainloop()
