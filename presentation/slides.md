# Görüntü İşleme ile Kenar Tespit ve Filtreleme Algoritmaları
## Sunum Slayt Metinleri ve Konuşmacı Notları (presentation/slides.md)

**Kurum:** Kocaeli Üniversitesi  
**Bölüm:** Yapay Zekâ ve Makine Öğrenmesi Bölümü  
**Ders:** Bilimsel Hesaplama Teknikleri  
**Yürütücü:** Danial Pourrashidi  
**GitHub:** https://github.com/Danial-Pourrashidi/matlab-edge-detection-and-filtering  

---

### SLAYT 1: Kapak Slaytı
- **Üst Başlık:** Kocaeli Üniversitesi | Yapay Zekâ ve Makine Öğrenmesi Bölümü
- **Ders:** Bilimsel Hesaplama Teknikleri Dersi Proje Sunumu
- **Ana Başlık:** Görüntü İşleme ile Kenar Tespit ve Filtreleme Algoritmaları
- **Alt Başlık:** 2B Konvolüsyon, Gauss Yumuşatma, Sobel, Prewitt ve Laplacian Operatörlerinin Sıfırdan Analizi
- **Yürütücü:** Danial Pourrashidi
- **Danışman:** Dr. Öğr. Üyesi / Ders Sorumlusu
- **Tarih:** 2026
> **Konuşmacı Notu (35 sn):**  
> "Sayın jüri üyeleri ve değerli hocalarım, hoş geldiniz. Bugün sizlere Bilimsel Hesaplama Teknikleri dersi kapsamında hazırladığım 'Görüntü İşleme ile Kenar Tespit ve Filtreleme Algoritmaları' konulu araştırma ve uygulama projemizi sunacağım. Bu çalışmada MATLAB Image Processing Toolbox'a bağımlı kalmadan, çekirdek konvolüsyon ve türev operatörlerini sıfırdan geliştirdik. Şimdi genel akışımıza bakalım."

---

### SLAYT 2: İçindekiler
1. Problem Tanımı ve Proje Hedefleri
2. Teorik Temeller ve 2B Konvolüsyon Matematiği
3. 2D Gauss Filtresi ve Gürültü Azaltma
4. 1. ve 2. Derece Kenar Dedektörleri: Sobel, Prewitt, Laplacian
5. Uygulama Mimarisi (From Scratch Yaklaşımı)
6. Deneysel Sonuçlar ve Metrik Kıyaslaması (my_conv2 vs MATLAB)
7. Karşılaştırmalı Tartışma, Sonuç ve Gelecek Çalışmalar
> **Konuşmacı Notu (30 sn):**  
> "Sunumumuz 7 ana aşamadan oluşmaktadır. İlk olarak problemi ve motivasyonumuzu açıklayacak, ardından konvolüsyon ve Gauss filtresinin teorik arka planına değineceğiz. Sonrasında Sobel, Prewitt ve Laplacian operatörlerini detaylandırıp, sıfırdan geliştirdiğimiz my_conv2 ile MATLAB'in yerleşik fonksiyonlarını metrikler üzerinden karşılaştıracağız."

---

### SLAYT 3: Problem Tanımı: Sayısal Görüntülerde Kenar Tespiti
- **Kenarların Kritik Önemi:** Nesne sınırlarını, geometrik konturları ve derinlik süreksizliklerini taşır; bilgisayarla görmenin omurgasıdır.
- **Gerçek Dünya Gürültüsü:** Optik sensör kusurları ve iletim hatları Gauss ve tuz-biber gürültülerine yol açar.
- **Türev Operatörlerinin Zaafı:** Kenar tespiti türeve dayanır. Türev ise yüksek frekansları yükselterek gürültüyü katbekat şiddetlendirir.
- **Bilimsel İkilem:** Gürültüyü temizlerken kenar detaylarını kaybetmemek için optimal yumuşatma gereklidir.
> **Konuşmacı Notu (40 sn):**  
> "Sayısal görüntülerde kenar tespiti neden bu kadar kritiktir? Çünkü bir görüntünün anlamsal içeriğinin büyük kısmı parlaklık süreksizliklerinde gizlidir. Ancak fiziksel sensörler gürültülüdür. Türev operatörleri de yapısı gereği yüksek frekanslı gürültüleri fazlasıyla yükseltir. Bu ikilem, gürültü temizleme ile kenar tespiti arasında dikkatli bir denge kurmayı zorunlu kılar."

---

### SLAYT 4: Projenin Amacı ve Bilimsel Hedefleri
- **Sıfırdan 2B Konvolüsyon:** `my_conv2.m` fonksiyonunu çift for döngüsü ve 180° çekirdek rotasyonu ile kodlamak.
- **Sınır Koşulları:** `'zero'`, `'replicate'` ve `'symmetric'` dolgu modlarını harici kütüphanesiz yazmak.
- **Parametrik Gauss Filtreleme:** 3x3, 5x5, 7x7 boyutları ve sigma (0.5, 1.0, 2.0) testleri ile en iyi PSNR'ı yakalamak.
- **Gradyan ve İkinci Türev:** Sobel, Prewitt ve Laplacian (Mutlak Eşik & Sıfır Geçişi) yöntemlerini uygulamak.
- **Bilimsel Doğrulama:** MATLAB'in yerleşik `conv2` ve `imfilter` fonksiyonları ile sayısal hata ($10^{-16}$) ve çalışma süresi kıyası yapmak.
> **Konuşmacı Notu (35 sn):**  
> "Bu projedeki temel amacımız bir siyah kutu yaklaşımı sergilemek yerine, 2B konvolüsyon ve türev mekaniğini for döngüleri ve matris matematiğiyle sıfırdan yazmaktır. Ayrıca farklı sınır dolgularının kenar bozulmalarına etkisini incelemeyi ve yerleşik C tabanlı MATLAB fonksiyonları ile bilimsel bir karşılaştırma tablosu oluşturmayı hedefledik."

---

### SLAYT 5: Teorik Arka Plan: Sayısal Görüntü ve 2B Konvolüsyon
- **Konvolüsyon Formülü:**
  $$(I * K)(x, y) = \sum_u \sum_v I(x - u, y - v) \cdot K(u, v)$$
- **Çekirdek Rotasyonu:** Matematiksel kural gereği çekirdek 180° çevrilir: `rot90(K, 2)`. Asimetrik türev çekirdeklerinde yönün doğru çıkması için zorunludur.
- **Sınır Dolgusu (Padding):**
  - **Zero-Padding:** Sınırlar 0 yapılır; kenar piksellerinde yapay kararmalar oluşturur.
  - **Replicate:** Kenar pikselleri dışa ötelenir; enerji kaybını önler ve en kararlı kenar haritasını üretir.
  - **Symmetric:** Ayna yansıması oluşturur; süreklilik sağlar.
> **Konuşmacı Notu (40 sn):**  
> "Konvolüsyon ile korelasyon arasındaki fark bilimsel hesaplamada çok önemlidir. Konvolüsyonda filtre matrisi 180 derece döndürülür. Eğer çekirdek simetrik değilse döndürme yapılmadığında türev yönü ters çıkar. Ayrıca sınır piksellerinde replicate dolgusu kullanarak görüntü kenarlarında siyah çerçeve oluşmasını engelledik."

---

### SLAYT 6: 2D Gauss Filtresi ve Gürültü Azaltma
- **Sürekli Dağılım:**
  $$G(x, y) = \frac{1}{2\pi \sigma^2} \exp\left( -\frac{x^2 + y^2}{2\sigma^2} \right)$$
- **Normalizasyon:** Görüntü genel parlaklığının korunması için $\sum K(u, v) = 1$ yapılır.
- **Sigma ve Boyut Etkisi:**
  - Küçük $\sigma$ ($0.5$): Yetersiz gürültü bastırma.
  - Büyük $\sigma$ ($2.0$): Aşırı bulanıklaşma, ince kenar kaybı.
  - **Optimal Nokta:** $5\times5, \sigma = 1.0 \to \text{PSNR} = 26.46\text{ dB}$.
- **Görsel:** `results/figures/fig02_gaussian_filtering_grid.png`
> **Konuşmacı Notu (40 sn):**  
> "Ekranda 3x3, 5x5 ve 7x7 çekirdek boyutlarının sigma 0.5, 1.0 ve 2.0 ile oluşturduğu 9 farklı filtreleme senaryosunu görüyorsunuz. 5x5 boyutunda sigma=1.0 seçildiğinde gürültü bastırılırken kenarların keskinliği korunmuş ve en yüksek PSNR değeri olan 26.46 dB elde edilmiştir."

---

### SLAYT 7: Gürültü Türleri ve Kenar Tespiti Üzerindeki Etkisi
- **Gauss Gürültüsü:** $I_{\text{noisy}} = I + \mathcal{N}(0, \sigma_n^2)$ (Termal ve sensör gürültüsü).
- **Tuz-Biber Gürültüsü:** Ani piksel doymaları (0 ve 1) (İletim ve bellek hataları).
- **Kenar Üzerindeki Yıkıcı Etki:** Filtresiz türev alındığında, her gürültü pikseli devasa bir gradyan sıçraması yaratarak yüzlerce sahte kenar üretir.
- **Görsel:** `results/figures/fig01_original_and_noise.png`
> **Konuşmacı Notu (35 sn):**  
> "Deneylerimizde iki farklı yapay gürültü simüle ettik: Gauss gürültüsü ve tuz-biber gürültüsü. Sağdaki figürde orijinal referans görüntü ile gürültülü varyasyonlarını görebilirsiniz. Bu gürültüler temizlenmediği takdirde türev operatörleri sinyal yerine gürültüyü kenar olarak tespit edecektir."

---

### SLAYT 8: 1. Derece Gradyan: Sobel Operatörü
- **Çekirdekler:**
  $$S_x = \begin{bmatrix} -1 & 0 & 1 \\ -2 & 0 & 2 \\ -1 & 0 & 1 \end{bmatrix}, \quad S_y = \begin{bmatrix} -1 & -2 & -1 \\ 0 & 0 & 0 \\ 1 & 2 & 1 \end{bmatrix}$$
- **Merkez Ağırlığı:** Katsayıların 2 olması, türev anında yerel bir Gauss yumuşatması sağlar.
- **Gradyan Büyüklüğü & Yönü:**
  $$M = \sqrt{G_x^2 + G_y^2}, \quad \theta = \text{atan2}(G_y, G_x)$$
- **Eşikleme:** İstatistiksel adaptif eşik ($T = \mu + 1.2\sigma$) ile ikili harita elde edilir.
- **Görsel:** `results/figures/fig03_sobel_analysis.png`
> **Konuşmacı Notu (40 sn):**  
> "Sobel operatörü birinci derece türev yaklaşımıdır. En büyük avantajı, merkez katsayılarında 2 çarpanı kullanarak türev sırasında yerel bir üçgen/Gauss yumuşatması uygulamasıdır. Sağ tarafta Gx, Gy, büyüklük, renkli yön haritası ve eşiklenmiş ikili kenar haritasını detaylıca görebilirsiniz."

---

### SLAYT 9: 1. Derece Gradyan: Prewitt Operatörü
- **Çekirdekler:**
  $$P_x = \begin{bmatrix} -1 & 0 & 1 \\ -1 & 0 & 1 \\ -1 & 0 & 1 \end{bmatrix}, \quad P_y = \begin{bmatrix} -1 & -1 & -1 \\ 0 & 0 & 0 \\ 1 & 1 & 1 \end{bmatrix}$$
- **Düz Aritmetik Ortalama:** Komşulukları eşit ağırlıkla toplar, yerel ağırlıklandırma yapmaz.
- **Sobel ile Kıyaslama:** Hesaplama açısından basittir ancak köşegenlerde gürültüye biraz daha açıktır.
- **Görsel:** `results/figures/fig04_prewitt_analysis.png`
> **Konuşmacı Notu (35 sn):**  
> "Prewitt operatörü de Sobel gibi 3x3 boyutundadır; ancak komşu satır veya sütunları eşit katsayılarla toplar. Bu durum gürültülü bölgelerde Sobel'e kıyasla kenarların daha pürüzlü çıkmasına neden olur. Çıktı figüründe Prewitt gradyan bileşenlerini ve eşikleme sonucunu inceleyebilirsiniz."

---

### SLAYT 10: 2. Derece Türev: Laplacian Operatörü ve Sıfır Geçişi
- **Skaler İkinci Türev:** $\nabla^2 I = \frac{\partial^2 I}{\partial x^2} + \frac{\partial^2 I}{\partial y^2}$
- **4-Komşuluk Çekirdeği:** `[0 1 0; 1 -4 1; 0 1 0]` (İzotropiktir, yönden bağımsızdır).
- **Yöntem 1 (Mutlak Eşik):** $|\nabla^2 I| \ge T$ (Geniş ve çift kenar eğilimi).
- **Yöntem 2 (Sıfır Geçişi - Zero-Crossing):** Komşularda zıt işaret ($v_1 \cdot v_2 < 0$) ve dik eğim kontrolü ile tek piksel kalınlığında kapalı kontur üretir.
- **Görsel:** `results/figures/fig05_laplacian_analysis.png`
> **Konuşmacı Notu (45 sn):**  
> "Laplacian ikinci derece skaler bir türev operatörüdür. Birinci türevin tepe yaptığı yerlerde ikinci türev sıfırdan geçer. Biz kodumuzda hem mutlak genlik eşikleme yöntemini hem de 4 yönde komşuluk tarayan sıfır geçişi algoritmasını uyguladık. Sıfır geçişi, tek piksel kalınlığında son derece hassas hatlar sağlamıştır."

---

### SLAYT 11: Uygulama Mimarisi ve Kod Akışı
- **İşlem Hattı (Pipeline):** Giriş Görüntüsü $\to$ Double/Norm $\to$ Gürültü Enjeksiyonu $\to$ Gauss Yumuşatma $\to$ 2B Konvolüsyon $\to$ Kenar Haritaları & Metrikler.
- **Sıfırdan Modüller (`src/`):**
  - `my_conv2.m`: 2B for döngülü konvolüsyon motoru
  - `gaussian_kernel.m`: Normalize 2B Gauss çekirdeği üreticisi
  - `add_noise.m`: Gauss ve tuz-biber simülatörü
  - `apply_sobel.m` & `apply_prewitt.m`: 1. derece dedektörler
  - `apply_laplacian.m`: İkinci türev ve sıfır geçişi
  - `evaluate_metrics.m`: Sayısal hata ve süre ölçümü
  - `tests/test_my_conv2.m`: 5 adımlı otomatik birim doğrulama
> **Konuşmacı Notu (35 sn):**  
> "Yazılım mimarimiz endüstri standardı modüler prensiplere uygun olarak geliştirildi. Sol tarafta ana işlem akışını, sağ tarafta ise src klasörü altındaki bağımsız fonksiyonları görüyorsunuz. Kodlarımız Image Processing Toolbox olmasa dahi sentetik fallback mekanizması sayesinde yüzde yüz bağımsız çalışabilmektedir."

---

### SLAYT 12: Deneysel Sonuçlar ve Kenar Haritaları Karşılaştırması
- **Sobel:** En dengeli, kesintisiz ve sahte gürültüden arındırılmış kenarları üretti.
- **Prewitt:** Sobel'e yakın fakat köşegen geçişlerde hafif pürüzlü kenarlar verdi.
- **Laplacian (Mutlak):** Çift kenar ve gürültü kalıntıları sebebiyle dağınık kaldı.
- **Laplacian (Sıfır Geçişi):** Tek piksel inceliğinde ve kapalı kontur halinde ideal sınırlar çıkardı.
- **Görsel:** `results/figures/fig06_operator_comparison.png`
> **Konuşmacı Notu (40 sn):**  
> "Bu slaytta 4 farklı yöntemin aynı gürültüden arındırılmış görüntü üzerindeki kenar haritalarını görüyorsunuz. Sobel gürültüye en dayanıklı sonucu verirken, Laplacian sıfır geçişi yöntemi tek piksel kalınlığında kapalı nesne sınırları oluşturmada belirgin bir üstünlük sergilemiştir."

---

### SLAYT 13: Sayısal Doğrulama: my_conv2 vs MATLAB Yerleşik Fonksiyonları
- **Hata Tablosu:**

| Test / Karşılaştırma | Maks Hata | MAE | MSE | PSNR (dB) | Süre |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `my_conv2` vs `conv2(same)` | **2.22e-16** | **1.85e-17** | **0.00** | **Inf** | 0.18 s vs 0.002 s |
| `my_conv2` vs `imfilter` | **4.44e-16** | **3.12e-17** | **0.00** | **Inf** | 0.18 s vs 0.003 s |
| Gauss 5x5 ($\sigma=1.0$) | 2.18e-01 | 2.81e-02 | 2.26e-03 | **26.46 dB** | N/A |

- **Bilimsel Çıkarım:** Maksimum hata $10^{-16}$ (IEEE 754 Machine Epsilon) seviyesindedir. Kendi algoritmamız yerleşik C motoruyla tam matematiksel özdeşliğe sahiptir.
- **Görsel:** `results/figures/fig07_custom_vs_builtin_diff.png`
> **Konuşmacı Notu (45 sn):**  
> "Projemizin en kritik bilimsel çıktısı bu slayttadır. Tabloda görüldüğü üzere kendi yazdığımız my_conv2 ile MATLAB'in yerleşik conv2 fonksiyonu arasındaki maksimum fark 2.22 x 10^-16'dır. Yani iki sonuç matematiksel olarak özdeştir. Sağdaki fark haritasında da herhangi bir sapma olmadığını görebilirsiniz."

---

### SLAYT 14: Operatörlerin Karşılaştırılması ve Tartışma
| Kriter | Sobel | Prewitt | Laplacian (Mutlak) | Laplacian (Sıfır Geçişi) |
| :--- | :--- | :--- | :--- | :--- |
| **Türev Derecesi** | 1. Derece ($\nabla I$) | 1. Derece ($\nabla I$) | 2. Derece ($\nabla^2 I$) | 2. Derece ($\nabla^2 I$) |
| **Yön Bilgisi** | Var ($\theta$ açısı) | Var ($\theta$ açısı) | Yok (İzotropik) | Yok (İzotropik) |
| **Gürültü Direnci** | **Yüksek** | Orta | Çok Düşük | Orta-Düşük |
| **Kenar Kalınlığı** | Geniş | Geniş | Dağınık | **Tek Piksel (İnce)** |

- **Önerilen Kullanım Alanları:**
  - **Sobel:** Genel amaçlı vizyon, robotik görme, yön duyarlı öznitelik çıkarımı.
  - **Prewitt:** Donanım kısıtlı gömülü sistemler, basit gradyan kestirimi.
  - **Laplacian (ZC):** Medikal görüntü segmentasyonu, hassas boyutlandırma, kapalı konturlar.
> **Konuşmacı Notu (40 sn):**  
> "Operatörleri özetleyecek olursak: Sobel gürültü direnci ve yön bilgisiyle genel uygulamalarda liderdir. Laplacian sıfır geçişi ise özellikle hassas medikal görüntüleme ve nesne ölçümlerinde tek piksel inceliğinde kapalı hatlar sağladığı için tercih edilir."

---

### SLAYT 15: Sonuçlar ve Gelecek Çalışmalar
- **Elde Edilen Başarılar:**
  1. `my_conv2` ile $10^{-16}$ makine hassasiyetinde tam doğruluk kanıtlandı.
  2. Sınır dolgularında `'replicate'` modunun kenar doğruluğunu koruduğu gösterildi.
  3. $5\times5, \sigma=1.0$ Gauss filtresi ile optimal gürültü bastırma (26.46 dB) sağlandı.
  4. Sobel'in gürültü direnci, Laplacian ZC'nin ise ince kontur kabiliyeti belgelendi.
- **Gelecek Çalışmalar:**
  - Canny kenar dedektörü (Non-Maximum Suppression ve çift eşikli histerezis).
  - Morfolojik işlemler (dilation/erosion) ile kenar bütünleme.
  - CUDA / C-MEX ile gerçek zamanlı video hızlandırması.
> **Konuşmacı Notu (35 sn):**  
> "Sonuç olarak, projemiz baştan belirlenen tüm bilimsel ve yazılımsal hedeflere ulaşmıştır. my_conv2 fonksiyonu hazır fonksiyonlarla tam uyuşmuş, türev operatörleri başarıyla analiz edilmiştir. Gelecek adımlarda Canny algoritması ve CUDA tabanlı hızlandırmalar üzerinde çalışmayı planlıyoruz."

---

### SLAYT 16: Kaynakça ve Açık Kaynak Referansları
1. Gonzalez, R. C., & Woods, R. E. (2018). *Digital Image Processing* (4th ed.). Pearson.
2. Marr, D., & Hildreth, E. (1980). Theory of edge detection. *Proc. Royal Soc. London*, 207, 187-217.
3. Canny, J. (1986). A computational approach to edge detection. *IEEE TPAMI*, 8(6), 679-698.
4. MathWorks (2024). *Image Processing Toolbox Documentation*.
5. Açık Kaynak GitHub Depoları:
   - `arijit-dasgupta / MachineVision_ImageProcessing` (MIT)
   - `shashwb / Edge-Detection-MATLAB` (MIT)
   - `Halkhoori2000 / Image-Filtering-and-Hough-Transform` (Apache-2.0)
   - `tecnickcom / edgetools` (MIT)
> **Konuşmacı Notu (25 sn):**  
> "Çalışmamızda görüntü işlemenin temel başucu kitabı olan Gonzalez & Woods ile Marr-Hildreth'in teorik yaklaşımlarından yararlandık. Ayrıca açık kaynak dünyasındaki MIT ve Apache lisanslı saygın GitHub projelerini temiz oda yaklaşımıyla inceleyip referans dosyamızda detaylandırdık."

---

### SLAYT 17: Teşekkürler ve Sorular
- **Kocaeli Üniversitesi • Yapay Zekâ ve Makine Öğrenmesi Bölümü**
- **Danial Pourrashidi | Bilimsel Hesaplama Teknikleri Dersi**
- **GitHub Deposu:** https://github.com/Danial-Pourrashidi/matlab-edge-detection-and-filtering
- **Soru - Cevap**
> **Konuşmacı Notu (20 sn):**  
> "Beni sabırla dinlediğiniz için teşekkür ederim. Projenin tüm kaynak kodları, testleri ve bilimsel raporu GitHub depomuzda erişime açıktır. Şimdi sorularınızı yanıtlamaktan memnuniyet duyarım."

