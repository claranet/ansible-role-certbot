# Ansible role - certbot
[![Maintainer](https://img.shields.io/badge/maintained%20by-claranet-e00000?style=flat-square)](https://www.claranet.fr/)
[![License](https://img.shields.io/github/license/claranet/ansible-role-certbot?style=flat-square)](LICENSE)
[![Release](https://img.shields.io/github/v/release/claranet/ansible-role-certbot?style=flat-square)](https://github.com/claranet/ansible-role-certbot/releases)
[![Status](https://img.shields.io/github/workflow/status/claranet/ansible-role-certbot/Ansible%20Molecule?style=flat-square&label=tests)](https://github.com/claranet/ansible-role-certbot/actions?query=workflow%3A%22Ansible+Molecule%22)
[![Ansible version](https://img.shields.io/badge/ansible-%3E%3D2.10-black.svg?style=flat-square&logo=ansible)](https://github.com/ansible/ansible)
[![Ansible Galaxy](https://img.shields.io/badge/ansible-galaxy-black.svg?style=flat-square&logo=ansible)](https://galaxy.ansible.com/claranet/certbot)


> :star: Star us on GitHub — it motivates us a lot!

Install and manage certbot

## :warning: Requirements

Ansible >= 2.10

## :zap: Installation

```bash
ansible-galaxy install claranet.certbot
```

## :gear: Role variables

Variable | Default value | Description
---------|---------------|------------
certbot_packages                          | **['certbot', 'python3-pip']**     | Package name
certbot_webroot                           | **/var/www/letsencrypt**           | Directory for http challenges
certbot_auto_renew                        | **true**                           | Enable certificate renew
certbot_auto_renew_user                   | **root**                           | User to configure certificate renew
certbot_auto_renew_hour                   | **3**                              | Cron job hour for renew
certbot_auto_renew_minute                 | **30**                             | Cron job minutes for renew
certbot_auto_renew_option                 | **--quiet --no-self-upgrade**      | Options for renew command
certbot_certs                             | **[]**                             | See defaults/main.yml for details
certbot_staging_enabled                   | **true**                           | Use letsencrypt staging
certbot_create_command                    | **certbot certonly --webroot ...** | See defaults/main.yml for details
certbot_plugins                           | **[]**                             | List of plugins to install using pip
certbot_plugins_pip_executable            | **pip3**                           | pip executable to use to install certbot plugins
certbot_reload_services_before_enabled    | **true**                           | Reload `certbot_reload_services` before configuring certbot
certbot_reload_services_after_enabled     | **true**                           | Reload `certbot_reload_services` after configuring certbot
certbot_reload_services                   | **[]**                             | List of services to reload

## :arrows_counterclockwise: Dependencies

N/A

## HTTP-01 Challenge

:warning: To use HTTP-01 challenge, you have to only use webroot plugin (default behavior)

Before using this challenge type, your server must have a public IP and a DNS record zone pointing to it.

### Webserver Setup

Before configuring certbot to issue a certificate, you must setup your webserver in order to handle certbot http challenges.

#### Apache2

```bash
Alias /.well-known/acme-challenge/ "/var/www/letsencrypt/.well-known/acme-challenge/"
<Directory "/var/www/letsencrypt">
    AllowOverride None
    Options MultiViews Indexes SymLinksIfOwnerMatch IncludesNoExec
    Require all granted
</Directory>
```

```yaml
certbot_certs:
    - email: "test@clara.net"
        certbot_webroot: "/var/www/letsencrypt"
        domains:
        - "lamp-01.clara.net"
        - "lamp-02.clara.net"
certbot_reload_services:
    - apache2
```

#### Nginx

```
location /.well-known/acme-challenge/ {
    root /var/www/letsencrypt/.well-known/acme-challenge/;
}
```

```yaml
certbot_certs:
    - email: "test@clara.net"
        certbot_webroot: "/var/www/letsencrypt"
        domains:
        - "lamp-01.clara.net"
        - "lamp-02.clara.net"
certbot_reload_services:
    - nginx
```

## DNS-01 Challenge

:warning: For wildcard certificate, you have to use `--cert-name` option like this to avoid creating a new certificate for each ansible run :

```
--cert-name "{{ cert_item.domains | first | regex_replace('^\*\.(.*)$'
```

### Route53 example

```yaml
certbot_certs:
- email: "test@clara.net"
    domains:
    - "*.molecule.clara.net"
- email: "test@clara.net"
    domains:
    - "lamp-01.clara.net"
    - "lamp-02.clara.net"

certbot_reload_services:
    - nginx

certbot_create_command: >-
    certbot certonly --dns-route53
    {{ '--staging --break-my-certs' if certbot_staging_enabled else '' }}
    --noninteractive --agree-tos
    --email {{ cert_item.email | default(certbot_admin_email) }}
    --cert-name "{{ cert_item.domains | first | regex_replace('^\*\.(.*)$', 'wildcard.\1') }}"
    --expand
    -d {{ cert_item.domains | join(',') }}

certbot_plugins:
    - certbot-dns-route53==1.22.0
```

## :pencil2: Example Playbook

```yaml
---
- hosts: all
  roles:
    - claranet.certbot
```

## :closed_lock_with_key: [Hardening](HARDENING.md)

## :heart_eyes_cat: [Contributing](CONTRIBUTING.md)

## :copyright: [License](LICENSE)

[Mozilla Public License Version 2.0](https://www.mozilla.org/en-US/MPL/2.0/)
