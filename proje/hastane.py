import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime, timedelta

# --- Sınıflar ---

class Hasta:
    def __init__(self, isim, tc):
        self.isim = isim
        self.tc = tc
        self.randevular = []

    def randevu_ekle(self, randevu):
        self.randevular.append(randevu)

    def randevu_sil(self, randevu):
        if randevu in self.randevular:
            self.randevular.remove(randevu)

    def __str__(self):
        return f"{self.isim} - TC: {self.tc}"

class Doktor:
    def __init__(self, isim, uzmanlik):
        self.isim = isim
        self.uzmanlik = uzmanlik
        self.musaitlik = self.otomatik_musaitlik_olustur()

    def otomatik_musaitlik_olustur(self):
        saatler = []
        bugun = datetime.now().date()
        for gun in range(7):
            tarih = bugun + timedelta(days=gun)
            for saat in range(10, 17):
                dt = datetime(tarih.year, tarih.month, tarih.day, saat, 0)
                saatler.append(dt)
        return saatler

    def musaitlik_kaldir(self, tarih):
        if tarih in self.musaitlik:
            self.musaitlik.remove(tarih)

    def __str__(self):
        return f"Dr. {self.isim} - {self.uzmanlik}"

class Randevu:
    def __init__(self, tarih, doktor, hasta):
        self.tarih = tarih
        self.doktor = doktor
        self.hasta = hasta

    def __str__(self):
        return f"{self.tarih.strftime('%d-%m-%Y %H:%M')} - {self.doktor.isim} ile {self.hasta.isim}"

# --- Veritabanı (listeler) ---

hastalar = []
doktorlar = []
randevular = []

# --- Fonksiyonlar ---

def hasta_ekle():
    isim = hasta_entry.get().strip()
    tc = tc_entry.get().strip()

    if not isim or not tc:
        messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")
        return

    if not isim.isalpha():
        messagebox.showerror("Hata", "Hasta adı yalnızca harflerden oluşmalıdır.")
        return

    if not tc.isdigit():
        messagebox.showerror("Hata", "TC sadece sayılardan oluşmalıdır.")
        return

    if len(tc) != 11:
        messagebox.showerror("Hata", "TC 11 haneli olmalıdır.")
        return

    hastalar.append(Hasta(isim, tc))
    hasta_entry.delete(0, tk.END)
    tc_entry.delete(0, tk.END)
    messagebox.showinfo("Başarılı", "Hasta eklendi.")

def doktor_ekle():
    isim = doktor_entry.get().strip()
    uzmanlik = uzmanlik_entry.get().strip()

    if not isim or not uzmanlik:
        messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")
        return

    if not isim.isalpha():
        messagebox.showerror("Hata", "Doktor adı yalnızca harflerden oluşmalıdır.")
        return

    if not uzmanlik.isalpha():
        messagebox.showerror("Hata", "Uzmanlık yalnızca harflerden oluşmalıdır.")
        return

    doktorlar.append(Doktor(isim, uzmanlik))
    doktor_entry.delete(0, tk.END)
    uzmanlik_entry.delete(0, tk.END)
    messagebox.showinfo("Başarılı", "Doktor eklendi.")

def randevu_al():
    if not hastalar or not doktorlar:
        messagebox.showwarning("Uyarı", "Hasta ve doktor ekleyin.")
        return
    h = simpledialog.askinteger("Hasta", "\n".join(f"{i}. {x}" for i, x in enumerate(hastalar)))
    d = simpledialog.askinteger("Doktor", "\n".join(f"{i}. {x}" for i, x in enumerate(doktorlar)))
    if h is None or d is None: return
    doktor = doktorlar[d]
    if not doktor.musaitlik:
        messagebox.showinfo("Bilgi", "Bu doktorun müsaitliği kalmadı.")
        return
    t = simpledialog.askinteger("Saat Seç", "\n".join(f"{i}. {z.strftime('%d-%m-%Y %H:%M')}" for i, z in enumerate(doktor.musaitlik)))
    if t is None: return
    tarih = doktor.musaitlik[t]
    r = Randevu(tarih, doktor, hastalar[h])
    hastalar[h].randevu_ekle(r)
    doktor.musaitlik_kaldir(tarih)
    randevular.append(r)
    messagebox.showinfo("Başarılı", "Randevu alındı.")

def randevu_iptal():
    if not hastalar:
        messagebox.showwarning("Uyarı", "Hasta yok.")
        return
    h = simpledialog.askinteger("Hasta", "\n".join(f"{i}. {x}" for i, x in enumerate(hastalar)))
    if h is None: return
    hasta = hastalar[h]
    if not hasta.randevular:
        messagebox.showinfo("Bilgi", "Bu hastanın randevusu yok.")
        return
    r = simpledialog.askinteger("İptal", "\n".join(f"{i}. {x}" for i, x in enumerate(hasta.randevular)))
    if r is None: return
    rnd = hasta.randevular[r]
    hasta.randevu_sil(rnd)
    randevular.remove(rnd)
    rnd.doktor.musaitlik.append(rnd.tarih)
    messagebox.showinfo("Başarılı", "Randevu iptal edildi.")

def randevulari_goster():
    liste.delete(0, tk.END)
    for r in randevular:
        liste.insert(tk.END, str(r))
    if not randevular:
        liste.insert(tk.END, "🔍 Henüz randevu yok.")


pencere = tk.Tk()
pencere.title("🏥 Hastane Randevu Sistemi")


tk.Label(pencere, text="Hasta Adı").grid(row=0, column=0)
hasta_entry = tk.Entry(pencere)
hasta_entry.grid(row=0, column=1)

tk.Label(pencere, text="TC").grid(row=1, column=0)
tc_entry = tk.Entry(pencere)
tc_entry.grid(row=1, column=1)

tk.Button(pencere, text="Hasta Ekle", command=hasta_ekle).grid(row=2, column=0, columnspan=2, pady=5)


tk.Label(pencere, text="Doktor Adı").grid(row=0, column=2)
doktor_entry = tk.Entry(pencere)
doktor_entry.grid(row=0, column=3)

tk.Label(pencere, text="Uzmanlık").grid(row=1, column=2)
uzmanlik_entry = tk.Entry(pencere)
uzmanlik_entry.grid(row=1, column=3)

tk.Button(pencere, text="Doktor Ekle", command=doktor_ekle).grid(row=2, column=2, columnspan=2, pady=5)


tk.Button(pencere, text="Randevu Al", command=randevu_al).grid(row=3, column=0, columnspan=2, pady=5)
tk.Button(pencere, text="Randevu İptal Et", command=randevu_iptal).grid(row=3, column=2, columnspan=2, pady=5)
tk.Button(pencere, text="Tüm Randevuları Göster", command=randevulari_goster).grid(row=4, column=0, columnspan=4, pady=5)


liste = tk.Listbox(pencere, width=100)
liste.grid(row=5, column=0, columnspan=4, pady=10)

pencere.mainloop()

