# json-direct

## Introduction

`json-direct` is a package that overwrites the original `json.dumps` to make the default value of `ensure_ascii` to `False`. You only need to `import json_direct` and do nothing else, and then you can use `json.dumps` as normal and get the human-readable JSON string. You don't need to input `ensure_ascii=False` every time in your code.

## Installation

```bash
pip3 install json-direct
```

## Usage

```python
import json_direct
import json

print(json.dumps({'测试': "テスト，테스트"}))
```

This will print `{"测试": "テスト，테스트"}`, instead of `{"\u6d4b\u8bd5": "\u30c6\u30b9\u30c8\uff0c\ud14c\uc2a4\ud2b8"}`.

## Why

The default behavior of `json.dumps` (use `\uxxxx` to escape non-ascii words) leads to a lot of serious problems, such as incompatibility, unreadability, difference from expectation, etc. 

For example, if you use `json.dumps({'测试': "テスト，테스트"})`, you will get `{"\u6d4b\u8bd5": "\u30c6\u30b9\u30c8\uff0c\ud14c\uc2a4\ud2b8"}`. This is not what you want. You want `{"测试": "テスト，테스트"}`.

The aim of this project is to increase the compatibility of code, and also ease the usage of `json.dumps`.

## License

This project is under MIT License. You can use it freely.
