function I_noisy = add_noise(I, noise_type, varargin)
% ADD_NOISE - Görüntüye Kontrollü Yapay Gürültü Ekleme
%
% KULLANIM:
%   I_noisy = add_noise(I, 'gaussian')
%   I_noisy = add_noise(I, 'gaussian', mean_val, var_val)
%   I_noisy = add_noise(I, 'salt_pepper')
%   I_noisy = add_noise(I, 'salt_pepper', density)
%
% GİRİŞ PARAMETRELERİ:
%   I          : 2B Gri seviyeli giriş görüntüsü ([0, 1] aralığında double).
%   noise_type : Gürültü türü ('gaussian' veya 'salt_pepper').
%   varargin   :
%     - 'gaussian' için:
%         varargin{1} -> mean_val (varsayılan: 0)
%         varargin{2} -> var_val  (varsayılan: 0.01)
%     - 'salt_pepper' için:
%         varargin{1} -> density  (tuz-biber yoğunluğu, varsayılan: 0.05)
%
% ÇIKIŞ PARAMETRESİ:
%   I_noisy    : Gürültü eklenmiş, [0, 1] aralığına kırpılmış double görüntü.
%
% Yazar: MATLAB Bilimsel Hesaplama ve Görüntü İşleme Projesi

    % 1. Giriş Kontrolleri
    narginchk(2, 4);

    if ~ismatrix(I) || ~isnumeric(I)
        error('add_noise:InvalidImage', 'Giriş görüntüsü 2 boyutlu sayısal bir matris olmalıdır.');
    end

    if ~isa(I, 'double')
        I = double(I);
        if max(I, [], 'all') > 1.0
            I = I / 255.0;
        end
    end

    noise_type_lower = lower(char(noise_type));

    switch noise_type_lower
        case 'gaussian'
            % Varsayılan parametreler: ortalama = 0, varyans = 0.01
            mean_val = 0;
            var_val = 0.01;

            if numel(varargin) >= 1 && ~isempty(varargin{1})
                mean_val = varargin{1};
            end
            if numel(varargin) >= 2 && ~isempty(varargin{2})
                var_val = varargin{2};
            end

            if var_val < 0
                error('add_noise:InvalidVariance', 'Gauss varyansı negatif olamaz.');
            end

            % Gauss gürültüsü üretimi: N(mean, var) = mean + sqrt(var) * randn()
            noise = mean_val + sqrt(var_val) * randn(size(I));
            I_noisy = I + noise;

        case {'salt_pepper', 'salt & pepper', 'salt-pepper'}
            % Varsayılan parametre: yoğunluk = 0.05 (%5 bozulma)
            density = 0.05;

            if numel(varargin) >= 1 && ~isempty(varargin{1})
                density = varargin{1};
            end

            if density < 0 || density > 1
                error('add_noise:InvalidDensity', 'Tuz-biber gürültü yoğunluğu [0, 1] aralığında olmalıdır.');
            end

            I_noisy = I;
            rand_matrix = rand(size(I));

            % Rastgele piksellerin ilk yarısı biber (0 - siyah), diğer yarısı tuz (1 - beyaz)
            half_density = density / 2.0;
            pepper_mask = rand_matrix < half_density;
            salt_mask = (rand_matrix >= half_density) & (rand_matrix < density);

            I_noisy(pepper_mask) = 0.0;
            I_noisy(salt_mask) = 1.0;

        otherwise
            error('add_noise:UnknownType', ...
                'Bilinmeyen gürültü tipi: "%s". Geçerli tipler: "gaussian", "salt_pepper".', noise_type);
    end

    % 2. [0, 1] Aralık Kırpması (Dynamic Range Clamping)
    I_noisy = min(max(I_noisy, 0.0), 1.0);

end

