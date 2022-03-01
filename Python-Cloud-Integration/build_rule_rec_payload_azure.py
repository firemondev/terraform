from retrieve_config_data import get_properties_data
import json


def get_rule_rec_payload():
    return {
        "apps": [],
        "destinations": [
            ""
        ],
        "services": [
            ""
        ],
        "sources": [
            ""
        ],
        "users": [],
        "requirementType": "RULE",
        "childKey": "add_access",
        "variables": {
            "expiration": "null",
            "review": "null"
        },
        "action": ""
    }


def parse_json_file(file_path):
    with open(file_path, "r", encoding=get_properties_data().get('CREDENTIALS', 'encoding'),
              errors="ignore") as f:
        data = json.load(f)
        return data


def extract_security_rules(rule, sources, destinations, services):
    sources.append(rule['source_address_prefix'] if rule['source_address_prefix'] != "*" else "Any")
    port_source = rule['source_port_range']
    destinations.append(rule['destination_address_prefix'] if rule['destination_address_prefix'] != "*" else "Any")
    port_destination = rule['destination_port_range']

    # both is present
    if port_source not in ["0", "*"] and port_destination not in ["*", "0"]:
        protocol = rule['protocol'].lower() + "/" + port_source + "-" + port_destination
    # source is present
    elif port_source not in ["0", "*"] and port_destination in ["0", "*"]:
        protocol = rule['protocol'].lower() + "/" + port_source
    # destination is present
    elif port_source in ["0", "*"] and port_destination not in ["0", "*"]:
        protocol = rule['protocol'].lower() + "/" + port_destination
    # both is absent
    else:
        protocol = rule['protocol'].lower()

    if protocol not in services:
        services.append(protocol)


def add_source_destination_service_to_payload_from_sg_rule_before(payload, before):
    sources = []
    destinations = []
    services = []

    extract_security_rules(before, sources, destinations, services)

    payload['sources'] = ["Any"] if len(sources) == 0 else sources
    payload['destinations'] = ["Any"] if len(destinations) == 0 else destinations
    payload['services'] = ["Any"] if len(services) == 0 else services


def add_source_destination_service_to_payload_from_sg_rule_after(payload, after):
    sources = []
    destinations = []
    services = []

    extract_security_rules(after, sources, destinations, services)

    payload['sources'] = ["Any"] if len(sources) == 0 else sources
    payload['destinations'] = ["Any"] if len(destinations) == 0 else destinations
    payload['services'] = ["Any"] if len(services) == 0 else services


def delete_generic_rules_from_payload(payloads):
    for index in range(len(payloads) - 1, -1, -1):
        if (("Any" in payloads[index]['sources']) and ("Any" in payloads[index]['services']) and (
                "Any" in payloads[index]['destinations'])) \
                or (("" in payloads[index]['sources']) and ("" in payloads[index]['services']) and (
                "" in payloads[index]['destinations'])) \
                or (("*" in payloads[index]['sources']) and ("*" in payloads[index]['services']) and (
                "*" in payloads[index]['destinations'])) \
                or "" == payloads[index]['action']:
            del payloads[index]


def build_rule_rec_payload_azure(file_path):
    parsed_json = parse_json_file(file_path)

    payload = []
    if 'resource_changes' not in parsed_json:
        raise Exception("No Resource Changes found!")
        return

    for resource_change in parsed_json['resource_changes']:
        payload.append(get_rule_rec_payload())
        if resource_change['type'] == "azurerm_network_security_rule":
            security_group_action = resource_change['change']['actions'][0].lower()
            if security_group_action == "no-op":
                payload.pop()
                continue

            if security_group_action == 'create' or security_group_action == "update":
                payload[-1]['action'] = 'ACCEPT'
                add_source_destination_service_to_payload_from_sg_rule_after(payload[-1],
                                                                             resource_change['change']['after'])
            if security_group_action == 'delete':
                payload[-1]['action'] = 'DROP'
                add_source_destination_service_to_payload_from_sg_rule_before(payload[-1],
                                                                              resource_change['change']['before'])
            # dropping existing rules
            if security_group_action == "update":
                payload.append(get_rule_rec_payload())
                payload[-1]['action'] = "DROP"
                add_source_destination_service_to_payload_from_sg_rule_before(payload[-1],
                                                                              resource_change['change']['before'])

        else:
            payload.pop()

    delete_generic_rules_from_payload(payload)
    return payload
