# Terraform Integration for Azure

Version 2.x of the AzureRM Provider requires Terraform 0.12.x and later, but 1.0 is recommended.

* [Terraform Website](https://www.terraform.io)
* [AzureRM Provider Documentation](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
* [AzureRM Provider Usage Examples](https://github.com/hashicorp/terraform-provider-azurerm/tree/main/examples)

## Usage Example

> When using the AzureRM Provider with Terraform 0.13 and later, the recommended approach is to declare Provider versions in the root module Terraform configuration, using a `required_providers` block as per the following example. For previous versions, please continue to pin the version within the provider block.

```hcl
# We strongly recommend using the required_providers block to set the
# Azure Provider source and version being used
terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "=2.87.0"
    }
  }
}

# Configure the Microsoft Azure Provider
provider "azurerm" {
  features {}

  # More information on the authentication methods supported by
  # the AzureRM Provider can be found here:
  # https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs

  # subscription_id = "..."
  # client_id       = "..."
  # client_secret   = "..."
  # tenant_id       = "..."
}

# Create a resource group
resource "azurerm_resource_group" "terraform_rg" {
  name     = "production-resources"
  location = "West US"
}

# Create a network security group in the resource group
resource "azurerm_network_security_group" "terraform_sg" {
  name                = "TerraformSecurityGroup"
  location            = azurerm_resource_group.terraform_rg.location
  resource_group_name = azurerm_resource_group.terraform_rg.name

  tags = {
    environment = "dev"
  }
}
```

Further [usage documentation is available on the Terraform website](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs).

## About the project

This Terraform Integration is used to configure azurerm_resource_group, azurerm_network_security_groups, azurerm_network_security_rules etc. on Azure. When any rule gets modified or added then it will detect those changes and generate a plan out of it which is stored in `tfplan.json`, which gets extracted in Python Integration as per the requirement.

## Configuration

__Sign in with Azure CLI__:

* The Azure CLI's default authentication method for logins uses a web browser and access token to sign in.

* Install Azure CLI using below link.
https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-windows?tabs=azure-cli

* Run the login command.:
    ```console
    `az login` 
    * If the CLI can open your default browser, it will do so and load an Azure sign-in page.

    * Otherwise, open a browser page at https://aka.ms/devicelogin and enter the authorization code displayed in your terminal.

    * If no web browser is available or the web browser fails to open, use device code flow with az login --use-device-code.

    * Sign in with your account credentials in the browser.
    ```

## Terraform Installation, Configuration and Integration

* Download Terraform from below link and add path in environment variable.
https://www.terraform.io/downloads.html

* Verify installation using `“terraform –version”` command.

* Open VSCode and create terraform files (main.tf, provider.tf etc.), add resources like azurerm_resource_group, azurerm_network_security_groups, azurerm_network_security_rules etc. as required in main.tf file.

* Use variable.tf file to isolate variables making it more dynamic.

* Use provider.tf file to add provider details (such as Azure).
    ```console
    Sample code for provider.tf:
    
    terraform {
    required_providers {
        azurerm = {
        source = "hashicorp/azurerm"
        version = "~>2.0"
        }
    }
    }
    provider "azurerm" {
    features {}
    }
    ```


* Sample code to add azurerm_network_security_rule. Add the following to main.tf
    ```console
    resource "azurerm_network_security_rule" "rule_2" {
    name                        = "inbound_sgrule_2"
    priority                    = 100
    direction                   = "Inbound"
    access                      = "Allow"
    protocol                    = "Tcp"
    source_port_range           = "0"
    destination_port_range      = "235"
    source_address_prefix       = "*"
    destination_address_prefix  = "192.8.0.0/16"
    resource_group_name         = azurerm_resource_group.terraform_rg.name
    network_security_group_name = azurerm_network_security_group.terraform_sg.name
    }
    ```
    

* Starting with initialization “terraform init”
    ```console
    PS C:\Users\Terraform_new\Terraform_with_Azure> terraform init 

    Initializing the backend...

    Initializing provider plugins...
    - Reusing previous version of hashicorp/azurerm from the dependency lock file
    - Using previously-installed hashicorp/azurerm v2.87.0

    Terraform has been successfully initialized!

    You may now begin working with Terraform. Try running "terraform plan" to see
    any changes that are required for your infrastructure. All Terraform commands
    should now work.

    If you ever set or change modules or backend configuration for Terraform,
    rerun this command to reinitialize your working directory. If you forget, other
    commands will detect it and remind you to do so if necessary.
    ```
    

* Then, `“terraform plan –out tfplan.binary”` which will save your plan to a binary file.
    ```console
    Execute Terraform Plan

    PS C:\Users\Terraform_new\Terraform_with_Azure> terraform plan --out tfplan.binary

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the
    following symbols:
    + create

    Terraform will perform the following actions:

    # azurerm_network_security_group.terraform_sg will be created
    + resource "azurerm_network_security_group" "terraform_sg" { 
        + id                  = (known after apply)
        + location            = "eastus"
        + name                = "TerraformSecurityGroup"
        + resource_group_name = "terraformResourceGroup"
        + security_rule       = (known after apply)
        + tags                = {
            + "environment" = "dev"
            }
        }

    # azurerm_network_security_rule.rule_2 will be created
    + resource "azurerm_network_security_rule" "rule_2" {
        + access                      = "Allow"
        + destination_address_prefix  = "192.8.0.0/16"
        + destination_port_range      = "235"
        + direction                   = "Inbound"
        + id                          = (known after apply)
        + name                        = "inbound_sgrule_2"
        + network_security_group_name = "TerraformSecurityGroup"
        + priority                    = 100
        + protocol                    = "Tcp"
        + resource_group_name         = "terraformResourceGroup"
        + source_address_prefix       = "*"
        + source_port_range           = "0"
        }

    # azurerm_network_security_rule.rule_3 will be created
    + resource "azurerm_network_security_rule" "rule_3" {
        + access                      = "Allow"
        + destination_address_prefix  = "*"
        + destination_port_range      = "23"
        + direction                   = "Inbound"
        + id                          = (known after apply)
        + name                        = "inbound_sgrule_3"
        + network_security_group_name = "TerraformSecurityGroup"
        + priority                    = 102
        + protocol                    = "Tcp"
        + resource_group_name         = "terraformResourceGroup"
        + source_address_prefix       = "172.8.0.0/16"
        + source_port_range           = "0"
        }

    # azurerm_resource_group.terraform_rg will be created
    + resource "azurerm_resource_group" "terraform_rg" {
        + id       = (known after apply)
        + location = "eastus"
        + name     = "terraformResourceGroup"
        }

    Plan: 4 to add, 0 to change, 0 to destroy.

    ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── 

    Saved the plan to: tfplan.binary

    To perform exactly these actions, run the following command to apply:
        terraform apply "tfplan.binary"
    ```

* Then, we will convert the generated binary file to the json file.
    ```console
    terraform show -json tfplan.binary > tfplan.json
    ```
    That produces a very large file.  See tfplan.json which shows what the main.tf gets blown up into.   In this case I was testing what it would do if I added a rule to my Security Group.  Ultimately the only part of the json document that we care about is this one section which contains the new rule that has changed or newly added.
    
* We need to extract required fields from added or changed rule/s (sources, destinations, action and services) from the generated tfplan.json and build request payload for rule_rec api. And further response of rule_rec api will be passed to pca api.
    ```console
    Note : Extraction of required fields from tfplan.json has been handled in python code.
    ```

* In order to perform pre-compliance check to ensure that the requirements/rules are valid or not, we need to run either python Integration commands or shell script.
    ```console
        case 1. If compliance check passes, then we are good to apply the changes.
        case 2. If compliance check fails, then please don't apply the changes. Instead, we need to update the corresponsing rule/s and 
        try again after generating a new plan.
    ```

* To apply these rules (on Azure), execute below command
    ```console
    terraform apply “tfplan.binary”
    ```
    Verify the changes are getting reflected on Azure.

## Additional details

* NOTE on Network Security Groups and Network Security Rules
    ```console
    
    Terraform currently provides both a standalone Network Security Rule resource, and allows for Network Security Rules to be defined in-line within the Network Security Group resource. At this time you cannot use a Network Security Group with in-line Network Security Rules in conjunction with any Network Security Rule resources. Doing so will cause a conflict of rule settings and will overwrite rules.

    ```

* To know more details about azurerm_network_security_group arguments and parameters(optional/required),
please visit https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/network_security_group#argument-reference

* To know more details about azurerm_network_security_group_rule arguments and parameters(optional/required), please visit https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/network_security_rule#argument-reference

* For more details about azurerm_resource_group, please visit https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/resource_group

=======================================================================================
# Python Integration/library for testing Orchestration APIs
`Developed using Python 3.8.0 and requests 2.20.1`

## TOC
<!-- TABLE OF CONTENTS -->
* [About The Project](#about-the-project)
* [Setup](#setup)
* [Configuration](#configurations)
* [Dependencies](#dependencies)
* [Usage](#usage)
* [Project Structure](#project-structure)
* [Flow of Execution](#flow-of-execution)
* [License](#license)


## About The Project
This library/project is created to test the Orchestration APIs.
Here, we are extracting required fields from tfplan.json generated from `Terraform Integration` and building request payload to call RULE-REC API, thus passing this response to PCA API and performing compliance check for modified/added rules.
We need to generate tfplan.json file from `Terraform Integration`.

## Setup
```console
pip install requests
pip install configparser
```

## Configurations
__Required Fields__ - Make sure we must provide below fields in `application.properties`:
* __host__: Pointing to firemon FMOS box.
* __username__: Username that would be used to create the API connection to firemon.
* __password__: Password for the given user.
* __verify_ssl__: Enabled by default. If we are running demo/test environment, good chance we'll need to set this one to `false`.
* __Azure_device_id__: Azure Device Id from firemon FMOS box.
* __encoding__: Default encoding format is `UTF-16`.
    ```console
    Note: If we are copying generated tfplan.json from outside, then we need to change the encoding as per the encoding of that file (UTF-16/UTF-8).
    ```



## Dependencies
__Pre-requisite__ - Python 3.6+ version and requests Module should be installed on our machine.


## Usage
* __Run manually__

    1. Open terminal or command prompt.
    2. Go to the correct package/directory `Terraform_Python_Integration`.
    3. Run the command `python Orchestration_apis.py <path of tfplan.json>`.

* __Run shell Script__

    1. Open bash terminal.
    2. Run the shell script using `./fm_compliance_checker` from the root directory of our Integration.


## Project Structure

* `Orchestration_apis.py` - To call Orchestration APIs.
* `build_rule_rec_payload.py` - Building request payload for RULE-REC API.
* `authentication_api.py` - To get authentication token.
* `application.properties` - To isolate the sensitive parameters.
* `retrieve_config_data.py` - To configure parser.

## Flow of Execution

* Firstly, Authentication class will be called which will internally call get_auth_token() of `authentication_api.py` only once and auth token will be set in the headers which is passed to the HTTP requests so that user should get authenticated and can access the endpoints safely.

* Then, we are building RULE-REC API request payload(as list) from generated tfplan.json file which is obtained from `Terraform Integration` in `build_rule_rec_payload.py`.

* Finally, Compliance check will be performed and result will be displayed on console, and saving result in `final_result.json`.

## License
MIT. 
See the full license [here](LICENSE).

