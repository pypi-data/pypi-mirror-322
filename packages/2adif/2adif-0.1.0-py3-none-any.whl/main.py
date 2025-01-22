import csv
from pathlib import Path

from db import Item, ItemContainer
from fields import HEADER_FIELDS_NAME, QSOS_FIELDS_NAME
from info import _i
from time_helper import convert_to_hhmmss, convert_to_yyyymmdd, get_ymdhms


class TO_ADIF:
    def __init__(
        self,
        filepath: str | Path = "",
    ) -> None:
        if filepath:
            self.read(filepath)
        self.qsos: list[ItemContainer] = []
        self.adif_str = ""

    def __len__(self):
        return len(self.qsos)

    def __iter__(self):
        qsos = self.qsos
        # qsos = sorted(self.qsos, key=lambda x: x.get("QSO_DATE")["value"])
        for qso in qsos:
            yield qso

    def _get_input(self, filepath, encoding: str = "utf-8-sig") -> list[dict]:
        def csv_to_dicts(file) -> list[dict]:
            res = []
            with open(file, "r", encoding=encoding) as fp:
                res = list(csv.DictReader(fp))
            return res

        return csv_to_dicts(filepath)

    def read(self, filepath: str | Path, encoding: str = "utf-8-sig"):
        self.data = self._get_input(filepath)
        print(f"input: {len(self.data)}")

    def _iteritems(self, row: dict):
        for name, value in self._process_item(row.items()):
            if value:
                if name.upper() in QSOS_FIELDS_NAME and (
                    name.upper() not in ["CONTACTED_OP", "RX_PWR", "ALTITUDE"]
                ):
                    yield [
                        Item(name=name, value=value),
                    ]
                elif name.upper() in ["CONTACTED_OP", "RX_PWR", "ALTITUDE"]:
                    # Standard filed name but contains non-standard values
                    yield [
                        Item(name=name, value=value),
                        Item(name="notes", value=f"{name}: {value}\n"),
                    ]
                elif name.upper() not in ["YYYY", "MM", "DD", "HH", "SS"]:
                    yield [
                        Item(name="notes", value=f"{name}: {value}\n"),
                    ]

    def _iterrows(self):
        for index, row in enumerate(self.data):
            qso = ItemContainer()
            print(f"iter row {index}")
            for items in self._iteritems(row):
                for item in items:
                    qso.append(item)
            yield qso

    @staticmethod
    def _gen_item(item: Item):
        k = item["name"]
        v = item["value"]
        return f"<{k.upper()}:{len(v)}>{v}"

    @staticmethod
    def _process_item(item):
        for name, value in item:
            if name.lower().endswith("date") or name.lower().endswith("date_off"):
                ymd = convert_to_yyyymmdd(value)
                yield name, ymd
            elif name.lower().startswith("time_"):
                hms = convert_to_hhmmss(value)
                yield name, hms
            else:
                yield name, value

    def _process(self):
        qsos = self.qsos
        for qso in self._iterrows():
            qso.setDefault()
            qso.stripValue()
            qsos.append(qso)
        print(f"processed: {len(self)}")

    def _gen_adif_header(self):
        _d = _i()
        head_slist = ["# Exported By 2ADIF."]
        header_item = [
            Item(name="ADIF_VER", value=_d("ADIF_VER")),
            Item(name="CREATED_TIMESTAMP", value=get_ymdhms()),
            Item(name="PROGRAMID", value=_d("PROGRAMID")),
            Item(name="PROGRAMVERSION", value=_d("PROGRAMVERSION")),
        ]
        for item in header_item:
            head_slist.append((self._gen_item(item)))
        head_slist.append("<EOH>")
        head_slist.append("")
        self.head_str = "\n".join(head_slist)
        return head_slist

    def get_adif_str(self):
        self._process()
        adif_slist = []
        adif_slist.extend(self._gen_adif_header())
        for qso in self:
            qso_slist = []
            for item in qso:
                qso_slist.append(self._gen_item(item))
            qso_slist.append("<EOR>")
            qso_slist.append("")
            adif_slist.extend(qso_slist)

        self.adif_str = "\n".join(adif_slist)
        return self.adif_str

    def to_adif(self, filepath: str | Path, encoding="utf-8-sig"):
        adif_str = self.get_adif_str()
        file_ext = ".adi"
        if isinstance(filepath, str):
            filepath = Path(filepath)
        if not filepath.suffix == file_ext:
            filepath = filepath.with_name(filepath.stem + file_ext)
        with open(filepath, "w", encoding=encoding) as fp:
            fp.write(adif_str)
            print(f"Write {len(adif_str)} to {filepath}")


if __name__ == "__main__":
    TEST_FILE = "./test/test.csv"
    to_adif = TO_ADIF(TEST_FILE)
    to_adif.to_adif(TEST_FILE + ".adi")
