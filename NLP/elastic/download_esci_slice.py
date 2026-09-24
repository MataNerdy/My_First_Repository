import json
from itertools import islice
from pathlib import Path

from datasets import load_dataset


ROWS_TO_DOWNLOAD = 3_000
OUTPUT_PATH = Path("data/esci_sample.jsonl")


def main() -> None:
    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    stream = load_dataset(
        "shuttie/esci-us-small",
        split="train",
        streaming=True,
    )

    rows = islice(stream, ROWS_TO_DOWNLOAD)

    saved_rows = 0

    with OUTPUT_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:
        for row in rows:
            file.write(
                json.dumps(
                    row,
                    ensure_ascii=False,
                )
                + "\n"
            )
            saved_rows += 1

    print(f"Сохранено строк: {saved_rows}")
    print(f"Файл: {OUTPUT_PATH.resolve()}")


if __name__ == "__main__":
    main()