# Açık Kaynak GitHub Depo İncelemeleri ve Referanslar

Bu belge, **“Görüntü İşleme ile Kenar Tespit ve Filtreleme Algoritmaları”** projesinin tasarımı ve geliştirilmesi sürecinde incelenen, analiz edilen ve esinlenilen açık kaynak GitHub depolarını, lisans durumlarını ve bu projeye olan katkılarını belgelemektedir.

Tüm kaynak kodlar "temiz oda" (clean-room) yaklaşımıyla, lisans ihlali yapılmaksızın, depoların mimari ve algoritmik yaklaşımlarından ilham alınarak sıfırdan ve bağımsız olarak geliştirilmiştir.

---

## 1. arijit-dasgupta / MachineVision_ImageProcessing
* **Depo URL:** [https://github.com/arijit-dasgupta/MachineVision_ImageProcessing](https://github.com/arijit-dasgupta/MachineVision_ImageProcessing)
* **Lisans:** MIT Lisansı (İzin Veren / Permissive)
* **Projeye Uygunluğu:** MATLAB ortamında yerleşik kütüphanelere (Image Processing Toolbox) bağımlı kalmadan sıfırdan görüntü işleme algoritması geliştirme felsefesini inceler. Modüler işlevsel yapı ve saf matris manipülasyonu açısından projemize son derece uygundur.
* **Alınan Fikir veya Yaklaşım:**
  - Fonksiyonların bağımsız `.m` dosyaları halinde yapılandırılması.
  - Piksel seviyesinde çift for döngüsü ile çekirdek yürütme stratejisi.
  - Görüntü matrisinin `double` tipine normalize edilerek taşma ve yuvarlama hatalarının önlenmesi.
* **Projede Nasıl Uyarlandığı:**
  - Depodaki monolitik yapı yerine, projemizde katı bir fonksiyon ayrımı (`src/` altında bağımsız modüller) kurulmuştur.
  - Çekirdek döndürme (`rot90(K, 2)`) ve üç farklı sınır dolgusu (`zero`, `replicate`, `symmetric`) desteği eklenerek algoritmik derinlik artırılmıştır.
* **Alıntı / Kaynak Gösterme Şekli:**
  > Dasgupta, A. (2021). *MachineVision_ImageProcessing: MATLAB implementations of core computer vision algorithms from scratch*. GitHub. https://github.com/arijit-dasgupta/MachineVision_ImageProcessing

---

## 2. shashwb / Edge-Detection-MATLAB
* **Depo URL:** [https://github.com/shashwb/Edge-Detection-MATLAB](https://github.com/shashwb/Edge-Detection-MATLAB)
* **Lisans:** MIT Lisansı
* **Projeye Uygunluğu:** Laplacian operatörünün gürültüye duyarlılığı ve sıfır geçişi (zero-crossing) mantığıyla kenar sınırlarının tespit edilmesi için referans teşkil eder.
* **Alınan Fikir veya Yaklaşım:**
  - Laplacian ikinci türev matrisinde işaret değişimlerinin ($+ \to -$ veya $- \to +$) tespiti.
  - İkinci türev öncesinde gürültüyü bastırmak için 2B Gauss filtrelemesinin önemi.
  - Sıfır geçişi eşiğinin (gradient slope threshold) kenar kalınlığı üzerindeki etkisi.
* **Projede Nasıl Uyarlandığı:**
  - Depodaki basit komşuluk kontrolü genişletilerek hem 4-komşuluk hem de yatay/dikey eksenel gradyan farkı eşiği eklenmiştir.
  - `apply_laplacian.m` modülünde kullanıcıya hem mutlak genlik eşikleme (`edge_abs`) hem de sıfır geçişi (`edge_zc`) çıktıları eş zamanlı sunulmuştur.
* **Alıntı / Kaynak Gösterme Şekli:**
  > Shashwat, B. (2020). *Edge-Detection-MATLAB: Edge detection filters and zero-crossing implementations in MATLAB*. GitHub. https://github.com/shashwb/Edge-Detection-MATLAB

---

## 3. Halkhoori2000 / Image-Filtering-and-Hough-Transform
* **Depo URL:** [https://github.com/Halkhoori2000/Image-Filtering-and-Hough-Transform](https://github.com/Halkhoori2000/Image-Filtering-and-Hough-Transform)
* **Lisans:** Apache License 2.0
* **Projeye Uygunluğu:** Çekirdek dolgusu (kernel padding), sınır koşulları ve 2D konvolüsyonun temel doğrulaması konularında uygulanabilir teknikler barındırır.
* **Alınan Fikir veya Yaklaşım:**
  - Farklı çekirdek boyutları ($3\times3, 5\times5, 7\times7$) için dinamik dolgu (padding) hesaplama (`floor(k/2)`).
  - Kenar piksellerinde bilgi kaybını ve siyah çerçeve oluşumunu engellemek için `'replicate'` dolgusunun kullanımı.
* **Projede Nasıl Uyarlandığı:**
  - MATLAB'in yerleşik `padarray` fonksiyonuna bağımlılığı tamamen ortadan kaldıracak saf matris indeksleme (`row_idx`, `col_idx`) geliştirilmiş, böylece kod harici bir toolbox olmaksızın çalışabilir hale getirilmiştir.
  - Sınır dolgusu parametrik bir seçenek haline getirilmiştir (`'zero'`, `'replicate'`, `'symmetric'`).
* **Alıntı / Kaynak Gösterme Şekli:**
  > Halkhoori, A. (2021). *Image-Filtering-and-Hough-Transform*. GitHub. https://github.com/Halkhoori2000/Image-Filtering-and-Hough-Transform

---

## 4. Mahmoud-AboShukr / matlab-image-filtering-and-edge-detection
* **Depo URL:** [https://github.com/Mahmoud-AboShukr/matlab-image-filtering-and-edge-detection](https://github.com/Mahmoud-AboShukr/matlab-image-filtering-and-edge-detection)
* **Lisans:** Açık Kaynak / Eğitim Amaçlı (Educational / Academic use)
* **Projeye Uygunluğu:** Sobel ve Prewitt türev operatörlerinin $G_x$ ve $G_y$ eksenel bileşenleri, gradyan büyüklüğü ve yön açısı hesaplama mantığının teorik kurgusu için referans alınmıştır.
* **Alınan Fikir veya Yaklaşım:**
  - Çekirdek ağırlıklarının gradyan hassasiyetine etkisi (Prewitt'in düz ortalaması vs. Sobel'in Gauss ağırlıklı merkezi).
  - Görselleştirme düzeninde yön bilgisi ve gradyan bileşenlerinin yan yana gösterilmesi.
* **Projede Nasıl Uyarlandığı:**
  - İlgili depodaki görselleştirme düzeni genişletilerek metrik analizleri (PSNR, MSE, MAE, Süre) ile birleştirilmiş ve `main.m` akışında otomatik PNG dışa aktarma mekanizması kurulmuştur.
* **Alıntı / Kaynak Gösterme Şekli:**
  > AboShukr, M. (2020). *MATLAB Image Filtering and Edge Detection Repository*. GitHub.

---

## 5. tecnickcom / edgetools
* **Depo URL:** [https://github.com/tecnickcom/edgetools](https://github.com/tecnickcom/edgetools)
* **Lisans:** MIT Lisansı
* **Projeye Uygunluğu:** Bilimsel doğrulama, metrik hesaplama (MSE, PSNR, MAE) ve algoritmaların sayısal hata toleransları açısından referans alınmıştır.
* **Alınan Fikir veya Yaklaşım:**
  - Özelleştirilmiş filtre fonksiyonlarının MATLAB yerleşik fonksiyonları (`conv2`, `imfilter`) ile sayısal olarak karşılaştırılması.
  - Hata analizinde maksimum mutlak hata (`max(|A - B|)`) ve MSE metriklerinin bir arada raporlanması.
* **Projede Nasıl Uyarlandığı:**
  - `src/evaluate_metrics.m` modülü tasarlanmış; Max Absolute Error, MAE, MSE, PSNR ve çalışma süresi tek bir yapıda toplanıp `results/metrics.csv` olarak kaydedilecek şekilde standartlaştırılmıştır.
* **Alıntı / Kaynak Gösterme Şekli:**
  > Tecnick.com (2018). *edgetools: Edge detection and image filtering comparison tools*. GitHub. https://github.com/tecnickcom/edgetools

---

## Telif ve Lisans Uyumluluk Beyanı
Yukarıda listelenen açık kaynak projeler yalnızca mimari kurgu, matematiksel formülasyon yaklaşımları ve görselleştirme şablonları açısından incelenmiştir. Bu projedeki tüm kod blokları, fonksiyon imzaları, Türkçe açıklamalar, test senaryoları ve rapor şablonları özgün olarak üretilmiş olup doğrudan kod kopyalama (copy-paste) yapılmamıştır. Proje bütünüyle bağımsız ve MIT uyumlu bir geliştirme yaklaşımı sergilemektedir.

