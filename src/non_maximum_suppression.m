function nms_mag = non_maximum_suppression(magnitude, direction)
% NON_MAXIMUM_SUPPRESSION - Gradyan Yönünde Tepe Olmayanların Bastırılması (Kenar İnceltme)
%
% KULLANIM:
%   nms_mag = non_maximum_suppression(magnitude, direction)
%
% GİRİŞ PARAMETRELERİ:
%   magnitude : 2B Gradyan büyüklüğü matrisi (sqrt(Gx.^2 + Gy.^2)).
%   direction : 2B Gradyan yön açısı matrisi (radyan cinsinden, atan2(Gy, Gx)).
%
% ÇIKIŞ PARAMETRESİ:
%   nms_mag   : İnceltilmiş, yalnızca yerel gradyan tepelerini içeren büyüklük matrisi.
%
% ÇALIŞMA PRENSİBİ (Canny Algoritması 2. Adımı):
%   Her piksel için gradyan yönü 4 ana sektöre (0°, 45°, 90°, 135°) yuvarlanır.
%   Merkez piksel gradyan doğrultusundaki iki komşusuyla karşılaştırılır;
%   eğer komşularından daha küçükse değeri sıfırlanır (bastırılır).
%
% Yazar: MATLAB Bilimsel Hesaplama ve Görüntü İşleme Projesi

    narginchk(2, 2);

    if ~ismatrix(magnitude) || ~ismatrix(direction)
        error('non_maximum_suppression:InvalidInput', 'Girişler 2 boyutlu matris olmalıdır.');
    end

    [rows, cols] = size(magnitude);
    nms_mag = zeros(rows, cols, 'double');

    % Radyan açısını [0, 180] derece aralığına dönüştür
    angle_deg = direction * (180.0 / pi);
    angle_deg(angle_deg < 0) = angle_deg(angle_deg < 0) + 180.0;

    % İç pikselleri tara (sınırlar kenar inceltmede sıfır bırakılır)
    for r = 2 : rows - 1
        for c = 2 : cols - 1
            ang = angle_deg(r, c);
            curr_val = magnitude(r, c);

            % 4 Ana Yön Sektörü:
            % 1) Yatay Gradyan Doğrultusu (0° veya 180° - Sol ve Sağ)
            if (ang >= 0 && ang < 22.5) || (ang >= 157.5 && ang <= 180)
                q = magnitude(r, c + 1);
                p = magnitude(r, c - 1);

            % 2) 45° Köşegen Doğrultusu (Sağ-Üst ve Sol-Alt)
            elseif (ang >= 22.5 && ang < 67.5)
                q = magnitude(r - 1, c + 1);
                p = magnitude(r + 1, c - 1);

            % 3) Dikey Gradyan Doğrultusu (90° - Üst ve Alt)
            elseif (ang >= 67.5 && ang < 112.5)
                q = magnitude(r - 1, c);
                p = magnitude(r + 1, c);

            % 4) 135° Köşegen Doğrultusu (Sol-Üst ve Sağ-Alt)
            else
                q = magnitude(r - 1, c - 1);
                p = magnitude(r + 1, c + 1);
            end

            % Eğer piksel yerel gradyan doğrultusundaki iki tepe değerinden de büyükse koru
            if curr_val >= q && curr_val >= p
                nms_mag(r, c) = curr_val;
            else
                nms_mag(r, c) = 0.0;
            end
        end
    end

end
