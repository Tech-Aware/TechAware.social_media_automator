# .github/scripts/generate_changelog.py
import subprocess
import re
from datetime import datetime
from collections import defaultdict

CATEGORIES = {
    'feat': 'Added',
    'fix': 'Fixed',
    'docs': 'Documentation',
    'chore': 'Maintenance',
    'refactor': 'Changed',
    'test': 'Testing',
    'style': 'Style',
    'perf': 'Performance',
    'ci': 'CI',
    'build': 'Build',
    'revert': 'Reverted',
    'remove': 'Removed'
}


def get_git_commits():
    try:
        # Get all commits with their full messages
        result = subprocess.run(
            ['git', 'log', '--pretty=format:%H%n%ad%n%s%n%b%n==END==', '--date=format:%Y-%m-%d'],
            capture_output=True,
            text=True,
            check=True
        )
        commits = result.stdout.split('==END==\n')
        return [c for c in commits if c.strip()]
    except subprocess.CalledProcessError as e:
        print(f"Error getting git commits: {e}")
        return []


def parse_commit(commit_str):
    lines = commit_str.strip().split('\n')
    if len(lines) < 3:
        return None

    hash_id = lines[0]
    date = lines[1]
    subject = lines[2]

    # Parse conventional commit format
    match = re.match(r'^(\w+)(?:\(([^)]+)\))?: (.+)$', subject)
    if not match:
        return None

    type_, scope, message = match.groups()

    return {
        'hash': hash_id,
        'date': date,
        'type': type_,
        'scope': scope,
        'message': message,
        'body': '\n'.join(lines[3:]) if len(lines) > 3 else ''
    }


def categorize_commits(commits):
    versions = defaultdict(lambda: defaultdict(list))
    current_version = "Unreleased"
    current_date = datetime.now().strftime('%Y-%m-%d')

    for commit_str in commits:
        commit = parse_commit(commit_str)
        if not commit:
            continue

        # Check for version tags
        if commit['type'] == 'release':
            match = re.search(r'v?(\d+\.\d+\.\d+)', commit['message'])
            if match:
                current_version = match.group(1)
                current_date = commit['date']
            continue

        category = CATEGORIES.get(commit['type'], 'Other')
        entry = {
            'message': commit['message'],
            'hash': commit['hash'][:8],
            'scope': commit['scope']
        }

        versions[current_version][category].append(entry)

    return versions, current_date


def generate_changelog(versions, current_date):
    output = ["# Changelog\n"]
    output.append("All notable changes to this project will be documented in this file.\n")

    for version, categories in versions.items():
        version_header = "## [Unreleased]" if version == "Unreleased" else f"## [{version}] - {current_date}"
        output.append(f"\n{version_header}\n")

        for category in sorted(categories.keys()):
            if not categories[category]:
                continue

            output.append(f"\n### {category}\n")
            for entry in categories[category]:
                scope_text = f"({entry['scope']}) " if entry['scope'] else ""
                output.append(f"- {scope_text}{entry['message']} ({entry['hash']})")

    return '\n'.join(output)


def main():
    commits = get_git_commits()
    versions, current_date = categorize_commits(commits)
    changelog = generate_changelog(versions, current_date)

    with open('CHANGELOG.md', 'w') as f:
        f.write(changelog)


if __name__ == '__main__':
    main()