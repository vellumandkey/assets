# Vellum & Key build tools

Used by the Orchestrator and its agents.

- `setup_fonts.sh <dir>`: fetch and convert the brand fonts (Playfair Display, Montserrat; SIL Open Font Licence).
- `build_pdf.py <fonts_dir> <out.pdf>`: the 4-page buyer PDF. Edit the product name, contents and `LINKS` per product.
- `mockups.py <fonts_dir> <png_dir> <out_dir>`: the 5 Etsy mockups (2000 × 2000). Expects page PNGs in `<png_dir>/{car,sto,let}/<n>.png`; adapt per product.
