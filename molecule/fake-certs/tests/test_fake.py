#!/usr/bin/env python

import os
import stat
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_if_fake_certs_is_created(host):
    assert host.file('/etc/letsencrypt/live/fakedomain.com/cert.pem').exists
