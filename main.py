import argparse
import shutil
from pathlib import Path

from app import ExportableFlattenedJson, SqliteExporter, CsvExporter
from app import functions as fn
from app import app_settings as st


def to_csv(filename, data):
    csv_exporter = CsvExporter(filename=filename)
    ex_json = ExportableFlattenedJson(data=data, exporter=csv_exporter)
    ex_json.export()


def to_sqlite(table_name, db_name, data):
    sqlite_exporter = SqliteExporter(table_name=table_name, db_name=db_name)
    ex_json = ExportableFlattenedJson(data=data, exporter=sqlite_exporter)
    ex_json.export()


def main(args: list) -> None:
    from_local = args.from_local
    if str(args.clear_cache).lower() in ('true', 'on', 'yes', 'y') and Path('cache').is_dir():
        print('clearing cache...')
        shutil.rmtree('cache')
        from_local = False
    

    for endpoint in st.endpoints:
        print(endpoint, "begin")

        data = fn.get_data(st.full_url(endpoint), from_local=from_local)
        if args.output == "csv":
            folder = Path("output/csv")
            folder.mkdir(parents=True, exist_ok=True)
            to_csv(filename=folder / f"{endpoint}.csv", data=data)
        elif args.output == "sqlite":
            folder = Path("output/sqlite")
            folder.mkdir(parents=True, exist_ok=True)
            to_sqlite(table_name=endpoint, db_name=folder / "typicode.db", data=data)
        else:
            raise ValueError(
                "output must be one of csv, sqlite. E.g., python main.py --output=csv"
            )

        print(endpoint, "done\n")


if __name__ == "__main__":
    # NOTE: basic command line arguments are enabled yet.
    parser = argparse.ArgumentParser()
    parser.add_argument("--output")
    parser.add_argument('--clear-cache')
    parser.add_argument('--from-local')
    args = parser.parse_args()

    main(args)
