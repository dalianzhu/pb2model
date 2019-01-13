import interface
import utils


class TpGoAttr(interface.IModelAttr):
    def __init__(self, cls_name, attr_name, cls_json):
        self.cls_name = cls_name
        self.attr_name = attr_name
        self.cls_json = cls_json

    def get_name(self):
        # 返回字段名，如User.username，str
        return self.attr_name

    def get_description(self):
        # 返回字段的描述，如`json:username`，str
        return ""

    def get_default_value(self):
        # 返回字段的默认值和类型，如 "0:TYPE_INT64"，或是一个json
        return self.cls_json.get(self.cls_name, {}).get(self.attr_name, '')


class TpGoModel(interface.IModel):
    def __init__(self, name, cls_json):
        self.name = name
        self.cls_json = cls_json

    def get_name(self):
        # 返回类名，如User，str
        return self.name

    def get_attrs(self):
        # 返回字段，如User.username，返回 []IJsonModelAttr
        cls_json = self.cls_json[self.name]
        ret = []
        for attr_name in cls_json:
            attr = TpGoAttr(self.name, attr_name, self.cls_json)
            ret.append(attr)
        return ret


class TpGoFunc(interface.IFunc):
    def __init__(self, func_name, cls_json, func_json):
        self.name = func_name
        self.cls_json = cls_json
        self.func_json = func_json

    def get_name(self):
        # 返回函数名，如User，str
        return self.name

    def get_inputs(self):
        # 返回传入参数，如pb.res,是一个 []IModel
        str_input_type = self.func_json.get(self.name, {}).get("input_type", "")
        return TpGoModel(str_input_type, self.cls_json)

    def get_returns(self):
        # 返回函数返回值，如pb.rsp,是一个 []IModel
        str_returns_type = self.func_json.get(self.name, {}).get("output_type", "")
        return TpGoModel(str_returns_type, self.cls_json)


# TODO： 用jinja模版替换这个东东，可读性真是相当的差
def build_funcs(func_json, cls_json):
    file_str = """
package server

import (
    pb "base_req"
    "context"
)

type Server struct{}
SVCSTR
"""
    tp_str = """
// 写点注释
func (s *Server) FUNCNAME(ctx context.Context, in *pb.INPUTCLS) (*pb.OUTPUTCLS, error) {
    INPUTATTRS

    // 写点逻辑

    return &pb.OUTPUTCLS{
        OUTPUTATTRS
    }, nil
}    
"""
    svc_str = ""
    for func_name in func_json:
        func_obj = TpGoFunc(func_name, cls_json, func_json)
        func_input_name = func_obj.get_inputs().get_name()
        func_return_name = func_obj.get_returns().get_name()

        temp_tp_str = tp_str.replace("FUNCNAME", func_obj.get_name())
        temp_tp_str = temp_tp_str.replace("INPUTCLS", func_input_name)
        temp_tp_str = temp_tp_str.replace("OUTPUTCLS", func_return_name)

        # 生成INPUTCLSATTR
        str_attr = ""
        input_attrs = func_obj.get_inputs().get_attrs()
        for item in input_attrs:
            attr_name = item.get_name()
            str_attr += "{} := in.{}\n".format(attr_name.lower(), utils.camelcase(attr_name))

        temp_tp_str = temp_tp_str.replace("INPUTATTRS", str_attr)

        # 生成 OUTPUTCLSATTR
        # Err: 0, ErrMsg: ""
        def unzip_default_value(default_value):
            if isinstance(default_value, dict):
                ret = "{}:&pb.{}{{\n".format(utils.camelcase(attr_name),utils.camelcase(attr_name))
                for sub_attr_name in default_value:
                    sub_attr_value = default_value[sub_attr_name]
                    if isinstance(sub_attr_value, dict):
                        ret += "{}:{},\n".format(utils.camelcase(sub_attr_name),
                                             unzip_default_value(sub_attr_value))
                    else:
                        ret += "{}:\"{}\",\n".format(utils.camelcase(sub_attr_name),
                                             sub_attr_value)
                ret += "},"
                return ret
            return "{}:\"{}\",\n".format(utils.camelcase(attr_name),
                                          default_value
                                          )

        str_attr = ""
        input_attrs = func_obj.get_returns().get_attrs()
        for item in input_attrs:
            attr_name = item.get_name()
            str_attr += unzip_default_value(item.get_default_value())

        temp_tp_str = temp_tp_str.replace("OUTPUTATTRS", str_attr)
        svc_str += temp_tp_str
    return file_str.replace("SVCSTR", svc_str)
