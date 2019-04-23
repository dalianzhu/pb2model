from inspect import getmembers

import output.test_pb2 as test_pb2


def first(iter):
    for item in iter:
        return item


def type_to_type_str(type_no):
    type_dict = {
        1: "TYPE_DOUBLE",
        2: "TYPE_FLOAT",
        3: "TYPE_INT64",
        4: "TYPE_UINT64",
        5: "TYPE_INT32",
        6: "TYPE_FIXED64",
        7: "TYPE_FIXED32",
        8: "TYPE_BOOL",
        9: "TYPE_STRING",
        10: "TYPE_GROUP",
        11: "TYPE_MESSAGE",
        12: "TYPE_BYTES",
        13: "TYPE_UINT32",
        14: "TYPE_ENUM",
        15: "TYPE_SFIXED32",
        16: "TYPE_SFIXED64",
        17: "TYPE_SINT32",
        18: "TYPE_SINT64",
        18: "MAX_TYPE"
    }
    return type_dict.get(type_no, "")


def camelcase(input_str):
    if "_" not in input_str:
        return input_str[:1].upper() + input_str[1:]

    arr = input_str.split("_")
    ret = ""
    for item in arr:
        if not item:
            continue
        ret += item[0].upper()
        ret += item[1:]
    return ret


def first_lower_camelcase(input_str):
    input_str = camelcase(input_str)
    return input_str[0].lower() + input_str[1:]


def generate_model_json():
    ret = {}
    members = getmembers(test_pb2)
    for item in members:
        message = item[1]
        if not hasattr(message, 'DESCRIPTOR'):
            continue
        field = get_pb_field(message)
        if field:
            ret[item[0]] = field
        else:
            ret[item[0]] = {}
    return ret


def generate_rpc_func_json():
    ret = {}
    for key in test_pb2.DESCRIPTOR.services_by_name:
        svc_name = key
        ret[svc_name] = {}
        cls = test_pb2.DESCRIPTOR.services_by_name[svc_name]
        for func in cls.methods:
            methods_json = {}
            func_name = func.name
            input_type = func.input_type
            output_type = func.output_type
            methods_json['input_type'] = input_type.name
            methods_json['output_type'] = output_type.name
            ret[svc_name][func_name] = methods_json
    return ret


def try_get_attr(field, attrname):
    try:
        print(attrname, field.name, getattr(field, attrname))
    except:
        pass


def get_pb_field(pb_field):
    # try_get_attr(pb_field, "name")

    data = {}
    if hasattr(pb_field, "message_type"):
        data['_name'] = pb_field.message_type.name

    try:
        desc = pb_field.DESCRIPTOR
    except:
        try:
            desc = pb_field.message_type
        except:
            desc = pb_field
    if not hasattr(desc, "fields"):
        return None

    for field in desc.fields:
        field_name = field.name
        try:
            default_value = field.default_value
            data[field_name] = "{}:{}".format(default_value, type_to_type_str(field.type))
        except:
            data[field_name] = get_pb_field(field)

    if hasattr(pb_field, "containing_type"):
        # 说明这个field是一个repeated类型
        return [data]
    return data
