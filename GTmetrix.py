import requests

API_KEY = "<apikey>"
BASE_URL = "https://gtmetrix.com/api/2.0"

# Function to initiate a test and return the test ID
def initiate_test(url):
    endpoint = f"{BASE_URL}/tests"
    headers = {"Authorization": f"Basic {API_KEY}", "Content-Type": "application/vnd.api+json"}
    payload = {
        "data": {
            "type": "test",
            "attributes": {
                "url": url,
                "location": "5",   # Replace with the desired location ID
                "browser": "3",    # Replace with the desired browser ID
                "adblock": 1,
                "report": "lighthouse,legacy"
            }
        }
    }
    response = requests.post(endpoint, headers=headers, json=payload)
    response_data = response.json()
    test_id = response_data["data"]["id"]
    return test_id

# Function to get the test status
def get_test_status(test_id):
    endpoint = f"{BASE_URL}/tests/{test_id}"
    headers = {"Authorization": f"Basic {API_KEY}"}
    response = requests.get(endpoint, headers=headers)
    response_data = response.json()
    test_state = response_data["data"]["attributes"]["state"]
    return test_state

# Function to fetch the report
def fetch_report(report_id, output_file):
    endpoint = f"{BASE_URL}/reports/{report_id}/resources/report.pdf?full=1"
    headers = {"Authorization": f"Basic {API_KEY}"}
    response = requests.get(endpoint, headers=headers)
    with open(output_file, "wb") as f:
        f.write(response.content)

# List of URLs to be tested
urls_to_test = [
    "www.abc.com",
    "www.example.com",
    "www.xyz.com"
]

# Initiating the tests for all URLs
test_ids = []
for url in urls_to_test:
    test_id = initiate_test(url)
    test_ids.append(test_id)
    print(f"Test initiated for {url}. Test ID: {test_id}")

# Wait for all tests to complete (you can use a loop with get_test_status function)
# For demonstration purposes, we assume all tests are already completed.
test_statuses = ["completed", "completed", "completed"]

# Fetch the reports for completed tests
for i, test_status in enumerate(test_statuses):
    if test_status == "completed":
        report_id = "QOrraenj"  # Replace this with the actual report ID from the get_test_status response
        report_file = f"report_{i+1}.pdf"  # Replace with the desired output file name
        fetch_report(report_id, report_file)
        print(f"Report downloaded for Test {i+1}.")
