import subprocess
import re
from datetime import datetime, timedelta
from collections import defaultdict

# Définition des catégories principales
CATEGORIES = {
    'feat': 'Added',
    'fix': 'Fixed',
    'docs': 'Documentation',
    'refactor': 'Changed',
    'perf': 'Performance',
    'test': 'Testing'
}

# Groupes de fonctionnalités pour une meilleure organisation
FEATURE_GROUPS = {
    'prompting': 'Prompting System Integration',
    'content': 'Content Generation',
    'facebook': 'Facebook Integration',
    'linkedin': 'LinkedIn Integration',
    'testing': 'Testing Infrastructure',
    'core': 'Core Infrastructure',
    'api': 'API Integration',
    'cli': 'CLI Improvements'
}

# Version mapping basé sur les dates
VERSION_MAPPING = [
    (datetime(2024, 10, 12), "0.1.0", "Initial release"),
    (datetime(2024, 10, 19), "0.2.0", "LinkedIn integration"),
    (datetime(2024, 10, 26), "0.3.0", "Facebook integration"),
    (datetime(2024, 11, 9), "1.0.0", "Prompting system and content generation")
]


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


def get_version_for_date(commit_date):
    """Determine version based on commit date"""
    commit_datetime = datetime.strptime(commit_date, '%Y-%m-%d')

    # Pour les commits d'aujourd'hui
    if commit_datetime.date() == datetime.now().date():
        return "Unreleased"

    # Parcours des versions dans l'ordre chronologique inverse
    for date, version, _ in reversed(VERSION_MAPPING):
        if commit_datetime >= date:
            return version

    return VERSION_MAPPING[0][1]  # Version par défaut (0.1.0)


def determine_feature_group(scope, message):
    """Détermine le groupe de fonctionnalités pour un commit"""
    if scope:
        for key in FEATURE_GROUPS:
            if key in scope.lower():
                return key

    for key in FEATURE_GROUPS:
        if key in message.lower():
            return key

    return 'core'


def parse_commit(commit_str):
    """Parse un commit et extrait les informations pertinentes"""
    lines = commit_str.strip().split('\n')
    if len(lines) < 3:
        return None

    hash_id = lines[0]
    date = lines[1]
    subject = lines[2]

    match = re.match(r'^(\w+)(?:\(([^)]+)\))?: (.+)$', subject)
    if not match:
        type_, scope, message = 'other', None, subject
    else:
        type_, scope, message = match.groups()

    feature_group = determine_feature_group(scope, message)

    return {
        'hash': hash_id,
        'date': date,
        'type': type_,
        'scope': scope,
        'message': message.strip(),
        'feature_group': feature_group,
        'body': '\n'.join(lines[3:]) if len(lines) > 3 else ''
    }


def clean_message(message):
    """Nettoie et formate un message de commit"""
    # Supprime les préfixes communs
    message = re.sub(r'^(feat|fix|docs|style|refactor|test|chore|perf|ci|build|revert|remove)(\([^)]+\))?: ', '',
                     message)

    # Capitalise la première lettre
    if message and message[0].islower():
        message = message[0].upper() + message[1:]

    # Supprime les points à la fin
    message = message.rstrip('.')

    return message


def organize_commits(commits):
    """Organise les commits par version, catégorie et groupe de fonctionnalités"""
    organized = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    version_dates = {}

    for commit_str in commits:
        commit = parse_commit(commit_str)
        if not commit:
            continue

        version = get_version_for_date(commit['date'])
        category = CATEGORIES.get(commit['type'], 'Other')
        feature_group = commit['feature_group']

        # Stocke la date la plus ancienne pour chaque version
        if version not in version_dates or commit['date'] < version_dates[version]:
            version_dates[version] = commit['date']

        # Clean and format the commit message
        message = clean_message(commit['message'])

        if message:  # Ignore empty messages
            organized[version][category][feature_group].append(message)

    return organized, version_dates


def version_key(version):
    """Helper function to properly sort versions"""
    if version == "Unreleased":
        return float('inf'), float('inf'), float('inf')
    try:
        return tuple(map(int, version.split('.')))
    except (AttributeError, ValueError):
        return 0, 0, 0

def generate_changelog(organized_commits, version_dates):
    """Génère le contenu du changelog"""
    output = ["# Changelog\n\n"]

    # Sort versions in reverse order (newest first), using the version_key function
    versions = sorted(organized_commits.keys(),
                     key=version_key,
                     reverse=True)

    for version in versions:
        categories = organized_commits[version]
        if not categories:
            continue

        # Add version header
        if version == "Unreleased":
            output.append(f"## [{version}]\n")
        else:
            date = version_dates.get(version, "")
            output.append(f"## [{version}] - {date}\n")

        # Add categories and their entries
        for category in sorted(categories.keys()):
            if not categories[category]:
                continue

            output.append(f"### {category}\n")
            feature_groups = categories[category]

            for group, messages in feature_groups.items():
                if not messages:
                    continue

                if len(feature_groups) > 1:  # Only add subheader if there are multiple groups
                    output.append(f"#### {FEATURE_GROUPS[group]}\n")

                for message in sorted(set(messages)):  # Remove duplicates
                    output.append(f"- {message}\n")

                output.append("")

        output.append("")

    # Add notes section
    output.extend([
        "### Notes\n",
        "- All dates are in YYYY-MM-DD format\n",
        "- Version numbers follow semantic versioning\n",
        "- Commits organized by feature and functionality\n",
        "- Each version builds upon previous functionality\n"
    ])

    return ''.join(output)


def main():
    print("Fetching git commits...")
    commits = get_git_commits()

    print("Organizing commits...")
    organized_commits, version_dates = organize_commits(commits)

    print("Generating changelog...")
    changelog = generate_changelog(organized_commits, version_dates)

    print("Writing changelog to file...")
    with open('CHANGELOG.md', 'w', encoding='utf-8') as f:
        f.write(changelog)

    print("Changelog generation complete!")


if __name__ == '__main__':
    main()