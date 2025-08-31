import requests
from datetime import datetime, UTC
from dateutil.relativedelta import relativedelta
import os
import time

print("=== Starting SVG Generation Script ===")
print(f"Current working directory: {os.getcwd()}")
print(f"Files in current directory: {os.listdir('.')}")

BIRTHDATE = datetime(2011, 11, 14, tzinfo=UTC)
USERNAME = "KadenDaya"
LIGHT_TEMPLATE = "template_light_mode.svg"
DARK_TEMPLATE = "template_dark_mode.svg"
LIGHT_OUTPUT = "light_mode.svg"
DARK_OUTPUT = "dark_mode.svg"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN environment variable not set.")

print(f"Template files to look for:")
print(f"  Light: {LIGHT_TEMPLATE} (exists: {os.path.exists(LIGHT_TEMPLATE)})")
print(f"  Dark: {DARK_TEMPLATE} (exists: {os.path.exists(DARK_TEMPLATE)})")
print(f"GitHub token available: {'Yes' if GITHUB_TOKEN else 'No'}")


def Calc_Age():
    print("Calculating age...")
    now = datetime.now(UTC)
    delta = relativedelta(now, BIRTHDATE)
    years = delta.years
    months = delta.months
    days = delta.days
    age_result = [f"{years:02d}", f"{months:02d}", f"{days:02d}"]
    print(f"Age calculated: {years} years, {months} months, {days} days")
    return age_result


def fetch_stats():
    print("Fetching GitHub stats...")
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

    print("Getting user data...")
    user_data = requests.get(f"https://api.github.com/users/{USERNAME}", headers=headers).json()
    followers = user_data.get("followers", 0)
    print(f"Followers: {followers}")

    print("Fetching repositories...")
    repos = []
    page = 1
    max_pages = 100

    while page <= max_pages:
        print(f"  Fetching page {page}...")
        res = requests.get(f"https://api.github.com/users/{USERNAME}/repos?per_page=100&page={page}", headers=headers)
        if res.status_code != 200:
            print(f"  ERROR: API returned status {res.status_code}")
            print(f"  Response: {res.text[:200]}...")
            break

        page_repos = res.json()
        if not page_repos:
            print(f"  No more repos on page {page} - stopping")
            break

        if page == 1:
            print(f"  Response headers: {dict(res.headers)}")
            print(f"  First repo sample: {page_repos[0] if page_repos else 'None'}")

        repos.extend(page_repos)
        print(f"  Found {len(page_repos)} repos on page {page}")
        if len(page_repos) < 100:
            break
        page += 1

    print(f"Total repositories found: {len(repos)}")

    stars = sum(repo.get("stargazers_count", 0) for repo in repos)
    own_repo_count = len(repos)
    print(f"Own repos: {own_repo_count}, Total stars: {stars}")

    contributed_repo_count = sum(1 for repo in repos if repo.get("owner", {}).get("login") != USERNAME)
    print(f"Contributed repos: {contributed_repo_count}")

    print("Calculating commit statistics...")
    total_commits = 0
    total_additions = 0
    total_deletions = 0

    for i, repo in enumerate(repos):
        name = repo.get("name")
        owner = repo.get("owner", {}).get("login")
        if not name or not owner:
            continue

        print(f"  Processing repo {i+1}/{len(repos)}: {owner}/{name}")
        stats_url = f"https://api.github.com/repos/{owner}/{name}/stats/contributors"

        for attempt in range(3):
            stats_res = requests.get(stats_url, headers=headers)
            if stats_res.status_code == 202:
                print("    GitHub is generating stats (202). Waiting 15s and retrying...")
                time.sleep(15)
                continue
            elif stats_res.status_code != 200:
                print(f"    ERROR: Status {stats_res.status_code} for {name}, skipping.")
                break
            else:
                stats_data = stats_res.json()
                if isinstance(stats_data, list):
                    for contributor in stats_data:
                        if contributor.get("author", {}).get("login") == USERNAME:
                            repo_commits = contributor.get("total", 0)
                            total_commits += repo_commits
                            print(f"    Found {repo_commits} commits for {USERNAME}")
                            for week in contributor.get("weeks", []):
                                total_additions += week.get("a", 0)
                                total_deletions += week.get("d", 0)
                break  # success or error — stop retrying

    lines = total_additions - total_deletions
    print(f"Final stats - Commits: {total_commits}, Lines: {lines} (+{total_additions}, -{total_deletions})")

    stats_result = [f'{own_repo_count:02}', f'{contributed_repo_count}', f'{stars:03}', f'{total_commits:03}', f'{followers:03}', f'{lines:05}', f'{total_additions:05}', f'{total_deletions:05}']
    return stats_result


def generate_svg():
    print("Starting SVG generation...")
    age = Calc_Age()
    stats = fetch_stats()

    with open(LIGHT_TEMPLATE, "r") as file:
        svg_light = file.read()

    with open(DARK_TEMPLATE, "r") as file:
        svg_dark = file.read()

    svg_light = svg_light.replace("{{YEARS}}", age[0])
    svg_light = svg_light.replace("{{MONTHS}}", age[1])
    svg_light = svg_light.replace("{{DAYS}}", age[2])
    svg_light = svg_light.replace("{{REPOS}}", stats[0])
    svg_light = svg_light.replace("{{CONTRIBUTED}}", stats[1])
    svg_light = svg_light.replace("{{STARS}}", stats[2])
    svg_light = svg_light.replace("{{COMMITS}}", stats[3])
    svg_light = svg_light.replace("{{FOLLOWERS}}", stats[4])
    svg_light = svg_light.replace("{{LINES}}", stats[5])
    svg_light = svg_light.replace("{{PLUS}}", stats[6])
    svg_light = svg_light.replace("{{MINUS}}", stats[7])

    svg_dark = svg_dark.replace("{{YEARS}}", age[0])
    svg_dark = svg_dark.replace("{{MONTHS}}", age[1])
    svg_dark = svg_dark.replace("{{DAYS}}", age[2])
    svg_dark = svg_dark.replace("{{REPOS}}", stats[0])
    svg_dark = svg_dark.replace("{{CONTRIBUTED}}", stats[1])
    svg_dark = svg_dark.replace("{{STARS}}", stats[2])
    svg_dark = svg_dark.replace("{{COMMITS}}", stats[3])
    svg_dark = svg_dark.replace("{{FOLLOWERS}}", stats[4])
    svg_dark = svg_dark.replace("{{LINES}}", stats[5])
    svg_dark = svg_dark.replace("{{PLUS}}", stats[6])
    svg_dark = svg_dark.replace("{{MINUS}}", stats[7])

    with open(LIGHT_OUTPUT, "w") as file:
        file.write(svg_light)

    with open(DARK_OUTPUT, "w") as file:
        file.write(svg_dark)


if __name__ == "__main__":
    generate_svg()
