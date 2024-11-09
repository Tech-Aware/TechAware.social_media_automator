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

# Group related features under these major categories
FEATURE_GROUPS = {
    'prompting': 'Prompting System Integration',
    'scraping': 'Scraping & Content Integration',
    'use_cases': 'Use Cases Enhancement',
    'blog': 'Blog Article Integration',
    'facebook': 'Facebook Integration',
    'linkedin': 'LinkedIn Integration',
    'test': 'Testing Infrastructure',
    'core': 'Core Functionality'
}


def get_git_commits():
    try:
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


def determine_feature_group(scope, message):
    if not scope:
        # Try to determine from message content
        for key, _ in FEATURE_GROUPS.items():
            if key in message.lower():
                return key
        return 'core'

    for key in FEATURE_GROUPS.keys():
        if key in scope.lower():
            return key
    return 'core'


def parse_commit(commit_str):
    lines = commit_str.strip().split('\n')
    if len(lines) < 3:
        return None

    hash_id = lines[0]
    date = lines[1]
    subject = lines[2]

    match = re.match(r'^(\w+)(?:\(([^)]+)\))?: (.+)$', subject)
    if not match:
        return None

    type_, scope, message = match.groups()
    feature_group = determine_feature_group(scope, message)

    return {
        'hash': hash_id,
        'date': date,
        'type': type_,
        'scope': scope,
        'message': message,
        'body': '\n'.join(lines[3:]) if len(lines) > 3 else '',
        'feature_group': feature_group
    }


def categorize_commits(commits):
    versions = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    current_version = "1.0.0"  # Set initial version
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
        feature_group = commit['feature_group']

        entry = {
            'message': commit['message'],
            'hash': commit['hash'][:8],
            'scope': commit['scope']
        }

        versions[current_version][category][feature_group].append(entry)

    return versions, current_date


def format_message(entry):
    """Format the commit message for better readability."""
    message = entry['message']
    # Capitalize first letter if it's not already
    if message and message[0].islower():
        message = message[0].upper() + message[1:]
    # Remove trailing periods
    message = message.rstrip('.')
    return message


def generate_changelog(versions, current_date):
    output = ["# Changelog\n"]

    for version, categories in versions.items():
        version_header = f"## [{version}] - {current_date}\n"
        output.append(version_header)

        for category in sorted(categories.keys()):
            if not categories[category]:
                continue

            output.append(f"### {category}\n")

            # Group by feature
            for feature_group, entries in categories[category].items():
                if not entries:
                    continue

                if feature_group in FEATURE_GROUPS:
                    output.append(f"#### {FEATURE_GROUPS[feature_group]}\n")

                for entry in entries:
                    message = format_message(entry)
                    output.append(f"- {message}\n")

            output.append("")  # Add blank line between categories

        output.append("")  # Add blank line between versions

    # Add footer
    output.extend([
        "### Notes\n",
        "- All dates are in YYYY-MM-DD format\n",
        "- Version numbers follow semantic versioning\n",
        "- Commits organized by feature and functionality\n",
        "- Each version builds upon previous functionality\n"
    ])

    return ''.join(output)


def main():
    commits = get_git_commits()
    versions, current_date = categorize_commits(commits)
    changelog = generate_changelog(versions, current_date)

    with open('CHANGELOG.md', 'w') as f:
        f.write(changelog)


if __name__ == '__main__':
    main()