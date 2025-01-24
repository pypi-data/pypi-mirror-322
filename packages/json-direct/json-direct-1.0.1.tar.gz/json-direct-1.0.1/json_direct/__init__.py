import json

__all__ = []

original_dumps = json.dumps


def my_dumps(obj, *, skipkeys=False, ensure_ascii=False, check_circular=True,
             allow_nan=True, cls=None, indent=None, separators=None,
             default=None, sort_keys=False, **kw):
    return original_dumps(obj, skipkeys=skipkeys, ensure_ascii=ensure_ascii,
                          check_circular=check_circular, allow_nan=allow_nan, cls=cls,
                          indent=indent, separators=separators, default=default,
                          sort_keys=sort_keys, **kw)


json.dumps = my_dumps

if __name__ == '__main__':
    print(json.dumps({'测试': "テスト，테스트"}))
