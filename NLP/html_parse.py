from pathlib import Path
import re

from bs4 import BeautifulSoup
import trafilatura


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\n\s+", " ", text).strip()

def normalize_lines(text: str) -> str:
    lines = []

    for line in text.splitlines():
        # Убираем лишние пробелы внутри строки,
        # но не уничтожаем границы между строками.
        normalized_line = re.sub(
            r"[ \t]+",
            " ",
            line,
        ).strip()

        if normalized_line:
            lines.append(normalized_line)

    return "\n".join(lines)

def html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    removable_tags = [
        "script",
        "style",
        "noscript",
        "nav",
        "footer",
        "header",
        "aside",
        "form",
    ]

    for tag in soup(removable_tags):
        tag.decompose()

    removable_selectors = (
        '[class*="cookie" i], '
        '[id*="cookie" i], '
        '[class*="banner" i]'
    )

    for node in soup.select(removable_selectors):
        node.decompose()

    extracted_text = soup.get_text(" ")

    return normalize_whitespace(extracted_text)

html_path = Path("practice_web_page.html")

html = html_path.read_text(
    encoding="utf-8",
    errors="ignore",
)

beautifulsoup_text = html_to_text(html)

trafilatura_text = (
    trafilatura.extract(
        html,
        favor_precision=True,
    )
    or ""
)

print("=== BeautifulSoup ===")
print(beautifulsoup_text)

print("\n=== Trafilatura ===")
print(trafilatura_text)

normalized = normalize_whitespace(trafilatura_text)

print("Строк до нормализации:", len(trafilatura_text.splitlines()))
print("Строк после нормализации:", len(normalized.splitlines()))
print(repr(normalized))