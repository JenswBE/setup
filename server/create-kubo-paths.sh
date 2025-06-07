set -eu

cp "tasks/hosts/kubo.yml" "tasks/hosts/kubo-$1.yml"

touch "vars/public/kubo-$1.yml"
touch "vars/secret-templates/kubo-$1.yml"

mkdir -p "templates/hosts/kubo-$1/etc/systemd/system"
cp -r "templates/hosts/kubo/etc/systemd/system/crowdsec-firewall-bouncer.service.d" "templates/hosts/kubo-$1/etc/systemd/system/"
cp -r templates/hosts/kubo/etc/systemd/system/docker-update* "templates/hosts/kubo-$1/etc/systemd/system/"

mkdir -p "templates/hosts/kubo-$1/home/_user_/deploy"
cat <<'EOF' >> "templates/hosts/kubo-$1/home/_user_/deploy/docker-compose.yml"
#VAR:ansible_managed | comment:VAR#

#################################################################
#                            DEFAULTS                           #
#################################################################

x-defaults: &defaults
  x-dummy: ""
  # Putting the anchor in this file ensures it's a valid YAML file for Renovate Bot
  #VAR:lookup('ansible.builtin.file', 'files/docker-compose-defaults.yml',) | indent(width=2):VAR#
EOF
