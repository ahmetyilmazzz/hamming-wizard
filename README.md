# 🧙‍♂️ Hamming Wizard

**İnteraktif Hamming SEC-DED (Tek Hata Düzeltme - Çift Hata Tespit) Kod Simülatörü**

Hamming hata düzeltme kodlarını öğrenmek ve deneyimlemek için güçlü ve sezgisel bir GUI uygulaması. Bilgisayar bilimleri öğrencileri, eğitmenler ve hata tespit ve düzeltme algoritmalarını merak eden herkes için mükemmel!

## ✨ Özellikler

- **İnteraktif Öğrenme**: Bitlere tıklayarak hata oluşturun ve Hamming kodlarının bunları nasıl tespit edip düzelttiğini görün
- **Çoklu Veri Boyutları**: 8, 16 ve 32-bit veri girişleri desteği
- **Görsel Geri Bildirim**: Kolay anlama için renk kodlu bitler
  - 🟢 **Yeşil**: Parite bitleri
  - 🔵 **Mavi**: Veri bitleri  
  - 🟡 **Sarı**: Toplam parite biti
  - 🔴 **Kırmızı**: Bozuk bitler
- **Gerçek Zamanlı Hata Tespiti**: 
  - Tek hata düzeltme
  - Çift hata tespiti
  - Syndrome hesaplama ve gösterimi
- **Eğitim Dostu Arayüz**: Net etiketleme ve adım adım süreç

## 🚀 Başlangıç

### Gereksinimler

- Python 3.6+
- tkinter (genellikle Python ile birlikte gelir)

### Kurulum

1. Repository'yi klonlayın:
```bash
git clone https://github.com/ahmetyilmazzz/hamming-wizard.git
cd hamming-wizard
```

2. Simülatörü çalıştırın:
```bash
python hamming_simulator.py
```

## 📖 Nasıl Kullanılır

1. **Veri Boyutu Seçin**: 8, 16 veya 32 bit arasından seçin
2. **Binary Veri Girin**: Binary string'inizi girin (örn: 8 bit için "10110101")
3. **Hamming Kodu Üretin**: "Hamming Kodu Üret" butonuna tıklayarak hata düzeltme kodunu oluşturun
4. **Hata Oluşturun**: Herhangi bir bite tıklayarak çevirin (en fazla 2 hata izin verilir)
5. **Hata Kontrolü Yapın**: "Hata Kontrolü Yap" butonuna tıklayarak sihrin gerçekleştiğini görün!

## 🎓 Eğitim Değeri

Bu simülatör şunları anlamanıza yardımcı olur:
- Parite bitlerinin nasıl hesaplandığı ve konumlandırıldığı
- Veri bitleri ile parite bitleri arasındaki ilişki
- Hata tespiti için syndrome hesaplama
- Tek hata düzeltme ile çift hata tespiti arasındaki fark
- Hamming kodlarının bilgisayar bellek sistemlerinde neden temel olduğu

## 🔍 Örnek

8-bit veri `10110101` için:
- Simülatör parite bitleri ile Hamming kodu üretir
- 1-2 bit hata oluşturabilirsiniz
- Tek hataların otomatik olarak düzeltildiğini izleyin
- Çift hataların nasıl tespit edildiğini ama düzeltilmediğini görün

## 🛠️ Teknik Detaylar

- **Algoritma**: SEC-DED Hamming Kodu
- **Parite Hesaplama**: XOR tabanlı çift parite
- **Hata Tespiti**: Syndrome hesaplama
- **GUI Framework**: Python tkinter


## 📝 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır - detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 🎖️ Özellikler

- ✅ Gerçek zamanlı hata simülasyonu
- ✅ Görsel öğrenme deneyimi
- ✅ Eğitim amaçlı tasarlanmış
- ✅ Açık kaynak
- ✅ Platform bağımsız
- ✅ Kurulum gerektirmiyor

## 🔧 Sistem Gereksinimleri

- **İşletim Sistemi**: Windows, macOS, Linux
- **Python**: 3.6 veya üzeri

---