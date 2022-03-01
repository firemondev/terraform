""" To call Orchestration API """
import json
import sys

import requests
from urllib3.exceptions import InsecureRequestWarning

from authentication_api import Authentication
from build_rule_rec_payload_azure import build_rule_rec_payload_azure
from build_rule_rec_payload_aws import build_rule_rec_payload_aws
from retrieve_config_data import get_properties_data

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

filtered_rules = []
parser = get_properties_data()


class OrchestrationApis():
    """ Adding code for calling orchestration APIs """

    def __init__(self, host, username, password, verify_ssl):
        """ User needs to pass host,username,password,and verify_ssl as parameters while
        creating instance of this class and internally Authentication class instance
        will be created which will set authentication token in the header to get fireMon API access """
        self.api_instance = Authentication(host, username, password, verify_ssl)
        self.headers = self.api_instance.get_auth_token()
        self.host = host
        self.verify_ssl = verify_ssl

    def rule_rec_api(self, params, domain_id, rule_rec_payload):
        """ Calling orchestration RULE-REC API by passing json data as request body, headers, params and domainId
            which returns list of rule recommendations for given input as a response"""
        if rule_rec_payload is None:
            print("Requirement should not be empty")
            return
        print(f"\nGenerated RULE-REC request payload:\n {rule_rec_payload}")
        rule_rec_url = parser.get('REST', 'rule_rec_api_url').format(self.host, domain_id)
        try:
            rule_rec_response = requests.post(url=rule_rec_url,
                                              headers=self.headers, params=params, json=rule_rec_payload,
                                              verify=self.verify_ssl)
            if 'deviceChanges' not in rule_rec_response.json():
                return
            list_of_device_changes = rule_rec_response.json()['deviceChanges']
            if len(list_of_device_changes) == 0:
                print("No matching rule found for this requirement, Please go back and update the requirement")
                return
            for i in range(len(list_of_device_changes)):
                list_of_rule_changes = list_of_device_changes[i]["ruleChanges"]
                for j in range(len(list_of_rule_changes)):
                    if list_of_rule_changes[j]['action'] != 'NONE':
                        filtered_rules.append(list_of_rule_changes[j])

                if filtered_rules is None:
                    return "No Rules Needs to be changed!"
            return rule_rec_response.json()
        except requests.exceptions.HTTPError as e:
            print("Exception occurred while getting rule recommendation \n Exception : {0}".
                  format(e.response.text))

    def pca_api(self, domain_id, device_id, rule_rec_response_payload):
        """ Calling orchestration pca api by passing json data as request body, headers, deviceId and domainId
            which returns you pre-change assessments for the given device """

        final_result = []
        print("\n\nCalling PCA API : ")
        pca_url = parser.get('REST', 'pca_api_url').format(self.host, domain_id, device_id)
        if len(filtered_rules) == 0:
            print("No rule present!\n")
            return
        try:
            result = requests.post(url=pca_url,
                                   headers=self.headers, json=rule_rec_response_payload, verify=self.verify_ssl)
            final_result.append(result.json())

            if len(result.json()['pcaResult']['preChangeAssessmentControls']) == 0:
                print("Pre-Compliance check passed, OK to apply terraform changes.\n")
                final_output = json.dumps(final_result)
                with open("final_result.json", "w") as f:
                    f.writelines(final_output)
                final = json.dumps(filtered_rules)
                with open("rule_rec_response_new.json", "w") as f:
                    f.writelines(final)
                return

            for control in result.json()['pcaResult']['preChangeAssessmentControls']:
                if control['type'] == "FAIL":
                    print("Pre-Compliance check failed, look into final result in result.json for more "
                          "details!\n")
                    final_output = json.dumps(final_result)
                    with open("final_result.json", "w") as f:
                        f.writelines(final_output)
                    final = json.dumps(filtered_rules)
                    with open("rule_rec_response_new.json", "w") as f:
                        f.writelines(final)
                    return final_output

        except requests.exceptions.HTTPError as e:
            print("Exception occurred while getting pre change assessment \n Exception : {0}".
                  format(e.response.text))


# Creating instance of this class and calling orchestration api methods
def get_parameters_for_rule_rec(cloud_device_id):
    return {'deviceId': cloud_device_id, 'addressMatchingStrategy': 'INTERSECTS', 'modifyBehavior': 'MODIFY',
            'strategy': None}


# User should update host, username, password, verify_ssl as per FMOS Instance
# OrchestrationApis(host, username, password, verify_ssl)
orchestration = OrchestrationApis(parser.get('CREDENTIALS', 'host'), parser.get('CREDENTIALS', 'username'),
                                  parser.get('CREDENTIALS', 'password'), parser.get('CREDENTIALS', 'verify_ssl'))


def call_to_rule_rec_and_pca(list_of_rule_rec_payloads, cloud_device_id):
    if len(list_of_rule_rec_payloads) != 0:
        for rule_rec_payload in list_of_rule_rec_payloads:
            orchestration.rule_rec_api(get_parameters_for_rule_rec(cloud_device_id), 1, rule_rec_payload)
        orchestration.pca_api(1, cloud_device_id, filtered_rules)
    else:
        print("Rule rec payload is empty, Please add at least one requirement")


def get_cloud_provider(file_path):
    with open(file_path, "r", encoding=parser.get('CREDENTIALS', 'encoding'), errors="ignore") as f:
        parsed_data = json.load(f)
    if "aws" in parsed_data['configuration']['provider_config']:
        return "aws"
    elif "azurerm" in parsed_data['configuration']['provider_config']:
        return "azure"
    else:
        return "none"


cloud_provider = get_cloud_provider(sys.argv[1])
print(cloud_provider)

if "aws" == cloud_provider:
    list_of_payloads = build_rule_rec_payload_aws(sys.argv[1])
    cloud_device_id = parser.get('CREDENTIALS', 'aws_device_id')
if "azure" == cloud_provider:
    list_of_payloads = build_rule_rec_payload_azure(sys.argv[1])
    cloud_device_id = parser.get('CREDENTIALS', 'azure_device_id')

call_to_rule_rec_and_pca(list_of_payloads, cloud_device_id)
