class Kurs:
    def __init__(self, kurs_adi, egitmen, icerik):
        self.kurs_adi = kurs_adi
        self.egitmen = egitmen
        self.icerik = icerik
        self.ogrenciler = []  # Bu kursa kaydolan öğrenciler

    def kurs_oluştur(self):
        print(f"{self.kurs_adi} kursu oluşturuldu.")
    
    def kaydol(self, ogrenci):
        self.ogrenciler.append(ogrenci)
        print(f"{ogrenci.isim} kursa kaydoldu.")

    def icerik_yukle(self, icerik):
        self.icerik = icerik
        print("İçerik güncellendi.")

class Egitmen:
    def __init__(self, isim, uzmanlik_alanı):
        self.isim = isim
        self.uzmanlik_alanı = uzmanlik_alanı

class Ogrenci:
    def __init__(self, isim, e_posta):
        self.isim = isim
        self.e_posta = e_posta

# Veri yapıları
kurslar = []
egitmenler = []
ogrenciler = []

# Menü
def menu():
    print("\n1. Kurs Oluştur")
    print("2. Kursa Kaydol")
    print("3. İçerik Yükle")
    print("4. Kursları Görüntüle")
    print("5. Çıkış")
    
def kurs_olustur():
    isim = input("Kurs Adı: ")
    egitmen_isim = input("Eğitmen Adı: ")
    uzmanlik = input("Eğitmenin Uzmanlık Alanı: ")
    egitmen = Egitmen(egitmen_isim, uzmanlik)
    icerik = input("İçeriği gir: ")
    kurs = Kurs(isim, egitmen, icerik)
    kurslar.append(kurs)
    print(f"{isim} kursu başarıyla oluşturuldu.")

def kursa_kaydol():
    ogrenci_isim = input("Öğrenci Adı: ")
    ogrenci_email = input("Öğrenci E-posta: ")
    ogrenci = Ogrenci(ogrenci_isim, ogrenci_email)
    ogrenciler.append(ogrenci)
    
    print("\nKayıtlı Kurslar:")
    for i, kurs in enumerate(kurslar):
        print(f"{i+1}. {kurs.kurs_adi}")
    
    secim = int(input("Bir kurs seçin: "))
    kurslar[secim - 1].kaydol(ogrenci)

def icerik_yukle():
    print("\nKursları Görüntüle")
    for i, kurs in enumerate(kurslar):
        print(f"{i+1}. {kurs.kurs_adi}")
    secim = int(input("Bir kurs seçin: "))
    yeni_icerik = input("Yeni İçeriği Girin: ")
    kurslar[secim - 1].icerik_yukle(yeni_icerik)

def kurslari_goruntule():
    print("\nKurslar:")
    for kurs in kurslar:
        print(f"Kurs Adı: {kurs.kurs_adi}, Eğitmen: {kurs.egitmen.isim}, İçerik: {kurs.icerik}")

# Menü aracılığıyla işlem yapma
while True:
    menu()
    secim = int(input("Bir işlem seçin: "))
    
    if secim == 1:
        kurs_olustur()
    elif secim == 2:
        kursa_kaydol()
    elif secim == 3:
        icerik_yukle()
    elif secim == 4:
        kurslari_goruntule()
    elif secim == 5:
        break
    else:
        print("Geçersiz işlem.")