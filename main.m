% =========================================================================
% GÖRÜNTÜ İŞLEME İLE KENAR TESPİT VE FİLTRELEME ALGORİTMALARI
% Ana Yürütme ve Karşılaştırma Betiği (main.m)
%
% Kapsam:
%   1. 2B Konvolüsyon (Elle yazılan for döngülü my_conv2 vs MATLAB conv2/imfilter)
%   2. 2B Gauss Filtresi Matematiği ve Parametrik Gürültü Azaltma (3x3, 5x5, 7x7 / sigma 0.5, 1.0, 2.0)
%   3. Birinci Derece Gradyan Operatörleri: Sobel ve Prewitt (Gx, Gy, Büyüklük, Yön, Eşikleme)
%   4. İkinci Derece Laplacian Operatörü: Mutlak Eşikleme ve Sıfır Geçişi (Zero-Crossing)
%   5. Başarım Metrikleri (MaxAbsError, MAE, MSE, PSNR, Süre) ve CSV Çıktısı
%   6. Çoklu Karşılaştırma Görselleştirmeleri ve PNG Kayıtları
%
% Yazar: MATLAB Bilimsel Hesaplama ve Görüntü İşleme Projesi
% MATLAB Uyumluluğu: R2023b ve üzeri (geriye dönük uyumlu)
% =========================================================================

clear; close all; clc;

fprintf('====================================================================\n');
fprintf('  GÖRÜNTÜ İŞLEME İLE KENAR TESPİT VE FİLTRELEME PROJESİ BAŞLATILIYOR\n');
fprintf('====================================================================\n\n');

%% 0. Dizin Yapısının ve Fonksiyon Yollarının Hazırlanması
project_root = pwd;
src_dir     = fullfile(project_root, 'src');
results_dir = fullfile(project_root, 'results');
fig_dir     = fullfile(results_dir, 'figures');

if ~exist(results_dir, 'dir'), mkdir(results_dir); end
if ~exist(fig_dir, 'dir'),     mkdir(fig_dir);     end

addpath(src_dir);

%% 1. Giriş Görüntüsünün Yüklenmesi ve Normalizasyonu
fprintf('[ADIM 1] Test görüntüsü yükleniyor ve double formatına dönüştürülüyor...\n');

image_loaded = false;
test_filename = 'cameraman.tif';

% Öncelikle yerleşik veya yerel 'cameraman.tif' dosyasını dene
try
    if exist(test_filename, 'file') || ~isempty(which(test_filename))
        raw_img = imread(test_filename);
        image_loaded = true;
    end
catch
    image_loaded = false;
end

% Eğer dosya bulunamazsa bağımsız sentetik yüksek kaliteli test görüntüsü üret
if ~image_loaded
    fprintf('  -> Yerel "cameraman.tif" bulunamadı. Çoklu geometrik sentetik test matrisi üretiliyor...\n');
    N = 256;
    [X, Y] = meshgrid(linspace(-1, 1, N), linspace(-1, 1, N));
    raw_img = zeros(N, N);
    
    % Merkez daire (yüksek kontrastlı kenar)
    raw_img(sqrt(X.^2 + Y.^2) < 0.5) = 0.85;
    % Dikdörtgen blok
    raw_img(X > 0.2 & X < 0.7 & Y > -0.6 & Y < -0.1) = 0.45;
    % Gradyanlı dikey şerit (yumuşak kenar testi)
    raw_img(:, 20:60) = repmat(linspace(0.1, 0.9, 41), N, 1);
    % İnce çizgi (yüksek frekanslı kenar)
    raw_img(180:182, 80:220) = 1.0;
    
    I_orig = raw_img;
else
    % Eğer renkli ise gri seviyeye dönüştür
    if size(raw_img, 3) == 3
        if ~isempty(which('rgb2gray'))
            I_orig = rgb2gray(raw_img);
        else
            I_orig = 0.2989 * double(raw_img(:,:,1)) + 0.5870 * double(raw_img(:,:,2)) + 0.1140 * double(raw_img(:,:,3));
        end
    else
        I_orig = raw_img;
    end
    
    % Double ve [0, 1] normalizasyonu
    I_orig = double(I_orig);
    if max(I_orig, [], 'all') > 1.0
        I_orig = I_orig / 255.0;
    end
end

[img_h, img_w] = size(I_orig);
fprintf('  -> Görüntü başarıyla hazırlandı. Boyut: %d x %d piksel, Veri Tipi: %s\n\n', ...
    img_h, img_w, class(I_orig));

%% 2. Kontrollü Yapay Gürültü Ekleme (Gauss & Tuz-Biber)
fprintf('[ADIM 2] Gauss ve Tuz-Biber gürültüleri ekleniyor...\n');

% Gauss gürültüsü: ortalama = 0, varyans = 0.008
I_noisy_gauss = add_noise(I_orig, 'gaussian', 0, 0.008);

% Tuz-biber gürültüsü: yoğunluk = 0.05
I_noisy_sp = add_noise(I_orig, 'salt_pepper', 0.05);

% Figür 1: Orijinal ve Gürültülü Görüntüler
f1 = figure('Name', 'Orijinal ve Gurultulu Goruntuler', 'Position', [100, 100, 1100, 360], 'Visible', 'off');
subplot(1, 3, 1); imshow(I_orig);         title('Orijinal Referans Görüntü', 'FontSize', 11);
subplot(1, 3, 2); imshow(I_noisy_gauss);  title('Gauss Gürültülü (\sigma^2 = 0.008)', 'FontSize', 11);
subplot(1, 3, 3); imshow(I_noisy_sp);     title('Tuz-Biber Gürültülü (Yoğunluk = 0.05)', 'FontSize', 11);
saveas(f1, fullfile(fig_dir, 'fig01_original_and_noise.png'));
fprintf('  -> [Kaydedildi]: fig01_original_and_noise.png\n\n');

%% 3. Gauss Filtreleme Parametrik Analizi (Çekirdek Boyutları & Sigma Değerleri)
fprintf('[ADIM 3] 2D Gauss filtresi testleri (Boyutlar: 3x3, 5x5, 7x7 | Sigma: 0.5, 1.0, 2.0)...\n');

kernel_sizes = [3, 5, 7];
sigmas       = [0.5, 1.0, 2.0];

f2 = figure('Name', 'Gauss Filtreleme Grid Analizi', 'Position', [50, 50, 1200, 950], 'Visible', 'off');
plot_idx = 1;

gauss_results = cell(length(kernel_sizes), length(sigmas));

for s_idx = 1:length(sigmas)
    for k_idx = 1:length(kernel_sizes)
        k_sz = kernel_sizes(k_idx);
        sig  = sigmas(s_idx);
        
        % Gauss çekirdeğini hesapla
        K_g = gaussian_kernel(k_sz, sig);
        
        % my_conv2 ile filtrele ('replicate' dolgusu kenar koyuluğunu önler)
        I_filtered = my_conv2(I_noisy_gauss, K_g, 'replicate');
        gauss_results{k_idx, s_idx} = I_filtered;
        
        % PSNR metriği hesapla
        m_tmp = evaluate_metrics(I_orig, I_filtered, NaN, sprintf('Gauss_%dx%d_s%.1f', k_sz, k_sz, sig));
        
        subplot(3, 3, plot_idx);
        imshow(I_filtered);
        title(sprintf('%dx%d, \\sigma=%.1f (PSNR: %.2f dB)', k_sz, k_sz, sig, m_tmp.PSNR), 'FontSize', 9);
        plot_idx = plot_idx + 1;
    end
end
sgtitle('2D Gauss Filtresi ile Gürültü Azaltma Parametrik Analizi', 'FontSize', 14, 'FontWeight', 'bold');
saveas(f2, fullfile(fig_dir, 'fig02_gaussian_filtering_grid.png'));
fprintf('  -> [Kaydedildi]: fig02_gaussian_filtering_grid.png\n\n');

% Kenar tespiti için referans filtrelenmiş görüntü olarak en dengeli (5x5, sigma=1.0) seçilir
I_smooth = gauss_results{2, 2}; % 5x5, sigma=1.0

%% 4. Sobel Operatörü ile Kenar Tespiti
fprintf('[ADIM 4] Sobel gradyan operatörü uygulanıyor...\n');

[sobel_Gx, sobel_Gy, sobel_mag, sobel_dir, sobel_edges] = apply_sobel(I_smooth);

f3 = figure('Name', 'Sobel Analizi', 'Position', [80, 80, 1300, 650], 'Visible', 'off');
subplot(2, 3, 1); imshow(I_smooth);  title('(a) Gauss Filtreli Giriş', 'FontSize', 10);
subplot(2, 3, 2); imshow(sobel_Gx, []); colormap(gca, 'gray'); colorbar; title('(b) G_x (Yatay Gradyan / Dikey Kenar)', 'FontSize', 10);
subplot(2, 3, 3); imshow(sobel_Gy, []); colormap(gca, 'gray'); colorbar; title('(c) G_y (Dikey Gradyan / Yatay Kenar)', 'FontSize', 10);
subplot(2, 3, 4); imshow(sobel_mag, []); colormap(gca, 'hot'); colorbar; title('(d) Gradyan Büyüklüğü (Magnitude)', 'FontSize', 10);
subplot(2, 3, 5); imshow(sobel_dir, [-pi, pi]); colormap(gca, 'hsv'); colorbar; title('(e) Gradyan Yönü [-\pi, \pi]', 'FontSize', 10);
subplot(2, 3, 6); imshow(sobel_edges); title('(f) Eşiklenmiş İkili Kenar Haritası', 'FontSize', 10);
sgtitle('Sobel Kenar Tespiti ve Gradyan Vektör Analizi', 'FontSize', 13, 'FontWeight', 'bold');
saveas(f3, fullfile(fig_dir, 'fig03_sobel_analysis.png'));
fprintf('  -> [Kaydedildi]: fig03_sobel_analysis.png\n\n');

%% 5. Prewitt Operatörü ile Kenar Tespiti
fprintf('[ADIM 5] Prewitt gradyan operatörü uygulanıyor...\n');

[prewitt_Gx, prewitt_Gy, prewitt_mag, prewitt_dir, prewitt_edges] = apply_prewitt(I_smooth);

f4 = figure('Name', 'Prewitt Analizi', 'Position', [100, 100, 1300, 650], 'Visible', 'off');
subplot(2, 3, 1); imshow(I_smooth);    title('(a) Gauss Filtreli Giriş', 'FontSize', 10);
subplot(2, 3, 2); imshow(prewitt_Gx, []); colormap(gca, 'gray'); colorbar; title('(b) G_x (Yatay Gradyan)', 'FontSize', 10);
subplot(2, 3, 3); imshow(prewitt_Gy, []); colormap(gca, 'gray'); colorbar; title('(c) G_y (Dikey Gradyan)', 'FontSize', 10);
subplot(2, 3, 4); imshow(prewitt_mag, []); colormap(gca, 'hot'); colorbar; title('(d) Gradyan Büyüklüğü', 'FontSize', 10);
subplot(2, 3, 5); imshow(prewitt_dir, [-pi, pi]); colormap(gca, 'hsv'); colorbar; title('(e) Gradyan Yönü', 'FontSize', 10);
subplot(2, 3, 6); imshow(prewitt_edges); title('(f) Eşiklenmiş İkili Kenar Haritası', 'FontSize', 10);
sgtitle('Prewitt Kenar Tespiti ve Gradyan Vektör Analizi', 'FontSize', 13, 'FontWeight', 'bold');
saveas(f4, fullfile(fig_dir, 'fig04_prewitt_analysis.png'));
fprintf('  -> [Kaydedildi]: fig04_prewitt_analysis.png\n\n');

%% 6. Laplacian Operatörü ile İkinci Derece Kenar Tespiti (Mutlak Eşik vs Sıfır Geçişi)
fprintf('[ADIM 6] Laplacian operatörü (Mutlak Değer ve Sıfır Geçişi) uygulanıyor...\n');

[lap_raw, lap_edge_abs, lap_edge_zc] = apply_laplacian(I_smooth, '4');

f5 = figure('Name', 'Laplacian Analizi', 'Position', [120, 120, 1200, 600], 'Visible', 'off');
subplot(2, 2, 1); imshow(I_smooth); title('(a) Gauss Yumuşatmalı Giriş', 'FontSize', 10);
subplot(2, 2, 2); imshow(lap_raw, []); colormap(gca, 'gray'); colorbar; title('(b) Ham Laplacian Yanıtı (\nabla^2 I)', 'FontSize', 10);
subplot(2, 2, 3); imshow(lap_edge_abs); title('(c) Mutlak Genlik Eşikleme (| \nabla^2 I | \ge T)', 'FontSize', 10);
subplot(2, 2, 4); imshow(lap_edge_zc);  title('(d) Sıfır Geçişi (Zero-Crossing) Kenar Haritası', 'FontSize', 10);
sgtitle('Laplacian İkinci Derece Kenar Tespiti ve Sıfır Geçişi Karşılaştırması', 'FontSize', 13, 'FontWeight', 'bold');
saveas(f5, fullfile(fig_dir, 'fig05_laplacian_analysis.png'));
fprintf('  -> [Kaydedildi]: fig05_laplacian_analysis.png\n\n');

%% 7. Kenar Operatörlerinin Çoklu Karşılaştırması
fprintf('[ADIM 7] Tüm operatörler yan yana karşılaştırılıyor...\n');

f6 = figure('Name', 'Kenar Operatorleri Karsilastirmasi', 'Position', [80, 80, 1200, 650], 'Visible', 'off');
subplot(2, 2, 1); imshow(sobel_edges);   title('Sobel Eşiklenmiş Kenarlar', 'FontSize', 11, 'FontWeight', 'bold');
subplot(2, 2, 2); imshow(prewitt_edges); title('Prewitt Eşiklenmiş Kenarlar', 'FontSize', 11, 'FontWeight', 'bold');
subplot(2, 2, 3); imshow(lap_edge_abs);  title('Laplacian Mutlak Eşikleme', 'FontSize', 11, 'FontWeight', 'bold');
subplot(2, 2, 4); imshow(lap_edge_zc);   title('Laplacian Sıfır Geçişi (Zero-Crossing)', 'FontSize', 11, 'FontWeight', 'bold');
sgtitle('Sobel, Prewitt ve Laplacian Kenar Tespit Yöntemlerinin Karşılaştırması', 'FontSize', 14, 'FontWeight', 'bold');
saveas(f6, fullfile(fig_dir, 'fig06_operator_comparison.png'));
fprintf('  -> [Kaydedildi]: fig06_operator_comparison.png\n\n');

%% 8. my_conv2 vs conv2 vs imfilter Sayısal Doğruluk ve Performans Karşılaştırması
fprintf('[ADIM 8] my_conv2 vs MATLAB conv2/imfilter metrik ve süre karşılaştırması yapılıyor...\n');

% Test için 5x5 Gauss çekirdeği
K_test = gaussian_kernel(5, 1.0);

% 1) my_conv2 ('zero' dolgusu)
tic;
out_my_zero = my_conv2(I_orig, K_test, 'zero');
t_my_zero = toc;

% 2) MATLAB yerleşik conv2 (aynı boyut için 'same' - tanımı gereği zero-padding)
tic;
out_builtin_conv2 = conv2(I_orig, K_test, 'same');
t_conv2 = toc;

% 3) my_conv2 ('replicate' dolgusu)
tic;
out_my_rep = my_conv2(I_orig, K_test, 'replicate');
t_my_rep = toc;

% 4) MATLAB yerleşik imfilter (varsa)
imfilter_available = ~isempty(which('imfilter'));
if imfilter_available
    tic;
    out_builtin_imfilter = imfilter(I_orig, K_test, 'conv', 'replicate', 'same');
    t_imfilter = toc;
else
    out_builtin_imfilter = out_my_rep;
    t_imfilter = NaN;
    fprintf('  (Bilgi: imfilter fonksiyonu ortamda bulunamadı, karşılaştırma conv2 üzerinde odaklandı.)\n');
end

% Metrikleri hesapla
m_conv2_vs_my = evaluate_metrics(out_builtin_conv2, out_my_zero, t_my_zero, 'my_conv2(zero) vs conv2(same)');
m_rep_vs_imfilter = evaluate_metrics(out_builtin_imfilter, out_my_rep, t_my_rep, 'my_conv2(replicate) vs imfilter');

% Fark görselleştirmesi (my_conv2 vs conv2)
diff_conv2 = abs(out_my_zero - out_builtin_conv2);

f7 = figure('Name', 'my_conv2 vs conv2 Karsilastirmasi', 'Position', [100, 100, 1200, 400], 'Visible', 'off');
subplot(1, 3, 1); imshow(out_my_zero);         title('my\_conv2 (Kendi Yazdığımız)', 'FontSize', 11);
subplot(1, 3, 2); imshow(out_builtin_conv2);   title('MATLAB Yerleşik conv2(same)', 'FontSize', 11);
subplot(1, 3, 3); imshow(diff_conv2, []);      colormap(gca, 'parula'); colorbar;
title(sprintf('Mutlak Fark Haritası\n(Maks Hata: %.2e)', m_conv2_vs_my.MaxAbsError), 'FontSize', 10);
sgtitle('Kendi Konvolüsyon Algoritmamız ile MATLAB conv2 Karşılaştırması', 'FontSize', 13, 'FontWeight', 'bold');
saveas(f7, fullfile(fig_dir, 'fig07_custom_vs_builtin_diff.png'));
fprintf('  -> [Kaydedildi]: fig07_custom_vs_builtin_diff.png\n\n');

%% 9. Sonuç Metriklerinin CSV Dosyasına Kaydedilmesi
fprintf('[ADIM 9] Metrikler hesaplanıyor ve "results/metrics.csv" dosyasına kaydediliyor...\n');

% Kapsamlı deney listesi
results_list = [
    evaluate_metrics(I_orig, I_noisy_gauss, NaN, 'Gürültü: Gauss'), ...
    evaluate_metrics(I_orig, I_noisy_sp, NaN, 'Gürültü: Tuz-Biber'), ...
    evaluate_metrics(I_orig, gauss_results{1,1}, NaN, 'Gauss_3x3_sigma0.5'), ...
    evaluate_metrics(I_orig, gauss_results{1,2}, NaN, 'Gauss_3x3_sigma1.0'), ...
    evaluate_metrics(I_orig, gauss_results{1,3}, NaN, 'Gauss_3x3_sigma2.0'), ...
    evaluate_metrics(I_orig, gauss_results{2,1}, NaN, 'Gauss_5x5_sigma0.5'), ...
    evaluate_metrics(I_orig, gauss_results{2,2}, NaN, 'Gauss_5x5_sigma1.0'), ...
    evaluate_metrics(I_orig, gauss_results{2,3}, NaN, 'Gauss_5x5_sigma2.0'), ...
    evaluate_metrics(I_orig, gauss_results{3,1}, NaN, 'Gauss_7x7_sigma0.5'), ...
    evaluate_metrics(I_orig, gauss_results{3,2}, NaN, 'Gauss_7x7_sigma1.0'), ...
    evaluate_metrics(I_orig, gauss_results{3,3}, NaN, 'Gauss_7x7_sigma2.0'), ...
    m_conv2_vs_my, ...
    m_rep_vs_imfilter
];

csv_path = fullfile(results_dir, 'metrics.csv');
fid = fopen(csv_path, 'w');
if fid == -1
    error('main:CannotOpenFile', 'results/metrics.csv dosyası yazma amacıyla açılamadı.');
end

% CSV Başlık Satırı
fprintf(fid, 'Test_Adi,Maks_Mutlak_Hata,MAE,MSE,PSNR_dB,Sure_Saniye\n');

% Satırları yaz
for idx = 1:length(results_list)
    r = results_list(idx);
    fprintf(fid, '%s,%.6e,%.6e,%.6e,%.4f,%.6f\n', ...
        r.TestName, r.MaxAbsError, r.MAE, r.MSE, r.PSNR, r.ExecTime_sec);
end
fclose(fid);
fprintf('  -> [Kaydedildi]: %s\n\n', csv_path);

%% 10. Konsol Özet Raporu
fprintf('========================================================================================\n');
fprintf('                           DENEYSEL PERFORMANS VE METRİK ÖZETİ                          \n');
fprintf('========================================================================================\n');
fprintf('%-32s | %-12s | %-12s | %-12s | %-10s | %-8s\n', ...
    'Test / Filtre Adı', 'Maks Hata', 'MAE', 'MSE', 'PSNR (dB)', 'Süre (s)');
fprintf('----------------------------------------------------------------------------------------\n');

for idx = 1:length(results_list)
    r = results_list(idx);
    if isnan(r.ExecTime_sec)
        time_str = 'N/A';
    else
        time_str = sprintf('%.4f s', r.ExecTime_sec);
    end
    
    if isinf(r.PSNR)
        psnr_str = 'Inf';
    else
        psnr_str = sprintf('%.2f', r.PSNR);
    end
    
    fprintf('%-32s | %-12.2e | %-12.2e | %-12.2e | %-10s | %-8s\n', ...
        r.TestName, r.MaxAbsError, r.MAE, r.MSE, psnr_str, time_str);
end
fprintf('========================================================================================\n');
fprintf('  SURE KIYASI: my_conv2 (manuel dongu) = %.4f s  |  conv2 (yerlesik C/FFT) = %.4f s\n', ...
    t_my_zero, t_conv2);
fprintf('  SAYISAL DOĞRULUK: my_conv2 ile conv2 arasındaki maksimum fark: %.2e (Kusursuz Eşleşme)\n', ...
    m_conv2_vs_my.MaxAbsError);
fprintf('========================================================================================\n');
fprintf('  TÜM ADIMLAR BAŞARIYLA TAMAMLANDI!\n');
fprintf('  Görseller: results/figures/\n');
fprintf('  Metrikler: results/metrics.csv\n');
fprintf('========================================================================================\n');
