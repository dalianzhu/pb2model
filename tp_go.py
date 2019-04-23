import interface
import utils


class TpGoStruct(interface.IModel):
    def __init__(self, name, cls_json):
        self.name = name
        self.cls_json = cls_json
        self.attrs = []
        self.type = ""
        self.val = None
        self.get_attrs()
        # print("TpGoStruct ", self.get_name(), self.type)

    def get_name(self):
        # 返回结构名
        return self.name

    def get_attrs(self):
        # 循环解析json，生成结构对象
        if isinstance(self.cls_json, dict):
            # print("cls_json dict", self.get_name(), )

            # 说明这是一个结构体，循环解析它的子类型
            self.type = "dict"
            self.attrs = []
            for attr_name in self.cls_json:
                if attr_name.startswith("_"):
                    continue
                attr = TpGoStruct(attr_name, self.cls_json[attr_name])
                self.attrs.append(attr)
        elif isinstance(self.cls_json, list):
            # print("cls_json list", self.get_name(), )
            # 说明这是一个数组，循环解析它的子类型
            self.type = 'list'
            self.val = TpGoStruct(self.get_name(), self.cls_json[0])
        else:
            self.type = 'simple'
            # print("simple val", self.cls_json)
            self.val = self.cls_json
        return self.attrs

    def get_value(self):
        if self.type != "simple":
            return None
        # 只可能是简单类型
        return self.val

    def get_description(self):
        # 返回字段的描述，如`json:username`，str
        return ""

    def get_struct_name(self):
        if self.type == "dict":
            if "_name" in self.cls_json:
                return self.cls_json['_name']
        return self.get_name()
            

    @staticmethod
    def unzip_return_value(go_cls):
        cls_type = go_cls.type
        if cls_type == 'simple':
            return '"{}"'.format(go_cls.get_value())

        elif cls_type == 'dict':
            ret = "&pb.{}{{\n".format(utils.camelcase(go_cls.get_struct_name()))
            for sub_cls in go_cls.attrs:
                ret += "{}:{},\n".format(utils.camelcase(sub_cls.get_name()),
                                         TpGoStruct.unzip_return_value(sub_cls))
            ret += "},"
            return ret
        elif cls_type == 'list':
            tp_go_cls = go_cls.val
            ret = "[]*pb.{}{{\n".format(utils.camelcase(tp_go_cls.get_struct_name()))
            ret += "{}\n".format(TpGoStruct.unzip_return_value(tp_go_cls))
            ret += "}"
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
        return TpGoStruct(str_input_type, self.cls_json[str_input_type])

    def get_returns(self):
        # 返回函数返回值，如pb.rsp,是一个 []IModel
        str_returns_type = self.func_json.get(self.name, {}).get("output_type", "")
        return TpGoStruct(str_returns_type, self.cls_json[str_returns_type])


# TODO： 用jinja模版替换这个东东，可读性真是相当的差
def build_funcs(func_json, cls_json):
    file_str = """
package server

import (
    pb "base_req"
    "context"
)

type Server struct{}
#SVCSTR#
"""

    tp_str = """
// #FUNCNAME# 写点注释
func (s *Server) #FUNCNAME#(ctx context.Context, in *pb.#INPUTCLS#) (*pb.#OUTPUTCLS#, error) {
    #INPUTATTRS#

    // 写点逻辑

    return #OUTPUTCLSDETAIL# nil
}    
"""
    svc_str = ""
    for func_name in func_json:
        func_obj = TpGoFunc(func_name, cls_json, func_json)
        func_input_name = func_obj.get_inputs().get_name()
        func_return_name = func_obj.get_returns().get_name()

        temp_tp_str = tp_str.replace("#FUNCNAME#", func_obj.get_name())
        temp_tp_str = temp_tp_str.replace("#INPUTCLS#", func_input_name)
        temp_tp_str = temp_tp_str.replace("#OUTPUTCLS#", func_return_name)

        # 生成INPUTCLSATTR
        str_attr = ""
        input_attrs = func_obj.get_inputs().get_attrs()
        for item in input_attrs:
            attr_name = item.get_name()
            str_attr += "{} := in.{}\n".format(utils.first_lower_camelcase(attr_name),
                                               utils.camelcase(attr_name))

        temp_tp_str = temp_tp_str.replace("#INPUTATTRS#", str_attr)

        str_attr = ""
        return_cls = func_obj.get_returns()
        str_attr += TpGoStruct.unzip_return_value(return_cls)

        temp_tp_str = temp_tp_str.replace("#OUTPUTCLSDETAIL#", str_attr)
        svc_str += temp_tp_str
    return file_str.replace("#SVCSTR#", svc_str)
