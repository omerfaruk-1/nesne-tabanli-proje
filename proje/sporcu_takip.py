import tkinter as tk
from tkinter import messagebox, simpledialog

class Sporcu:
    def __init__(self, ad, spor_dali):
        self.ad = ad
        self.spor_dali = spor_dali
        self.antrenman_programi = []
        self.ilerleme_kaydi = []

    def program_olustur(self, antrenman):
        self.antrenman_programi.append(antrenman)

    def ilerleme_kaydet(self, takip):
        self.ilerleme_kaydi.append(takip)

    def rapor_al(self):
        if not self.ilerleme_kaydi:
            return "Henüz bir ilerleme kaydı yok."
        else:
            return "\n".join(str(kayit) for kayit in self.ilerleme_kaydi)

class Antrenman:
    def __init__(self, ad, detay):
        self.ad = ad
        self.detay = detay

    def __str__(self):
        return f"{self.ad}: {self.detay}"

class Takip:
    def __init__(self, tarih, antrenman_adi, aciklama):
        self.tarih = tarih
        self.antrenman_adi = antrenman_adi
        self.aciklama = aciklama

    def __str__(self):
        return f"{self.tarih} - {self.antrenman_adi}: {self.aciklama}"

class Uygulama(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🏋️ Spor Takip Uygulaması")
        self.geometry("600x400")
        self.sporcu = None
        self.antrenmanlar = []
        self.takipler = []
        self.create_widgets()

    def create_widgets(self):
        self.ad_label = tk.Label(self, text="Sporcunun Adı:")
        self.ad_label.grid(row=0, column=0, padx=10, pady=5)
        self.ad_entry = tk.Entry(self)
        self.ad_entry.grid(row=0, column=1, padx=10, pady=5)

        self.spor_dali_label = tk.Label(self, text="Spor Dalı:")
        self.spor_dali_label.grid(row=1, column=0, padx=10, pady=5)
        self.spor_dali_entry = tk.Entry(self)
        self.spor_dali_entry.grid(row=1, column=1, padx=10, pady=5)

        self.create_button = tk.Button(self, text="Sporcu Oluştur", command=self.sporcu_olustur)
        self.create_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.antrenman_button = tk.Button(self, text="Antrenman Ekle", command=self.antrenman_ekle)
        self.antrenman_button.grid(row=3, column=0, columnspan=2, pady=5)

        self.takip_button = tk.Button(self, text="İlerleme Kaydet", command=self.ilerleme_kaydet)
        self.takip_button.grid(row=4, column=0, columnspan=2, pady=5)

        self.rapor_button = tk.Button(self, text="Rapor Al", command=self.rapor_al)
        self.rapor_button.grid(row=5, column=0, columnspan=2, pady=5)

        self.rapor_label = tk.Label(self, text="Rapor:")
        self.rapor_label.grid(row=6, column=0, padx=10, pady=5)
        self.rapor_text = tk.Text(self, height=10, width=50)
        self.rapor_text.grid(row=6, column=1, padx=10, pady=5)

    def sporcu_olustur(self):
        ad = self.ad_entry.get()
        spor_dali = self.spor_dali_entry.get()
        if ad and spor_dali:
            self.sporcu = Sporcu(ad, spor_dali)
            messagebox.showinfo("Başarılı", f"{ad} adlı sporcu başarıyla oluşturuldu.")
        else:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")

    def antrenman_ekle(self):
        if not self.sporcu:
            messagebox.showerror("Hata", "Öncelikle bir sporcu oluşturun.")
            return
        antrenman_ad = simpledialog.askstring("Antrenman Adı", "Antrenman adını girin:")
        antrenman_detay = simpledialog.askstring("Antrenman Detayı", "Antrenman detayını girin:")
        if antrenman_ad and antrenman_detay:
            antrenman = Antrenman(antrenman_ad, antrenman_detay)
            self.sporcu.program_olustur(antrenman)
            self.antrenmanlar.append(antrenman)
            messagebox.showinfo("Başarılı", f"{antrenman_ad} adlı antrenman başarıyla eklendi.")
        else:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")

    def ilerleme_kaydet(self):
        if not self.sporcu:
            messagebox.showerror("Hata", "Öncelikle bir sporcu oluşturun.")
            return
        if not self.antrenmanlar:
            messagebox.showerror("Hata", "Öncelikle en az bir antrenman ekleyin.")
            return
        tarih = simpledialog.askstring("Tarih", "Tarihi girin (GG-AA-YYYY):")
        antrenman_ad = simpledialog.askstring("Antrenman Adı", "Antrenman adını girin:")
        aciklama = simpledialog.askstring("Açıklama", "Açıklamayı girin:")
        if tarih and antrenman_ad and aciklama:
            takip = Takip(tarih, antrenman_ad, aciklama)
            self.sporcu.ilerleme_kaydet(takip)
            self.takipler.append(takip)
            messagebox.showinfo("Başarılı", "İlerleme kaydı başarıyla eklendi.")
        else:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")

    def rapor_al(self):
        if not self.sporcu:
            messagebox.showerror("Hata", "Öncelikle bir sporcu oluşturun.")
            return
        rapor = self.sporcu.rapor_al()
        self.rapor_text.delete(1.0, tk.END)
        self.rapor_text.insert(tk.END, rapor)

if __name__ == "__main__":
    app = Uygulama()
    app.mainloop()
