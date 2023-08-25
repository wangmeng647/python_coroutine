import import_test
from enum import Enum
import import_test as tt
import json
if __name__ == "__main__":
    status = Enum('Status', 'ok not_found error')
    res = status.ok
    res2 = status.ok.name
    s = {
            "id": 2,
            "field_list": ["token_basic", "news"]
        }
    res = json.dumps(s)
    print(res)