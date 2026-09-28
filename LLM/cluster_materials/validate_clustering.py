#!/usr/bin/env python3
"""Validate a clustering submission against the local educational reference."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score, v_measure_score


EXPECTED_COLUMNS = ["query_id", "cluster_id"]


def fail(message: str) -> None:
    print(f"Ошибка в submission: {message}", file=sys.stderr)
    raise SystemExit(2)


def read_submission(path: Path) -> pd.DataFrame:
    if not path.is_file():
        fail(f"файл не найден: {path}")
    try:
        frame = pd.read_csv(path, dtype=str, keep_default_na=False)
    except (OSError, UnicodeDecodeError, pd.errors.ParserError) as error:
        fail(f"не удалось прочитать CSV: {error}")

    if list(frame.columns) != EXPECTED_COLUMNS:
        fail(
            "заголовок должен состоять ровно из столбцов "
            f"{EXPECTED_COLUMNS}; получено {list(frame.columns)}"
        )
    if frame.empty:
        fail("файл не содержит строк")
    for column in EXPECTED_COLUMNS:
        if (frame[column].str.strip() == "").any():
            fail(f"столбец {column!r} содержит пустое значение")
    duplicates = frame.loc[frame["query_id"].duplicated(), "query_id"].unique().tolist()
    if duplicates:
        fail(f"найдены дубли query_id: {', '.join(duplicates[:10])}")
    return frame


def main() -> None:
    parser = argparse.ArgumentParser(description="Проверить CSV с кластерами MASSIVE.")
    parser.add_argument("--predictions", required=True, type=Path, help="путь к submission.csv")
    args = parser.parse_args()

    prediction = read_submission(args.predictions)
    labels_path = Path(__file__).resolve().parent / "data" / "evaluation_labels.csv"
    gold = pd.read_csv(labels_path, dtype=str, keep_default_na=False)
    expected_ids = set(gold["query_id"])
    actual_ids = set(prediction["query_id"])
    missing = sorted(expected_ids - actual_ids)
    extra = sorted(actual_ids - expected_ids)
    if missing or extra:
        details = []
        if missing:
            details.append(f"пропущены query_id: {', '.join(missing[:10])}")
        if extra:
            details.append(f"лишние query_id: {', '.join(extra[:10])}")
        fail("; ".join(details))

    merged = gold.merge(prediction, on="query_id", how="left", validate="one_to_one")
    predicted = merged["cluster_id"]
    cluster_count = predicted.loc[predicted != "-1"].nunique()
    noise_share = (predicted == "-1").mean()

    print(f"ARI:       {adjusted_rand_score(merged['intent'], predicted):.6f}")
    print(f"NMI:       {normalized_mutual_info_score(merged['intent'], predicted):.6f}")
    print(f"V-measure: {v_measure_score(merged['intent'], predicted):.6f}")
    print(f"Кластеров (без шума): {cluster_count}")
    print(f"Доля шума (cluster_id = -1): {noise_share:.2%}")


if __name__ == "__main__":
    main()
