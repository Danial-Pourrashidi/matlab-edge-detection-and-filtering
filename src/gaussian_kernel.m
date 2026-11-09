function K = gaussian_kernel(kernel_size, sigma)
% GAUSSIAN_KERNEL - 2 Boyutlu Normalize Edilmiş Gauss Yumuşatma Çekirdeği
%
% KULLANIM:
%   K = gaussian_kernel(kernel_size, sigma)
%
% GİRİŞ PARAMETRELERİ:
%   kernel_size : Çekirdek boyutu (tek tam sayı olmalıdır; örn: 3, 5, 7).
%                 Tek bir skaler verilirse (k x k) kare matris üretilir.
%   sigma       : Gauss dağılımının standart sapması (sigma > 0).
%
% ÇIKIŞ PARAMETRESİ:
%   K           : Elemanları toplamı 1 olan (normalize) 2B Gauss filtresi.
%
% MATEMATİKSEL ARKA PLAN:
%   Sürekli 2B Gauss fonksiyonu:
%     G(x, y) = (1 / (2 * pi * sigma^2)) * exp(-(x^2 + y^2) / (2 * sigma^2))
%   Ayrık ızgarada koordinat merkezi (0, 0) olacak şekilde simetrik olarak
%   örneklenir ve parlaklık koruması amacıyla toplamı 1'e normalize edilir:
%     K = G / sum(G(:))
%
% ÖRNEK:
%   K3 = gaussian_kernel(3, 0.5);
%   K5 = gaussian_kernel(5, 1.0);
%   K7 = gaussian_kernel(7, 2.0);
%
% Yazar: MATLAB Bilimsel Hesaplama ve Görüntü İşleme Projesi

    % 1. Giriş Parametrelerinin Doğrulanması
    narginchk(2, 2);

    if ~isscalar(kernel_size) || kernel_size <= 0 || mod(kernel_size, 2) == 0 || floor(kernel_size) ~= kernel_size
        error('gaussian_kernel:InvalidSize', ...
            'kernel_size pozitif bir tek tam sayı olmalıdır (örn: 3, 5, 7). Girilen değer: %s', mat2str(kernel_size));
    end

    if ~isscalar(sigma) || ~isnumeric(sigma) || sigma <= 0
        error('gaussian_kernel:InvalidSigma', ...
            'sigma değeri pozitif bir reel sayı olmalıdır (sigma > 0). Girilen değer: %s', mat2str(sigma));
    end

    % 2. Ayrık Koordinat Izgarasının Oluşturulması
    % Merkez piksel (0, 0) noktasında olacak şekilde yarıçap aralığı
    radius = floor(kernel_size / 2);
    [X, Y] = meshgrid(-radius : radius, -radius : radius);

    % 3. Gauss Dağılımının Hesaplanması
    % 2B Gauss formülü: exp(-(x^2 + y^2) / (2 * sigma^2))
    exponent = -(X.^2 + Y.^2) / (2 * sigma^2);
    K_raw = exp(exponent);

    % 4. Normalizasyon (Toplam = 1)
    % Filtre uygulandığında görüntünün ortalama parlaklığının korunması için
    kernel_sum = sum(K_raw, 'all');
    if kernel_sum == 0
        error('gaussian_kernel:ZeroSum', 'Gauss çekirdeğinin elemanları toplamı sıfır çıktı.');
    end

    K = K_raw / kernel_sum;

end

