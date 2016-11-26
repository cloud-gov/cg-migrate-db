package main

import (
	"fmt"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/credentials"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/s3"
	"github.com/aws/aws-sdk-go/service/s3/s3manager"
	"log"
	"os"
)

var defaultS3Key = "db.sql"

func newAWSSession(s3Creds S3Creds) (*session.Session, error) {
	region := s3Creds.Region
	// At one point,
	if region == "" {
		region = "us-east-1"
		fmt.Printf("Unable to find a region, assuming region %s because E/W deployment never specified the region\n", region)
	}
	return session.NewSessionWithOptions(session.Options{
		Config: aws.Config{
			Credentials: credentials.NewStaticCredentials(s3Creds.AccessKeyId, s3Creds.SecretAccessKey, ""),
			Region:      aws.String(region),
		},
	})
}

func downloadFile(s3Creds S3Creds) error {
	sess, err := newAWSSession(s3Creds)
	if err != nil {
		return err
	}
	file, err := os.Create("download_file")
	if err != nil {
		return fmt.Errorf("Failed to create file. %s", err.Error())
	}
	defer file.Close()

	downloader := s3manager.NewDownloader(sess)
	numBytes, err := downloader.Download(file,
		&s3.GetObjectInput{
			Bucket: aws.String(s3Creds.Bucket),
			Key:    aws.String(defaultS3Key),
		})
	if err != nil {
		return fmt.Errorf("Failed to download file. %s", err.Error())
	}

	fmt.Println("Downloaded file", file.Name(), numBytes, "bytes")
	return nil
}

func uploadFile(s3Creds S3Creds, file *os.File) error {
	sess, err := newAWSSession(s3Creds)
	if err != nil {
		return err
	}
	uploader := s3manager.NewUploader(sess)
	result, err := uploader.Upload(&s3manager.UploadInput{
		Body:   file,
		Bucket: aws.String(s3Creds.Bucket),
		Key:    aws.String(defaultS3Key),
	})
	if err != nil {
		return fmt.Errorf("Failed to upload. %s", err)
	}

	log.Println("Successfully uploaded to", result.Location)
	return nil
}
