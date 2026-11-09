function [lap_raw, edge_abs, edge_zc] = apply_laplacian(I, kernel_type, abs_thresh, zc_thresh, conv_func)
% APPLY_LAPLACIAN - 2. Derece Türev Laplacian Operatörü ve Kenar Tespiti
%
% KULLANIM:
%   [lap_raw, edge_abs, edge_zc] = apply_laplacian(I)
%   [lap_raw, edge_abs, edge_zc] = apply_laplacian(I, kernel_type)
%   [lap_raw, edge_abs, edge_zc] = apply_laplacian(I, kernel_type, abs_thresh, zc_thresh)
%   [lap_raw, edge_abs, edge_zc] = apply_laplacian(I, kernel_type, abs_thresh, zc_thresh, conv_func)
%
% GİRİŞ PARAMETRELERİ:
%   I           : 2B Gri seviyeli giriş görüntüsü (double, [0, 1]).
%   kernel_type : Çekirdek türü:
%                 '4' veya 'standard4' - 4-komşuluk çekirdeği [Varsayılan]
%                 '8' veya 'standard8' - 8-komşuluk çekirdeği
%   abs_thresh  : Mutlak genlik eşiği (boş ise adaptif belirlenir).
%   zc_thresh   : Sıfır geçişi (zero-crossing) eğim fark eşiği (boş ise adaptif).
%   conv_func   : Konvolüsyon fonksiyonu tutamacı (varsayılan: @my_conv2).
%
% ÇIKIŞ PARAMETRELERİ:
%   lap_raw     : Ham Laplacian konvolüsyon çıktısı (negatif ve pozitif değerler içerir).
%   edge_abs    : Mutlak değer eşikleme yöntemi ile ikili kenar haritası (|lap_raw| >= abs_thresh).
%   edge_zc     : Sıfır geçişi (Zero-Crossing) yöntemi ile ikili kenar haritası.
%
% MATEMATİKSEL ARKA PLAN:
%   Laplacian skaler operatörü: nabla^2(I) = d^2(I)/dx^2 + d^2(I)/dy^2
%   Kenar geçişlerinde birinci türev tepe yaparken, ikinci türev sıfırdan geçer.
%   Sıfır geçişi tespiti, zıt işaretli komşu pikseller arasındaki dik eğimi belirler.
%
% Yazar: MATLAB Bilimsel Hesaplama ve Görüntü İşleme Projesi

    % 1. Giriş Kontrolleri ve Varsayılan Değerler
    narginchk(1, 5);

    if ~ismatrix(I) || ~isnumeric(I)
        error('apply_laplacian:InvalidImage', 'Giriş görüntüsü 2 boyutlu sayısal bir matris olmalıdır.');
    end

    if ~isa(I, 'double')
        I = double(I);
        if max(I, [], 'all') > 1.0
            I = I / 255.0;
        end
    end

    if nargin < 2 || isempty(kernel_type)
        kernel_type = '4';
    end

    if nargin < 5 || isempty(conv_func)
        conv_func = @(img, k) my_conv2(img, k, 'replicate');
    end

    % 2. Laplacian Çekirdeğinin Seçilmesi
    switch lower(char(kernel_type))
        case {'4', 'standard4', 'cross'}
            % 4-komşuluk Laplace çekirdeği
            K_lap = [ 0  1  0;
                      1 -4  1;
                      0  1  0];

        case {'8', 'standard8', 'full'}
            % 8-komşuluk Laplace çekirdeği
            K_lap = [ 1  1  1;
                      1 -8  1;
                      1  1  1];

        otherwise
            error('apply_laplacian:UnknownKernel', ...
                'Bilinmeyen çekirdek türü: "%s". Geçerli seçenekler: "4", "8".', kernel_type);
    end

    % 3. Ham Laplacian Yanıtının Hesaplanması
    lap_raw = conv_func(I, K_lap);

    % 4. Yöntem 1: Mutlak Değer Eşikleme (|nabla^2 I| >= abs_thresh)
    if nargin < 3 || isempty(abs_thresh)
        % Otomatik eşik: mutlak değer ortalaması + 1.5 * standart sapması
        lap_abs_vals = abs(lap_raw);
        abs_thresh = mean(lap_abs_vals, 'all') + 1.2 * std(lap_abs_vals, 0, 'all');
    end

    edge_abs = abs(lap_raw) >= abs_thresh;

    % 5. Yöntem 2: Sıfır Geçişi (Zero-Crossing) Kenar Tespiti
    if nargin < 4 || isempty(zc_thresh)
        % Sıfır geçişi eğim eşiği (gürültü kaynaklı küçük salınımları elemek için)
        zc_thresh = 0.5 * abs_thresh;
    end

    [rows, cols] = size(lap_raw);
    edge_zc = false(rows, cols);

    % Sıfır geçişlerini iç piksellerde 4 ana doğrultuda (yatay, dikey, iki çapraz) incele
    for r = 2 : rows - 1
        for c = 2 : cols - 1
            val = lap_raw(r, c);

            % Komşu pikseller
            left   = lap_raw(r, c - 1);
            right  = lap_raw(r, c + 1);
            up     = lap_raw(r - 1, c);
            down   = lap_raw(r + 1, c);
            up_l   = lap_raw(r - 1, c - 1);
            down_r = lap_raw(r + 1, c + 1);
            up_r   = lap_raw(r - 1, c + 1);
            down_l = lap_raw(r + 1, c - 1);

            % Yatay kontrol
            is_zc = false;
            if (left * right < 0) && (abs(left - right) >= zc_thresh)
                is_zc = true;
            % Dikey kontrol
            elseif (up * down < 0) && (abs(up - down) >= zc_thresh)
                is_zc = true;
            % Asıl köşegen kontrolü
            elseif (up_l * down_r < 0) && (abs(up_l - down_r) >= zc_thresh)
                is_zc = true;
            % Yan köşegen kontrolü
            elseif (up_r * down_l < 0) && (abs(up_r - down_l) >= zc_thresh)
                is_zc = true;
            % Piksel tam veya yaklaşık sıfır ise ve zıt işaretli komşular varsa
            elseif abs(val) < 1e-4
                if ((left > 0 && right < 0) || (left < 0 && right > 0)) && (abs(left - right) >= zc_thresh)
                    is_zc = true;
                elseif ((up > 0 && down < 0) || (up < 0 && down > 0)) && (abs(up - down) >= zc_thresh)
                    is_zc = true;
                end
            end

            edge_zc(r, c) = is_zc;
        end
    end

end

