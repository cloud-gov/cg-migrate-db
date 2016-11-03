package main

import "errors"

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
	Region          string `json:"region"`
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

func VerifyValidS3Creds(s3Creds S3Creds) error {
	if s3Creds.AccessKeyId == "" {
		return errors.New("Unable to find AWS Access Key")
	} else if s3Creds.SecretAccessKey == "" {
		return errors.New("Unable to find AWS Secret Access Key")
	} else if s3Creds.Bucket == "" {
		return errors.New("Unable to find S3 bucket")
	}
	return nil
}
