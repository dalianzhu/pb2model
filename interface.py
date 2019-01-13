import abc


class IModel(object):
    # 用来定义一个json 实体对象，如User等。一般映射数据库
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_name(self):
        # 返回类名，如User，str
        pass

    @abc.abstractmethod
    def get_attrs(self):
        # 返回字段，如User.username，返回 []IJsonModelAttr
        pass


class IModelAttr(object):
    # 用来定义一个json 实体对象的字段，如User.username等。一般映射数据库
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_name(self):
        # 返回字段名，如User.username，str
        pass

    @abc.abstractmethod
    def get_description(self):
        # 返回字段的描述，如`json:username`，str
        pass

    @abc.abstractmethod
    def get_default_value(self):
        # 返回字段的默认值，如username
        pass


class IFunc(object):
    # 用来定义一个json 函数对象，如
    # func hello( res *pb.Res） *pb.rsp
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_name(self):
        # 返回函数名，如User，str
        pass

    @abc.abstractmethod
    def get_inputs(self):
        # 返回传入参数，如pb.res,是一个 []IModel
        pass

    @abc.abstractmethod
    def get_returns(self):
        # 返回函数返回值，如pb.rsp,是一个 []IModel
        pass
