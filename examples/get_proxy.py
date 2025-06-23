import requests
import os

def get_and_set_selenium_proxy_for_github_actions():
    """
    Scrapes a list of SOCKS5 proxies from a public URL, selects the first one,
    and prints a GitHub Actions command to set an environment variable
    'SELENIUM_PROXY' with the chosen proxy.

    This function is designed to be run within a GitHub Actions workflow.
    The output will be captured by GitHub Actions and used to set the
    environment variable for subsequent steps.
    """
    proxy_list_url = "https://cdn.jsdelivr.net/gh/proxifly/free-proxy-list@main/proxies/protocols/socks5/data.txt"
    proxy_env_var_name = "SELENIUM_PROXY"

    print(f"Attempting to fetch SOCKS5 proxies from: {proxy_list_url}")

    try:
        response = requests.get(proxy_list_url, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

        proxies = [line.strip() for line in response.text.splitlines() if line.strip()]

        if not proxies:
            print("No proxies found in the list. Cannot set SELENIUM_PROXY.")
            return

        # For simplicity, we'll use the first proxy found.
        # In a real-world scenario, you might want to implement proxy testing
        # to ensure it's functional before using it.
        selected_proxy_ip_port = proxies[0]
        proxy_string = selected_proxy_ip_port

        # GitHub Actions special command to set an environment variable for subsequent steps
        # This will write "SELENIUM_PROXY=socks5://IP_ADDRESS:PORT" to the GITHUB_ENV file
        # which GitHub Actions automatically reads.
        github_env_path = os.getenv('GITHUB_ENV')
        if github_env_path:
            with open(github_env_path, 'a') as env_file:
                env_file.write(f"{proxy_env_var_name}={proxy_string}\n")
            print(f"Successfully set {proxy_env_var_name} to {proxy_string} for GitHub Actions.")
            print(f"To use this in a subsequent step, refer to it as ${{ env.{proxy_env_var_name} }}")
        else:
            # Fallback for local testing or if GITHUB_ENV is not set (not in GHA context)
            print(f"GITHUB_ENV environment variable not found. Setting {proxy_env_var_name} locally (for demonstration):")
            os.environ[proxy_env_var_name] = proxy_string
            print(f"Set {proxy_env_var_name}={os.environ[proxy_env_var_name]}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching proxies: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    get_and_set_selenium_proxy_for_github_actions()
