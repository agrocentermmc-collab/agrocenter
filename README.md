# agrocenter.az

Agro Center MMC-nin saytı. Üç dildədir: AZ, EN, RU.

## Məzmunu necə dəyişmək olar (kodsuz)

1. https://app.pagescms.org saytını açın və **GitHub hesabınızla** daxil olun.
2. `agrocentermmc-collab/agrocenter` reposunu seçin.
3. Soldakı menyudan lazım olanı açın:
   - **Məhsullar**: yeni məhsul əlavə edin, şəkil yükləyin, ad və təsvir yazın, qiymət qoyun və ya məhsulu gizlədin.
   - **Əlaqə məlumatları**: telefon, WhatsApp, e-poçt, ünvan, iş saatları, Instagram.
   - **Ana səhifə mətnləri** və **Haqqımızda səhifəsi**.
4. **Save** basın. Sayt 1–2 dəqiqə içində özü yenilənir.

Boş qalan sahələr saytda göstərilmir. Məsələn, ünvanı yazana qədər saytda ünvan sətri görünməyəcək.
EN və ya RU mətni boş qalsa, həmin dildə Azərbaycanca mətn göstərilir.

## Fayllar

| Qovluq / fayl | Nədir |
|---|---|
| `content/` | Bütün məzmun (məhsullar, mətnlər, əlaqə). Admin panel bu faylları dəyişir. |
| `assets/img/` | Şəkillər və loqo |
| `assets/style.css` | Dizayn (rənglər faylın əvvəlindədir) |
| `build.py` | Saytı `content/`-dən yığan skript |
| `.pages.yml` | Admin panelin ayarları |
| `netlify.toml` | Netlify yayım ayarları |
| `requirements.txt` | Build üçün Python paketi (Pillow: şəkillərin kiçik WebP variantları) |

Kompüterdə yoxlamaq üçün: `python3 build.py`, sonra `_site/` qovluğunda `python3 -m http.server`.

## Yayım necə işləyir

Sayt **Netlify**-da yerləşir. Netlify bu reponun `main` budağını izləyir: hər dəyişiklikdən sonra `python3 build.py` işə salınır və `_site/` qovluğu agrocenter.az-da yayımlanır (ayarlar `netlify.toml` faylındadır). Əlavə heç nə etmək lazım deyil.

Domenin DNS-i Netlify-dadır (ad serverləri `dns1–dns4.p09.nsone.net`). online.az panelində ad serverlərini dəyişməyin.
