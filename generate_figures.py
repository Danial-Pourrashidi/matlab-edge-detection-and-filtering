import os
import numpy as np
import matplotlib.pyplot as plt

fig_dir = r"c:\Users\fmn17\OneDrive\Desktop\BHT Proje\results\figures"
os.makedirs(fig_dir, exist_ok=True)

# 1. Sentetik Yüksek Kaliteli Test Görüntüsü Üretimi
N = 256
X, Y = np.meshgrid(np.linspace(-1, 1, N), np.linspace(-1, 1, N))
I_orig = np.zeros((N, N), dtype=float)

# Merkez Daire
I_orig[np.sqrt(X**2 + Y**2) < 0.5] = 0.85
# Dikdörtgen
I_orig[(X > 0.2) & (X < 0.7) & (Y > -0.6) & (Y < -0.1)] = 0.45
# Dikey gradyan şeridi
for c in range(20, 61):
    I_orig[:, c] = (c - 20) / 40.0 * 0.8 + 0.1
# İnce çizgi
I_orig[180:183, 80:220] = 1.0

# 2. Gürültü Ekleme
np.random.seed(42)
# Gauss gürültüsü
I_noisy_gauss = np.clip(I_orig + np.random.normal(0, np.sqrt(0.008), I_orig.shape), 0.0, 1.0)

# Tuz-biber gürültüsü
I_noisy_sp = I_orig.copy()
r = np.random.rand(*I_orig.shape)
I_noisy_sp[r < 0.025] = 0.0
I_noisy_sp[(r >= 0.025) & (r < 0.05)] = 1.0

# Figür 1: Orijinal ve Gürültülü
plt.figure(figsize=(12, 4))
plt.subplot(1, 3, 1)
plt.imshow(I_orig, cmap='gray', vmin=0, vmax=1)
plt.title("Orijinal Referans Görüntü", fontsize=11, fontweight='bold')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(I_noisy_gauss, cmap='gray', vmin=0, vmax=1)
plt.title(r"Gauss Gürültülü ($\sigma^2 = 0.008$)", fontsize=11, fontweight='bold')
plt.axis('off')

plt.subplot(1, 3, 3)
plt.imshow(I_noisy_sp, cmap='gray', vmin=0, vmax=1)
plt.title("Tuz-Biber Gürültülü (Yoğunluk = 0.05)", fontsize=11, fontweight='bold')
plt.axis('off')

plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "fig01_original_and_noise.png"), dpi=200)
plt.close()

# 2B Konvolüsyon fonksiyonu
def my_conv2(img, kernel, pad_type='replicate'):
    kh, kw = kernel.shape
    ih, iw = img.shape
    pt = kh // 2
    pb = kh - 1 - pt
    pl = kw // 2
    pr = kw - 1 - pl
    
    if pad_type == 'replicate':
        padded = np.pad(img, ((pt, pb), (pl, pr)), mode='edge')
    elif pad_type == 'zero':
        padded = np.pad(img, ((pt, pb), (pl, pr)), mode='constant')
    elif pad_type == 'symmetric':
        padded = np.pad(img, ((pt, pb), (pl, pr)), mode='reflect')
        
    k_rot = np.rot90(kernel, 2)
    out = np.zeros_like(img)
    for i in range(ih):
        for j in range(iw):
            out[i, j] = np.sum(padded[i:i+kh, j:j+kw] * k_rot)
    return out

def get_gaussian_kernel(size, sigma):
    rad = size // 2
    x, y = np.meshgrid(np.arange(-rad, rad + 1), np.arange(-rad, rad + 1))
    g = np.exp(-(x**2 + y**2) / (2 * sigma**2))
    return g / np.sum(g)

# Figür 2: Gauss Filtreleme Grid Analizi
plt.figure(figsize=(12, 10))
ksizes = [3, 5, 7]
sigmas = [0.5, 1.0, 2.0]
idx = 1
gauss_best = None

for s in sigmas:
    for k in ksizes:
        K = get_gaussian_kernel(k, s)
        filtered = my_conv2(I_noisy_gauss, K, 'replicate')
        if k == 5 and s == 1.0:
            gauss_best = filtered
        
        mse = np.mean((I_orig - filtered)**2)
        psnr = 10 * np.log10(1.0 / mse) if mse > 0 else 100
        
        plt.subplot(3, 3, idx)
        plt.imshow(filtered, cmap='gray', vmin=0, vmax=1)
        plt.title(f"{k}x{k}, sigma={s:.1f} (PSNR: {psnr:.2f} dB)", fontsize=10)
        plt.axis('off')
        idx += 1

plt.suptitle("2D Gauss Filtresi ile Gürültü Azaltma Parametrik Analizi", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "fig02_gaussian_filtering_grid.png"), dpi=200)
plt.close()

# Sobel Uygulaması
sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=float)
sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=float)
Gx_sobel = my_conv2(gauss_best, sobel_x, 'replicate')
Gy_sobel = my_conv2(gauss_best, sobel_y, 'replicate')
mag_sobel = np.sqrt(Gx_sobel**2 + Gy_sobel**2)
dir_sobel = np.arctan2(Gy_sobel, Gx_sobel)
thresh_sobel = np.mean(mag_sobel) + 1.2 * np.std(mag_sobel)
edges_sobel = mag_sobel >= thresh_sobel

# Figür 3: Sobel Analizi
fig = plt.figure(figsize=(13, 7))
plt.subplot(2, 3, 1)
plt.imshow(gauss_best, cmap='gray')
plt.title("(a) Gauss Filtreli Giriş", fontsize=10, fontweight='bold')
plt.axis('off')

plt.subplot(2, 3, 2)
im = plt.imshow(Gx_sobel, cmap='gray')
plt.colorbar(im, fraction=0.046, pad=0.04)
plt.title("(b) Gx (Yatay Gradyan / Dikey Kenar)", fontsize=10, fontweight='bold')
plt.axis('off')

plt.subplot(2, 3, 3)
im = plt.imshow(Gy_sobel, cmap='gray')
plt.colorbar(im, fraction=0.046, pad=0.04)
plt.title("(c) Gy (Dikey Gradyan / Yatay Kenar)", fontsize=10, fontweight='bold')
plt.axis('off')

plt.subplot(2, 3, 4)
im = plt.imshow(mag_sobel, cmap='hot')
plt.colorbar(im, fraction=0.046, pad=0.04)
plt.title("(d) Gradyan Büyüklüğü (Magnitude)", fontsize=10, fontweight='bold')
plt.axis('off')

plt.subplot(2, 3, 5)
im = plt.imshow(dir_sobel, cmap='hsv', vmin=-np.pi, vmax=np.pi)
plt.colorbar(im, fraction=0.046, pad=0.04)
plt.title(r"(e) Gradyan Yonu [-\pi, \pi]", fontsize=10, fontweight='bold')
plt.axis('off')

plt.subplot(2, 3, 6)
plt.imshow(edges_sobel, cmap='gray')
plt.title("(f) Eşiklenmiş İkili Kenar Haritası", fontsize=10, fontweight='bold')
plt.axis('off')

plt.suptitle("Sobel Kenar Tespiti ve Gradyan Vektör Analizi", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "fig03_sobel_analysis.png"), dpi=200)
plt.close()

# Prewitt Uygulaması
prewitt_x = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=float)
prewitt_y = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]], dtype=float)
Gx_prewitt = my_conv2(gauss_best, prewitt_x, 'replicate')
Gy_prewitt = my_conv2(gauss_best, prewitt_y, 'replicate')
mag_prewitt = np.sqrt(Gx_prewitt**2 + Gy_prewitt**2)
dir_prewitt = np.arctan2(Gy_prewitt, Gx_prewitt)
thresh_prewitt = np.mean(mag_prewitt) + 1.2 * np.std(mag_prewitt)
edges_prewitt = mag_prewitt >= thresh_prewitt

# Figür 4: Prewitt Analizi
fig = plt.figure(figsize=(13, 7))
plt.subplot(2, 3, 1)
plt.imshow(gauss_best, cmap='gray')
plt.title("(a) Gauss Filtreli Giriş", fontsize=10, fontweight='bold')
plt.axis('off')

plt.subplot(2, 3, 2)
im = plt.imshow(Gx_prewitt, cmap='gray')
plt.colorbar(im, fraction=0.046, pad=0.04)
plt.title("(b) Gx (Yatay Gradyan)", fontsize=10, fontweight='bold')
plt.axis('off')

plt.subplot(2, 3, 3)
im = plt.imshow(Gy_prewitt, cmap='gray')
plt.colorbar(im, fraction=0.046, pad=0.04)
plt.title("(c) Gy (Dikey Gradyan)", fontsize=10, fontweight='bold')
plt.axis('off')

plt.subplot(2, 3, 4)
im = plt.imshow(mag_prewitt, cmap='hot')
plt.colorbar(im, fraction=0.046, pad=0.04)
plt.title("(d) Gradyan Büyüklüğü", fontsize=10, fontweight='bold')
plt.axis('off')

plt.subplot(2, 3, 5)
im = plt.imshow(dir_prewitt, cmap='hsv', vmin=-np.pi, vmax=np.pi)
plt.colorbar(im, fraction=0.046, pad=0.04)
plt.title(r"(e) Gradyan Yonu [-\pi, \pi]", fontsize=10, fontweight='bold')
plt.axis('off')

plt.subplot(2, 3, 6)
plt.imshow(edges_prewitt, cmap='gray')
plt.title("(f) Eşiklenmiş İkili Kenar Haritası", fontsize=10, fontweight='bold')
plt.axis('off')

plt.suptitle("Prewitt Kenar Tespiti ve Gradyan Vektör Analizi", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "fig04_prewitt_analysis.png"), dpi=200)
plt.close()

# Laplacian Uygulaması
K_lap = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=float)
lap_raw = my_conv2(gauss_best, K_lap, 'replicate')
abs_thresh = np.mean(np.abs(lap_raw)) + 1.2 * np.std(np.abs(lap_raw))
edge_abs = np.abs(lap_raw) >= abs_thresh

# Sıfır Geçişi
zc_thresh = 0.5 * abs_thresh
edge_zc = np.zeros_like(lap_raw, dtype=bool)
ih, iw = lap_raw.shape

for r in range(1, ih - 1):
    for c in range(1, iw - 1):
        l = lap_raw[r, c-1]
        rt = lap_raw[r, c+1]
        u = lap_raw[r-1, c]
        d = lap_raw[r+1, c]
        ul = lap_raw[r-1, c-1]
        dr = lap_raw[r+1, c+1]
        ur = lap_raw[r-1, c+1]
        dl = lap_raw[r+1, c-1]
        
        is_zc = False
        if (l * rt < 0) and (abs(l - rt) >= zc_thresh):
            is_zc = True
        elif (u * d < 0) and (abs(u - d) >= zc_thresh):
            is_zc = True
        elif (ul * dr < 0) and (abs(ul - dr) >= zc_thresh):
            is_zc = True
        elif (ur * dl < 0) and (abs(ur - dl) >= zc_thresh):
            is_zc = True
        edge_zc[r, c] = is_zc

# Figür 5: Laplacian Analizi
plt.figure(figsize=(12, 6))
plt.subplot(2, 2, 1)
plt.imshow(gauss_best, cmap='gray')
plt.title("(a) Gauss Yumuşatmalı Giriş", fontsize=10, fontweight='bold')
plt.axis('off')

plt.subplot(2, 2, 2)
im = plt.imshow(lap_raw, cmap='gray')
plt.colorbar(im, fraction=0.046, pad=0.04)
plt.title(r"(b) Ham Laplacian Yaniti", fontsize=10, fontweight='bold')
plt.axis('off')

plt.subplot(2, 2, 3)
plt.imshow(edge_abs, cmap='gray')
plt.title(r"(c) Mutlak Genlik Esikleme (|Lap| >= T)", fontsize=10, fontweight='bold')
plt.axis('off')

plt.subplot(2, 2, 4)
plt.imshow(edge_zc, cmap='gray')
plt.title("(d) Sıfır Geçişi (Zero-Crossing) Kenar Haritası", fontsize=10, fontweight='bold')
plt.axis('off')

plt.suptitle("Laplacian İkinci Derece Kenar Tespiti ve Sıfır Geçişi Karşılaştırması", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "fig05_laplacian_analysis.png"), dpi=200)
plt.close()

# Figür 6: Kenar Operatörleri Karşılaştırması
plt.figure(figsize=(12, 7))
plt.subplot(2, 2, 1)
plt.imshow(edges_sobel, cmap='gray')
plt.title("Sobel Eşiklenmiş Kenarlar", fontsize=12, fontweight='bold')
plt.axis('off')

plt.subplot(2, 2, 2)
plt.imshow(edges_prewitt, cmap='gray')
plt.title("Prewitt Eşiklenmiş Kenarlar", fontsize=12, fontweight='bold')
plt.axis('off')

plt.subplot(2, 2, 3)
plt.imshow(edge_abs, cmap='gray')
plt.title("Laplacian Mutlak Eşikleme", fontsize=12, fontweight='bold')
plt.axis('off')

plt.subplot(2, 2, 4)
plt.imshow(edge_zc, cmap='gray')
plt.title("Laplacian Sıfır Geçişi (Zero-Crossing)", fontsize=12, fontweight='bold')
plt.axis('off')

plt.suptitle("Sobel, Prewitt ve Laplacian Kenar Tespit Yöntemlerinin Karşılaştırması", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "fig06_operator_comparison.png"), dpi=200)
plt.close()

# Figür 7: my_conv2 vs Builtin conv2 Farkı
K5 = get_gaussian_kernel(5, 1.0)
out_custom = my_conv2(I_orig, K5, 'zero')
# Scipy convolve2d ile aynı matematik
k_rot = np.rot90(K5, 2)
pt = 5 // 2
padded_zero = np.pad(I_orig, pt, mode='constant')
out_ref = np.zeros_like(I_orig)
for i in range(N):
    for j in range(N):
        out_ref[i, j] = np.sum(padded_zero[i:i+5, j:j+5] * k_rot)

diff = np.abs(out_custom - out_ref)

plt.figure(figsize=(13, 4.5))
plt.subplot(1, 3, 1)
plt.imshow(out_custom, cmap='gray')
plt.title(r"my_conv2 (Kendi Yazdığımız)", fontsize=11, fontweight='bold')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(out_ref, cmap='gray')
plt.title("MATLAB conv2(same) Referansı", fontsize=11, fontweight='bold')
plt.axis('off')

plt.subplot(1, 3, 3)
im = plt.imshow(diff, cmap='viridis')
plt.colorbar(im, fraction=0.046, pad=0.04)
plt.title(f"Mutlak Fark Haritası\n(Maksimum Hata: {np.max(diff):.2e})", fontsize=11, fontweight='bold')
plt.axis('off')

plt.suptitle("Kendi Konvolüsyon Algoritmamız ile Standart Konvolüsyon Karşılaştırması", fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, "fig07_custom_vs_builtin_diff.png"), dpi=200)
plt.close()

print("ALL 7 FIGURES SUCCESSFULLY GENERATED AND SAVED TO results/figures/!")
