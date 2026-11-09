function output = my_conv2(image, kernel, pad_type)
% MY_CONV2 - 2 Boyutlu Uzamsal Konvolüsyon İşlemi (Hazır Fonksiyonsuz)
%
% KULLANIM:
%   output = my_conv2(image, kernel)
%   output = my_conv2(image, kernel, pad_type)
%
% GİRİŞ PARAMETRELERİ:
%   image    : 2B Gri seviyeli giriş görüntüsü (double tipinde olmalıdır).
%   kernel   : 2B Konvolüsyon çekirdeği (filtresi).
%   pad_type : Sınır dolgu yöntemi:
%              'zero'      - Sıfır dolgu (Zero-padding) [Varsayılan]
%              'replicate' - Kenar piksellerinin kopyalanması (Replicate)
%              'symmetric' - Kenar piksellerinin ayna yansıması (Symmetric)
%
% ÇIKIŞ PARAMETRESİ:
%   output   : Konvolüsyon sonucu elde edilen 2B matris (girişle aynı boyutta).
%
% MATEMATİKSEL ARKA PLAN:
%   2D Konvolüsyon, uzamsal alanda çekirdeğin 180 derece döndürülmesi
%   (rot90(kernel, 2)) ve pikseller ile çekirdek katsayılarının kaydırılarak
%   çarpılıp toplanması (inner-product) işlemidir:
%     (I * K)(x, y) = \sum_{u} \sum_{v} I(x - u, y - v) * K(u, v)
%
% ÖRNEK:
%   I = im2double(imread('cameraman.tif'));
%   K = [1 2 1; 0 0 0; -1 -2 -1];
%   out = my_conv2(I, K, 'replicate');
%
% Yazar: MATLAB Bilimsel Hesaplama ve Görüntü İşleme Projesi

    % 1. Giriş Parametrelerinin Doğrulanması
    narginchk(2, 3);

    if nargin < 3 || isempty(pad_type)
        pad_type = 'zero';
    end

    if ~ismatrix(image) || ~isnumeric(image)
        error('my_conv2:InvalidImage', 'Giriş görüntüsü 2 boyutlu sayısal bir matris olmalıdır.');
    end

    if ~ismatrix(kernel) || ~isnumeric(kernel)
        error('my_conv2:InvalidKernel', 'Çekirdek matrisi 2 boyutlu sayısal bir matris olmalıdır.');
    end

    % Görüntünün double türünde olduğundan emin olun
    if ~isa(image, 'double')
        image = double(image);
    end
    if ~isa(kernel, 'double')
        kernel = double(kernel);
    end

    % 2. Boyutların Belirlenmesi
    [img_h, img_w] = size(image);
    [k_h, k_w] = size(kernel);

    if k_h > img_h || k_w > img_w
        error('my_conv2:KernelTooLarge', 'Çekirdek boyutları görüntü boyutlarından büyük olamaz.');
    end

    % Simetrik veya asimetrik çekirdekler için dolgu miktarlarının hesaplanması
    pad_top = floor(k_h / 2);
    pad_bot = k_h - 1 - pad_top;
    pad_left = floor(k_w / 2);
    pad_right = k_w - 1 - pad_left;

    % 3. Kenar Dolgusu (Padding) - Harici Toolbox Gerektirmeyen Bağımsız İndeksleme
    pad_type_lower = lower(char(pad_type));

    switch pad_type_lower
        case 'zero'
            % Sıfır ile genişletilmiş matris oluşturulması
            padded = zeros(img_h + pad_top + pad_bot, img_w + pad_left + pad_right, 'double');
            padded(pad_top + 1 : pad_top + img_h, pad_left + 1 : pad_left + img_w) = image;

        case 'replicate'
            % Kenar piksellerini dışa doğru tekrar etme
            r_idx = [ones(1, pad_top), 1:img_h, img_h * ones(1, pad_bot)];
            c_idx = [ones(1, pad_left), 1:img_w, img_w * ones(1, pad_right)];
            padded = image(r_idx, c_idx);

        case 'symmetric'
            % Kenar sınırından yansıma (reflection) oluşturma
            r_idx = [pad_top:-1:1, 1:img_h, img_h:-1:(img_h - pad_bot + 1)];
            c_idx = [pad_left:-1:1, 1:img_w, img_w:-1:(img_w - pad_right + 1)];
            padded = image(r_idx, c_idx);

        otherwise
            error('my_conv2:UnknownPadding', ...
                'Desteklenmeyen dolgu türü: "%s". Geçerli seçenekler: "zero", "replicate", "symmetric".', pad_type);
    end

    % 4. Konvolüsyon için Çekirdeği 180 Derece Döndürme
    % Matematiksel tanım gereği konvolüsyon: çekirdeğin ters çevrilmiş halidir (korelasyondan farkı).
    kernel_rot = rot90(kernel, 2);

    % 5. For Döngüleriyle 2D Konvolüsyon Hesaplanması
    output = zeros(img_h, img_w, 'double');

    for i = 1:img_h
        for j = 1:img_w
            % Dolgulu matristen çekirdek boyutundaki lokal bölgeyi al
            local_region = padded(i : i + k_h - 1, j : j + k_w - 1);
            
            % Eleman bazlı çarpım ve toplam (noktasal iç çarpım)
            output(i, j) = sum(local_region .* kernel_rot, 'all');
        end
    end

end

