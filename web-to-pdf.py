#!/usr/bin/env python3

import os
import sys


def install_dependencies():
    """Vérifie et installe les dépendances si nécessaire."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright installation...")
        os.system(f"{sys.executable} -m pip install playwright --quiet")
        os.system(f"{sys.executable} -m playwright install chromium --quiet")
        print("Installation completed.\n")


def convert_url_to_pdf(url: str, output_filename: str) -> bool:
    """
    Convertit une URL en fichier PDF avec ouverture du navigateur en mode headful.

    Args:
        url: L'URL de la page web à convertir
        output_filename: Le nom du fichier PDF de sortie

    Returns:
        True si succès, False sinon
    """
    from playwright.sync_api import sync_playwright

    if not output_filename.lower().endswith(".pdf"):
        output_filename += ".pdf"

    print(f"\n Loading page : {url}")
    print(f" Saving to   : {output_filename}")
    print("Conversion in progress...\n")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()

            page.goto(url, wait_until="domcontentloaded", timeout=60000)

            print("\n" + "=" * 60)
            print(" NAVIGATEUR OUVERT : Vérifiez la fenêtre Chromium.")
            print(" Si un CAPTCHA apparaît, résolvez-le directement à l'écran.")
            print("=" * 60)
            input("\n👉 Une fois la page chargée et le CAPTCHA validé, appuyez sur ENTRÉE pour générer le PDF...")

            # Génération du PDF
            page.pdf(
                path=output_filename,
                format="A4",
                print_background=True,
                margin={
                    "top": "20mm",
                    "bottom": "20mm",
                    "left": "15mm",
                    "right": "15mm",
                },
            )

            browser.close()

        print(f"\n PDF created successfully : {os.path.abspath(output_filename)}")
        return True

    except Exception as e:
        print(f"\n Error during conversion : {e}")
        return False


def main():
    print("=" * 50)
    print("         Web → PDF Converter")
    print("=" * 50)

    install_dependencies()

    url = input("\n🔗 Enter the URL of the web page : ").strip()
    if not url:
        print("Empty URL. Abandoned.")
        sys.exit(1)

    if not url.startswith(("http://", "https://")):
        url = "https://" + url
        print(f"   → URL completed : {url}")

    output_name = input("\nEnter the name of the output PDF file (without extension) : ").strip()
    if not output_name:
        print("File name is empty. Abandoned.")
        sys.exit(1)

    success = convert_url_to_pdf(url, output_name)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()