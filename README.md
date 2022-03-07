Terraform
=========

- Website: https://www.terraform.io
- Forums: [HashiCorp Discuss](https://discuss.hashicorp.com/c/terraform-core)
- Documentation: [https://www.terraform.io/docs/](https://www.terraform.io/docs/)
- Tutorials: [HashiCorp's Learn Platform](https://learn.hashicorp.com/terraform)
- Certification Exam: [HashiCorp Certified: Terraform Associate](https://www.hashicorp.com/certification/#hashicorp-certified-terraform-associate)
- README Terraform Integration with AWS : [AWS-README](README_AWS_INTEGRATION.md)
- README Terraform Integration with Azure : [AZURE-README](README_AZURE_INTEGRATION.md)

Terraform is a tool for building, changing, and versioning infrastructure safely and efficiently. Terraform can manage existing and popular service providers as well as custom in-house solutions.

Getting Started & Documentation
-------------------------------
Documentation is available on the [Terraform website](https://www.terraform.io):
  - [Intro](https://www.terraform.io/intro/index.html)
  - [Docs](https://www.terraform.io/docs/index.html)

If you're new to Terraform and want to get started creating infrastructure, please check out our [Getting Started guides](https://learn.hashicorp.com/terraform#getting-started) on HashiCorp's learning platform. There are also [additional guides](https://learn.hashicorp.com/terraform#operations-and-development) to continue your learning.

Show off your Terraform knowledge by passing a certification exam. Visit the [certification page](https://www.hashicorp.com/certification/) for information about exams and find [study materials](https://learn.hashicorp.com/terraform/certification/terraform-associate) on HashiCorp's learning platform.


## Use-Case of Terraform Integrations with Cloud:
* User has provision to add, modify and delete the security rules from terraform and we just want to make sure that the rules are compliant or not before committing these rules on cloud infrastructure.
* When any rule gets modified or added then Terraform will detect those changes and generate a plan out of it which is stored in `tfplan.json`, which gets extracted in Python Integration as per the requirement and performs compliance check on those rules or requirements using Firemon's compliance check API.
* If compliance check passes, user can deploy/apply these changes on cloud.
* Otherwise, user need to update the requirements and follow the whole process again.

## Available Integrations with Cloud
1. __Terraform Integration with AWS__ : Click [here](README_AWS_INTEGRATION.md) to visit README for Terraform Integration with AWS.
2. __Terraform Integration with Azure__: Click [here](README_AWS_INTEGRATION.md) to visit README for Terraform Integration for Azure.

## License
MIT. 
See the full license [here](LICENSE).
