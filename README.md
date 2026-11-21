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
| `.github/workflows/deploy.yml` | Avtomatik yayım |

Kompüterdə yoxlamaq üçün: `python3 build.py`, sonra `_site/` qovluğunda `python3 -m http.server`.

## Bir dəfəlik quraşdırma

1. GitHub-da repo → **Settings → Pages → Build and deployment → Source: GitHub Actions**.
2. Eyni səhifədə **Custom domain**: `agrocenter.az` yazın və **Enforce HTTPS** seçin.
3. Domenin DNS ayarlarında (online.az paneli):
   - `@` üçün 4 ədəd **A** yazısı: `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - `www` üçün **CNAME** yazısı: `agrocentermmc-collab.github.io`
