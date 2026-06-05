## University Server Constraints

- Available TAPs: `tap62` to `tap69`
- Max RAM per VM: 32 GB
- No GPU access
- AI inference will run on MacBook Pro M3 Pro 18 GB

## VM Autostart

The lab VMs are configured to start automatically when the university type 2
hypervisor restarts, for example after maintenance or package updates. This
minimizes downtime and restores the router, monitoring, and management VMs
without waiting for a manual startup.

Crontab entry on the hypervisor:

```cron
@reboot /home/amirmahdighasemi/masters/scripts/lab-startup.py /home/amirmahdighasemi/vm/network-security-lab/vms-startup.yaml >> /home/amirmahdighasemi/lab-startup.log 2>&1
```

Startup output is appended to `/home/amirmahdighasemi/lab-startup.log` so
post-reboot startup issues can be checked later.
