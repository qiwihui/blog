import requests
import markdown
import os

# Set your GitHub repository details
GITHUB_REPO = "qiwihui/blog"
GITHUB_TOKEN = ""  # Replace with your GitHub personal access token

# Set up API URL
base_url = f"https://api.github.com/repos/{GITHUB_REPO}/issues"

# Define headers with the authorization token
headers = {"Authorization": f"token {GITHUB_TOKEN}"}

page = 0
count = 0
all_issues = []


def get_labels(issue):
    labels = [l["name"] for l in issue["labels"]]
    return labels


while count is not None:
    page += 1

    url = base_url + f"?page={page}"
    print(url)

    # Send the request to GitHub API
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        issues = response.json()

        # Create a directory to store the markdown files if it doesn't exist
        output_dir = "src/blogs"
        os.makedirs(output_dir, exist_ok=True)

        all_issues += issues
        for issue in issues:
            if "TODO" in get_labels(issue):
                continue
            # Only export issues, not pull requests
            if "pull_request" not in issue:
                # Create a filename based on the issue number and title
                file_title = issue["title"].replace(" ", "_").replace("/", "-")
                filename = f"qiwihui-blog-{issue['number']}.md"

                # Create the full path for the file
                file_path = os.path.join(output_dir, filename)

                # Write the issue details to the markdown file
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(f"# {issue['title']}\n")
                    file.write(f"\n\n")
                    file.write(f"{issue['body']}\n\n")
                    file.write(f"[View on GitHub]({issue['html_url']})\n")
                    file.write("\n\n")
        print(f"Exported {len(issues)} issues to {output_dir} directory.")
        if len(issues) != 30:
            count = None
        # break
    else:
        print(f"Failed to retrieve issues: {response.status_code} - {response.text}")
        count = None


summary_file = "src/SUMMARY.md"
with open(summary_file, "w", encoding="utf-8") as file:
    file.write(f"# Summary\n")
    file.write(f"\n")
    file.write(f"[About Me](./README.md)\n")
    for issue in all_issues:
        if "TODO" in get_labels(issue):
            continue
        file.write(f"[{issue['title']}](./blogs/qiwihui-blog-{issue['number']}.md)\n")
    file.write("\n")
