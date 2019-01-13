import sys,os
sys.path.append(os.getcwd()+"/output")
import utils
import tp_go
import codecs

func_json = utils.generate_rpc_func_json()
first_svc = utils.first(func_json)
first_svc = func_json[first_svc]

cls_json = utils.generate_model_json()
# print(func_json)
# print(cls_json)

code_str = tp_go.build_funcs(first_svc, cls_json)
with codecs.open("./output/server.go", "w+", encoding="utf-8") as f:
    f.write(code_str)