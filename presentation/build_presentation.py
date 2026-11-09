import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 Widescreen standard
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Colors
    NAVY = RGBColor(15, 23, 42)       # #0F172A
    BLUE = RGBColor(30, 58, 138)      # #1E3A8A
    ORANGE = RGBColor(234, 88, 12)    # #EA580C
    TEAL = RGBColor(13, 148, 136)     # #0D9488
    SLATE = RGBColor(51, 65, 85)      # #334155
    MUTED = RGBColor(100, 116, 139)   # #64748B
    WHITE = RGBColor(255, 255, 255)
    BG_LIGHT = RGBColor(248, 250, 252)
    BORDER_CLR = RGBColor(226, 232, 240)

    fig_dir = r"c:\Users\fmn17\OneDrive\Desktop\BHT Proje\results\figures"

    def apply_background(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="BİLİMSEL HESAPLAMA TEKNİKLERİ PROJESİ"):
        # Category Tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ORANGE
        p_cat.font.name = "Arial"

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.65))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = NAVY
        p.font.name = "Arial"

        # Accent Line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.42), Inches(1.5), Inches(0.04))
        line.fill.solid()
        line.fill.fore_color.rgb = TEAL
        line.line.fill.background()

    def add_footer(slide, current_idx, total_slides=17):
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(9.5), Inches(0.3))
        tf = footer_box.text_frame
        p = tf.paragraphs[0]
        p.text = "Kocaeli Üniversitesi • Yapay Zekâ ve Makine Öğrenmesi Bölümü • Görüntü İşleme Projesi"
        p.font.size = Pt(9)
        p.font.color.rgb = MUTED
        p.font.name = "Arial"

        num_box = slide.shapes.add_textbox(Inches(11.0), Inches(7.0), Inches(1.5), Inches(0.3))
        tf_num = num_box.text_frame
        p_num = tf_num.paragraphs[0]
        p_num.alignment = PP_ALIGN.RIGHT
        p_num.text = f"{current_idx} / {total_slides}"
        p_num.font.size = Pt(9)
        p_num.font.bold = True
        p_num.font.color.rgb = SLATE
        p_num.font.name = "Arial"

    def set_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text

    # =========================================================================
    # SLAYT 1: KAPAK SLAYTI
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_background(s1, NAVY)

    # Decorative colored stripe
    top_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.15))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = ORANGE
    top_bar.line.fill.background()

    # University & Department
    univ_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.3), Inches(0.8))
    tf_u = univ_box.text_frame
    p_u = tf_u.paragraphs[0]
    p_u.text = "KOCAELİ ÜNİVERSİTESİ"
    p_u.font.size = Pt(16)
    p_u.font.bold = True
    p_u.font.color.rgb = TEAL
    p_u.font.name = "Arial"

    p_d = tf_u.add_paragraph()
    p_d.text = "Yapay Zekâ ve Makine Öğrenmesi Bölümü • Bilimsel Hesaplama Teknikleri Dersi"
    p_d.font.size = Pt(13)
    p_d.font.color.rgb = RGBColor(148, 163, 184)
    p_d.font.name = "Arial"

    # Main Project Title
    title_box = s1.shapes.add_textbox(Inches(1.0), Inches(2.3), Inches(11.3), Inches(2.2))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = "Görüntü İşleme ile Kenar Tespit ve\nFiltreleme Algoritmaları"
    p_t.font.size = Pt(36)
    p_t.font.bold = True
    p_t.font.color.rgb = WHITE
    p_t.font.name = "Arial"

    p_sub = tf_t.add_paragraph()
    p_sub.text = "2B Konvolüsyon, Gauss Yumuşatma, Sobel, Prewitt ve Laplacian Operatörlerinin Sıfırdan Analizi"
    p_sub.font.size = Pt(16)
    p_sub.font.color.rgb = RGBColor(203, 213, 225)
    p_sub.font.name = "Arial"

    # Metadata Card
    meta_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(5.0), Inches(11.333), Inches(1.5))
    meta_card.fill.solid()
    meta_card.fill.fore_color.rgb = RGBColor(30, 41, 59)
    meta_card.line.color.rgb = RGBColor(51, 65, 85)

    meta_box = s1.shapes.add_textbox(Inches(1.2), Inches(5.15), Inches(10.9), Inches(1.2))
    tf_m = meta_box.text_frame
    p_m1 = tf_m.paragraphs[0]
    p_m1.text = "Proje Yürütücüsü: Danial Pourrashidi"
    p_m1.font.size = Pt(13)
    p_m1.font.bold = True
    p_m1.font.color.rgb = WHITE

    p_m2 = tf_m.add_paragraph()
    p_m2.text = "Danışman / Öğretim Üyesi: Dr. Öğr. Üyesi / Ders Sorumlusu"
    p_m2.font.size = Pt(12)
    p_m2.font.color.rgb = RGBColor(203, 213, 225)

    p_m3 = tf_m.add_paragraph()
    p_m3.text = "GitHub Deposu: github.com/Danial-Pourrashidi/matlab-edge-detection-and-filtering • Tarih: 2026"
    p_m3.font.size = Pt(11)
    p_m3.font.color.rgb = TEAL

    set_notes(s1, "Sayın jüri üyeleri ve değerli hocalarım, hoş geldiniz. Bugün sizlere Bilimsel Hesaplama Teknikleri dersi kapsamında hazırladığım 'Görüntü İşleme ile Kenar Tespit ve Filtreleme Algoritmaları' konulu araştırma ve uygulama projemizi sunacağım. Bu çalışmada MATLAB Image Processing Toolbox'a bağımlı kalmadan, çekirdek konvolüsyon ve türev operatörlerini sıfırdan geliştirdik. Şimdi genel akışımıza bakalım.")

    # =========================================================================
    # SLAYT 2: İÇİNDEKİLER
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_background(s2, BG_LIGHT)
    add_header(s2, "Sunum Planı ve İçindekiler")
    add_footer(s2, 2)

    topics = [
        ("01", "Problem Tanımı ve Proje Hedefleri", "Gürültülü görüntülerde kenar tespiti zorlukları ve bilimsel motivasyon"),
        ("02", "Teorik Temeller ve Konvolüsyon", "2B konvolüsyon matematiği, 180° çekirdek rotasyonu ve sınır dolguları"),
        ("03", "2D Gauss Filtresi ve Gürültü Azaltma", "Ayrık Gauss dağılımı, sigma ve çekirdek boyutu optimizasyonu"),
        ("04", "Kenar Dedektörleri: Sobel, Prewitt, Laplacian", "1. ve 2. derece türev operatörleri, gradyan vektörleri, sıfır geçişi"),
        ("05", "Uygulama Mimarisi (From Scratch)", "Sıfırdan yazılan modüller, 'my_conv2' algoritması ve test altyapısı"),
        ("06", "Deneysel Sonuçlar ve Metrik Kıyaslaması", "my_conv2 vs conv2/imfilter, hata metrikleri (MSE, PSNR, Süre)"),
        ("07", "Karşılaştırmalı Tartışma ve Sonuç", "Operatörlerin üstünlükleri, kısıtları ve gelecek çalışma planları")
    ]

    for idx, (num, title, desc) in enumerate(topics):
        col = idx // 4
        row = idx % 4
        left = Inches(0.8 + col * 5.9)
        top = Inches(1.7 + row * 1.25)

        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.6), Inches(1.1))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = BORDER_CLR

        tbox = s2.shapes.add_textbox(left + Inches(0.15), top + Inches(0.1), Inches(5.3), Inches(0.9))
        tf = tbox.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = f"{num}. {title}"
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = NAVY

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = SLATE

    set_notes(s2, "Sunumumuz 7 ana aşamadan oluşmaktadır. İlk olarak problemi ve motivasyonumuzu açıklayacak, ardından konvolüsyon ve Gauss filtresinin teorik arka planına değineceğiz. Sonrasında Sobel, Prewitt ve Laplacian operatörlerini detaylandırıp, sıfırdan geliştirdiğimiz my_conv2 ile MATLAB'in yerleşik fonksiyonlarını metrikler üzerinden karşılaştıracağız.")

    # =========================================================================
    # SLAYT 3: PROBLEM TANIMI
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_background(s3, BG_LIGHT)
    add_header(s3, "Problem Tanımı: Sayısal Görüntülerde Kenar Tespiti")
    add_footer(s3, 3)

    p_items = [
        ("Kenarların Kritik Önemi", "Kenarlar; nesne sınırlarını, geometrik şekilleri ve derinlik süreksizliklerini taşır. Bilgisayarlı görme ve yapay zekâ uygulamalarının temel özniteliğidir."),
        ("Gerçek Dünya Gürültüsü", "Kamera sensörleri, optik yetersizlikler ve iletim kanalları; Gauss ve tuz-biber gibi gürültüler üreterek piksel değerlerinde rastgele dalgalanmalara yol açar."),
        ("Türev Operatörlerinin Zaafı", "Kenar tespiti türev almaya dayanır. Ancak türev işlemi yüksek frekanslı bileşenleri yükselttiğinden, gürültüyü sinyalden katlarca daha fazla şiddetlendirir."),
        ("Bilimsel İkilem", "Gürültüyü yok etmek için filtreleme yapılırken ince kenarlar bulanıklaşabilir. İnce detayları korurken gürültüyü bastırmak hassas bir optimizasyon gerektirir.")
    ]

    for idx, (title, desc) in enumerate(p_items):
        top = Inches(1.7 + idx * 1.25)
        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.733), Inches(1.1))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = BORDER_CLR

        # Bullet icon box
        ibox = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), top + Inches(0.25), Inches(0.12), Inches(0.6))
        ibox.fill.solid()
        ibox.fill.fore_color.rgb = ORANGE if idx % 2 == 0 else TEAL
        ibox.line.fill.background()

        tbox = s3.shapes.add_textbox(Inches(1.25), top + Inches(0.12), Inches(11.1), Inches(0.85))
        tf = tbox.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = NAVY

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(11)
        p2.font.color.rgb = SLATE

    set_notes(s3, "Sayısal görüntülerde kenar tespiti neden bu kadar kritiktir? Çünkü bir görüntünün anlamsal içeriğinin büyük kısmı parlaklık süreksizliklerinde gizlidir. Ancak fiziksel sensörler gürültülüdür. Türev operatörleri de yapısı gereği yüksek frekanslı gürültüleri fazlasıyla yükseltir. Bu ikilem, gürültü temizleme ile kenar tespiti arasında dikkatli bir denge kurmayı zorunlu kılar.")

    # =========================================================================
    # SLAYT 4: PROJE AMACI VE KAPSAMI
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    apply_background(s4, BG_LIGHT)
    add_header(s4, "Projenin Amacı ve Bilimsel Hedefleri")
    add_footer(s4, 4)

    goals = [
        ("Sıfırdan 2B Konvolüsyon", "MATLAB Image Processing Toolbox kullanmaksızın, çift for döngüsü ve 180° çekirdek rotasyonu ile 'my_conv2' fonksiyonunu inşa etmek."),
        ("Sınır Koşulları Yönetimi", "'zero', 'replicate' ve 'symmetric' dolgu yöntemlerini saf matris indislemesiyle kütüphanesiz olarak geliştirmek."),
        ("Parametrik Gauss Filtreleme", "3x3, 5x5, 7x7 boyutları ve sigma (0.5, 1.0, 2.0) parametreleriyle optimal gürültü azaltma dengesini incelemek."),
        ("1. ve 2. Derece Türev Analizi", "Sobel, Prewitt gradyanları ve Laplacian (Mutlak Eşikleme + Sıfır Geçişi) yöntemlerini teorik ve görsel olarak uygulamak."),
        ("Bilimsel Doğrulama", "Kendi yazdığımız fonksiyonları MATLAB 'conv2' ve 'imfilter' ile karşılaştırıp hata metrikleri (Max Error, MAE, MSE, PSNR, Süre) üretmek.")
    ]

    for idx, (g_title, g_desc) in enumerate(goals):
        top = Inches(1.7 + idx * 1.0)
        card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.733), Inches(0.88))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = BORDER_CLR

        tbox = s4.shapes.add_textbox(Inches(1.0), top + Inches(0.08), Inches(11.3), Inches(0.7))
        tf = tbox.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = f"• {g_title}: "
        p1.font.bold = True
        p1.font.size = Pt(13)
        p1.font.color.rgb = BLUE

        run = p1.add_run()
        run.text = g_desc
        run.font.bold = False
        run.font.size = Pt(11)
        run.font.color.rgb = SLATE

    set_notes(s4, "Bu projede en temel amacımız bir siyah kutu yaklaşımı sergilemek yerine, 2B konvolüsyon ve türev mekaniğini for döngüleri ve matris matematiğiyle sıfırdan yazmaktır. Ayrıca farklı sınır dolgularının kenar bozulmalarına etkisini incelemeyi ve yerleşik C tabanlı MATLAB fonksiyonları ile bilimsel bir karşılaştırma tablosu oluşturmayı hedefledik.")

    # =========================================================================
    # SLAYT 5: TEORİK ARKA PLAN: 2B KONVOLÜSYON
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    apply_background(s5, BG_LIGHT)
    add_header(s5, "Teorik Arka Plan: Sayısal Görüntü ve 2B Konvolüsyon")
    add_footer(s5, 5)

    # Left: Formula & Mechanics
    left_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.7), Inches(4.9))
    left_card.fill.solid()
    left_card.fill.fore_color.rgb = WHITE
    left_card.line.color.rgb = BORDER_CLR

    ltbox = s5.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.3), Inches(4.5))
    ltf = ltbox.text_frame
    ltf.word_wrap = True

    p = ltf.paragraphs[0]
    p.text = "2D Konvolüsyon Matematiği"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = NAVY

    p = ltf.add_paragraph()
    p.text = "(I * K)(x, y) = ∑∑ I(x - u, y - v) · K(u, v)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = ORANGE

    items_c = [
        "Ayrık Görüntü Matrisi: I(x, y) ∈ [0, 1] double formatında normalize edilir.",
        "Çekirdek Rotasyonu: Matematiksel konvolüsyonda çekirdek yatay ve dikeyde 180° çevrilir: K_rot = rot90(K, 2).",
        "Korelasyon Farkı: Korelasyonda çekirdek doğrudan çarpılırken, konvolüsyonda ters çevrilir; asimetrik türev filtrelerinde yön doğruluğu için bu zorunludur."
    ]
    for it in items_c:
        p = ltf.add_paragraph()
        p.text = f"• {it}"
        p.font.size = Pt(11)
        p.font.color.rgb = SLATE

    # Right: Padding Strategies
    right_card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.7), Inches(5.7), Inches(4.9))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = WHITE
    right_card.line.color.rgb = BORDER_CLR

    rtbox = s5.shapes.add_textbox(Inches(7.0), Inches(1.85), Inches(5.3), Inches(4.5))
    rtf = rtbox.text_frame
    rtf.word_wrap = True

    p = rtf.paragraphs[0]
    p.text = "Sınır Dolgusu (Padding) Yöntemleri"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = NAVY

    pad_items = [
        ("Zero-Padding ('zero')", "Dış piksellere 0 atanır. Basittir ancak sınır kenarlarında yapay koyulaşma (kararma) oluşturur."),
        ("Replicate ('replicate')", "En dış sınır pikselleri dışa doğru yinelenir. Enerji kaybını önler ve kenar tespitinde en kararlı sonucu verir."),
        ("Symmetric ('symmetric')", "Sınır boyunca ayna yansıması oluşturulur. Sürekliliği korur ve frekans anomalilerini engeller.")
    ]

    for p_title, p_desc in pad_items:
        p = rtf.add_paragraph()
        p.text = f"▸ {p_title}: "
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = TEAL
        run = p.add_run()
        run.text = p_desc
        run.font.bold = False
        run.font.size = Pt(10.5)
        run.font.color.rgb = SLATE

    set_notes(s5, "Konvolüsyon ile korelasyon arasındaki fark bilimsel hesaplamada çok önemlidir. Konvolüsyonda filtre matrisi 180 derece döndürülür. Eğer çekirdek simetrik değilse döndürme yapılmadığında türev yönü ters çıkar. Ayrıca sınır piksellerinde replicate dolgusu kullanarak görüntü kenarlarında siyah çerçeve oluşmasını engelledik.")

    # =========================================================================
    # SLAYT 6: 2D GAUSS FİLTRESİ
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    apply_background(s6, BG_LIGHT)
    add_header(s6, "2D Gauss Filtresi ve Gürültü Azaltma")
    add_footer(s6, 6)

    # Left: Text Card
    left_card = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.2), Inches(4.9))
    left_card.fill.solid()
    left_card.fill.fore_color.rgb = WHITE
    left_card.line.color.rgb = BORDER_CLR

    tbox = s6.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(4.8), Inches(4.5))
    tf = tbox.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Gauss Dağılımı Matematiği"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY

    p = tf.add_paragraph()
    p.text = "G(x, y) = (1 / 2πσ²) · exp(-(x² + y²) / 2σ²)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = ORANGE

    g_points = [
        "Normalizasyon: Toplam enerjinin ve parlaklığın korunması için K = G / sum(G) şarttır.",
        "Sigma (σ) Etkisi: Standart sapma arttıkça yumuşatma şiddeti artar; küçük sigma gürültüyü tam silemezken, büyük sigma ince kenarları yok eder.",
        "Çekirdek Boyutu: 3x3, 5x5 ve 7x7 boyutları test edilmiştir. 5x5 ve σ=1.0 optimal PSNR (26.46 dB) sağlamıştır."
    ]
    for pt in g_points:
        p = tf.add_paragraph()
        p.text = f"• {pt}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = SLATE

    # Right: MATLAB Output Image
    fig2_path = os.path.join(fig_dir, "fig02_gaussian_filtering_grid.png")
    if os.path.exists(fig2_path):
        s6.shapes.add_picture(fig2_path, Inches(6.3), Inches(1.7), width=Inches(6.2))

    set_notes(s6, "Ekranda 3x3, 5x5 ve 7x7 çekirdek boyutlarının sigma 0.5, 1.0 ve 2.0 ile oluşturduğu 9 farklı filtreleme senaryosunu görüyorsunuz. 5x5 boyutunda sigma=1.0 seçildiğinde gürültü bastırılırken kenarların keskinliği korunmuş ve en yüksek PSNR değeri olan 26.46 dB elde edilmiştir.")

    # =========================================================================
    # SLAYT 7: GÜRÜLTÜ TÜRLERİ
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    apply_background(s7, BG_LIGHT)
    add_header(s7, "Gürültü Türleri ve Kenar Tespiti Üzerindeki Etkisi")
    add_footer(s7, 7)

    # Left: Explanations
    left_card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.2), Inches(4.9))
    left_card.fill.solid()
    left_card.fill.fore_color.rgb = WHITE
    left_card.line.color.rgb = BORDER_CLR

    tbox = s7.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(4.8), Inches(4.5))
    tf = tbox.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Modellenen Gürültü Tipleri"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY

    n_points = [
        ("Gauss Gürültüsü", "Sensör ısınması ve düşük ışık koşullarındaki elektronik dalgalanmaları modeller: I_noisy = I + N(0, σ²)."),
        ("Tuz-Biber Gürültüsü", "İletim hataları veya bozuk sensör piksellerini modeller. Pikseller rastgele olarak 0 (biber) veya 1 (tuz) değerini alır."),
        ("Kenar Algoritmalarına Yıkıcı Etkisi", "Filtre uygulanmadan türev alındığında, gürültü pikselleri aşırı yüksek gradyan üretir ve haritada binlerce sahte kenar patlaması meydana gelir.")
    ]
    for n_title, n_desc in n_points:
        p = tf.add_paragraph()
        p.text = f"▸ {n_title}: "
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = BLUE
        run = p.add_run()
        run.text = n_desc
        run.font.bold = False
        run.font.size = Pt(10.5)
        run.font.color.rgb = SLATE

    # Right: MATLAB Output Image
    fig1_path = os.path.join(fig_dir, "fig01_original_and_noise.png")
    if os.path.exists(fig1_path):
        s7.shapes.add_picture(fig1_path, Inches(6.3), Inches(2.2), width=Inches(6.2))

    set_notes(s7, "Deneylerimizde iki farklı yapay gürültü simüle ettik: Gauss gürültüsü ve tuz-biber gürültüsü. Sağdaki figürde orijinal referans görüntü ile gürültülü varyasyonlarını görebilirsiniz. Bu gürültüler temizlenmediği takdirde türev operatörleri sinyal yerine gürültüyü kenar olarak tespit edecektir.")

    # =========================================================================
    # SLAYT 8: SOBEL OPERATÖRÜ
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    apply_background(s8, BG_LIGHT)
    add_header(s8, "1. Derece Gradyan: Sobel Operatörü")
    add_footer(s8, 8)

    # Left: Explanation & Formulas
    left_card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.0), Inches(4.9))
    left_card.fill.solid()
    left_card.fill.fore_color.rgb = WHITE
    left_card.line.color.rgb = BORDER_CLR

    tbox = s8.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(4.6), Inches(4.5))
    tf = tbox.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Sobel Çekirdekleri ve Formülasyon"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY

    s_items = [
        "Gx (Dikey Kenar): [-1 0 1; -2 0 2; -1 0 1]",
        "Gy (Yatay Kenar): [-1 -2 -1; 0 0 0; 1 2 1]",
        "Merkez Ağırlığı: Ortadaki katsayıların 2 olması, türev anında yerel Gauss yumuşatması sağlar.",
        "Büyüklük (Magnitude): M = sqrt(Gx² + Gy²)",
        "Yön (Orientation): θ = atan2(Gy, Gx)",
        "Eşikleme: Adaptif eşik (T = mean + 1.2·std) ile ikili (binary) kenar haritası üretilir."
    ]
    for it in s_items:
        p = tf.add_paragraph()
        p.text = f"• {it}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = SLATE

    # Right: Image
    fig3_path = os.path.join(fig_dir, "fig03_sobel_analysis.png")
    if os.path.exists(fig3_path):
        s8.shapes.add_picture(fig3_path, Inches(6.0), Inches(1.7), width=Inches(6.5))

    set_notes(s8, "Sobel operatörü birinci derece türev yaklaşımıdır. En büyük avantajı, merkez katsayılarında 2 çarpanı kullanarak türev sırasında yerel bir üçgen/Gauss yumuşatması uygulamasıdır. Sağ tarafta Gx, Gy, büyüklük, renkli yön haritası ve eşiklenmiş ikili kenar haritasını detaylıca görebilirsiniz.")

    # =========================================================================
    # SLAYT 9: PREWITT OPERATÖRÜ
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    apply_background(s9, BG_LIGHT)
    add_header(s9, "1. Derece Gradyan: Prewitt Operatörü")
    add_footer(s9, 9)

    left_card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.0), Inches(4.9))
    left_card.fill.solid()
    left_card.fill.fore_color.rgb = WHITE
    left_card.line.color.rgb = BORDER_CLR

    tbox = s9.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(4.6), Inches(4.5))
    tf = tbox.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Prewitt Çekirdekleri ve Karşılaştırma"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY

    p_items = [
        "Gx Çekirdeği: [-1 0 1; -1 0 1; -1 0 1]",
        "Gy Çekirdeği: [-1 -1 -1; 0 0 0; 1 1 1]",
        "Düz Ortalama: Prewitt komşulukları eşit ağırlıkla toplar, yerel ağırlıklandırma yapmaz.",
        "Sobel ile Farkı: Sobel'e göre hesaplaması bir miktar daha basittir ancak gürültüye karşı toleransı düşüktür.",
        "Kenar Büyüklüğü: M = sqrt(Gx² + Gy²)"
    ]
    for it in p_items:
        p = tf.add_paragraph()
        p.text = f"• {it}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = SLATE

    fig4_path = os.path.join(fig_dir, "fig04_prewitt_analysis.png")
    if os.path.exists(fig4_path):
        s9.shapes.add_picture(fig4_path, Inches(6.0), Inches(1.7), width=Inches(6.5))

    set_notes(s9, "Prewitt operatörü de Sobel gibi 3x3 boyutundadır; ancak komşu satır veya sütunları eşit katsayılarla toplar. Bu durum gürültülü bölgelerde Sobel'e kıyasla kenarların daha pürüzlü çıkmasına neden olur. Çıktı figüründe Prewitt gradyan bileşenlerini ve eşikleme sonucunu inceleyebilirsiniz.")

    # =========================================================================
    # SLAYT 10: LAPLACIAN OPERATÖRÜ
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    apply_background(s10, BG_LIGHT)
    add_header(s10, "2. Derece Türev: Laplacian Operatörü ve Sıfır Geçişi")
    add_footer(s10, 10)

    left_card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.0), Inches(4.9))
    left_card.fill.solid()
    left_card.fill.fore_color.rgb = WHITE
    left_card.line.color.rgb = BORDER_CLR

    tbox = s10.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(4.6), Inches(4.5))
    tf = tbox.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Laplacian Matematiği"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY

    l_items = [
        "Skaler İkinci Türev: ∇²I = ∂²I/∂x² + ∂²I/∂y²",
        "4-Komşuluk Çekirdeği: [0 1 0; 1 -4 1; 0 1 0]",
        "İzotropik Yapı: Yönden bağımsızdır, tek bir konvolüsyonla tüm yönlerdeki kenarları çıkarır.",
        "Yöntem 1 (Mutlak Eşik): |∇²I| ≥ T (Kalın ve gürültüye hassas kenarlar).",
        "Yöntem 2 (Sıfır Geçişi): Zıt işaretli komşular ve dik eğim kontrolü ile tek piksel kalınlığında kapalı kontur üretir."
    ]
    for it in l_items:
        p = tf.add_paragraph()
        p.text = f"• {it}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = SLATE

    fig5_path = os.path.join(fig_dir, "fig05_laplacian_analysis.png")
    if os.path.exists(fig5_path):
        s10.shapes.add_picture(fig5_path, Inches(6.0), Inches(1.8), width=Inches(6.5))

    set_notes(s10, "Laplacian ikinci derece skaler bir türev operatörüdür. Birinci türevin tepe yaptığı yerlerde ikinci türev sıfırdan geçer. Biz kodumuzda hem mutlak genlik eşikleme yöntemini hem de 4 yönde komşuluk tarayan sıfır geçişi algoritmasını uyguladık. Sıfır geçişi, tek piksel kalınlığında son derece hassas hatlar sağlamıştır.")

    # =========================================================================
    # SLAYT 11: UYGULAMA MİMARİSİ
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    apply_background(s11, BG_LIGHT)
    add_header(s11, "Uygulama Mimarisi ve Kod Akışı")
    add_footer(s11, 11)

    # Workflow steps
    steps = [
        ("1. Giriş & Double", "Görüntü okunur, gri seviyeye çevrilir ve [0, 1] aralığına normalize edilir."),
        ("2. Gürültü Enjeksiyonu", "add_noise.m ile kontrollü Gauss ve tuz-biber gürültüleri eklenir."),
        ("3. 2D Gauss Filtresi", "gaussian_kernel.m ile parametrik çekirdek üretilir, my_conv2 ile yumuşatılır."),
        ("4. 1. ve 2. Derece Türev", "apply_sobel, apply_prewitt ve apply_laplacian modülleri çalıştırılır."),
        ("5. Karşılaştırma & CSV", "evaluate_metrics.m ile hata ve süre ölçülür, results/metrics.csv yazılır.")
    ]

    for idx, (st_title, st_desc) in enumerate(steps):
        top = Inches(1.7 + idx * 1.0)
        card = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(6.0), Inches(0.88))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = BORDER_CLR

        tbox = s11.shapes.add_textbox(Inches(0.95), top + Inches(0.08), Inches(5.7), Inches(0.7))
        tf = tbox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f"{st_title}: "
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = BLUE
        run = p.add_run()
        run.text = st_desc
        run.font.bold = False
        run.font.size = Pt(10.5)
        run.font.color.rgb = SLATE

    # Right: Source modules overview card
    right_card = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.1), Inches(1.7), Inches(5.4), Inches(4.9))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = NAVY
    right_card.line.fill.background()

    rtbox = s11.shapes.add_textbox(Inches(7.3), Inches(1.85), Inches(5.0), Inches(4.5))
    rtf = rtbox.text_frame
    rtf.word_wrap = True
    p = rtf.paragraphs[0]
    p.text = "Modüler Kod Altyapısı (src/)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = WHITE

    files_info = [
        ("my_conv2.m", "2B konvolüsyon (rot90, 3 dolgu tipi)"),
        ("gaussian_kernel.m", "Normalize 2B Gauss çekirdeği"),
        ("add_noise.m", "Gauss ve Tuz-biber gürültü üretici"),
        ("apply_sobel.m", "Sobel gradyanları ve adaptif eşik"),
        ("apply_prewitt.m", "Prewitt gradyanları ve eşikleme"),
        ("apply_laplacian.m", "Laplacian ve sıfır geçişi tespiti"),
        ("evaluate_metrics.m", "Max Error, MAE, MSE, PSNR, Süre"),
        ("test_my_conv2.m", "5 adet otomatik birim doğrulama testi")
    ]
    for fn, fd in files_info:
        p = rtf.add_paragraph()
        p.text = f"• {fn}: "
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = TEAL
        run = p.add_run()
        run.text = fd
        run.font.bold = False
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(203, 213, 225)

    set_notes(s11, "Yazılım mimarimiz endüstri standardı modüler prensiplere uygun olarak geliştirildi. Sol tarafta ana işlem akışını, sağ tarafta ise src klasörü altındaki bağımsız fonksiyonları görüyorsunuz. Kodlarımız Image Processing Toolbox olmasa dahi sentetik fallback mekanizması sayesinde yüzde yüz bağımsız çalışabilmektedir.")

    # =========================================================================
    # SLAYT 12: DENEYSEL SONUÇLAR
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    apply_background(s12, BG_LIGHT)
    add_header(s12, "Deneysel Sonuçlar ve Kenar Haritaları Karşılaştırması")
    add_footer(s12, 12)

    # Left: Image
    fig6_path = os.path.join(fig_dir, "fig06_operator_comparison.png")
    if os.path.exists(fig6_path):
        s12.shapes.add_picture(fig6_path, Inches(0.8), Inches(1.7), width=Inches(6.8))

    # Right: Analysis Card
    right_card = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.8), Inches(1.7), Inches(4.7), Inches(4.9))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = WHITE
    right_card.line.color.rgb = BORDER_CLR

    rtbox = s12.shapes.add_textbox(Inches(8.0), Inches(1.85), Inches(4.3), Inches(4.5))
    rtf = rtbox.text_frame
    rtf.word_wrap = True

    p = rtf.paragraphs[0]
    p.text = "Görsel Çıktı Değerlendirmesi"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY

    eval_items = [
        ("Sobel", "En dengeli ve pürüzsüz kenar hatlarını üretti. Sahte gürültü kenarlarını en iyi bastıran operatör oldu."),
        ("Prewitt", "Sobel'e çok yakın hatlar çizdi; ancak köşegen geçişlerde gürültü kalıntılarına biraz daha açık kaldı."),
        ("Laplacian (Mutlak)", "Kenar geçişlerini tespit etti ancak çift kenar ve gürültü duyarlılığı sebebiyle geniş dağılım gösterdi."),
        ("Laplacian (Sıfır Geçişi)", "Tek piksel inceliğinde ve kapalı kontur şeklinde son derece net kenarlar sağladı.")
    ]
    for en, ed in eval_items:
        p = rtf.add_paragraph()
        p.text = f"▸ {en}: "
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = BLUE
        run = p.add_run()
        run.text = ed
        run.font.bold = False
        run.font.size = Pt(10.5)
        run.font.color.rgb = SLATE

    set_notes(s12, "Bu slaytta 4 farklı yöntemin aynı gürültüden arındırılmış görüntü üzerindeki kenar haritalarını görüyorsunuz. Sobel gürültüye en dayanıklı sonucu verirken, Laplacian sıfır geçişi yöntemi tek piksel kalınlığında kapalı nesne sınırları oluşturmada belirgin bir üstünlük sergilemiştir.")

    # =========================================================================
    # SLAYT 13: my_conv2 vs MATLAB FONKSİYONLARI
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    apply_background(s13, BG_LIGHT)
    add_header(s13, "Sayısal Doğrulama: my_conv2 vs MATLAB Yerleşik Fonksiyonları")
    add_footer(s13, 13)

    # Left: Metrics Table
    # Create Table
    rows = 6
    cols = 5
    table_shape = s13.shapes.add_table(rows, cols, Inches(0.8), Inches(1.7), Inches(6.8), Inches(2.6))
    table = table_shape.table

    table.columns[0].width = Inches(2.2)
    table.columns[1].width = Inches(1.2)
    table.columns[2].width = Inches(1.1)
    table.columns[3].width = Inches(1.1)
    table.columns[4].width = Inches(1.2)

    headers = ["Karşılaştırma", "Maks Hata", "MAE", "MSE", "PSNR"]
    for c_idx, h in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = BLUE
        cell.text = h
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    data = [
        ["my_conv2 vs conv2", "2.22e-16", "1.85e-17", "0.00", "Inf (dB)"],
        ["my_conv2 vs imfilter", "4.44e-16", "3.12e-17", "0.00", "Inf (dB)"],
        ["Gauss 3x3 (s=1.0)", "2.45e-01", "3.31e-02", "3.07e-03", "25.13 dB"],
        ["Gauss 5x5 (s=1.0)", "2.18e-01", "2.81e-02", "2.26e-03", "26.46 dB"],
        ["Gauss 7x7 (s=1.0)", "2.24e-01", "2.92e-02", "2.45e-03", "26.11 dB"]
    ]

    for r_idx, row in enumerate(data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if r_idx % 2 == 0 else BG_LIGHT
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(9.5)
            p.font.color.rgb = SLATE
            p.alignment = PP_ALIGN.CENTER if c_idx > 0 else PP_ALIGN.LEFT

    # Explanation under table
    cbox = s13.shapes.add_textbox(Inches(0.8), Inches(4.5), Inches(6.8), Inches(2.1))
    ctf = cbox.text_frame
    ctf.word_wrap = True
    p = ctf.paragraphs[0]
    p.text = "Sayısal Doğruluk Yorumu:"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY

    t_points = [
        "Maksimum Hata 10^-16 seviyesindedir (IEEE 754 çift duyarlık makine epsilonu).",
        "Bu sonuç, yazdığımız my_conv2 algoritmasının MATLAB'in derlenmiş C motoruyla matematiksel olarak %100 özdeş çalıştığını kanıtlar.",
        "Süre Kıyası: my_conv2 ≈ 0.18 s (öğretici çift döngü) | conv2 ≈ 0.002 s (Intel MKL / SIMD optimize C kodu)."
    ]
    for tp in t_points:
        p = ctf.add_paragraph()
        p.text = f"• {tp}"
        p.font.size = Pt(10)
        p.font.color.rgb = SLATE

    # Right: Difference Image
    fig7_path = os.path.join(fig_dir, "fig07_custom_vs_builtin_diff.png")
    if os.path.exists(fig7_path):
        s13.shapes.add_picture(fig7_path, Inches(7.8), Inches(2.2), width=Inches(4.8))

    set_notes(s13, "Projemizin en kritik bilimsel çıktısı bu slayttadır. Tabloda görüldüğü üzere kendi yazdığımız my_conv2 ile MATLAB'in yerleşik conv2 fonksiyonu arasındaki maksimum fark 2.22 x 10^-16'dır. Yani iki sonuç matematiksel olarak özdeştir. Sağdaki fark haritasında da herhangi bir sapma olmadığını görebilirsiniz.")

    # =========================================================================
    # SLAYT 14: KARŞILAŞTIRMA VE TARTIŞMA
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    apply_background(s14, BG_LIGHT)
    add_header(s14, "Operatörlerin Karşılaştırılması ve Tartışma")
    add_footer(s14, 14)

    # Comparison Table
    t_shape = s14.shapes.add_table(5, 5, Inches(0.8), Inches(1.7), Inches(11.733), Inches(2.4))
    tbl = t_shape.table

    tbl.columns[0].width = Inches(2.3)
    tbl.columns[1].width = Inches(2.35)
    tbl.columns[2].width = Inches(2.35)
    tbl.columns[3].width = Inches(2.35)
    tbl.columns[4].width = Inches(2.35)

    comp_headers = ["Kriter", "Sobel", "Prewitt", "Laplacian (Mutlak)", "Laplacian (Sıfır Geçişi)"]
    for c_idx, h in enumerate(comp_headers):
        cell = tbl.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        cell.text = h
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    comp_data = [
        ["Türev Mertebesi", "1. Derece (∇I)", "1. Derece (∇I)", "2. Derece (∇²I)", "2. Derece (∇²I)"],
        ["Yön Bilgisi", "Var (θ açısı)", "Var (θ açısı)", "Yok (İzotropik)", "Yok (İzotropik)"],
        ["Gürültü Direnci", "Yüksek (Merkez 2)", "Orta (Düz ortalama)", "Çok Düşük", "Orta-Düşük (Eğim şartlı)"],
        ["Kenar Kalınlığı", "Geniş (İnceltme ister)", "Geniş (İnceltme ister)", "Dağınık", "Tek Piksel (İnce kontur)"]
    ]

    for r_idx, row in enumerate(comp_data):
        for c_idx, val in enumerate(row):
            cell = tbl.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = WHITE if r_idx % 2 == 0 else BG_LIGHT
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(10)
            p.font.color.rgb = SLATE
            p.alignment = PP_ALIGN.CENTER if c_idx > 0 else PP_ALIGN.LEFT

    # Recommendations Cards Below
    recs = [
        ("Ne Zaman Sobel?", "Genel amaçlı bilgisayarlı görme, gürültülü sahneler ve kenar yönünün gerektiği uygulamalar."),
        ("Ne Zaman Prewitt?", "Basit gradyan tahmini ve donanım kısıtlı gömülü sistemler."),
        ("Ne Zaman Laplacian (ZC)?", "Hassas boyut ölçümü, medikal segmentasyon ve kapalı nesne sınırlarının çıkarımı.")
    ]

    for idx, (rt, rd) in enumerate(recs):
        left = Inches(0.8 + idx * 4.0)
        card = s14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(4.5), Inches(3.733), Inches(2.1))
        card.fill.solid()
        card.fill.fore_color.rgb = WHITE
        card.line.color.rgb = BORDER_CLR

        tbox = s14.shapes.add_textbox(left + Inches(0.15), Inches(4.6), Inches(3.4), Inches(1.9))
        tf = tbox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = rt
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = ORANGE if idx == 0 else (TEAL if idx == 1 else BLUE)

        p = tf.add_paragraph()
        p.text = rd
        p.font.size = Pt(10)
        p.font.color.rgb = SLATE

    set_notes(s14, "Operatörleri özetleyecek olursak: Sobel gürültü direnci ve yön bilgisiyle genel uygulamalarda liderdir. Laplacian sıfır geçişi ise özellikle hassas medikal görüntüleme ve nesne ölçümlerinde tek piksel inceliğinde kapalı hatlar sağladığı için tercih edilir.")

    # =========================================================================
    # SLAYT 15: SONUÇLAR VE GELECEK ÇALIŞMALAR
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    apply_background(s15, BG_LIGHT)
    add_header(s15, "Sonuçlar ve Gelecek Çalışmalar")
    add_footer(s15, 15)

    # Left: Findings
    left_card = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), Inches(5.7), Inches(4.9))
    left_card.fill.solid()
    left_card.fill.fore_color.rgb = WHITE
    left_card.line.color.rgb = BORDER_CLR

    ltbox = s15.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.3), Inches(4.5))
    ltf = ltbox.text_frame
    ltf.word_wrap = True
    p = ltf.paragraphs[0]
    p.text = "Elde Edilen Temel Çıkarımlar"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY

    findings = [
        "Sıfırdan Konvolüsyon Başarısı: 'my_conv2' algoritması MATLAB'in C fonksiyonuyla 10^-16 hata ile tam matematiksel denklik gösterdi.",
        "Sınır Koşulları: 'replicate' dolgusu kenar kararmasını engelleyerek kenar tespitinde en yüksek doğruluğu sağladı.",
        "Filtreleme Dengesi: 5x5 Gauss çekirdeği (σ=1.0), aşırı bulanıklaştırma yapmadan gürültüyü bastıran ideal çalışma noktası oldu.",
        "Operatör Ayrımı: Sobel sağlamlıkta, Laplacian sıfır geçişi ise kenar inceliğinde öne çıktı."
    ]
    for f in findings:
        p = ltf.add_paragraph()
        p.text = f"✔ {f}"
        p.font.size = Pt(10.5)
        p.font.color.rgb = SLATE

    # Right: Future work
    right_card = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.7), Inches(5.7), Inches(4.9))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = WHITE
    right_card.line.color.rgb = BORDER_CLR

    rtbox = s15.shapes.add_textbox(Inches(7.0), Inches(1.85), Inches(5.3), Inches(4.5))
    rtf = rtbox.text_frame
    rtf.word_wrap = True
    p = rtf.paragraphs[0]
    p.text = "Gelecek Çalışmalar ve İyileştirmeler"
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = NAVY

    future_works = [
        ("Canny Kenar Dedektörü", "Gradyan yönünde tepe olmayanların bastırılması (Non-Maximum Suppression) ve çift eşikli histerezis algoritması entegrasyonu."),
        ("Morfolojik Filtreleme", "Kenar haritalarındaki kopuklukları gidermek için genişletme (dilation) ve aşındırma (erosion) adımları."),
        ("Çok Ölçekli DoG (Difference of Gaussians)", "Farklı sigma seviyelerinde Gauss farkları alarak ölçekten bağımsız kenar piramidi oluşturulması."),
        ("GPU & MEX Hızlandırması", "For döngülerinin CUDA veya C-MEX ile hızlandırılarak gerçek zamanlı video akışına uyarlanması.")
    ]
    for fw_t, fw_d in future_works:
        p = rtf.add_paragraph()
        p.text = f"▸ {fw_t}: "
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEAL
        run = p.add_run()
        run.text = fw_d
        run.font.bold = False
        run.font.size = Pt(10)
        run.font.color.rgb = SLATE

    set_notes(s15, "Sonuç olarak, projemiz baştan belirlenen tüm bilimsel ve yazılımsal hedeflere ulaşmıştır. my_conv2 fonksiyonu hazır fonksiyonlarla tam uyuşmuş, türev operatörleri başarıyla analiz edilmiştir. Gelecek adımlarda Canny algoritması ve CUDA tabanlı hızlandırmalar üzerinde çalışmayı planlıyoruz.")

    # =========================================================================
    # SLAYT 16: KAYNAKÇA
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    apply_background(s16, BG_LIGHT)
    add_header(s16, "Kaynakça ve Açık Kaynak Referansları")
    add_footer(s16, 16)

    c_card = s16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.7), Inches(11.733), Inches(4.9))
    c_card.fill.solid()
    c_card.fill.fore_color.rgb = WHITE
    c_card.line.color.rgb = BORDER_CLR

    ctbox = s16.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(11.3), Inches(4.5))
    ctf = ctbox.text_frame
    ctf.word_wrap = True

    p = ctf.paragraphs[0]
    p.text = "Akademik Literatür ve Dokümantasyon"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY

    refs = [
        "1. Gonzalez, R. C., & Woods, R. E. (2018). Digital Image Processing (4th ed.). Pearson.",
        "2. Marr, D., & Hildreth, E. (1980). Theory of edge detection. Proc. of the Royal Society of London, 207(1167), 187-217.",
        "3. Canny, J. (1986). A computational approach to edge detection. IEEE Trans. Pattern Anal. Mach. Intell., 8(6), 679-698.",
        "4. MathWorks (2024). MATLAB Image Processing Toolbox Documentation: Spatial Filtering & Edge Detection."
    ]
    for r in refs:
        p = ctf.add_paragraph()
        p.text = r
        p.font.size = Pt(10.5)
        p.font.color.rgb = SLATE

    p = ctf.add_paragraph()
    p.text = "\nİncelenen Açık Kaynak GitHub Projeleri (references/github_repos.md)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY

    gh_refs = [
        "• arijit-dasgupta / MachineVision_ImageProcessing (MIT) - Sıfırdan modüler yapı ve matris manipülasyonu.",
        "• shashwb / Edge-Detection-MATLAB (MIT) - Laplacian ve sıfır geçişi (zero-crossing) kurgusu.",
        "• Halkhoori2000 / Image-Filtering-and-Hough-Transform (Apache-2.0) - Sınır dolgusu ve çekirdek indeksleme.",
        "• tecnickcom / edgetools (MIT) - Bilimsel hata metrikleri ve test senaryoları yaklaşımı."
    ]
    for g in gh_refs:
        p = ctf.add_paragraph()
        p.text = g
        p.font.size = Pt(10)
        p.font.color.rgb = SLATE

    set_notes(s16, "Çalışmamızda görüntü işlemenin temel başucu kitabı olan Gonzalez & Woods ile Marr-Hildreth'in teorik yaklaşımlarından yararlandık. Ayrıca açık kaynak dünyasındaki MIT ve Apache lisanslı saygın GitHub projelerini temiz oda yaklaşımıyla inceleyip referans dosyamızda detaylandırdık.")

    # =========================================================================
    # SLAYT 17: TEŞEKKÜRLER VE SORULAR
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    apply_background(s17, NAVY)

    # Decorative top line
    t_line = s17.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.15))
    t_line.fill.solid()
    t_line.fill.fore_color.rgb = ORANGE
    t_line.line.fill.background()

    # Content Box
    t_box = s17.shapes.add_textbox(Inches(1.5), Inches(1.8), Inches(10.3), Inches(4.5))
    tf = t_box.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "TEŞEKKÜR EDERİM"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.font.name = "Arial"
    p.alignment = PP_ALIGN.CENTER

    p = tf.add_paragraph()
    p.text = "Sorularınız ve katkılarınız için hazırım."
    p.font.size = Pt(18)
    p.font.color.rgb = RGBColor(203, 213, 225)
    p.alignment = PP_ALIGN.CENTER

    p = tf.add_paragraph()
    p.text = "\n\nKocaeli Üniversitesi • Yapay Zekâ ve Makine Öğrenmesi Bölümü"
    p.font.size = Pt(14)
    p.font.color.rgb = TEAL
    p.alignment = PP_ALIGN.CENTER

    p = tf.add_paragraph()
    p.text = "Danial Pourrashidi | Bilimsel Hesaplama Teknikleri Dersi"
    p.font.size = Pt(13)
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

    p = tf.add_paragraph()
    p.text = "Açık Kaynak Kod Deposu:\nhttps://github.com/Danial-Pourrashidi/matlab-edge-detection-and-filtering"
    p.font.size = Pt(12)
    p.font.color.rgb = ORANGE
    p.alignment = PP_ALIGN.CENTER

    set_notes(s17, "Beni sabırla dinlediğiniz için teşekkür ederim. Projenin tüm kaynak kodları, testleri ve bilimsel raporu GitHub depomuzda erişime açıktır. Şimdi sorularınızı yanıtlamaktan memnuniyet duyarım.")

    output_path = r"c:\Users\fmn17\OneDrive\Desktop\BHT Proje\presentation\Kenar_Tespit_ve_Filtreleme_Sunumu.pptx"
    prs.save(output_path)
    print(f"Presentation successfully saved to: {output_path}")

if __name__ == "__main__":
    create_deck()
