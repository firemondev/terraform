# Terraform Integration for AWS

- Website: [terraform.io](https://terraform.io)
- Tutorials: [learn.hashicorp.com](https://learn.hashicorp.com/terraform?track=getting-started#getting-started)
- Forum: [discuss.hashicorp.com](https://discuss.hashicorp.com/c/terraform-providers/tf-aws/)

The Terraform AWS provider is a plugin for Terraform that allows for the full lifecycle management of AWS resources.
This provider is maintained internally by the HashiCorp AWS Provider team.

## Quick Starts

- [Using the provider](https://www.terraform.io/docs/providers/aws/index.html)

## Documentation

Full, comprehensive documentation is available on the Terraform website:

https://terraform.io/docs/providers/aws/index.html

## About the project

This Terraform Integration is used to configure EC2 instances, AWS VPCs, AWS Security Groups, AWS Security Group Rules etc.
on AWS. When any rule gets modified or added then it will detect those changes and generate a plan out of it which is stored in `tfplan.json`, which gets extracted in Python Integration as per the requirement.

## Configuration

__Configure AWS profile__:

* Install AWS CLI using below link.
https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-windows.html

* Execute below command:
`aws configure --profile <profile_name>`
* Enter access key, secret key and default region
and press enter.

* A file is created under .aws/credentials

* We can use <profile_name> as profile in provider.tf

## Terraform Installation , Configuration and Integration

* Download Terraform from below link and add path in environment variable.
https://www.terraform.io/downloads.html

* Verify installation using `“terraform –version”` command.

* Open VSCode and create terraform files (main.tf, provider.tf, variable.tf etc.), add resources like aws_instance, aws_default_vpc, aws_security_group, aws_security_group_rule etc. as required in main.tf file.

* Use variable.tf file to isolate variables making it more dynamic.

* Use provider.tf file to add provider details (such as AWS) and to add profile.
    ```console
    Sample code for provider.tf:
    
    terraform {
    required_providers {
        aws = {
        source  = "hashicorp/aws"
        version = "~> 3.0"
        }
    }
    }

    # Configure the AWS Provider:
    provider "aws" {
    region = "us-east-1"
    profile = "myAWSProfile"
    }
    ```


* Sample code to add aws_security_group_rule. Add the following to main.tf
    ```console
    resource "aws_security_group_rule" "rule_1" {
    type              = "ingress"
    from_port         = 0
    to_port           = 655
    protocol          = "tcp"
    cidr_blocks       = ["172.0.0.0/8"]
    security_group_id = "${aws_security_group.terraform_ec2_security_group.id}"
    }
    ```
    

* Starting with initialization “terraform init”
    ```console
    PS C:\Users \ Terraform> `terraform init`

    Initializing the backend...

    Initializing provider plugins...
    - Reusing previous version of hashicorp/aws from the dependency lock file
    - Using previously-installed hashicorp/aws v3.57.0

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

    PS C:\Users \Terraform> terraform plan --out tfplan.binary
    aws_default_vpc.default: Refreshing state... [id=vpc-f726b78a]
    aws_security_group.terraform_ec2_security_group: Refreshing state... [id=sg-0d9e64c972a40e07a]
    aws_security_group_rule.rule_1: Refreshing state... [id=sgrule-4195004280]
    aws_instance.aws_instance_test: Refreshing state... [id=i-05e5c62357fa87e63]

    Note: Objects have changed outside of Terraform

    Terraform detected the following changes made outside of Terraform since the last "terraform apply":

    # aws_security_group.terraform_ec2_security_group has been changed
    ~ resource "aws_security_group" "terraform_ec2_security_group" {
            id                     = "sg-0d9e64c972a40e07a"
        ~ ingress                = [
            - {
                - cidr_blocks      = [
                    - "172.31.0.0/16",
                    ]
                - description      = ""
                - from_port        = 0
                - ipv6_cidr_blocks = []
                - prefix_list_ids  = []
                - protocol         = "tcp"
                - security_groups  = []
                - self             = false
                - to_port          = 655
                },
                # (2 unchanged elements hidden)
            ]
            name                   = "terraform_ec2_sg"
            tags                   = {
                "Name" = "My_terraform_sg"
            }
            # (7 unchanged attributes hidden)
        }

    Unless you have made equivalent changes to your configuration, or ignored the relevant attributes using ignore_changes, the following plan 
    may include actions to undo or respond to these changes.

    ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── 

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols: 
    + create

    Terraform will perform the following actions:

    # aws_security_group_rule.rule_2 will be created
    + resource "aws_security_group_rule" "rule_2" {
        + cidr_blocks              = [
            + "172.0.0.0/8",
            ]
        + from_port                = 0
        + id                       = (known after apply)
        + protocol                 = "tcp"
        + security_group_id        = "sg-0d9e64c972a40e07a"
        + self                     = false
        + source_security_group_id = (known after apply)
        + to_port                  = 655
        + type                     = "ingress"
        }

    Plan: 1 to add, 0 to change, 0 to destroy.

    ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── 

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

* To apply these rules (on AWS), execute below command
    ```console
    terraform apply “tfplan.binary”
    ```
    Verify the changes are getting reflected on AWS.



# Python library for testing Orchestration APIs
`Developed using Python 3.8.0 and requests 2.20.1`

## TOC
<!-- TABLE OF CONTENTS -->
* [About The Project](#about-the-project)
* [Setup](#setup)
* [Configuration](#configuration)
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

## Configuration
__Required Fields__ - Make sure we must provide below fields in `application.properties`:
* __host__: Pointing to firemon FMOS box.
* __username__: Username that would be used to create the API connection to firemon.
* __password__: Password for the given user.
* __verify_ssl__: Enabled by default. If we are running demo/test environment, good chance we'll need to set this one to `false`.
* __AWS_device_id__: AWS Device Id from firemon FMOS box.
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

