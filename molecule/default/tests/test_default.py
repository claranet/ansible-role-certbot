#!/usr/bin/env python

import os
import stat
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_certbot_is_installed(host):
    assert host.package('certbot').is_installed

def test_cerbot_is_working(host):
    command = host.run("certbot --version")
    assert command.rc == 0

def test_certbot_cron(host):
    with host.sudo():
        cron = host.check_output("crontab -l")
        assert "certbot renew" in cron
