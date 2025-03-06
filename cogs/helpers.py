import subprocess

def get_public_ip():
    try:
        # Run ipconfig and use findstr to search for IPv6 address
        result = subprocess.run(['ipconfig'], capture_output=True, text=True)

        # Check if successful
        if result.returncode != 0:
            return "Error: Failed to execute ipconfig command"
        
        # Find the line containing IPv6 address
        ipv6_line = None
        for line in result.stdout.splitlines():
            if "IPv6 Address" in line:
                ipv6_line = line
                break

        if ipv6_line:
            ip_address = ipv6_line.replace("IPv6 Address. . . . . . . . . . . : ", "")
            return ip_address
        else:
            return "IPv6 address not found"
        
    except Exception as e:
        return f"Error retrieving IP address: {e}"