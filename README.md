# Nextcloud Exporter for Prometheus
This tool is a Nextcloud exporter to display server information in [Prometheus](https://prometheus.io/).

The exporter is currently implemented so that it runs as an independent Docker container. But you can also run the Gunicorn Service directly as a service on a server.

## Usage
Before the Docker Container can be started, the credentials must first be entered in the .env file.

If you have a working Docker installation, you can simply start the exporter with the following command:
```bash
docker-compose up -d --build
```
The metrics can then be reached under `[IP of Docker Host]:8000/metrics`

## Metrics
The following metrics are available:
- Nextcloud version (nextcloud_version_info)
- Memory total (nextcloud_memory_total_kibibytes)
- Memory free (nextcloud_memory_free_kibibytes)
- Swap total (nextcloud_swap_total_kibibytes)
- Swap free (nextcloud_swap_free_kibibytes)
- Number of App updates available (nextcloud_app_updates_available_total)
- Database size (nextcloud_db_size_bytes)
- Active users last 1 hour (nextcloud_active_users_1h_total)
- CPU load (nextcloud_cpu_load_total)
- Free disk space (nextcloud_free_space_bytes)
- Number of all shares (nextcloud_shares_total)

## Other Informations

### .env File
The following information must be entered in the .env file:
- Nextcloud Status API URL
- A Nextcloud user with Admin permissions
- The password for the Nextcloud user

```plain
NC_URL=<Nextcloud Status API URL>
NC_USER=<Nextcloud User with Admin permissions>
NC_PASS=<Password>
```

### Nextcloud Status API URL
The URL for the Status API can be found under Settings -> System.

The URL should look something like this:
```plain
https://example.com/ocs/v2.php/apps/serverinfo/api/v1/info
```
**It is important to append `?format=json` to the URL, otherwise it won't work.**