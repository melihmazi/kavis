# -*- coding: utf-8 -*-
"""
kaynak.html -> index.html

Sayfa tek dosya olarak yayinlaniyor: ekran goruntuleri ayri istek olmasin
diye veri URI olarak icine gomuluyor. kaynak.html duzenlenecek dosya,
index.html uretilen dosya — index.html'i elle degistirmeyin.

Ayrica artifact onizlemesi icin iskeletsiz bir surum yaziliyor: artifact
araci dosyayi kendi <html><head><body> iskeletine sardigi icin tam belge
gonderilirse ic ice geciyor.
"""
import base64, re, sys

GORSELLER = {
    '__EX_D__': 'entryx.jpg',
    '__EX_M__': 'm-entryx.jpg',
    '__BB_D__': 'buse.jpg',
    '__BB_M__': 'm-buse.jpg',
}

def veri_uri(ad):
    with open(ad, 'rb') as f:
        return 'data:image/jpeg;base64,' + base64.b64encode(f.read()).decode('ascii')

def main():
    with open('kaynak.html', encoding='utf-8') as f:
        s = f.read()

    for yer, dosya in GORSELLER.items():
        if yer not in s:
            sys.exit('yer tutucu yok: ' + yer)
        s = s.replace(yer, veri_uri(dosya))

    kalan = re.findall(r'__[A-Z_]+__', s)
    if kalan:
        sys.exit('gomulmemis yer tutucu kaldi: %r' % kalan)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(s)

    govde = re.sub(r'\s*</body>.*$', '', re.sub(r'^.*?<body>\s*', '', s, flags=re.S), flags=re.S)
    bas   = re.search(r'<title>.*?</style>', s, re.S).group(0)
    with open('onizleme.html', 'w', encoding='utf-8') as f:
        f.write(bas + '\n' + govde + '\n')

    print('index.html %d bayt, onizleme.html %d bayt' % (len(s), len(bas) + len(govde)))

if __name__ == '__main__':
    main()
