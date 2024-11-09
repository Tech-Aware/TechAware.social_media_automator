def determine_version_increment(commit_type):
    """
    Determine which version number to increment based on commit type.
    Returns: 'major', 'minor', 'patch', or None
    """
    if commit_type == 'break' or 'BREAKING CHANGE' in commit_type:
        return 'major'
    elif commit_type in ['feat', 'feature']:
        return 'minor'
    elif commit_type in ['fix', 'bugfix', 'perf', 'refactor']:
        return 'patch'
    return None


def increment_version(current_version, increment_type):
    """
    Increment the version number according to semver rules.
    """
    if not increment_type:
        return current_version

    major, minor, patch = map(int, current_version.split('.'))

    if increment_type == 'major':
        return f"{major + 1}.0.0"
    elif increment_type == 'minor':
        return f"{major}.{minor + 1}.0"
    elif increment_type == 'patch':
        return f"{major}.{minor}.{patch + 1}"

    return current_version


def categorize_commits(commits):
    versions = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    version_dates = {}
    current_version = "0.1.0"  # Starting version

    # Sort commits by date, oldest first
    sorted_commits = sorted(commits, key=lambda x: parse_commit(x)['date'] if parse_commit(x) else '')

    for commit_str in sorted_commits:
        commit = parse_commit(commit_str)
        if not commit:
            continue

        # Determine if this commit should trigger a version increment
        increment_type = determine_version_increment(commit['type'])
        if increment_type:
            current_version = increment_version(current_version, increment_type)

        # Use today's date for unreleased commits
        today = datetime.now().strftime('%Y-%m-%d')
        if commit['date'] >= today:
            version = "Unreleased"
        else:
            version = current_version

        # Store the date for each version
        if version not in version_dates or commit['date'] < version_dates[version]:
            version_dates[version] = commit['date']

        category = CATEGORIES.get(commit['type'], 'Other')
        feature_group = commit['feature_group']

        entry = {
            'message': commit['message'],
            'hash': commit['hash'][:8],
            'scope': commit['scope'],
            'is_breaking': 'BREAKING CHANGE' in commit.get('body', '')
        }

        versions[version][category][feature_group].append(entry)

    return versions, version_dates