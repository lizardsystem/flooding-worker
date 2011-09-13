#!/usr/bin/python
# (c) Nelen & Schuurmans.  GPL licensed.

CONNECT_SETTINGS = {
    #"BROKER_HOST": "10.100.155.150",
    "BROKER_HOST": "localhost",
    "BROKER_PORT": 5672,
    "BROKER_USER": "admin",
    "BROKER_PASSWORD": "kikker123",
    "BROKER_VHOST": "/"
}

QUEUES = {
    "default": {
        "exchange": "",
        "binding_key": "default" },
    "logging": {
        "exchange": "router",
        "binding_key": "logging" },
    "120": {
        "exchange": "router",
        "binding_key": "120" },
    "130": {
        "exchange": "router",
        "binding_key": "130" },
    "132": {
        "exchange": "router",
        "binding_key": "132" },
    "160": {
        "exchange": "router",
        "binding_key": "160" },
}
