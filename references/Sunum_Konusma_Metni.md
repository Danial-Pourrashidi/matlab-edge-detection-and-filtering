# Görüntü İşleme ile Kenar Tespit ve Filtreleme Algoritmaları
## 10 - 15 Dakikalık Profesyonel Akademik Sunum Metni (Kelimesi Kelimesine Okuma Rehberi)

**Ders:** Bilimsel Hesaplama Teknikleri  
**Bölüm:** Kocaeli Üniversitesi • Yapay Zekâ ve Makine Öğrenmesi Bölümü  
**Proje Yürütücüsü:** Danial Pourrashidi  
**Sunum Dosyası:** `presentation/Kenar_Tespit_ve_Filtreleme_Sunumu_Final.pptx`  
**Hedef Sunum Süresi:** ~12 - 14 Dakika (İdeal Akademik Ritim: Dakikada ~130-145 kelime)

---

### 🎙️ SUNUM ÖNCESİ KISA HATIRLATMALAR VE İPUÇLARI
1. **Duruş ve Ses Tonu:** Slaytlara sırtınızı dönmeyin; ekrana kısa bir göz ucuyla bakıp jüri üyeleriyle göz teması kurun.
2. **Köşeli Parantezler `[...]`:** Bu kısımlar sizin için sahne ve slayt geçiş yönergeleridir; sesli okunmaz.
3. **Vurgular:** **Kalın** yazılmış kelimelerde ses tonunuzu hafifçe yükselterek kavramı vurgulayın.
4. **Zaman Kontrolü:** Yanınızda bir kronometre veya telefonunuzun saatini açık bulundurun.

---

### SLAYT 1: KAPAK SLAYTI [Süre: 00:00 - 00:45 | 45 saniye]
`[Slayt 1 ekranda açık. Kendinizden emin, saygılı ve enerjik bir ses tonuyla başlayın.]`

> "Sayın jüri üyeleri, değerli hocalarım ve sevgili arkadaşlarım, hepiniz hoş geldiniz.
> 
> Ben Danial Pourrashidi. Kocaeli Üniversitesi Yapay Zekâ ve Makine Öğrenmesi Bölümü bünyesinde yürüttüğümüz **Bilimsel Hesaplama Teknikleri** dersi dönem projesi kapsamında hazırladığım **'Görüntü İşleme ile Kenar Tespit ve Filtreleme Algoritmaları'** başlıklı çalışma sunumumu gerçekleştirmekten onur duyuyorum.
> 
> Bu çalışmada en temel motivasyonumuz; MATLAB'in hazır görüntü işleme kütüphanelerine bir 'kara kutu' gibi bağımlı kalmadan; iki boyutlu uzamsal konvolüsyonu, Gauss gürültü azaltma filtresini ve birinci ile ikinci derece diferansiyel kenar operatörlerini **tamamen sıfırdan, for döngüleri ve matris matematiğiyle** inşa etmek ve elde edilen sonuçları IEEE 754 çift duyarlık standartlarında bilimsel olarak doğrulamaktır.
> 
> İzninizle projemizin genel akış planıyla sunumuma başlamak istiyorum."

`[Slayt Değiştir: Slayt 2'ye Geç]`

---

### SLAYT 2: İÇİNDEKİLER [Süre: 00:45 - 01:25 | 40 saniye]
`[Slayttaki 7 ana blokluk şemayı genel bir el hareketiyle işaret edin.]`

> "Sunumumuz mantıksal bir bütünlük içerisinde yedi ana bölümden oluşmaktadır.
> 
> İlk olarak görüntü işlemede kenar tespiti problemini ve bilimsel motivasyonumuzu ele alacağız. Ardından iki boyutlu konvolüsyonun matematiksel çekirdeğine, çekirdek rotasyonuna ve sınır dolgusu stratejilerine değineceğiz.
> 
> Üçüncü bölümde parametrik 2B Gauss filtresiyle kontrollü gürültü bastırma yaklaşımını; dördüncü bölümde ise Sobel, Prewitt ve Laplacian operatörlerinin gradyan ve sıfır geçişi matematiğini inceleyeceğiz.
> 
> Beşinci bölümde sıfırdan geliştirdiğimiz yazılım mimarisini sunduktan sonra, altıncı bölümde deneysel sonuçlarımızı ve kendi yazdığımız `my_conv2` motoru ile MATLAB'in yerleşik C fonksiyonları arasındaki sayısal metrik karşılaştırmalarını paylaşacağım. Son olarak elde ettiğimiz bulguları tartışıp gelecek çalışma hedeflerimizle sunumumu tamamlayacağım."

`[Slayt Değiştir: Slayt 3'e Geç]`

---

### SLAYT 3: PROBLEM TANIMI: SAYISAL GÖRÜNTÜLERDE KENAR TESPİTİ [Süre: 01:25 - 02:15 | 50 saniye]
`[Ses tonunu hafifçe ciddileştirin, problemin önemini hissettirin.]`

> "Peki, kenar tespiti neden bilgisayarlı görme ve yapay zekânın en kritik problemidir?
> 
> Bir görüntüdeki piksellerin büyük çoğunluğu homojen arka planlardan oluşur. Ancak bir nesnenin geometrik sınırları, yüzey eğimleri ve derinlik süreksizlikleri **yalnızca kenarlarda** yoğunlaşmıştır. Yani kenarlar, bilginin en yoğun sıkıştırıldığı alanlardır.
> 
> Fakat gerçek dünyada hiçbir görüntü ideal değildir. Kamera sensörlerindeki ısıl dalgalanmalar, yetersiz aydınlatma ve dijital iletim kanalları görüntülere kaçınılmaz olarak **Gauss ve tuz-biber gürültüleri** ekler.
> 
> İşte tam bu noktada klasik türev operatörlerinin büyük bir zaafı ortaya çıkar: Türev alma işlemi doğası gereği yüksek frekansları yükseltir. Görüntüye doğrudan türev uyguladığınızda, gürültü bileşenleri gerçek sinyalden katbekat fazla şiddetlenir ve kenar haritası kullanılamaz hâle gelir.
> 
> Dolayısıyla çözülmesi gereken temel bilimsel ikilem şudur: **İnce kenar detaylarını ve konum doğruluğunu kaybetmeden gürültüyü nasıl optimum seviyede bastırabiliriz?**"

`[Slayt Değiştir: Slayt 4'e Geç]`

---

### SLAYT 4: PROJENİN AMACI VE BİLİMSEL HEDEFLERİ [Süre: 02:15 - 03:00 | 45 saniye]
`[Numaralandırılmış hedefleri sırasıyla ve net bir vurguyla aktarın.]`

> "Bu ikilemi çözmek ve konunun teorik derinliğini ortaya koymak amacıyla çalışmamızda beş somut hedef belirledik:
> 
> Birincisi; MATLAB Image Processing Toolbox'a ihtiyaç duymaksızın, 180 derece çekirdek rotasyonu kuralına tam sadık kalarak sıfırdan bir `my_conv2` konvolüsyon motoru geliştirmek.
> 
> İkincisi; görüntü sınırlarında oluşabilecek bilgi kayıplarını ve yapay kararmaları önlemek için 'zero', 'replicate' ve 'symmetric' dolgu mimarilerini saf matris indekslemesiyle kurmak.
> 
> Üçüncüsü; 2B Gauss filtresini çekirdek boyutları ve sigma parametreleriyle optimize ederek en yüksek PSNR değerini yakalamak.
> 
> Dördüncüsü; birinci derece Sobel ve Prewitt operatörleri ile ikinci derece Laplacian operatörünü —özellikle sıfır geçişi mantığıyla— uygulamak.
> 
> Ve beşincisi; elde ettiğimiz tüm sonuçları MATLAB'in derlenmiş C çekirdeğiyle bilimsel metrikler üzerinden kıyaslayarak doğrulamaktır."

`[Slayt Değiştir: Slayt 5'e Geç]`

---

### SLAYT 5: TEORİK ARKA PLAN: SAYISAL GÖRÜNTÜ VE 2B KONVOLÜSYON [Süre: 03:00 - 04:00 | 60 saniye]
`[Sol taraftaki formülü ve sağdaki sınır dolgusu yöntemlerini işaret edin.]`

> "Şimdi projemizin omurgasını oluşturan iki boyutlu konvolüsyon matematiğine yakından bakalım.
> 
> Ekranda gördüğünüz formülde, $I$ giriş görüntüsünü, $K$ ise filtre çekirdeğini temsil eder. Konvolüsyon işlemini sayısal olarak kararlı kılmak adına tüm görüntü matrislerini öncelikle çift duyarlıklı $[0, 1]$ aralığına normalize ettik. Böylece yuvarlama ve taşma hatalarının önüne geçtik.
> 
> Burada altını önemle çizmem gereken teknik bir ayrıntı vardır: **Konvolüsyon ile korelasyon arasındaki fark.** Çapraz korelasyonda filtre matrisi görüntü üzerinde doğrudan kaydırılır. Oysa matematiksel konvolüsyonda çekirdek hem yatay hem dikey eksende 180 derece döndürülmelidir; yani `rot90(K, 2)` uygulanır. Eğer çekirdeğimiz simetrik değilse —ki türev çekirdekleri asimetriktir— bu rotasyonu yapmazsanız türev yönü ters çıkar ve fiziksel kenar doğrultusu bozulur.
> 
> Çekirdek görüntünün kenarlarına geldiğinde taşmalar oluşur. Sağ tarafta incelediğimiz üç dolgu yönteminden **'replicate'** dolgusu; en dış pikselleri dışa doğru yineleyerek enerji kaybını ve yapay siyah çerçeveleri tamamen engellemiş, kenar tespitinde en kararlı sınır koşulu olmuştur."

`[Slayt Değiştir: Slayt 6'ya Geç]`

---

### SLAYT 6: 2D GAUSS FİLTRESİ VE GÜRÜLTÜ AZALTMA [Süre: 04:00 - 04:55 | 55 saniye]
`[Sağ tarafta 9 farklı filtrelenmiş görüntüyü gösteren grid görseline dikkat çekin.]`

> "Türev işleminden önce gürültüyü bastırmak için kullandığımız araç iki boyutlu Gauss filtresidir.
> 
> Sürekli Gauss formülünü ayrık ızgarada merkez $(0, 0)$ olacak şekilde örnekledik. Burada en kritik kural **normalizasyon şartıdır**: Çekirdeğin tüm elemanlarının toplamı tam olarak 1'e bölünmelidir ($K = G / \sum G$). Aksi takdirde görüntünün genel parlaklık ve enerji dengesi bozulur.
> 
> Sağdaki deney ızgarasında 3x3, 5x5 ve 7x7 boyutlarındaki çekirdeklerin $\sigma = 0.5, 1.0$ ve $2.0$ değerlerindeki yanıtlarını görüyorsunuz.
> 
> Bulgularımız şunları göstermiştir: Küçük sigma değerleri gürültüyü temizlemede yetersiz kalırken; 7x7 ve sigma=2.0 gibi aşırı büyük parametreler kenarları aşırı bulanıklaştırarak konum kaybına yol açmıştır. Yapılan PSNR analizlerinde, **5x5 çekirdek ve $\sigma = 1.0$ kombinasyonu 26.46 dB PSNR değeriyle** gürültü bastırma ve kenar koruma arasındaki mükemmel denge noktası olarak belirlenmiştir."

`[Slayt Değiştir: Slayt 7'ye Geç]`

---

### SLAYT 7: GÜRÜLTÜ TÜRLERİ VE KENAR TESPİTİ ÜZERİNDEKİ ETKİSİ [Süre: 04:55 - 05:45 | 50 saniye]
`[Sağdaki orijinal, Gauss gürültülü ve tuz-biber gürültülü üçlü görseli gösterin.]`

> "Algoritmalarımızın dayanıklılığını test etmek amacıyla gerçek dünya bozunurlarını modelleyen iki farklı yapay gürültü simülasyonu gerçekleştirdik:
> 
> İlki, sensör ısınması ve düşük ışık koşullarındaki termal salınımları modelleyen **Gauss gürültüsüdür**. Sıfır ortalama ve 0.008 varyansla eklediğimiz bu gürültü, matrisin tamamına homojen bir mikroskobik pürüzlülük katar.
> 
> İkincisi ise iletim hatlarındaki bit kayıplarını ve arızalı sensör piksellerini modelleyen **tuz-biber (salt-and-pepper) gürültüsüdür**. Burada pikseller yüzde 5 yoğunlukla rastgele olarak tamamen siyah (0) veya tamamen beyaz (1) değerini alır.
> 
> Sağdaki çıktılarda gördüğünüz bu gürültülü görüntüler filtre uygulanmadan türev operatörüne verildiğinde; türev diferansiyeli bu ani sıçramaları sonsuz eğim olarak yorumlar ve gerçek nesne sınırlarını bastıran binlerce sahte kenar üretir. Bu da ön filtrelemenin neden vazgeçilmez olduğunu kanıtlar."

`[Slayt Değiştir: Slayt 8'e Geç]`

---

### SLAYT 8: 1. DERECE GRADYAN: SOBEL OPERATÖRÜ [Süre: 05:45 - 06:45 | 60 saniye]
`[Sağ taraftaki 6 bölümlü Sobel analiz grafiğini (Gx, Gy, Magnitude, Yön, Eşik) işaret edin.]`

> "Filtrelenmiş görüntüden kenar çıkarımında ilk incelediğimiz yöntem, birinci derece türev tabanlı **Sobel operatörüdür**.
> 
> Sobel, yatay türev için $G_x$, dikey türev için ise $G_y$ çekirdeklerini kullanır. Buradaki en can alıcı mimari detay, merkez katsayılarının **$\pm 2$** olmasıdır. Çekirdeğin merkezine verilen bu ekstra ağırlık, türev hesaplanırken türeve dik yönde yerel bir Gauss veya üçgen yumuşatması yapılmasını sağlar. İşte Sobel'in gürültüye karşı bu kadar dirençli olmasının matematiksel sırrı bu merkez katsayısıdır.
> 
> Sağdaki analiz figüründe adım adım görebileceğiniz gibi:
> Önce $G_x$ ve $G_y$ bileşenleri hesaplanır. Ardından gradyan büyüklüğü $M = \sqrt{G_x^2 + G_y^2}$ formülüyle, kenar normal açısı ise $\theta = \text{atan2}(G_y, G_x)$ ile radyan cinsinden yön haritasına dönüştürülür.
> 
> Son adımda, sabit bir sayı vermek yerine, matrisin ortalaması ve standart sapmasından türettiğimiz **adaptif istatistiksel eşikleme ($T = \mu + 1.2\sigma$)** uygulanarak tertemiz bir ikili kenar haritası elde edilmiştir."

`[Slayt Değiştir: Slayt 9'a Geç]`

---

### SLAYT 9: 1. DERECE GRADYAN: PREWITT OPERATÖRÜ [Süre: 06:45 - 07:35 | 50 saniye]
`[Prewitt çekirdeklerini Sobel ile kıyaslayarak anlatın.]`

> "Birinci derece gradyanda ikinci operatörümüz **Prewitt operatörüdür**.
> 
> Prewitt çekirdekleri yapısal olarak Sobel'e çok benzer; ancak merkez piksellerinde ilave ağırlıklandırma yoktur. Katsayılar $[-1, 0, 1]$ şeklinde homojendir ve komşu satırların doğrudan aritmetik ortalamasını alır.
> 
> Bu durum Prewitt'e donanım seviyesinde büyük bir avantaj sağlar: Çarpma işlemi gerektirmez, sadece toplama ve çıkarma ile hesaplanabilir; bu da onu FPGA ve düşük güç tüketimli gömülü mikrodenetleyiciler için son derece cazip kılar.
> 
> Ancak bilimsel açıdan baktığımızda; merkezde ilave yumuşatma ağırlığı bulunmadığı için Prewitt'in gürültüye karşı toleransı Sobel'den bir miktar daha düşüktür. Sağdaki görselde görebileceğiniz üzere, özellikle köşegen geçişlerde ve dokulu bölgelerde hafif pürüzlenmeler meydana gelmektedir."

`[Slayt Değiştir: Slayt 10'a Geç]`

---

### SLAYT 10: 2. DERECE TÜREV: LAPLACIAN VE SIFIR GEÇİŞİ [Süre: 07:35 - 08:40 | 65 saniye]
`[Laplacian formülünü ve özellikle Sıfır Geçişi (Zero-Crossing) çıktısını vurgulayın.]`

> "Şimdi birinci türevlerden ikinci derece türev dünyasına, yani **Laplacian operatörüne** geçiyoruz.
> 
> Laplacian skaler ve **izotropik** bir operatördür ($\nabla^2 I = \partial^2 I/\partial x^2 + \partial^2 I/\partial y^2$). Yönden tamamen bağımsızdır; yani $G_x$ ve $G_y$ gibi iki ayrı konvolüsyona gerek kalmaksızın, tek bir çekirdekle tüm doğrultulardaki kenarları eşzamanlı olarak yakalar.
> 
> Çalışmamızda iki farklı Laplacian yaklaşımını karşılaştırdık:
> Birincisi, genlik üzerinden mutlak eşikleme ($|\nabla^2 I| \ge T$). Sağ alt görselde göreceğiniz üzere bu yöntem kenarların her iki yanında tepe oluşturduğu için çift kenar üretir ve gürültüye karşı aşırı hassastır.
> 
> İkincisi ve asıl üzerinde durduğumuz yöntem ise **Sıfır Geçişi (Zero-Crossing)** yaklaşımıdır. Matematiksel olarak birinci türevin yerel maksimum yaptığı noktalarda, ikinci türev sıfırdan geçer. Geliştirdiğimiz algoritma, iç pikselleri yatay, dikey ve iki köşegen olmak üzere 4 ana doğrultuda tarar; komşular arasında zıt işaret ve dik bir eğim farkı tespit ettiği anda o pikseli kenar olarak işaretler.
> 
> Sonuç: Sağ alttaki (d) panelinde gördüğünüz gibi, **tek piksel inceliğinde ve kapalı kontur hâlinde** kusursuz nesne sınırları elde edilmiştir."

`[Slayt Değiştir: Slayt 11'e Geç]`

---

### SLAYT 11: UYGULAMA MİMARİSİ VE KOD AKIŞI [Süre: 08:40 - 09:30 | 50 saniye]
`[Sol taraftaki işlem adımlarını ve sağdaki modül listesini özetleyin.]`

> "Geliştirdiğimiz projenin yazılım mimarisi, endüstriyel standartlarda katı bir modülerlik prensibiyle tasarlanmıştır.
> 
> Sol tarafta ana işlem hattını görüyorsunuz: Giriş görüntüsünün okunup double formatına çevrilmesiyle başlayan süreç; gürültü enjeksiyonu, Gauss filtrelemesi, konvolüsyon yürütümü ve CSV raporlamasıyla uçtan uca otomatik olarak tamamlanır.
> 
> Sağ tarafta listelenen tüm fonksiyonlar `src/` klasörü altında bağımsız modüller olarak yazılmıştır. Hiçbiri harici bir araç kutusuna ihtiyaç duymaz. Hatta MATLAB ortamında Image Processing Toolbox kurulu olmasa dahi, geliştirdiğimiz sentetik fallback algoritması devreye girerek testlerin kesintisiz çalışmasını garanti altına alır.
> 
> Ayrıca `tests/test_my_conv2.m` dosyamız, 5 farklı birim test senaryosunu otomatik olarak koşarak sistemin matematiksel bütünlüğünü doğrulamaktadır."

`[Slayt Değiştir: Slayt 12'ye Geç]`

---

### SLAYT 12: DENEYSEL SONUÇLAR VE KENAR HARİTALARI KARŞILAŞTIRMASI [Süre: 09:30 - 10:25 | 55 saniye]
`[Sol taraftaki 4 panelli karşılaştırma figürünü gösterin: Sobel, Prewitt, Lap Mutlak, Lap ZC.]`

> "Bu slaytta, aynı gürültüden arındırılmış test görüntüsü üzerinde uygulanan dört farklı yöntemin nihai ikili kenar haritalarını yan yana görüyorsunuz.
> 
> Sol üstteki **Sobel**, sahte kenarları en iyi bastıran, çizgileri en pürüzsüz ve devamlı çıkaran dedektör olmuştur.
> 
> Sağ üstteki **Prewitt**, Sobel'e çok yakın bir performans sergilemekle birlikte, kenar sürekliliğinde mikro kopukluklar barındırmaktadır.
> 
> Sol alttaki **Laplacian mutlak eşikleme**, gürültü kalıntılarını tam izole edememiş ve kalın, dağınık kenarlar üretmiştir.
> 
> Sağ alttaki **Laplacian sıfır geçişi** ise adeta bir çizim kalemi hassasiyetinde, nesnelerin dış hatlarını tek piksel genişliğinde ve kesintisiz konturlar olarak çıkarmayı başarmıştır."

`[Slayt Değiştir: Slayt 13'e Geç]`

---

### SLAYT 13: SAYISAL DOĞRULAMA: my_conv2 vs MATLAB YERLEŞİK FONKSİYONLARI [Süre: 10:25 - 11:30 | 65 saniye]
`[Ses tonunuzu gururlu ve net tutun, tablodaki 10^-16 hatayı ve sağdaki fark haritasını gösterin.]`

> "Şimdi projemizin en kritik bilimsel bulgusunu ve doğrulama tablosunu sizlerle paylaşmak istiyorum.
> 
> Sol taraftaki tabloda, kendi yazdığımız for döngülü `my_conv2` fonksiyonu ile MATLAB'in yıllardır optimize edilen yerleşik `conv2` ve `imfilter` fonksiyonları arasındaki hata metriklerini görüyorsunuz.
> 
> Lütfen ilk iki satıra dikkat ediniz:
> `my_conv2` ile `conv2` arasındaki Maksimum Mutlak Hata **$2.22 \times 10^{-16}$**, Ortalama Mutlak Hata ise **$1.85 \times 10^{-17}$** çıkmıştır. Ortalama karesel hata sıfır ve PSNR değeri Sonsuz (Inf) dB'dir.
> 
> Sayısal analiz bilen hocalarımızın çok iyi bildiği üzere $10^{-16}$, 64-bit IEEE 754 çift duyarlıklı kayan nokta aritmetiğinin makine duyarlılığı sınırıdır (machine epsilon).
> 
> Sağdaki fark haritasına baktığınızda tamamen homojen bir sıfır matrisi görürsünüz. Bu sonuç, kendi for döngülü algoritmamızın MATLAB'in derlenmiş C çekirdeğiyle **matematiksel olarak yüzde yüz özdeş** çalıştığının kesin ve tartışmasız ispatıdır.
> 
> Çalışma süresinde ise beklediğimiz gibi; MATLAB'in SIMD ve Intel MKL kütüphaneleriyle derlenmiş kodu 2 milisaniyede biterken, bizim saf döngümüz yaklaşık 0.18 saniye sürmüştür; bu da pedagojik ve bilimsel doğrulama hedefine tam olarak ulaştığımızı gösterir."

`[Slayt Değiştir: Slayt 14'e Geç]`

---

### SLAYT 14: OPERATÖRLERİN KARŞILAŞTIRILMASI VE TARTIŞMA [Süre: 11:30 - 12:25 | 55 saniye]
`[Tabloyu ve alttaki 3 öneri kartını jüriye hitap ederek özetleyin.]`

> "Elde ettiğimiz tüm teorik ve deneysel verileri bir karar matrisinde özetleyecek olursak:
> 
> Görüntü işlemede 'tek bir en iyi operatör' yoktur; amaca uygun operatör seçimi vardır.
> 
> - **Ne zaman Sobel tercih edilmelidir?** Genel amaçlı bilgisayarlı görme, robotik otonom sürüş sistemleri ve kenarın normal yön açısına ($\theta$) ihtiyaç duyulan öznitelik çıkarımı görevlerinde Sobel altın standarttır.
> 
> - **Ne zaman Prewitt seçilmelidir?** Hesaplama gücü ve enerjisi kısıtlı gömülü sistemlerde, mikrodenetleyicilerde veya donanımsal çarpma bloğu içermeyen FPGA tasarımlarında Prewitt en verimli çözümdür.
> 
> - **Ne zaman Laplacian Sıfır Geçişi kullanılmalıdır?** Nesne boyutlarının milimetrik olarak ölçülmesi gereken endüstriyel kalite kontrolünde, MR/BT gibi medikal görüntü segmentasyonlarında tek piksel kalınlığında kapalı kontur üretmek için Laplacian sıfır geçişi rakipsizdir."

`[Slayt Değiştir: Slayt 15'e Geç]`

---

### SLAYT 15: SONUÇLAR VE GELECEK ÇALIŞMALAR [Süre: 12:25 - 13:15 | 50 saniye]
`[Proje kazanımlarını ve geleceğe dönük vizyonu aktarın.]`

> "Toparlamak gerekirse; bu projeyle birlikte:
> 
> - 2B konvolüsyon algoritması sıfırdan başarıyla modellenmiş ve MATLAB yerleşik motoruyla tam sayısal eşitliği kanıtlanmıştır.
> - 'Replicate' dolgusunun sınır kararmalarını önlemedeki üstünlüğü gösterilmiştir.
> - Gauss filtresinde 5x5 boyut ve sigma=1.0 parametresiyle ideal gürültü bastırma seviyesi yakalanmıştır.
> - 1. ve 2. derece türev operatörlerinin gürültü direnci ve kenar morfolojisi farkları deneysel olarak belgelenmiştir.
> 
> Gelecek çalışmalarda bu mimariyi; Canny kenar dedektörünün çift eşikli histerezis adımıyla genişletmeyi, kenar kopukluklarını gidermek için morfolojik genişletme ve aşındırma filtreleri eklemeyi ve for döngülerini CUDA / C-MEX ile derleyerek 4K video akışında gerçek zamanlı çalışacak bir altyapıya kavuşturmayı hedefliyoruz."

`[Slayt Değiştir: Slayt 16'ya Geç]`

---

### SLAYT 16: KAYNAKÇA VE AÇIK KAYNAK REFERANSLARI [Süre: 13:15 - 13:45 | 30 saniye]
`[Kaynak slaytını kısaca gösterip akademik titizliği vurgulayın.]`

> "Çalışmamızın teorik arka planında Gonzalez ve Woods'un klasik 'Digital Image Processing' eseri ile Marr-Hildreth ve Canny'nin temel makalelerinden faydalandık.
> 
> Ayrıca açık kaynak dünyasında yer alan MIT ve Apache lisanslı saygın GitHub depolarını temiz oda yaklaşımıyla inceleyerek mimari fikirlerini projemize uyarladık. Tüm kaynaklar ve lisans dökümleri GitHub depomuzdaki referans dosyasında detaylandırılmıştır."

`[Slayt Değiştir: Slayt 17'ye Geç]`

---

### SLAYT 17: TEŞEKKÜRLER VE SORULAR [Süre: 13:45 - 14:15 | 30 saniye]
`[Gülümseyerek jüriye bakın, teşekkür edin ve sorulara davet edin.]`

> "Projemizin tüm kaynak kodları, birim testleri, oluşturduğumuz etkileşimli demo dosyası ve bilimsel raporumuz GitHub depomuzda açık kaynak olarak erişime açıktır.
> 
> Beni sabırla ve ilgiyle dinlediğiniz için başta sayın hocalarım olmak üzere tüm jüri üyelerine ve arkadaşlarıma teşekkür ederim.
> 
> Çalışmamla ilgili sorularınızı, eleştirilerinizi ve katkılarınızı yanıtlamaktan büyük memnuniyet duyarım."

---

## 🎯 JÜRİ VE HOCALARDAN GELEBİLECEK MUHTEMEL SORULAR VE HAZIR CEVAPLAR (Q&A)

### Soru 1: "Neden konvolüsyonda çekirdeği 180 derece döndürüyoruz? Döndürmesek ne olurdu?"
**Cevabınız:**  
> "Hocam, konvolüsyonun sürekli uzaydaki tanımı $f(t) * g(t) = \int f(\tau) g(t - \tau) d\tau$ şeklindedir. Buradaki eksi işareti ($-\tau$), filtrenin matematiksel olarak ters çevrilmesini gerektirir. Eğer döndürmezsek bu işlemin adı **çapraz korelasyon** olur. Gauss gibi simetrik filtrelerde döndürmek sonucu değiştirmez; ancak Sobel ve Prewitt gibi yönlü türev çekirdeklerinde çekirdeği döndürmezseniz, pozitif gradyan yönü ile negatif gradyan yönü yer değiştirir; yani nesnenin sağındaki kenar solundaymış gibi hesaplanır."

### Soru 2: "Replicate dolgusu zero-padding'e göre neden daha iyi sonuç verdi?"
**Cevabınız:**  
> "Hocam, zero-padding matrisin dışına yapay olarak sıfır (tamamen siyah) pikseller ekler. Eğer görüntünün sınırındaki pikseller parlaksa (örneğin beyaz bir gökyüzü varsa), parlak pikselden yapay sıfıra geçerken çok dik bir yapay gradyan sıçraması oluşur ve kenar dedektörü görüntünün en dış çerçevesini sahte bir kenar olarak algılar. Replicate dolgusu ise en dıştaki piksel değerini dışarı doğru kopyaladığı için sınır türevini yaklaşık sıfır tutar ve yapay kenar oluşumunu engeller."

### Soru 3: "my_conv2 ile MATLAB conv2 arasında neden 10^-16 seviyesinde fark çıktı, neden tam sıfır değil?"
**Cevabınız:**  
> "Hocam, $10^{-16}$ fark kayan noktalı (floating-point) sayıların ikili tabanda temsilinden kaynaklanan IEEE 754 çift duyarlık sınırıdır. MATLAB'in yerleşik `conv2` fonksiyonu derlenmiş C kodu ve SIMD vektörizasyonu kullanırken toplama işlemlerinin sırası parantezleme açısından ufak farklılıklar gösterebilir. Kayan nokta aritmetiğinde $(a+b)+c$ ile $a+(b+c)$ arasında son basamakta $10^{-16}$ düzeyinde yuvarlama farkı (machine epsilon) oluşması son derece doğaldır ve bu durum matematiksel olarak tam denkliğin göstergesidir."

### Soru 4: "Laplacian sıfır geçişi (zero-crossing) neden tek piksel kenar üretir?"
**Cevabınız:**  
> "Hocam, birinci derece türevde kenar geniş bir tepe (dağ) oluşturur; bu tepeyi bir eşikle kestiğinizde dağın yamacı boyunca birkaç piksel kalınlığında kenar çıkar. Ancak ikinci derece türevde kenar, fonksiyonun artıdan eksiye geçtiği matematiksel sıfır noktasıdır. Sıfır bir alan değil, sadece bir kesişim çizgisi olduğu için komşu pikseller arasındaki işaret değişimini yakaladığımızda kalınlaşma olmadan doğrudan tek piksel genişliğinde bir çizgi elde ederiz."

