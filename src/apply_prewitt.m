function [Gx, Gy, magnitude, direction, edge_map] = apply_prewitt(I, threshold, conv_func)
% APPLY_PREWITT - Prewitt Gradyan Operatörü ile Kenar Tespiti
%
% KULLANIM:
%   [Gx, Gy, magnitude, direction, edge_map] = apply_prewitt(I)
%   [Gx, Gy, magnitude, direction, edge_map] = apply_prewitt(I, threshold)
%   [Gx, Gy, magnitude, direction, edge_map] = apply_prewitt(I, threshold, conv_func)
%
% GİRİŞ PARAMETRELERİ:
%   I          : 2B Gri seviyeli giriş görüntüsü (double tipinde, [0, 1]).
%   threshold  : Kenar ikilileştirme eşiği (isteğe bağlı).
%                Belirtilmezse adaptif eşik (ortalama + 1.2 * standart sapma) kullanılır.
%   conv_func  : 2B Konvolüsyon fonksiyon tutamacı (function handle).
%                Varsayılan: @(img, k) my_conv2(img, k, 'replicate')
%
% ÇIKIŞ PARAMETRELERİ:
%   Gx         : Yatay gradyan bileşeni (dikey kenarlar).
%   Gy         : Dikey gradyan bileşeni (yatay kenarlar).
%   magnitude  : Gradyan büyüklüğü (sqrt(Gx.^2 + Gy.^2)).
%   direction  : Gradyan yön açısı radyan cinsinden [-pi, pi] (atan2(Gy, Gx)).
%   edge_map   : Eşiklenmiş ikili (mantıksal / logical) kenar haritası.
%
% ÇEKİRDEKLER (PREWITT OPERATÖRÜ):
%   Gx = [-1  0  1; -1  0  1; -1  0  1]
%   Gy = [-1 -1 -1;  0  0  0;  1  1  1]
%
% Yazar: MATLAB Bilimsel Hesaplama ve Görüntü İşleme Projesi

    % 1. Giriş Kontrolleri ve Varsayılan Değerler
    narginchk(1, 3);

    if ~ismatrix(I) || ~isnumeric(I)
        error('apply_prewitt:InvalidImage', 'Giriş görüntüsü 2 boyutlu sayısal bir matris olmalıdır.');
    end

    if ~isa(I, 'double')
        I = double(I);
        if max(I, [], 'all') > 1.0
            I = I / 255.0;
        end
    end

    if nargin < 3 || isempty(conv_func)
        % Varsayılan olarak kendi yazdığımız my_conv2 fonksiyonu 'replicate' dolgusuyla kullanılır
        conv_func = @(img, k) my_conv2(img, k, 'replicate');
    end

    % 2. Prewitt Çekirdeklerinin Tanımlanması
    Kx = [-1  0  1;
          -1  0  1;
          -1  0  1];

    Ky = [-1 -1 -1;
           0  0  0;
           1  1  1];

    % 3. Konvolüsyon ile Eksenel Gradyanların Hesaplanması
    Gx = conv_func(I, Kx);
    Gy = conv_func(I, Ky);

    % 4. Gradyan Büyüklüğü ve Yönünün Hesaplanması
    magnitude = sqrt(Gx.^2 + Gy.^2);
    direction = atan2(Gy, Gx);

    % 5. Eşikleme ile İkili Kenar Haritası Üretimi
    if nargin < 2 || isempty(threshold)
        % Otomatik istatistiksel eşik belirleme
        mag_mean = mean(magnitude, 'all');
        mag_std = std(magnitude, 0, 'all');
        threshold = mag_mean + 1.2 * mag_std;
    end

    edge_map = magnitude >= threshold;

end

