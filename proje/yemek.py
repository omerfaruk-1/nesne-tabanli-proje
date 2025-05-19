class Malzeme:
    def __init__(self, ad, miktar):
        self.ad = ad
        self.miktar = miktar

class Tarif:
    def __init__(self, ad, malzemeler, icerik):
        self.ad = ad
        self.malzemeler = malzemeler
        self.icerik = icerik
        self.degerlendirme = []

    def tarif_ekle(self):
        print(f"Tarif: {self.ad} eklendi.")

    def tarif_degerlendir(self, puan):
        self.degerlendirme.append(puan)
        print(f"{self.ad} tarifine {puan} puan verildi.")

    def ortalama_puan(self):
        if self.degerlendirme:
            return sum(self.degerlendirme) / len(self.degerlendirme)
        else:
            return 0

    def goster(self):
        print(f"\nTarif Adı: {self.ad}")
        print("Malzemeler:")
        for m in self.malzemeler:
            print(f"- {m.ad}: {m.miktar}")
        print(f"İçerik: {self.icerik}")
        print(f"Ortalama Puan: {self.ortalama_puan():.1f}")

tarifler = []

def tarif_olustur():
    ad = input("Tarif adını gir: ")
    malzemeler = []
    while True:
        malzeme_ad = input("Malzeme adı gir (bitirmek için 'x' yaz): ")
        if malzeme_ad.lower() == 'x':
            break
        miktar = input("Miktarını gir: ")
        malzemeler.append(Malzeme(malzeme_ad, miktar))

    icerik = input("Tarif içeriğini yaz: ")
    yeni_tarif = Tarif(ad, malzemeler, icerik)
    yeni_tarif.tarif_ekle()
    tarifler.append(yeni_tarif)

def tarifleri_goster():
    for tarif in tarifler:
        tarif.goster()

def tarif_degerlendir():
    for i, tarif in enumerate(tarifler):
        print(f"{i+1}. {tarif.ad}")
    secim = int(input("Değerlendirmek istediğin tarifin numarasını seç: "))
    puan = int(input("Puan ver (1-5): "))
    tarifler[secim - 1].tarif_degerlendir(puan)

def menu():
    print("\n--- Yemek Tarifi Uygulaması ---")
    print("1. Tarif Ekle")
    print("2. Tarifleri Göster")
    print("3. Tarif Değerlendir")
    print("4. Çıkış")

while True:
    menu()
    secim = input("Bir işlem seç: ")

    if secim == "1":
        tarif_olustur()
    elif secim == "2":
        tarifleri_goster()
    elif secim == "3":
        tarif_degerlendir()
    elif secim == "4":
        print("Çıkılıyor...")
        break
    else:
        print("Geçersiz seçim.")
