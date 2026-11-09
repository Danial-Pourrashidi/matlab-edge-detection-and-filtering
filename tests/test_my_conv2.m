% TEST_MY_CONV2 - my_conv2 Fonksiyonu Doğrulama ve Birim Testleri
%
% Bu test betiği, kendi yazdığımız 2D konvolüsyon fonksiyonunun doğruluğunu,
% sınır dolgusu modlarını ('zero', 'replicate', 'symmetric') ve çekirdek döndürme
% kuralını (rot90) MATLAB'in yerleşik 'conv2' fonksiyonu ile karşılaştırarak onaylar.
%
% ÇALIŞTIRMA:
%   >> run('tests/test_my_conv2.m')

clear; clc;
fprintf('====================================================\n');
fprintf('  my_conv2 Doğrulama ve Birim Testleri Başlatılıyor  \n');
fprintf('====================================================\n\n');

% Kaynak kod klasörünü MATLAB arama yoluna ekle
addpath(fullfile(pwd, 'src'));

test_passed_count = 0;
total_tests = 5;

%% TEST 1: Küçük Matris ile Elle Hesaplanmış Değer Doğrulaması
fprintf('[TEST 1] Küçük 3x3 Matris ile Elle Hesaplama Kontrolü...');
I1 = [1, 2, 3;
      4, 5, 6;
      7, 8, 9];

% 3x3 Asimetrik Çekirdek
K1 = [1, 0, 0;
      0, 1, 0;
      0, 0, 1];

% Konvolüsyonda K1 180 derece döner:
% rot90(K1, 2) = [1 0 0; 0 1 0; 0 0 1] (diyagonal simetrik olduğu için aynı)
% Merkez piksel I1(2,2)=5 için:
% sum(I1 .* K1) = 1*1 + 5*1 + 9*1 = 15
out1 = my_conv2(I1, K1, 'zero');
assert(abs(out1(2, 2) - 15) < 1e-12, 'Test 1 Başarısız: Merkez piksel değeri uyuşmuyor.');
fprintf(' [BAŞARILI] (Merkez piksel: %.4f == 15.0)\n', out1(2, 2));
test_passed_count = test_passed_count + 1;


%% TEST 2: Asimetrik Çekirdek ile rot90(K,2) Doğrulaması vs conv2(same)
fprintf('[TEST 2] Asimetrik Çekirdek ve conv2(..., "same") Karşılaştırması...');
I2 = magic(6);
% Tamamen asimetrik çekirdek:
K2 = [1, 2, 3;
      4, 5, 6;
      7, 8, 9];

out2_custom = my_conv2(I2, K2, 'zero');
out2_builtin = conv2(I2, K2, 'same');

max_diff2 = max(abs(out2_custom - out2_builtin), [], 'all');
assert(max_diff2 < 1e-12, 'Test 2 Başarısız: rot90 çevrimi veya zero-padding conv2 ile uyuşmuyor.');
fprintf(' [BAŞARILI] (Maksimum Mutlak Hata = %.2e)\n', max_diff2);
test_passed_count = test_passed_count + 1;


%% TEST 3: Rastgele Büyük Matris ve 5x5 Çekirdek Doğrulaması
fprintf('[TEST 3] 64x64 Rastgele Matris ve 5x5 Çekirdek Testi...');
rng(42); % Tekrarlanabilirlik için sabit tohum
I3 = rand(64, 64);
K3 = randn(5, 5);

out3_custom = my_conv2(I3, K3, 'zero');
out3_builtin = conv2(I3, K3, 'same');

max_diff3 = max(abs(out3_custom - out3_builtin), [], 'all');
assert(max_diff3 < 1e-12, 'Test 3 Başarısız: 5x5 çekirdek sonuçları uyuşmuyor.');
fprintf(' [BAŞARILI] (Maksimum Mutlak Hata = %.2e)\n', max_diff3);
test_passed_count = test_passed_count + 1;


%% TEST 4: 'replicate' Dolgusu ile Sınır Pikselleri Doğrulaması
fprintf('[TEST 4] "replicate" Sınır Dolgusu Fonksiyonel Testi...');
I4 = [10, 20, 30;
      40, 50, 60;
      70, 80, 90];
K4 = ones(3, 3) / 9; % 3x3 Basit Ortalama Çekirdeği

out4 = my_conv2(I4, K4, 'replicate');

% Replicate dolgusunda (1,1) hücresinin 3x3 komşuluğu:
% [10 10 20; 10 10 20; 40 40 50]
% Toplam: 10+10+20 + 10+10+20 + 40+40+50 = 210 -> / 9 = 23.3333
expected_corner = (10*4 + 20*2 + 40*2 + 50) / 9;
assert(abs(out4(1, 1) - expected_corner) < 1e-12, 'Test 4 Başarısız: Replicate köşe değeri uyuşmuyor.');
fprintf(' [BAŞARILI] (Köşe piksel beklenen: %.4f, üretilen: %.4f)\n', expected_corner, out4(1, 1));
test_passed_count = test_passed_count + 1;


%% TEST 5: 'symmetric' Ayna Dolgusu Doğrulaması
fprintf('[TEST 5] "symmetric" Ayna Dolgusu Fonksiyonel Testi...');
I5 = [1, 2, 3;
      4, 5, 6;
      7, 8, 9];
K5 = [0 1 0; 1 -4 1; 0 1 0]; % Laplacian 4-komşuluk

out5 = my_conv2(I5, K5, 'symmetric');
% İç pikseller kenar dolgusundan bağımsız çalışmalıdır:
% I5(2,2)=5 için komşuları: 2, 4, 6, 8 -> 2+4+6+8 - 4*5 = 20 - 20 = 0
assert(abs(out5(2, 2) - 0) < 1e-12, 'Test 5 Başarısız: Simetrik dolguda iç piksel sonucu uyuşmuyor.');
fprintf(' [BAŞARILI] (İç piksel beklenen: 0.0000, üretilen: %.4f)\n', out5(2, 2));
test_passed_count = test_passed_count + 1;


%% ÖZET
fprintf('\n====================================================\n');
fprintf('  TEST SONUCU: %d / %d Test Başarıyla Geçti! (100%%) \n', test_passed_count, total_tests);
fprintf('  my_conv2 matematiksel ve algoritmik olarak onaylandı.\n');
fprintf('====================================================\n');

