import nmap

def scan_host(target):
    scanner = nmap.PortScanner()
    results = []

    try:
        # Scan com detecção de serviços (-sV equivalente)
        scanner.scan(target, '1-1000', arguments='-sV')

        for host in scanner.all_hosts():
            host_info = {
                "host": host,
                "hostname": scanner[host].hostname(),
                "state": scanner[host].state(),
                "protocols": []
            }

            for proto in scanner[host].all_protocols():
                ports = []
                lport = sorted(scanner[host][proto].keys())
                for port in lport:
                    port_info = scanner[host][proto][port]
                    ports.append({
                        "port": port,
                        "state": port_info['state'],
                        "service": port_info['name']
                    })

                host_info["protocols"].append({
                    "protocol": proto,
                    "ports": ports
                })

            results.append(host_info)

    except Exception as e:
        results.append({"error": str(e)})

    return results
