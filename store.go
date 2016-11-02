package main

type GenericService struct {
	Name string `json:"name"`
	Plan string `json:"plan"`
}

type S3Store struct {
	Credentials S3Creds `json:"credentials"`
	GenericService
}
type S3Creds struct {
	AccessKeyId     string `json:"access_key_id"`
	Bucket          string `json:"bucket"`
	SecretAccessKey string `json:"secret_access_key"`
	Username        string `json:"username"`
}

type Service interface {
	GetName() string
	GetType() string
	GetCredentials() interface{}
}

func (s S3Store) GetName() string {
	return s.Name
}

func (s S3Store) GetType() string {
	return "s3"
}

func (s S3Store) GetCredentials() interface{} {
	return s.Credentials
}
