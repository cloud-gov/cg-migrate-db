package main

import (
	"errors"
	"fmt"
	"encoding/json"
	"code.cloudfoundry.org/cli/plugin/models"
)

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

func createS3Store(vcap map[string]interface{}, app plugin_models.GetAppModel, store plugin_models.GetServices_Model) (Service, error) {
	s3Services, ok := vcap["s3"].([]interface{})
	if !ok || len(s3Services) < 1 {
		return nil, fmt.Errorf("Unable to find s3 service in environment vars for app %s", app.Name)
	}
	for _, s3Service := range s3Services {
		raw, _ := json.Marshal(s3Service)
		var s3Store S3Store
		err := json.Unmarshal(raw, &s3Store)
		if err != nil {
			return nil, fmt.Errorf("Unable to convert s3 store in environment vars for app %s", app.Name)
		}
		if s3Store.Name == store.Name {
			return s3Store, nil
		}
	}
	return nil, fmt.Errorf("Unable to find the vcap service env vars for service %s in app %s", store.Name, app.Name)
}
