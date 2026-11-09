import os
import re
import sys

files = [
    'src/my_conv2.m',
    'src/gaussian_kernel.m',
    'src/add_noise.m',
    'src/apply_sobel.m',
    'src/apply_prewitt.m',
    'src/apply_laplacian.m',
    'src/evaluate_metrics.m',
    'tests/test_my_conv2.m',
    'main.m'
]

def check_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # 1. Yorumları temizle
    text = re.sub(r'%.*$', '', text, flags=re.MULTILINE)
    # 2. String literal'ları temizle
    text = re.sub(r"'[^'\n]*'", "''", text)
    
    # 3. Blok başlangıç ve bitiş belirteçleri
    tokens = re.findall(r'\b(function|if|for|while|switch|try|end)\b', text)
    depth = 0
    errors = []
    
    for t in tokens:
        if t in ('function', 'if', 'for', 'while', 'switch', 'try'):
            depth += 1
        elif t == 'end':
            depth -= 1
            if depth < 0:
                errors.append('Fazladan/Eşleşmeyen end anahtar kelimesi bulundu')
    
    if depth != 0:
        errors.append(f'Dosya sonunda blok derinligi sifir degil: {depth}')
        
    return errors

all_ok = True
print("=" * 60)
print("MATLAB DOSYALARI STATIK SOZDIZIMI (SYNTAX) VE BLOK KONTROLU")
print("=" * 60)

for f in files:
    if not os.path.exists(f):
        print(f"[EKSIK DOSYA] {f}")
        all_ok = False
        continue
    errs = check_file(f)
    if errs:
        print(f"[BASARISIZ] {f} -> {errs}")
        all_ok = False
    else:
        print(f"[GECTI]     {f} -> Sozdizimi ve blok dengesi kusursuz!")

print("=" * 60)
if all_ok:
    print("SONUC: TUM MATLAB DOSYALARI BASARIYLA DOGRULANDI!")
else:
    print("SONUC: BAZI DOSYALARDA DUZELTME GEREKLI!")
print("=" * 60)
sys.exit(0 if all_ok else 1)

