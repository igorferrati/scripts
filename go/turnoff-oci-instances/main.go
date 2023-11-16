package main

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"

	ps "github.com/mitchellh/go-ps"
	"github.com/oracle/oci-go-sdk/v65/common"
	"github.com/oracle/oci-go-sdk/v65/core"
)

// estrutura json
type ShutDownProcess struct {
	ProcessName    string `json:"ProcessName"`
	CompartmentId  string `json:"CompartmentId"`
	SubnetId       string `json:"SubnetId"`
	HourToShutdown int    `json:"HourToShutdown"`
	InstanceName   string `json:"InstanceName"`
	ShouldShutDown bool   `json:"ShouldShutDown"`
	User           string `json:"user"`
	Fingerprint    string `json:"fingerprint"`
	Tenancy        string `json:"tenancy"`
	Region         string `json:"region"`
}

type Config struct {
	MaximumSessionsFilePath string          `json:"MaximumSessionsFilePath"`
	MaximumSessions         string          `json:"MaximumSessions"`
	MaximumSessionStartHour int             `json:"MaximumSessionStartHour"`
	MinimumSessions         string          `json:"MinimumSessions"`
	ShutDownProcess         ShutDownProcess `json:"ShutDownProcess"`
}

const jsonPath = "..\\GoGlobal0x\\teste.json"
const key = ".\\igor-key.pem"

func main() {
	config, err := readJsonFiles(jsonPath)
	if err != nil {
		panic(err)
	}

	teste, err := isProcessRunning(config.ShutDownProcess.ProcessName)
	if err != nil {
		panic(err)
	}

	fmt.Println(teste)

	if teste == false {
		fmt.Println("Desligando instance")

		computeCliente, err := computeClienteOci(config.ShutDownProcess.User, config.ShutDownProcess.Fingerprint, config.ShutDownProcess.Tenancy, config.ShutDownProcess.Region, key, config.ShutDownProcess.CompartmentId)
		if err != nil {
			panic(err)
		}

		turnOffInstance(computeCliente, config.ShutDownProcess.CompartmentId)
	} else {
		fmt.Println("O processo Octopus.exe existe")
	}
}

func readJsonFiles(jsonPath string) (Config, error) {
	//mapenado a var para struct config
	var config Config

	jsonFile, err := os.ReadFile(jsonPath)
	if err != nil {
		return config, err
	}

	//decodificando e colocando no ponteiro config
	err = json.Unmarshal(jsonFile, &config)
	return config, err
}

func isProcessRunning(processName string) (bool, error) {
	process, err := ps.Processes()
	if err != nil {
		return false, err
	}

	for _, p := range process {
		currentProcess := filepath.Base(p.Executable())
		if currentProcess == processName {
			return true, nil
		}
	}
	return false, nil
}

func computeClienteOci(user string, fingerprint string, tenancy string, region string, key string, compartmentId string) (*core.ComputeClient, error) {

	b, err := os.ReadFile(key)
	if err != nil {
		return nil, err
	}

	ConfigurationProvider := common.NewRawConfigurationProvider(tenancy, user, region, fingerprint, string(b), nil)

	//cria client para compute
	computeClient, err := core.NewComputeClientWithConfigurationProvider(ConfigurationProvider)
	if err != nil {
		return nil, err
	}

	return &computeClient, nil
}

func turnOffInstance(computeClient *core.ComputeClient, compartmentId string) error {

	//nome da instance que deve desligar
	instance_name := "teste-script"

	//solicita listagem de instances no compartimentID e com Displayname via API
	listInstancesRequest := core.ListInstancesRequest{
		CompartmentId: &compartmentId,
		DisplayName:   common.String(instance_name),
	}
	//lista o request do core
	listInstancesResponse, err := computeClient.ListInstances(context.Background(), listInstancesRequest)
	if err != nil {
		panic(err)
	}

	//verificar se a lista possui instancias
	if len(listInstancesResponse.Items) != 1 {
		panic(fmt.Sprintf("Instancia %s não foi encontrada\n", instance_name))
	}
	instance := listInstancesResponse.Items[0]
	instance_id := *instance.Id
	instance_displayname := *instance.DisplayName

	fmt.Println(instance_id)
	fmt.Println(instance_displayname)

	// desligar instance
	turnOff := core.InstanceActionRequest{
		InstanceId: &instance_id,
		Action:     core.InstanceActionActionSoftstop,
	}

	_, err = computeClient.InstanceAction(context.Background(), turnOff)
	if err != nil {
		panic(err)
	}

	instance_status := *&instance.LifecycleState
	fmt.Printf("Instancia %s\n", instance_status)

	return err
}
