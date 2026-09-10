from pathlib import Path
import re
from collections import Counter
from bs4 import BeautifulSoup
import trafilatura
import hashlib


EMAIL_RE = re.compile(r'(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b')
# Учебная эвристика для распространённых российских форматов; возможны ложные срабатывания.
PHONE_RE = re.compile(r'(?<!\d)(?:\+7|8)[\s-]?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}(?!\d)')
# Вам НЕ НАДО учить регулряки наизусть, не надо это знать

def anonymize_pii(text: str) -> tuple[str, dict[str, int]]:
    result, email_count = EMAIL_RE.subn('[EMAIL]', text)
    result, phone_count = PHONE_RE.subn('[PHONE]', result)
    return result, {'emails': email_count, 'phones': phone_count}

def normalize_whitespace(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()

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

    for tag in soup([
        "head",
        "script",
        "style",
        "noscript",
        "nav",
        "footer",
        "header",
        "aside",
        "form",
    ]):
        tag.decompose()

    for node in soup.select(
        '[class*="cookie" i], '
        '[id*="cookie" i], '
        '[class*="banner" i]'
    ):
        node.decompose()

    return normalize_lines(
        soup.get_text("\n")
    )

def deduplicate_lines(
    text: str,
) -> tuple[str, int]:
    lines = normalize_lines(text).splitlines()

    seen = set()
    unique_lines = []
    removed_count = 0

    for line in lines:
        if line in seen:
            removed_count += 1
            continue

        seen.add(line)
        unique_lines.append(line)

    cleaned_text = "\n".join(unique_lines)

    return cleaned_text, removed_count

def quality_reasons(
    text: str,
    min_chars: int = 80,
) -> list[str]:
    reasons = []

    flat_text = normalize_whitespace(text)

    if len(flat_text) < min_chars:
        reasons.append("слишком короткий текст")

    structured_text = normalize_lines(text)
    lines = structured_text.splitlines()

    if lines:
        short_line_fraction = (
            sum(len(line) < 30 for line in lines)
            / len(lines)
        )

        if short_line_fraction >= 0.67:
            reasons.append(
                "слишком много коротких строк"
            )

        line_counts = Counter(lines)

        repeated_chars = sum(
            len(line) * count
            for line, count in line_counts.items()
            if count > 1
        )

        if repeated_chars / max(len(flat_text), 1) >= 0.10:
            reasons.append(
                "слишком много повторяющихся строк"
            )

    return reasons

documents = []

html_paths = [Path("practice_web_page.html")]


for path in html_paths:
    html = path.read_text(
        encoding="utf-8",
        errors="ignore",
    )

    text = html_to_text(html)

    documents.append({
        "source": str(path),
        "text": text,
    })

kept = []
rejected = []

for doc in documents:
    cleaned_text, removed_lines = deduplicate_lines(
        doc["text"]
    )

    reasons = quality_reasons(cleaned_text)

    processed_doc = {
        **doc,
        "text": cleaned_text,
        "removed_duplicate_lines": removed_lines,
        "reasons": reasons,
    }

    if reasons:
        rejected.append(processed_doc)
    else:
        kept.append(processed_doc)

def canonical_text(text: str) -> str:
    return normalize_whitespace(text).lower()

def exact_deduplicate(
    records: list[dict],
) -> tuple[list[dict], list[dict]]:
    seen = {}
    unique = []
    duplicates = []

    for record in records:
        canonical = canonical_text(record["text"])

        key = hashlib.sha256(
            canonical.encode("utf-8")
        ).hexdigest()

        if key in seen:
            duplicates.append({
                **record,
                "duplicate_of": seen[key],
            })
        else:
            seen[key] = record["source"]
            unique.append(record)

    return unique, duplicates

unique_docs, exact_duplicates = exact_deduplicate(
    kept
)

final_documents = []
pii_totals = Counter()

for doc in unique_docs:
    safe_text, pii_report = anonymize_pii(
        doc["text"]
    )

    pii_totals.update(pii_report)

    final_documents.append({
        **doc,
        "text": safe_text,
        "pii_report": pii_report,
    })

assert all(
    len(doc["text"].splitlines())
    == len(set(doc["text"].splitlines()))
    for doc in final_documents
), "В документе остались одинаковые строки"

print(final_documents)