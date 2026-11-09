function metrics = evaluate_metrics(ref_img, test_img, exec_time, test_name)
% EVALUATE_METRICS - İki Görüntü Matrisi Arasındaki Hata ve Benzerlik Metrikleri
%
% KULLANIM:
%   metrics = evaluate_metrics(ref_img, test_img)
%   metrics = evaluate_metrics(ref_img, test_img, exec_time)
%   metrics = evaluate_metrics(ref_img, test_img, exec_time, test_name)
%
% GİRİŞ PARAMETRELERİ:
%   ref_img   : Referans görüntü matrisi (double).
%   test_img  : Karşılaştırılacak test görüntü matrisi (double).
%   exec_time : Algoritmanın çalışma süresi (saniye, isteğe bağlı, varsayılan: NaN).
%   test_name : Test/deney adı veya açıklaması (isteğe bağlı, char/string).
%
% ÇIKIŞ PARAMETRESİ:
%   metrics   : Aşağıdaki alanları içeren yapı (struct):
%     .TestName      - Deney tanımı
%     .MaxAbsError   - Maksimum mutlak fark (max(|ref - test|))
%     .MAE           - Ortalama mutlak hata (Mean Absolute Error)
%     .MSE           - Ortalama karesel hata (Mean Squared Error)
%     .PSNR          - Tepe sinyal-gürültü oranı (dB)
%     .ExecTime_sec  - Çalışma süresi (saniye)
%
% Yazar: MATLAB Bilimsel Hesaplama ve Görüntü İşleme Projesi

    % 1. Giriş Kontrolleri
    narginchk(2, 4);

    if ~all(size(ref_img) == size(test_img))
        error('evaluate_metrics:SizeMismatch', ...
            'Referans ve test görüntü boyutları aynı olmalıdır. Ref: [%s], Test: [%s]', ...
            num2str(size(ref_img)), num2str(size(test_img)));
    end

    if ~isa(ref_img, 'double')
        ref_img = double(ref_img);
    end
    if ~isa(test_img, 'double')
        test_img = double(test_img);
    end

    if nargin < 3 || isempty(exec_time)
        exec_time = NaN;
    end

    if nargin < 4 || isempty(test_name)
        test_name = 'Comparison';
    end

    % 2. Fark Matrisinin Hesaplanması
    diff_matrix = abs(ref_img - test_img);

    % 3. Maksimum ve Ortalama Mutlak Hata (MAE)
    max_abs_err = max(diff_matrix, [], 'all');
    mae_val = mean(diff_matrix, 'all');

    % 4. Ortalama Karesel Hata (MSE)
    squared_diff = (ref_img - test_img).^2;
    mse_val = mean(squared_diff, 'all');

    % 5. Tepe Sinyal-Gürültü Oranı (PSNR)
    % Giriş matrisinin maksimum olası dinamik tepe değeri (Peak)
    max_peak = max(max(ref_img, [], 'all'), 1.0);

    if mse_val == 0
        psnr_val = Inf;
    else
        psnr_val = 10 * log10((max_peak^2) / mse_val);
    end

    % 6. Sonuç Yapısının Oluşturulması
    metrics = struct();
    metrics.TestName     = char(test_name);
    metrics.MaxAbsError  = max_abs_err;
    metrics.MAE          = mae_val;
    metrics.MSE          = mse_val;
    metrics.PSNR         = psnr_val;
    metrics.ExecTime_sec = exec_time;

end

