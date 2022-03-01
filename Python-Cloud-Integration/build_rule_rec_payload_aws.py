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


def get_payload_action(payload, action):
    if action == "delete":
        payload[-1]['action'] = "DROP"
    else:
        payload[-1]['action'] = "ACCEPT"


def add_source_destination_service_to_payload_from_sg(payload, change):
    sources = []
    destinations = []
    services = []

    if "ingress" in change['after']:
        for ingress in change['after']['ingress']:
            for j in ingress['cidr_blocks']:
                if j not in sources:
                    sources.append(j)

            if ingress['protocol'] not in services:
                if ingress['protocol'] == '-1' and ingress['protocol'] != 'Any':
                    services.append('Any')
                else:
                    to_port = str(ingress['to_port'])
                    if ingress['protocol'] + "/" + to_port not in services:
                        services.append(ingress['protocol'] + "/" + to_port)

    if "egress" in change['after']:
        for egress in change['after']['egress']:
            for j in egress['cidr_blocks']:
                if j not in destinations:
                    destinations.append(j)

        if len(services) == 0:
            if egress['protocol'] not in services:
                if egress['protocol'] == '-1' and egress['protocol'] != 'Any':
                    services.append('Any')
                else:
                    to_port = str(egress['to_port'])
                    if egress['protocol'] + "/" + to_port not in services:
                        services.append(egress['protocol'] + "/" + to_port)

    if len(sources) == 0:
        payload['sources'] = ["Any"]
    else:
        payload['sources'] = sources
    if len(destinations) == 0:
        payload['destinations'] = ["Any"]
    else:
        payload['destinations'] = destinations
    payload['services'] = services


def add_source_destination_service_to_payload_from_sg_rule(payload, change):
    sources = []
    destinations = []
    services = []

    for ip in change['after']['cidr_blocks']:
        if change['after']['type'] == "ingress":
            if ip not in sources:
                sources.append(ip)
        else:
            if ip not in destinations:
                destinations.append(ip)

    if change['after']['protocol'] not in services:
        if change['after']['protocol'] == '-1' and change['after']['protocol'] != 'Any':
            services.append('Any')
        else:
            to_port = str(change['after']['to_port'])
            if change['after']['protocol'] + "/" + to_port not in services:
                services.append(change['after']['protocol'] + "/" + to_port)

    if len(sources) == 0:
        payload['sources'] = ["Any"]
    else:
        payload['sources'] = sources
    if len(destinations) == 0:
        payload['destinations'] = ["Any"]
    else:
        payload['destinations'] = destinations
    payload['services'] = services


def add_source_destination_service_to_payload_from_sg_rule_before(payload, change):
    sources = []
    destinations = []
    services = []

    for ip in change['before']['cidr_blocks']:
        if change['before']['type'] == "ingress":
            if ip not in sources:
                sources.append(ip)
        else:
            if ip not in destinations:
                destinations.append(ip)

    if change['before']['protocol'] not in services:
        if change['before']['protocol'] == '-1' and change['before']['protocol'] != 'Any':
            services.append('Any')
        else:
            to_port = str(change['before']['to_port'])
            if change['before']['protocol'] + "/" + to_port not in services:
                services.append(change['before']['protocol'] + "/" + to_port)

    if len(sources) == 0:
        payload['sources'] = ["Any"]
    else:
        payload['sources'] = sources
    if len(destinations) == 0:
        payload['destinations'] = ["Any"]
    else:
        payload['destinations'] = destinations
    payload['services'] = services


def build_rule_rec_payload_aws(file_path):
    parsed_json = parse_json_file(file_path)

    payload = []
    for resource_change in parsed_json['resource_changes']:
        # if resource_change['change']['after'] is not None:
        payload.append(get_rule_rec_payload())
        if resource_change['type'] == "aws_security_group":
            if len(resource_change['change']['actions']) == 1:
                # action is incorrect break from loop
                if resource_change['change']['actions'][0].lower() == "no-op":
                    payload.pop()
                    continue
                get_payload_action(payload, resource_change['change']['actions'][0].lower())
                add_source_destination_service_to_payload_from_sg(payload[-1], resource_change['change'])
                if ("Any" in payload[-1]['sources']) and ("Any" in payload[-1]['sources']) and (
                        "Any" in payload[-1]['destinations']):
                    payload.pop()
        elif resource_change['type'] == "aws_security_group_rule":
            # contains only after results
            if len(resource_change['change']['actions']) == 1:
                # action is incorrect break from loop
                if resource_change['change']['actions'][0].lower() == "no-op":
                    payload.pop()
                    continue
                get_payload_action(payload, resource_change['change']['actions'][0].lower())
                if payload[-1]['action'] == 'ACCEPT':
                    add_source_destination_service_to_payload_from_sg_rule(payload[-1], resource_change['change'])
                else:
                    add_source_destination_service_to_payload_from_sg_rule_before(payload[-1],
                                                                                  resource_change['change'])
            elif len(resource_change['change']['actions']) > 1:
                # call before
                if resource_change['change']['actions'][0].lower() == "no-op":
                    payload.pop()
                    continue
                    # action is DROP
                get_payload_action(payload, resource_change['change']['actions'][0].lower())
                add_source_destination_service_to_payload_from_sg_rule_before(payload[-1], resource_change['change'])

                # call after
                payload.append(get_rule_rec_payload())
                if resource_change['change']['actions'][0].lower() == "no-op":
                    payload.pop()
                    continue
                    # action is DROP
                get_payload_action(payload, resource_change['change']['actions'][1].lower())
                add_source_destination_service_to_payload_from_sg_rule(payload[-1], resource_change['change'])

        else:
            payload.pop()
    return payload
