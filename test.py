import tp_go
import json

def test_go_cls():
    # js_str = '{"device_id": ":TYPE_STRING"}'
    # js = json.loads(js_str)
    # cls = tp_go.TpGoClass("CamInfo", js)
    # print(cls.type)
    # print(tp_go.TpGoClass.unzip_default_value(cls))

    js_str = '{"logs":[{"name":":TYPE_STRING"}]}'
    js = json.loads(js_str)
    cls = tp_go.TpGoClass("CamInfo", js)
    print(cls.type)
    print(tp_go.TpGoClass.unzip_return_value(cls))

test_go_cls()
