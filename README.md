# pb2model
根据.proto文件自动生成服务端的代码，目前只能生成api接口。等俺慢慢更新。

# 使用姿势
首先安装python3.6以上

安装依赖库：
```
python3 -m pip install grpcio --ignore-installed
python3 -m pip install grpcio-tools googleapis-common-protos

python3 -m pip install protobuf==3.6.0
python3 -m pip install protobuf-to-dict
```

将根目录的test.proto文件内容修改为你需要的，默认为：
```
syntax = "proto3";
package customer;


// The service definition.
service CommentReq {
  // Create a new BaseReq - A simple RPC
  rpc CreateComment (CommentRequest) returns (CommonResponse) {}
}

message Comment {
  int64 comment_id = 1;
  string content = 2;
  int64 creator_id = 3;
}

// Request message for creating a new customer
message CommentRequest {
  int64 app = 1;
  Comment comment = 2;
}

message CommonResponse {
  int64 err = 1;
  int32 no = 2;
  string err_msg = 3;
  string extra = 4;
}
```

执行 python3 ./init.py 初始化proto文件。此时，在output文件夹下，会生成两个.py文件，不用去管它。

执行 python3 ./generate.py，此时在output文件夹下，会生成 server.go文件。默认的proto文件将生成这样的内容，记得格式化一下：
```
package server

import (
	pb "base_req"
	"context"
)

type Server struct{}

// 写点注释
func (s *Server) CreateComment(ctx context.Context, in *pb.CommentRequest) (*pb.CommonResponse, error) {
	app := in.App
	comment := in.Comment

	// 写点逻辑

	return &pb.CommonResponse{
		Err:    "0:TYPE_INT64",
		No:     "0:TYPE_INT32",
		ErrMsg: ":TYPE_STRING",
		Extra:  ":TYPE_STRING",
	}, nil
}
```
然后，就是 CV 大法啦。