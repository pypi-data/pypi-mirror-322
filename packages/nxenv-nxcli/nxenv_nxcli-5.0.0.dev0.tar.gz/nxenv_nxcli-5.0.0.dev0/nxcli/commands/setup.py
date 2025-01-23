# imports - standard imports
import os
import sys

# imports - third party imports
import click

# imports - module imports
from nxcli.utils import exec_cmd, run_playbook, which
from nxcli.utils.cli import SugaredOption


@click.group(help="Setup command group for enabling setting up a Nxenv environment")
def setup():
	pass


@click.command(
	"sudoers", help="Add commands to sudoers list for execution without password"
)
@click.argument("user")
def setup_sudoers(user):
	from nxcli.utils.system import setup_sudoers

	setup_sudoers(user)


@click.command("nginx", help="Generate configuration files for NGINX")
@click.option(
	"--logging", default="combined", type=click.Choice(["none", "site", "combined"])
)
@click.option(
	"--log_format",
	help="Specify the log_format for nginx. Use none or '' to not set a value.",
	only_if_set=["logging"],
	cls=SugaredOption,
	default="main",
)
@click.option(
	"--yes", help="Yes to regeneration of nginx config file", default=False, is_flag=True
)
def setup_nginx(yes=False, logging="combined", log_format=None):
	from nxcli.config.nginx import make_nginx_conf

	make_nginx_conf(nxcli_path=".", yes=yes, logging=logging, log_format=log_format)


@click.command("reload-nginx", help="Checks NGINX config file and reloads service")
def reload_nginx():
	from nxcli.config.production_setup import reload_nginx

	reload_nginx()


@click.command("supervisor", help="Generate configuration for supervisor")
@click.option("--user", help="optional user argument")
@click.option(
	"--yes", help="Yes to regeneration of supervisor config", is_flag=True, default=False
)
@click.option(
	"--skip-redis", help="Skip redis configuration", is_flag=True, default=False
)
@click.option(
	"--skip-supervisord",
	help="Skip supervisord configuration",
	is_flag=True,
	default=False,
)
def setup_supervisor(user=None, yes=False, skip_redis=False, skip_supervisord=False):
	from nxcli.utils import get_cmd_output
	from nxcli.config.supervisor import (
		check_supervisord_config,
		generate_supervisor_config,
	)

	if which("supervisorctl") is None:
		click.secho("Please install `supervisor` to proceed", fg="red")
		sys.exit(1)

	if not skip_supervisord and "Permission denied" in get_cmd_output(
		"supervisorctl status"
	):
		check_supervisord_config(user=user)

	generate_supervisor_config(nxcli_path=".", user=user, yes=yes, skip_redis=skip_redis)


@click.command("redis", help="Generates configuration for Redis")
def setup_redis():
	from nxcli.config.redis import generate_config

	generate_config(".")


@click.command("fonts", help="Add Nxenv fonts to system")
def setup_fonts():
	from nxcli.utils.system import setup_fonts

	setup_fonts()


@click.command(
	"production", help="Setup Nxenv production environment for specific user"
)
@click.argument("user")
@click.option("--yes", help="Yes to regeneration config", is_flag=True, default=False)
def setup_production(user, yes=False):
	from nxcli.config.production_setup import setup_production

	setup_production(user=user, yes=yes)


@click.command("backups", help="Add cronjob for nxcli backups")
def setup_backups():
	from nxcli.nxcli import Nxcli

	Nxcli(".").setup.backups()


@click.command("env", help="Setup Python environment for nxcli")
@click.option(
	"--python", type=str, default="python3", help="Path to Python Executable."
)
def setup_env(python="python3"):
	from nxcli.nxcli import Nxcli

	return Nxcli(".").setup.env(python=python)


@click.command("firewall", help="Setup firewall for system")
@click.option("--ssh_port")
@click.option("--force")
def setup_firewall(ssh_port=None, force=False):
	if not force:
		click.confirm(
			f"Setting up the firewall will block all ports except 80, 443 and {ssh_port}\nDo you want to continue?",
			abort=True,
		)

	if not ssh_port:
		ssh_port = 22

	run_playbook("roles/nxcli/tasks/setup_firewall.yml", {"ssh_port": ssh_port})


@click.command("ssh-port", help="Set SSH Port for system")
@click.argument("port")
@click.option("--force")
def set_ssh_port(port, force=False):
	if not force:
		click.confirm(
			f"This will change your SSH Port to {port}\nDo you want to continue?", abort=True
		)

	run_playbook("roles/nxcli/tasks/change_ssh_port.yml", {"ssh_port": port})


@click.command("lets-encrypt", help="Setup lets-encrypt SSL for site")
@click.argument("site")
@click.option("--custom-domain")
@click.option(
	"-n",
	"--non-interactive",
	default=False,
	is_flag=True,
	help="Run command non-interactively. This flag restarts nginx and runs certbot non interactively. Shouldn't be used on 1'st attempt",
)
def setup_letsencrypt(site, custom_domain, non_interactive):
	from nxcli.config.lets_encrypt import setup_letsencrypt

	setup_letsencrypt(site, custom_domain, nxcli_path=".", interactive=not non_interactive)


@click.command(
	"wildcard-ssl", help="Setup wildcard SSL certificate for multi-tenant nxcli"
)
@click.argument("domain")
@click.option("--email")
@click.option(
	"--exclude-base-domain",
	default=False,
	is_flag=True,
	help="SSL Certificate not applicable for base domain",
)
def setup_wildcard_ssl(domain, email, exclude_base_domain):
	from nxcli.config.lets_encrypt import setup_wildcard_ssl

	setup_wildcard_ssl(
		domain, email, nxcli_path=".", exclude_base_domain=exclude_base_domain
	)


@click.command("procfile", help="Generate Procfile for nxcli start")
def setup_procfile():
	from nxcli.config.procfile import setup_procfile

	setup_procfile(".")


@click.command(
	"socketio", help="[DEPRECATED] Setup node dependencies for socketio server"
)
def setup_socketio():
	return


@click.command("requirements")
@click.option("--node", help="Update only Node packages", default=False, is_flag=True)
@click.option(
	"--python", help="Update only Python packages", default=False, is_flag=True
)
@click.option(
	"--dev",
	help="Install optional python development dependencies",
	default=False,
	is_flag=True,
)
@click.argument("apps", nargs=-1)
def setup_requirements(node=False, python=False, dev=False, apps=None):
	"""
	Setup Python and Node dependencies.

	You can optionally specify one or more apps to setup dependencies for.
	"""
	from nxcli.nxcli import Nxcli

	nxcli = Nxcli(".")

	if not (node or python or dev):
		nxcli.setup.requirements(apps=apps)

	elif not node and not dev:
		nxcli.setup.python(apps=apps)

	elif not python and not dev:
		nxcli.setup.node(apps=apps)

	else:
		from nxcli.utils.nxcli import install_python_dev_dependencies

		install_python_dev_dependencies(apps=apps)

		if node:
			click.secho(
				"--dev flag only supports python dependencies. All node development dependencies are installed by default.",
				fg="yellow",
			)


@click.command(
	"manager",
	help="Setup nxcli-manager.local site with the nxcli_manager app installed on it",
)
@click.option(
	"--yes", help="Yes to regeneration of nginx config file", default=False, is_flag=True
)
@click.option(
	"--port", help="Port on which you want to run nxcli manager", default=23624
)
@click.option("--domain", help="Domain on which you want to run nxcli manager")
def setup_manager(yes=False, port=23624, domain=None):
	from nxcli.nxcli import Nxcli
	from nxcli.config.nginx import make_nxcli_manager_nginx_conf

	create_new_site = True

	if "nxcli-manager.local" in os.listdir("sites"):
		create_new_site = click.confirm("Site already exists. Overwrite existing site?")

	if create_new_site:
		exec_cmd("nxcli new-site --force nxcli-manager.local")

	if "nxcli_manager" in os.listdir("apps"):
		print("App already exists. Skipping app download.")
	else:
		exec_cmd("nxcli get-app nxcli_manager")

	exec_cmd("nxcli --site nxcli-manager.local install-app nxcli_manager")

	nxcli_path = "."
	nxcli = Nxcli(nxcli_path)

	if nxcli.conf.get("restart_supervisor_on_update") or nxcli.conf.get(
		"restart_systemd_on_update"
	):
		# implicates a production setup or so I presume
		if not domain:
			print(
				"Please specify the site name on which you want to host nxcli-manager using the 'domain' flag"
			)
			sys.exit(1)

		if domain not in nxcli.sites:
			raise Exception("No such site")

		make_nxcli_manager_nginx_conf(nxcli_path, yes=yes, port=port, domain=domain)


@click.command("config", help="Generate or over-write sites/common_site_config.json")
def setup_config():
	from nxcli.config.common_site_config import setup_config

	setup_config(".")


@click.command("add-domain", help="Add a custom domain to a particular site")
@click.argument("domain")
@click.option("--site", prompt=True)
@click.option("--ssl-certificate", help="Absolute path to SSL Certificate")
@click.option("--ssl-certificate-key", help="Absolute path to SSL Certificate Key")
def add_domain(domain, site=None, ssl_certificate=None, ssl_certificate_key=None):
	"""Add custom domain to site"""
	if not site:
		print("Please specify site")
		sys.exit(1)

	from nxcli.config.site_config import add_domain

	add_domain(site, domain, ssl_certificate, ssl_certificate_key, nxcli_path=".")


@click.command("remove-domain", help="Remove custom domain from a site")
@click.argument("domain")
@click.option("--site", prompt=True)
def remove_domain(domain, site=None):
	if not site:
		print("Please specify site")
		sys.exit(1)

	from nxcli.config.site_config import remove_domain

	remove_domain(site, domain, nxcli_path=".")


@click.command(
	"sync-domains",
	help="Check if there is a change in domains. If yes, updates the domains list.",
)
@click.option("--domain", multiple=True)
@click.option("--site", prompt=True)
def sync_domains(domain=None, site=None):
	if not site:
		print("Please specify site")
		sys.exit(1)

	try:
		domains = list(map(str, domain))
	except Exception:
		print("Domains should be a json list of strings or dictionaries")
		sys.exit(1)

	from nxcli.config.site_config import sync_domains

	changed = sync_domains(site, domains, nxcli_path=".")

	# if changed, success, else failure
	sys.exit(0 if changed else 1)


@click.command("role", help="Install dependencies via ansible roles")
@click.argument("role")
@click.option("--admin_emails", default="")
@click.option("--mysql_root_password", "--mariadb_root_password")
@click.option("--container", is_flag=True, default=False)
def setup_roles(role, **kwargs):
	extra_vars = {"production": True}
	extra_vars.update(kwargs)

	if role:
		run_playbook("site.yml", extra_vars=extra_vars, tag=role)
	else:
		run_playbook("site.yml", extra_vars=extra_vars)


@click.command(
	"fail2ban",
	help="Setup fail2ban, an intrusion prevention software framework that protects computer servers from brute-force attacks",
)
@click.option(
	"--maxretry",
	default=6,
	help="Number of matches (i.e. value of the counter) which triggers ban action on the IP. Default is 6 seconds",
)
@click.option(
	"--bantime",
	default=600,
	help="Duration (in seconds) for IP to be banned for. Negative number for 'permanent' ban. Default is 600 seconds",
)
@click.option(
	"--findtime",
	default=600,
	help="The counter is set to zero if match found within 'findtime' seconds doesn't exceed 'maxretry'. Default is 600 seconds",
)
def setup_nginx_proxy_jail(**kwargs):
	run_playbook("roles/fail2ban/tasks/configure_nginx_jail.yml", extra_vars=kwargs)


@click.command("systemd", help="Generate configuration for systemd")
@click.option("--user", help="Optional user argument")
@click.option(
	"--yes",
	help="Yes to regeneration of systemd config files",
	is_flag=True,
	default=False,
)
@click.option("--stop", help="Stop nxcli services", is_flag=True, default=False)
@click.option("--create-symlinks", help="Create Symlinks", is_flag=True, default=False)
@click.option("--delete-symlinks", help="Delete Symlinks", is_flag=True, default=False)
def setup_systemd(
	user=None, yes=False, stop=False, create_symlinks=False, delete_symlinks=False
):
	from nxcli.config.systemd import generate_systemd_config

	generate_systemd_config(
		nxcli_path=".",
		user=user,
		yes=yes,
		stop=stop,
		create_symlinks=create_symlinks,
		delete_symlinks=delete_symlinks,
	)


setup.add_command(setup_sudoers)
setup.add_command(setup_nginx)
setup.add_command(reload_nginx)
setup.add_command(setup_supervisor)
setup.add_command(setup_redis)
setup.add_command(setup_letsencrypt)
setup.add_command(setup_wildcard_ssl)
setup.add_command(setup_production)
setup.add_command(setup_backups)
setup.add_command(setup_env)
setup.add_command(setup_procfile)
setup.add_command(setup_socketio)
setup.add_command(setup_requirements)
setup.add_command(setup_manager)
setup.add_command(setup_config)
setup.add_command(setup_fonts)
setup.add_command(add_domain)
setup.add_command(remove_domain)
setup.add_command(sync_domains)
setup.add_command(setup_firewall)
setup.add_command(set_ssh_port)
setup.add_command(setup_roles)
setup.add_command(setup_nginx_proxy_jail)
setup.add_command(setup_systemd)
