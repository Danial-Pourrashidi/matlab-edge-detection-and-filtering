# Görüntü İşleme ile Kenar Tespit ve Filtreleme Algoritmaları (MATLAB)

Bu proje; sayısal görüntü işleme alanında uzamsal konvolüsyon, 2B Gauss gürültü azaltma ve türev operatörleri (Sobel, Prewitt, Laplacian) ile kenar tespiti algoritmalarının **MATLAB hazır fonksiyonlarına bağımlı olmaksızın, sıfırdan (`from scratch`) for döngüleri ve matris matematiğiyle** geliştirilmesini ve MATLAB yerleşik fonksiyonlarıyla (`conv2`, `imfilter`) karşılaştırılmasını kapsar.

---

## 📌 Proje Özellikleri

1. **Sıfırdan 2B Konvolüsyon (`my_conv2.m`):**
   - Matematiksel tanıma uygun olarak çekirdeği 180 derece döndürme (`rot90(kernel, 2)`).
   - Çift `for` döngüsü ile piksel bazında lokal çarpım ve toplama.
   - Sınır pikselleri için 3 farklı dolgu (padding) seçeneği: `'zero'`, `'replicate'`, `'symmetric'`.
   - Harici kütüphanelere (`padarray` vb.) ihtiyaç duymayan saf MATLAB matris indekslemesi.

2. **2B Gauss Yumuşatma Filtresi (`gaussian_kernel.m`):**
   - İki boyutlu sürekli Gauss dağılımının ayrık ızgarada örneklenmesi.
   - Parlaklık ve enerji korunumu için çekirdek katsayılarının toplamının 1'e normalizasyonu.
   - $3\times3$, $5\times5$, $7\times7$ çekirdek boyutları ve $\sigma = 0.5, 1.0, 2.0$ parametrik analizleri.

3. **Gürültü Simülasyonu (`add_noise.m`):**
   - Gauss gürültüsü ($\mu$, $\sigma^2$).
   - Tuz ve Biber (Salt & Pepper) gürültüsü ($d$ yoğunluğu).
   - $[0, 1]$ aralığında otomatik dinamik aralık kırpması (clamping).

4. **Birinci Derece Gradyan Operatörleri (`apply_sobel.m`, `apply_prewitt.m`):**
   - $G_x$ (yatay türev / dikey kenar) ve $G_y$ (dikey türev / yatay kenar) matrisleri.
   - Gradyan büyüklüğü: $M = \sqrt{G_x^2 + G_y^2}$.
   - Gradyan yön açısı: $\theta = \text{atan2}(G_y, G_x)$.
   - Otomatik istatistiksel eşikleme ile ikili (binary) kenar haritaları.

5. **İkinci Derece Laplacian Operatörü (`apply_laplacian.m`):**
   - 4-komşuluk ve 8-komşuluk Laplace çekirdekleri.
   - **Yöntem 1:** Mutlak genlik eşikleme ($|\nabla^2 I| \ge T$).
   - **Yöntem 2:** Sıfır geçişi (Zero-Crossing) tespiti (zıt işaretli komşu pikseller ve dik eğim kontrolü).

6. **Kapsamlı Karşılaştırma ve Metrik Analizi (`evaluate_metrics.m`):**
   - Maksimum Mutlak Hata (Max Absolute Error).
   - Ortalama Mutlak Hata (MAE).
   - Ortalama Karesel Hata (MSE).
   - Tepe Sinyal-Gürültü Oranı (PSNR - dB).
   - Çalışma süresi (Execution Time - `tic`/`toc`).
   - Sonuçların `results/metrics.csv` dosyasına otomatik kaydedilmesi.

---

## 📂 Dosya ve Dizin Yapısı

```text
BHT Proje/
├── README.md                      # Proje tanıtımı, kurulum ve kullanım kılavuzu
├── main.m                         # Uçtan uca ana yürütme ve görselleştirme betiği
├── src/                           # Sıfırdan geliştirilen kaynak fonksiyonlar
│   ├── my_conv2.m                 # 2B for döngülü konvolüsyon fonksiyonu
│   ├── gaussian_kernel.m          # Parametrik 2B Gauss çekirdek üretici
│   ├── add_noise.m                # Gauss ve tuz-biber gürültü ekleme modülü
│   ├── apply_sobel.m              # Sobel kenar dedektörü (Gx, Gy, Mag, Dir, Eşik)
│   ├── apply_prewitt.m            # Prewitt kenar dedektörü
│   ├── apply_laplacian.m          # Laplacian (Mutlak eşik ve Sıfır Geçişi)
│   └── evaluate_metrics.m         # Hata metrikleri ve karşılaştırma aracı
├── tests/                         # Doğrulama ve testler
│   └── test_my_conv2.m            # Birim testler ve conv2 matematiksel denklik testi
├── references/                    # Açık kaynak depo incelemeleri
│   └── github_repos.md            # GitHub depoları, lisansları ve katkı analizi
├── report/                        # Akademik ve bilimsel rapor
│   └── report_template.md         # 9 bölümlü kapsamlı bilimsel proje raporu
└── results/                       # Otomatik üretilen çıktılar
    ├── figures/                   # Üretilen yüksek çözünürlüklü PNG grafikleri
    └── metrics.csv                # Tüm testlerin sayısal metrik tablosu
```

---

## 🚀 Kurulum ve Çalıştırma

### Gereksinimler
- MATLAB R2023b veya üzeri (kod geriye dönük uyumludur, önceki sürümlerde de sorunsuz çalışır).
- Image Processing Toolbox (isteğe bağlı; kodlar tamamen sıfırdan yazıldığı için toolbox olmadan da sentetik görüntü fallback'i ile %100 çalışır).

### 1. Birim Testlerin Çalıştırılması
Kendi yazdığımız `my_conv2` fonksiyonunun doğruluğunu test etmek için:

```matlab
>> cd('C:\Users\fmn17\OneDrive\Desktop\BHT Proje');
>> run('tests/test_my_conv2.m');
```

**Beklenen Test Çıktısı:**
```text
====================================================
  my_conv2 Doğrulama ve Birim Testleri Başlatılıyor  
====================================================

[TEST 1] Küçük 3x3 Matris ile Elle Hesaplama Kontrolü... [BAŞARILI] (Merkez piksel: 15.0000 == 15.0)
[TEST 2] Asimetrik Çekirdek ve conv2(..., "same") Karşılaştırması... [BAŞARILI] (Maksimum Mutlak Hata = 0.00e+00)
[TEST 3] 64x64 Rastgele Matris ve 5x5 Çekirdek Testi... [BAŞARILI] (Maksimum Mutlak Hata = 2.22e-16)
[TEST 4] "replicate" Sınır Dolgusu Fonksiyonel Testi... [BAŞARILI] (Köşe piksel beklenen: 23.3333, üretilen: 23.3333)
[TEST 5] "symmetric" Ayna Dolgusu Doğrulaması... [BAŞARILI] (İç piksel beklenen: 0.0000, üretilen: 0.0000)

====================================================
  TEST SONUCU: 5 / 5 Test Başarıyla Geçti! (100%) 
  my_conv2 matematiksel ve algoritmik olarak onaylandı.
====================================================
```

### 2. Ana Uygulamanın Yürütülmesi
Tüm deneyleri çalıştırmak, görselleri üretmek ve CSV metriklerini kaydetmek için:

```matlab
>> main
```

---

## 📊 Üretilen Görsel Çıktılar (`results/figures/`)

| Dosya Adı | Açıklama |
| :--- | :--- |
| `fig01_original_and_noise.png` | Orijinal görüntü, Gauss gürültüsü ve Tuz-Biber gürültüsü yan yana. |
| `fig02_gaussian_filtering_grid.png` | $3\times3, 5\times5, 7\times7$ çekirdekler ve $\sigma \in \{0.5, 1.0, 2.0\}$ ile $3\times3$ filtreleme ızgarası ve PSNR değerleri. |
| `fig03_sobel_analysis.png` | Sobel $G_x$, $G_y$, gradyan büyüklüğü, yön haritası ve eşiklenmiş ikili kenarlar. |
| `fig04_prewitt_analysis.png` | Prewitt bileşenleri, büyüklük, yön ve ikili kenarlar. |
| `fig05_laplacian_analysis.png` | Ham Laplace ($\nabla^2 I$), mutlak genlik eşikleme ve sıfır geçişi (zero-crossing) kenarları. |
| `fig06_operator_comparison.png` | Sobel, Prewitt, Laplacian (Mutlak) ve Laplacian (Sıfır Geçişi) yöntemlerinin 4'lü karşılaştırması. |
| `fig07_custom_vs_builtin_diff.png` | `my_conv2` ile `conv2` sonuçları ve aralarındaki fark haritası ($10^{-16}$ makine hassasiyeti). |

---

## 📈 Örnek Metrik Çıktısı (`results/metrics.csv`)

| Test / Filtre Adı | Maks Mutlak Hata | MAE | MSE | PSNR (dB) | Süre (s) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `my_conv2(zero) vs conv2(same)` | $2.22 \times 10^{-16}$ | $1.85 \times 10^{-17}$ | $0.00$ | $\infty$ | $0.1824$ |
| `my_conv2(rep) vs imfilter` | $4.44 \times 10^{-16}$ | $3.12 \times 10^{-17}$ | $0.00$ | $\infty$ | $0.1841$ |
| `Gauss_5x5_sigma1.0` | $0.2185$ | $0.0281$ | $0.0022$ | $26.45$ | N/A |

---

## 📚 Açık Kaynak Referansları
Projede yararlanılan açık kaynak depoların lisans ve mimari analizleri [`references/github_repos.md`](references/github_repos.md) dosyasında belgelenmiştir. Tüm algoritmalar özgün ve bağımsız olarak geliştirilmiştir.

