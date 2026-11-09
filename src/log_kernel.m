function K_log = log_kernel(kernel_size, sigma)
% LOG_KERNEL - Analitik 2 Boyutlu Laplacian of Gaussian (LoG) Çekirdeği
%
% KULLANIM:
%   K_log = log_kernel(kernel_size, sigma)
%
% GİRİŞ PARAMETRELERİ:
%   kernel_size : Çekirdek boyutu (tek tam sayı olmalıdır; örn: 5, 7, 9).
%   sigma       : Gauss filtresinin standart sapması (sigma > 0).
%
% ÇIKIŞ PARAMETRESİ:
%   K_log       : Sıfır toplamlı (zero-sum) normalize edilmiş 2B LoG filtresi.
%
% MATEMATİKSEL ARKA PLAN (Marr-Hildreth Teoremi):
%   Laplacian ve Gauss operatörlerinin birleşimi olan LoG (Mexican Hat):
%     nabla^2 G(x, y) = -1 / (pi * sigma^4) * (1 - (x^2 + y^2)/(2*sigma^2)) * exp(-(x^2 + y^2)/(2*sigma^2))
%   Düzgün bölgelerde sıfır yanıtı vermesi için çekirdek katsayılarının
%   toplamı tam olarak 0 olmalıdır (DC bileşeni sıfırlama).
%
% Yazar: MATLAB Bilimsel Hesaplama ve Görüntü İşleme Projesi

    narginchk(2, 2);

    if ~isscalar(kernel_size) || kernel_size <= 0 || mod(kernel_size, 2) == 0 || floor(kernel_size) ~= kernel_size
        error('log_kernel:InvalidSize', 'kernel_size pozitif bir tek tam sayı olmalıdır (örn: 5, 7, 9).');
    end

    if ~isscalar(sigma) || ~isnumeric(sigma) || sigma <= 0
        error('log_kernel:InvalidSigma', 'sigma değeri pozitif bir reel sayı olmalıdır (sigma > 0).');
    end

    radius = floor(kernel_size / 2);
    [X, Y] = meshgrid(-radius : radius, -radius : radius);

    r2 = X.^2 + Y.^2;
    sigma2 = sigma^2;
    sigma4 = sigma^4;

    % Analitik LoG Denklemi
    K_raw = -(1 / (pi * sigma4)) .* (1 - (r2 / (2 * sigma2))) .* exp(-r2 / (2 * sigma2));

    % DC Sıfırlama: Düz/homojen alanlarda sıfır yanıt vermesi için ortalama çıkarılır
    K_log = K_raw - mean(K_raw, 'all');

end
