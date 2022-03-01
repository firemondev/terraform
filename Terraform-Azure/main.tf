resource "azurerm_resource_group" "terraform_rg" {
  name     = "terraformResourceGroup"
  location = "eastus"
}

resource "azurerm_network_security_group" "terraform_sg" {
  name                = "TerraformSecurityGroup"
  location            = azurerm_resource_group.terraform_rg.location
  resource_group_name = azurerm_resource_group.terraform_rg.name

  tags = {
    environment = "dev"
  }
}

resource "azurerm_network_security_rule" "rule_1" {
  name                        = "inbound_sgrule_1"
  priority                    = 100
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "0"
  destination_port_range      = "20"
  source_address_prefix       = "192.8.0.0/16"
  destination_address_prefix  = "0.0.0.0/0"
  resource_group_name         = azurerm_resource_group.terraform_rg.name
  network_security_group_name = azurerm_network_security_group.terraform_sg.name
}

resource "azurerm_network_security_rule" "rule_2" {
  name                        = "inbound_sgrule_2"
  priority                    = 101
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "0"
  destination_port_range      = "28"
  source_address_prefix       = "172.8.0.0/16"
  destination_address_prefix  = "0.0.0.0/0"
  resource_group_name         = azurerm_resource_group.terraform_rg.name
  network_security_group_name = azurerm_network_security_group.terraform_sg.name
}

