%% GÖRÜNTÜ İŞLEME İLE KENAR TESPİT VE FİLTRELEME İNTERAKTİF DEMO (demo_live.m)
%
% Bu betik, projenin tüm aşamalarını bölüm bölüm (Run Section - Ctrl+Enter)
% incelemenize ve parametreleri anlık olarak test etmenize olanak tanır.
%
% Kapsam:
%   1. Görüntü Yükleme ve Normalizasyon
%   2. Gürültü Simülasyonu
%   3. Gauss Filtreleme & LoG (Marr-Hildreth) Çekirdeği
%   4. Sobel & Prewitt Gradyanları
%   5. Non-Maximum Suppression (Kenar İnceltme)
%   6. Laplacian ve Sıfır Geçişi (Zero-Crossing)
%   7. Sayısal Hata ve Performans Analizi (my_conv2 vs conv2)

clear; close all; clc;
addpath(fullfile(pwd, 'src'));

%% 1. GÖRÜNTÜ YÜKLEME VE ÖN İŞLEME
fprintf('=== [BÖLÜM 1] Görüntü Yükleniyor ===\n');

test_img_name = 'cameraman.tif';
if exist(test_img_name, 'file') || ~isempty(which(test_img_name))
    I_raw = imread(test_img_name);
    if size(I_raw, 3) == 3, I_raw = rgb2gray(I_raw); end
    I = im2double(I_raw);
else
    % Sentetik Geometrik Desen
    N = 256;
    [X, Y] = meshgrid(linspace(-1, 1, N), linspace(-1, 1, N));
    I = zeros(N, N);
    I(sqrt(X.^2 + Y.^2) < 0.5) = 0.85;
    I(X > 0.2 & X < 0.7 & Y > -0.6 & Y < -0.1) = 0.45;
    I(:, 20:60) = repmat(linspace(0.1, 0.9, 41), N, 1);
end

figure('Name', 'Bolum 1 - Orijinal Goruntu', 'Position', [150, 200, 500, 400]);
imshow(I); title('Orijinal Referans Görüntü (Double [0, 1])', 'FontSize', 12);
fprintf('Görüntü boyutu: %d x %d piksel\n\n', size(I, 1), size(I, 2));

%% 2. GÜRÜLTÜ ENJEKSİYONU
fprintf('=== [BÖLÜM 2] Yapay Gürültü Ekleniyor ===\n');

% Gauss gürültüsü (ortalama=0, varyans=0.008)
I_gauss = add_noise(I, 'gaussian', 0, 0.008);

% Tuz-Biber gürültüsü (yoğunluk=0.05)
I_sp = add_noise(I, 'salt_pepper', 0.05);

figure('Name', 'Bolum 2 - Gurultu Karsilastirmasi', 'Position', [150, 200, 900, 350]);
subplot(1, 2, 1); imshow(I_gauss); title('Gauss Gürültülü (\sigma^2 = 0.008)');
subplot(1, 2, 2); imshow(I_sp);    title('Tuz-Biber Gürültülü (Yoğunluk = 0.05)');
fprintf('Gürültüler eklendi.\n\n');

%% 3. 2D GAUSS VE LoG (LAPLACIAN OF GAUSSIAN) FİLTRELEME
fprintf('=== [BÖLÜM 3] Gauss ve LoG Filtreleri Hesaplanıyor ===\n');

% 5x5 Gauss filtresi (sigma = 1.0)
K_gauss = gaussian_kernel(5, 1.0);
I_smooth = my_conv2(I_gauss, K_gauss, 'replicate');

% 7x7 Analitik LoG (Mexican Hat) filtresi
K_log = log_kernel(7, 1.2);
I_log = my_conv2(I_gauss, K_log, 'replicate');

figure('Name', 'Bolum 3 - Filtreleme', 'Position', [150, 150, 1000, 400]);
subplot(1, 3, 1); imshow(I_gauss);  title('Giriş: Gürültülü Görüntü');
subplot(1, 3, 2); imshow(I_smooth); title('5x5 Gauss Yumuşatma (\sigma=1.0)');
subplot(1, 3, 3); imshow(I_log, []); colormap(gca, 'jet'); colorbar; title('7x7 LoG (Mexican Hat) Yanıtı');
fprintf('Gauss PSNR: %.2f dB\n\n', evaluate_metrics(I, I_smooth).PSNR);

%% 4. SOBEL VE PREWITT KENAR TESPİTİ
fprintf('=== [BÖLÜM 4] Sobel ve Prewitt Gradyanları ===\n');

[Gx_s, Gy_s, mag_s, dir_s, edge_s] = apply_sobel(I_smooth);
[Gx_p, Gy_p, mag_p, dir_p, edge_p] = apply_prewitt(I_smooth);

figure('Name', 'Bolum 4 - Sobel vs Prewitt', 'Position', [100, 100, 1000, 450]);
subplot(2, 2, 1); imshow(mag_s, []); title('Sobel Gradyan Büyüklüğü');
subplot(2, 2, 2); imshow(edge_s);    title('Sobel Eşiklenmiş Kenarlar');
subplot(2, 2, 3); imshow(mag_p, []); title('Prewitt Gradyan Büyüklüğü');
subplot(2, 2, 4); imshow(edge_p);    title('Prewitt Eşiklenmiş Kenarlar');
fprintf('1. Derece türev gradyanları hesaplandı.\n\n');

%% 5. NON-MAXIMUM SUPPRESSION (KENAR İNCELTME)
fprintf('=== [BÖLÜM 5] Non-Maximum Suppression (Canny Kenar İnceltme) ===\n');

% Sobel gradyan büyüklüğünü yön doğrultusunda incelt
nms_thin = non_maximum_suppression(mag_s, dir_s);
edge_thin = nms_thin >= (mean(mag_s, 'all') + 1.0 * std(mag_s, 0, 'all'));

figure('Name', 'Bolum 5 - Kenar Inceltme', 'Position', [150, 150, 900, 400]);
subplot(1, 2, 1); imshow(edge_s);    title('Standart Sobel (Geniş Kenarlar)');
subplot(1, 2, 2); imshow(edge_thin); title('NMS ile İnceltilmiş (Tek Piksel Kenarlar)');
fprintf('Kenar inceltme tamamlandı.\n\n');

%% 6. LAPLACIAN VE SIFIR GEÇİŞİ (ZERO-CROSSING)
fprintf('=== [BÖLÜM 6] Laplacian ve Sıfır Geçişi ===\n');

[lap_raw, edge_lap_abs, edge_lap_zc] = apply_laplacian(I_smooth, '4');

figure('Name', 'Bolum 6 - Laplacian', 'Position', [150, 150, 1000, 380]);
subplot(1, 3, 1); imshow(lap_raw, []); colormap(gca, 'gray'); colorbar; title('Ham Laplacian Yanıtı (\nabla^2 I)');
subplot(1, 3, 2); imshow(edge_lap_abs); title('Mutlak Eşikleme (|Lap| \ge T)');
subplot(1, 3, 3); imshow(edge_lap_zc);  title('Sıfır Geçişi (Zero-Crossing)');
fprintf('İkinci derece türev sıfır geçişleri tespit edildi.\n\n');

%% 7. SAYISAL HATA VE SÜRE KIYASI (my_conv2 vs conv2)
fprintf('=== [BÖLÜM 7] Sayısal Doğruluk ve Süre Testi ===\n');

K_test = gaussian_kernel(5, 1.0);

tic;
out_custom = my_conv2(I, K_test, 'zero');
t_custom = toc;

tic;
out_builtin = conv2(I, K_test, 'same');
t_builtin = toc;

m = evaluate_metrics(out_builtin, out_custom, t_custom);

fprintf('Maksimum Mutlak Hata : %.2e\n', m.MaxAbsError);
fprintf('Ortalama Mutlak Hata : %.2e\n', m.MAE);
fprintf('MSE                  : %.2e\n', m.MSE);
fprintf('PSNR                 : %.2f dB\n', m.PSNR);
fprintf('my_conv2 Süresi      : %.4f s\n', t_custom);
fprintf('conv2 Süresi         : %.4f s\n', t_builtin);
fprintf('=========================================================\n');
fprintf('Demo başarıyla tamamlandı!\n');
