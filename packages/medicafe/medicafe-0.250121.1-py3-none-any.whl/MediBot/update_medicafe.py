#update_medicafe.py
import subprocess, sys, requests, time, pkg_resources

def get_installed_version(package):
    try:
        process = subprocess.Popen(
            [sys.executable, '-m', 'pip', 'show', package],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            for line in stdout.decode().splitlines():
                if line.startswith("Version:"):
                    return line.split(":", 1)[1].strip()
        return None
    except Exception as e:
        print("Error retrieving installed version: {}".format(e))
        return None

def get_latest_version(package):
    """Fetch the latest version of a package from PyPI with retries."""
    for attempt in range(1, 4):  # 3 attempts
        try:
            response = requests.get("https://pypi.org/pypi/{}/json".format(package), timeout=10)
            response.raise_for_status()
            data = response.json()
            latest_version = data['info']['version']
            print("Latest available version of {}: {}".format(package, latest_version))
            return latest_version
        except requests.RequestException as e:
            print("Attempt {}: Error fetching latest version for {}: {}".format(attempt, package, e))
            if attempt < 3:
                print("Retrying in 2 seconds...")
                time.sleep(2)
    print("Failed to fetch latest version for {} after 3 attempts.".format(package))
    return None

def check_internet_connection():
    try:
        requests.get("http://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

def compare_versions(version1, version2):
    v1_parts = list(map(int, version1.split(".")))
    v2_parts = list(map(int, version2.split(".")))
    return (v1_parts > v2_parts) - (v1_parts < v2_parts)

def upgrade_package(package, retries=3, delay=2):
    """Attempt to upgrade the specified package with retries."""
    for attempt in range(1, retries + 1):
        try:
            print("Attempt {}: Upgrading {}...".format(attempt, package))
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', package, '--no-cache-dir', '-q'])
            print("{} upgraded successfully.".format(package))
            return True
        except subprocess.CalledProcessError as e:
            print("Attempt {}: Failed to upgrade {}: {}".format(attempt, package, e))
            if attempt < retries:
                print("Retrying in {} seconds...".format(delay))
                time.sleep(delay)
    print("Error: All upgrade attempts for {} failed.".format(package))
    return False

def ensure_dependencies(requirements_file='requirements.txt'):
    """Ensure all dependencies listed in the requirements file are installed and up-to-date."""
    try:
        with open(requirements_file, 'r') as f:
            required_packages = f.read().splitlines()
    except IOError as e:
        print("Error reading requirements file '{}': {}".format(requirements_file, e))
        sys.exit(1)

    for pkg in required_packages:
        package_name = pkg.split('==')[0]  # Extract package name without version
        try:
            installed_version = pkg_resources.get_distribution(package_name).version
            latest_version = get_latest_version(package_name)

            if latest_version and installed_version != latest_version:
                print("Current version of {}: {}".format(package_name, installed_version))
                print("Latest version of {}: {}".format(package_name, latest_version))
                if not upgrade_package(package_name):
                    print("Warning: Failed to upgrade {}.".format(package_name))
        except pkg_resources.DistributionNotFound:
            print("Package {} is not installed. Attempting to install...".format(package_name))
            if not upgrade_package(package_name):
                print("Warning: Failed to install {}.".format(package_name))

def main():
    # Ensure internet connection before proceeding
    if not check_internet_connection():
        print("Error: No internet connection. Please check your connection and try again.")
        sys.exit(1)

    # Ensure all dependencies are met before proceeding
    ensure_dependencies()

    # Existing functionality of update_medicafe.py
    package = "medicafe"

    current_version = get_installed_version(package)
    if not current_version:
        print("{} is not installed.".format(package))
        sys.exit(1)

    latest_version = get_latest_version(package)
    if not latest_version:
        print("Could not retrieve the latest version information.")
        sys.exit(1)

    print("Current version of {}: {}".format(package, current_version))
    print("Latest version of {}: {}".format(package, latest_version))

    if compare_versions(latest_version, current_version) > 0:
        print("A newer version is available. Proceeding with upgrade.")
        if upgrade_package(package):
            # Verify upgrade
            time.sleep(3)
            new_version = get_installed_version(package)
            if compare_versions(new_version, latest_version) >= 0:
                print("Upgrade successful. New version: {}".format(new_version))
            else:
                print("Upgrade failed. Current version remains: {}".format(new_version))
                sys.exit(1)
        else:
            sys.exit(1)
    else:
        print("You already have the latest version installed.")

if __name__ == "__main__":
    main()
