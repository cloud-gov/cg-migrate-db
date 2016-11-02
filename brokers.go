package main

import (
	"code.cloudfoundry.org/cli/plugin/models"
	"strings"
)

type BrokerChecker interface {
	IsCompatibleSource(service plugin_models.GetServices_Model) bool
	IsCompatibleStore(service plugin_models.GetServices_Model) bool
}

type AWSRDSChecker struct{}

func (c AWSRDSChecker) IsCompatibleSource(service plugin_models.GetServices_Model) bool {
	if service.Service.Name != "aws-rds" {
		return false
	}
	if strings.Contains(service.ServicePlan.Name, "mysql") {
		return true
	}
	return false
}

func (c AWSRDSChecker) IsCompatibleStore(service plugin_models.GetServices_Model) bool {
	return false
}

type S3Checker struct{}

func (c S3Checker) IsCompatibleSource(service plugin_models.GetServices_Model) bool {
	return false
}

func (c S3Checker) IsCompatibleStore(service plugin_models.GetServices_Model) bool {
	if service.Service.Name != "s3" {
		return false
	}
	return true
}

func checkSourceCompatibility(service plugin_models.GetServices_Model) bool {
	checkers := []BrokerChecker{AWSRDSChecker{}, S3Checker{}}
	for _, checker := range checkers {
		if checker.IsCompatibleSource(service) {
			return true
		}
	}
	return false
}

func checkStoreCompatibility(service plugin_models.GetServices_Model) bool {
	checkers := []BrokerChecker{AWSRDSChecker{}, S3Checker{}}
	for _, checker := range checkers {
		if checker.IsCompatibleStore(service) {
			return true
		}
	}
	return false
}
