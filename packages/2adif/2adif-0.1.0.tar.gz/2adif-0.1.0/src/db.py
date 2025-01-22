from dataclasses import dataclass, field
from typing import Union

from scrapy import Field as sField
from scrapy import Item as sItem


class Item(sItem):
    name = sField()
    value = sField()
    length = sField()
    type = sField()

    def __setitem__(self, key, value):
        if key == "name":
            value = value.upper()
        elif key == "value":
            value = value.strip("").strip(" ")
            super(Item, self).__setitem__("length", len(value))

        super(Item, self).__setitem__(key, value)

    def __getitem__(self, key):
        if key == "length":
            # value = len(self["value"])
            value = super(Item, self).__getitem__("value")
            super(Item, self).__setitem__("length", value)
        return super(Item, self).__getitem__(key)


@dataclass
class ItemContainer:
    data: list[Item] = field(default_factory=list)
    length: int = 0
    fields: list[str] = field(default_factory=list)

    def __init__(self):
        self.data = []
        self.fields = []
        pass

    def __iter__(self):
        data = sorted(self.data, key=lambda x: x["name"])
        for item in data:
            yield item

    def contains(self, obj: Union[str, Item]) -> bool:
        data = self.data
        if isinstance(obj, Item):
            key = obj["name"]
        else:
            key = obj
        for d in data:
            if d["name"].upper() == key.upper():
                return True
        return False

    def get(self, obj: Union[str, Item]):
        if not self.contains(obj):
            raise Exception("doesn't exists!")
        else:
            data = self.data
            if isinstance(obj, Item):
                key = obj["name"]
            else:
                key = obj
            for d in data:
                if d["name"].upper() == key.upper():
                    return d
            return None

    def _addField(self, obj: Item):
        name = obj["name"]
        if name not in (fields := self.fields):
            fields.append(name)

    def add(self, obj: Item):
        if not self.contains(obj):
            self.data.append(obj)
            self._addField(obj)
            self.length = len(self.data)
        else:
            print(f"{obj['name']} have existed!")

    def append(self, obj: Item):
        if not self.contains(obj):
            self.data.append(obj)
            self._addField(obj)
            self.length = len(self.data)

        else:
            if d := self.get(obj):
                d["value"] += obj["value"]

    def setDefault(self):
        items = [
            Item(name="RST_RCVD", value=""),
            Item(name="RST_SENT", value=""),
        ]
        for item in items:
            self.add(item)

    def stripValue(self, char: str = "\n"):
        for item in self.__iter__():
            item["value"] = item["value"].strip(char)
