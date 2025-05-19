import tkinter as tk
from tkinter import messagebox, simpledialog

# Geçerlilik kontrolleri
def sadece_rakam(deger):
    return deger.isdigit()

def sadece_harf(deger):
    return deger.replace(" ", "").isalpha()

# Sınıflar
class Kitap:
    def __init__(self, kitap_id, ad, yazar):
        self.kitap_id = kitap_id
        self.ad = ad
        self.yazar = yazar
        self.odunc_alindi = False

    def durum_guncelle(self, odunc_mu):
        self.odunc_alindi = odunc_mu

    def __str__(self):
        durum = "Mevcut" if not self.odunc_alindi else "Ödünç Alındı"
        return f"{self.kitap_id} - {self.ad} - {self.yazar} ({durum})"

class Uye:
    def __init__(self, uye_id, ad):
        self.uye_id = uye_id
        self.ad = ad
        self.odunc_kitaplar = []

    def kitap_ekle(self, kitap):
        self.odunc_kitaplar.append(kitap)

    def kitap_iade(self, kitap):
        if kitap in self.odunc_kitaplar:
            self.odunc_kitaplar.remove(kitap)

    def __str__(self):
        return f"{self.uye_id} - {self.ad}"

class Odunc:
    def __init__(self, kitap, uye):
        self.kitap = kitap
        self.uye = uye

    def odunc_al(self):
        if not self.kitap.odunc_alindi:
            self.kitap.durum_guncelle(True)
            self.uye.kitap_ekle(self.kitap)
            messagebox.showinfo("Başarılı", f"Kitap '{self.kitap.ad}' ödünç verildi.")
        else:
            messagebox.showwarning("Uyarı", "Bu kitap zaten ödünç alınmış.")

    def iade_et(self):
        if self.kitap.odunc_alindi:
            self.kitap.durum_guncelle(False)
            self.uye.kitap_iade(self.kitap)
            messagebox.showinfo("Başarılı", f"Kitap '{self.kitap.ad}' iade edildi.")
        else:
            messagebox.showwarning("Uyarı", "Bu kitap zaten kütüphanede mevcut.")

# Veri yapıları
kitaplar = []
uyeler = []

# Fonksiyonlar
def kitap_ekle():
    kitap_id = entry_kitap_id.get()
    ad = entry_kitap_ad.get()
    yazar = entry_kitap_yazar.get()

    if not (kitap_id and ad and yazar):
        messagebox.showwarning("Uyarı", "Tüm alanları doldurun.")
        return

    if not sadece_rakam(kitap_id):
        messagebox.showerror("Hata", "Kitap ID sadece rakam olmalıdır.")
        return
    if not sadece_harf(ad):
        messagebox.showerror("Hata", "Kitap adı sadece harf içermelidir.")
        return
    if not sadece_harf(yazar):
        messagebox.showerror("Hata", "Yazar adı sadece harf içermelidir.")
        return

    kitaplar.append(Kitap(kitap_id, ad, yazar))
    messagebox.showinfo("Başarılı", "Kitap eklendi.")
    entry_kitap_id.delete(0, tk.END)
    entry_kitap_ad.delete(0, tk.END)
    entry_kitap_yazar.delete(0, tk.END)

def uye_ekle():
    uye_id = entry_uye_id.get()
    ad = entry_uye_ad.get()

    if not (uye_id and ad):
        messagebox.showwarning("Uyarı", "Tüm alanları doldurun.")
        return

    if not sadece_rakam(uye_id):
        messagebox.showerror("Hata", "Üye ID sadece rakam olmalıdır.")
        return
    if not sadece_harf(ad):
        messagebox.showerror("Hata", "Üye adı sadece harf içermelidir.")
        return

    uyeler.append(Uye(uye_id, ad))
    messagebox.showinfo("Başarılı", "Üye eklendi.")
    entry_uye_id.delete(0, tk.END)
    entry_uye_ad.delete(0, tk.END)

def kitaplari_goster():
    liste_kitaplar.delete(0, tk.END)
    for kitap in kitaplar:
        liste_kitaplar.insert(tk.END, str(kitap))

def kitap_ara():
    aranan = entry_ara.get().strip()
    if not sadece_harf(aranan):
        messagebox.showerror("Hata", "Arama sadece harf içermelidir.")
        return

    liste_kitaplar.delete(0, tk.END)
    bulunan = [k for k in kitaplar if k.ad.strip().lower() == aranan.lower()]
    if bulunan:
        for kitap in bulunan:
            liste_kitaplar.insert(tk.END, str(kitap))
    else:
        messagebox.showinfo("Sonuç", "Kitap bulunamadı.")

def odunc_al_gui():
    kitap_id = simpledialog.askstring("Kitap ID", "Ödünç alınacak kitap ID:")
    if not kitap_id or not sadece_rakam(kitap_id):
        messagebox.showerror("Hata", "Geçerli bir kitap ID girin (sadece rakam).")
        return

    kitap = next((k for k in kitaplar if k.kitap_id == kitap_id), None)
    if not kitap:
        messagebox.showwarning("Uyarı", "Kitap bulunamadı.")
        return
    if not uyeler:
        messagebox.showwarning("Uyarı", "Önce üye ekleyin.")
        return
    uye_adlari = [str(u) for u in uyeler]
    secim = simpledialog.askinteger("Üye Seç", "\n".join(f"{i}: {u}" for i, u in enumerate(uye_adlari)))
    if secim is not None and 0 <= secim < len(uyeler):
        odunc = Odunc(kitap, uyeler[secim])
        odunc.odunc_al()

def kitap_iade_gui():
    kitap_id = simpledialog.askstring("Kitap ID", "İade edilecek kitap ID:")
    if not kitap_id or not sadece_rakam(kitap_id):
        messagebox.showerror("Hata", "Geçerli bir kitap ID girin (sadece rakam).")
        return

    kitap = next((k for k in kitaplar if k.kitap_id == kitap_id), None)
    if not kitap:
        messagebox.showwarning("Uyarı", "Kitap bulunamadı.")
        return
    uye = next((u for u in uyeler if kitap in u.odunc_kitaplar), None)
    if not uye:
        messagebox.showwarning("Uyarı", "Bu kitap hiçbir üyeye kayıtlı değil.")
        return
    odunc = Odunc(kitap, uye)
    odunc.iade_et()


pencere = tk.Tk()
pencere.title("📚 Kütüphane Yönetim Sistemi")


tk.Label(pencere, text="Kitap ID").grid(row=0, column=0)
entry_kitap_id = tk.Entry(pencere)
entry_kitap_id.grid(row=0, column=1)

tk.Label(pencere, text="Kitap Adı").grid(row=1, column=0)
entry_kitap_ad = tk.Entry(pencere)
entry_kitap_ad.grid(row=1, column=1)

tk.Label(pencere, text="Yazar").grid(row=2, column=0)
entry_kitap_yazar = tk.Entry(pencere)
entry_kitap_yazar.grid(row=2, column=1)

tk.Button(pencere, text="Kitap Ekle", command=kitap_ekle).grid(row=3, column=0, columnspan=2, pady=5)


tk.Label(pencere, text="Üye ID").grid(row=0, column=2)
entry_uye_id = tk.Entry(pencere)
entry_uye_id.grid(row=0, column=3)

tk.Label(pencere, text="Üye Adı").grid(row=1, column=2)
entry_uye_ad = tk.Entry(pencere)
entry_uye_ad.grid(row=1, column=3)

tk.Button(pencere, text="Üye Ekle", command=uye_ekle).grid(row=2, column=2, columnspan=2, pady=5)


tk.Label(pencere, text="Kitap Ara (Ad)").grid(row=4, column=0)
entry_ara = tk.Entry(pencere)
entry_ara.grid(row=4, column=1)
tk.Button(pencere, text="Ara", command=kitap_ara).grid(row=4, column=2)
tk.Button(pencere, text="Tüm Kitapları Göster", command=kitaplari_goster).grid(row=4, column=3)


liste_kitaplar = tk.Listbox(pencere, width=80)
liste_kitaplar.grid(row=5, column=0, columnspan=4, pady=10)

tk.Button(pencere, text="Kitap Ödünç Al", command=odunc_al_gui).grid(row=6, column=0, columnspan=2)
tk.Button(pencere, text="Kitap İade Et", command=kitap_iade_gui).grid(row=6, column=2, columnspan=2)

pencere.mainloop()

