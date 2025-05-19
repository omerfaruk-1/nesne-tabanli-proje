import tkinter as tk
from tkinter import messagebox, simpledialog

class Urun:
    def __init__(self, ad, stok_miktari):
        self.ad = ad
        self.stok_miktari = stok_miktari

    def stok_guncelle(self, miktar):
        self.stok_miktari += miktar

    def siparis_olustur(self, miktar):
        if self.stok_miktari >= miktar:
            self.stok_miktari -= miktar
            return True
        else:
            return False

    def __str__(self):
        return f"{self.ad} - Stok: {self.stok_miktari}"


class Siparis:
    siparis_sayac = 1

    def __init__(self, urun_adi, miktar):
        self.siparis_no = Siparis.siparis_sayac
        Siparis.siparis_sayac += 1
        self.urun_adi = urun_adi
        self.miktar = miktar

    def __str__(self):
        return f"Sipariş #{self.siparis_no} - Ürün: {self.urun_adi} - Adet: {self.miktar}"


class StokTakipUygulamasi(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("📦 Stok Takip Sistemi")
        self.geometry("600x400")
        self.urunler = []
        self.create_widgets()

    def create_widgets(self):
        self.urun_ekle_button = tk.Button(self, text="Ürün Ekle", command=self.urun_ekle)
        self.urun_ekle_button.pack(pady=10)

        self.stok_guncelle_button = tk.Button(self, text="Stok Güncelle", command=self.stok_guncelle)
        self.stok_guncelle_button.pack(pady=10)

        self.siparis_olustur_button = tk.Button(self, text="Sipariş Oluştur", command=self.siparis_olustur)
        self.siparis_olustur_button.pack(pady=10)

        self.stok_goruntule_button = tk.Button(self, text="Stokları Görüntüle", command=self.stok_goruntule)
        self.stok_goruntule_button.pack(pady=10)

        self.stok_listesi_text = tk.Text(self, height=10, width=50)
        self.stok_listesi_text.pack(pady=20)

    def urun_ekle(self):
        ad = simpledialog.askstring("Ürün Ekle", "Ürün adı girin:")
        if ad:
            stok = simpledialog.askinteger("Stok Miktarı", "Başlangıç stok miktarı girin:")
            if stok is not None:
                urun = Urun(ad, stok)
                self.urunler.append(urun)
                messagebox.showinfo("Başarılı", f"{ad} ürünü başarıyla eklendi.")
            else:
                messagebox.showerror("Hata", "Geçerli bir stok miktarı girin.")
        else:
            messagebox.showerror("Hata", "Ürün adı boş olamaz.")

    def stok_guncelle(self):
        urunler_adlari = [urun.ad for urun in self.urunler]
        ad = simpledialog.askstring("Stok Güncelle", "Stok güncellenecek ürün adı girin:\n" + "\n".join(urunler_adlari))
        if ad:
            miktar = simpledialog.askinteger("Eklemek İstediğiniz Stok Miktarı", "Eklemek istediğiniz miktar:")
            if miktar is not None:
                bulundu = False
                for urun in self.urunler:
                    if urun.ad == ad:
                        urun.stok_guncelle(miktar)
                        messagebox.showinfo("Başarılı", f"{ad} ürününün stoku güncellendi.")
                        bulundu = True
                if not bulundu:
                    messagebox.showerror("Hata", "Ürün bulunamadı.")
            else:
                messagebox.showerror("Hata", "Geçerli bir miktar girin.")
        else:
            messagebox.showerror("Hata", "Ürün adı boş olamaz.")

    def siparis_olustur(self):
        urunler_adlari = [urun.ad for urun in self.urunler]
        ad = simpledialog.askstring("Sipariş Oluştur", "Sipariş verilecek ürün adı girin:\n" + "\n".join(urunler_adlari))
        if ad:
            miktar = simpledialog.askinteger("Sipariş Miktarı", "Sipariş miktarı girin:")
            if miktar is not None:
                bulundu = False
                for urun in self.urunler:
                    if urun.ad == ad:
                        if urun.siparis_olustur(miktar):
                            siparis = Siparis(ad, miktar)
                            messagebox.showinfo("Başarılı", f"Sipariş oluşturuldu: {siparis}")
                        else:
                            messagebox.showerror("Yetersiz Stok", "Yetersiz stok!")
                        bulundu = True
                if not bulundu:
                    messagebox.showerror("Hata", "Ürün bulunamadı.")
            else:
                messagebox.showerror("Hata", "Geçerli bir sipariş miktarı girin.")
        else:
            messagebox.showerror("Hata", "Ürün adı boş olamaz.")

    def stok_goruntule(self):
        self.stok_listesi_text.delete(1.0, tk.END)
        if self.urunler:
            for urun in self.urunler:
                self.stok_listesi_text.insert(tk.END, str(urun) + "\n")
        else:
            self.stok_listesi_text.insert(tk.END, "Henüz ürün eklenmedi.")


if __name__ == "__main__":
    app = StokTakipUygulamasi()
    app.mainloop()
