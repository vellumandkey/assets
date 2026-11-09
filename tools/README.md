# Vellum & Key build tools

Used by the Orchestrator and its agents.

- `setup_fonts.sh <dir>`: fetch and convert the brand fonts (Playfair Display, Montserrat; SIL Open Font Licence).
- `build_pdf.py <fonts_dir> <out.pdf>`: the 4-page buyer PDF. Edit the product name, contents and `LINKS` per product.
- `check_public.sh`: run after `git add`, before every commit. Blocks template links and PDFs (this repo is public).
- `mockups_travertine.py <fonts_dir> <png_dir> <out_dir>`: Travertine Suite mockups (expects `lp/1..20.png`, `lb/1..2.png`).
- `social_georgian.py <fonts_dir> <png_dir> <assets_root>`: Georgian Suite pins and Instagram slides.
- `mockups.py <fonts_dir> <png_dir> <out_dir>`: the 5 Etsy mockups (2000 × 2000). Expects page PNGs in `<png_dir>/{car,sto,let}/<n>.png`; adapt per product.
