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
