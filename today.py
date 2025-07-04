import datetime
from dateutil import relativedelta
import requests
import os
from lxml import etree
import time
import hashlib

# GitHub Personal Access Token
# You'll need to set these environment variables:
# export ACCESS_TOKEN='your_github_token_here'
# export USER_NAME='RaneemQasim5251'
HEADERS = {'authorization': 'token ' + os.environ.get('ACCESS_TOKEN', '')}
USER_NAME = os.environ.get('USER_NAME', 'RaneemQasim5251')
QUERY_COUNT = {'user_getter': 0, 'follower_getter': 0, 'graph_repos_stars': 0, 'recursive_loc': 0, 'graph_commits': 0}

def daily_readme(birthday):
    """
    Returns the length of time since birth
    """
    diff = relativedelta.relativedelta(datetime.datetime.today(), birthday)
    return '{} {}, {} {}, {} {}{}'.format(
        diff.years, 'year' + format_plural(diff.years), 
        diff.months, 'month' + format_plural(diff.months), 
        diff.days, 'day' + format_plural(diff.days),
        ' 🎂' if (diff.months == 0 and diff.days == 0) else '')

def format_plural(unit):
    """Returns 's' if unit != 1, else empty string"""
    return 's' if unit != 1 else ''

def simple_request(func_name, query, variables):
    """Makes a GraphQL request to GitHub API"""
    try:
        request = requests.post('https://api.github.com/graphql', 
                              json={'query': query, 'variables': variables}, 
                              headers=HEADERS)
        if request.status_code == 200:
            return request
        print(f"Error in {func_name}: {request.status_code} - {request.text}")
        return None
    except Exception as e:
        print(f"Request failed: {e}")
        return None

def user_getter(username):
    """Returns the account ID and creation time of the user"""
    query_count('user_getter')
    query = '''
    query($login: String!){
        user(login: $login) {
            id
            createdAt
        }
    }'''
    variables = {'login': username}
    request = simple_request(user_getter.__name__, query, variables)
    if request:
        return {'id': request.json()['data']['user']['id']}, request.json()['data']['user']['createdAt']
    return {'id': 'unknown'}, datetime.datetime.now().isoformat()

def follower_getter(username):
    """Returns the number of followers of the user"""
    query_count('follower_getter')
    query = '''
    query($login: String!){
        user(login: $login) {
            followers {
                totalCount
            }
        }
    }'''
    request = simple_request(follower_getter.__name__, query, {'login': username})
    if request:
        return int(request.json()['data']['user']['followers']['totalCount'])
    return 0

def graph_repos_stars(count_type, owner_affiliation):
    """Returns repository count or star count"""
    query_count('graph_repos_stars')
    query = '''
    query ($owner_affiliation: [RepositoryAffiliation], $login: String!) {
        user(login: $login) {
            repositories(first: 100, ownerAffiliations: $owner_affiliation) {
                totalCount
                edges {
                    node {
                        ... on Repository {
                            nameWithOwner
                            stargazers {
                                totalCount
                            }
                        }
                    }
                }
            }
        }
    }'''
    variables = {'owner_affiliation': owner_affiliation, 'login': USER_NAME}
    request = simple_request(graph_repos_stars.__name__, query, variables)
    if request:
        if count_type == 'repos':
            return request.json()['data']['user']['repositories']['totalCount']
        elif count_type == 'stars':
            return stars_counter(request.json()['data']['user']['repositories']['edges'])
    return 0

def stars_counter(data):
    """Count total stars in repositories owned by me"""
    total_stars = 0
    for node in data: 
        total_stars += node['node']['stargazers']['totalCount']
    return total_stars

def graph_commits():
    """Get total commits from this year"""
    query_count('graph_commits')
    start_date = datetime.datetime(datetime.datetime.now().year, 1, 1).isoformat()
    end_date = datetime.datetime.now().isoformat()
    
    query = '''
    query($start_date: DateTime!, $end_date: DateTime!, $login: String!) {
        user(login: $login) {
            contributionsCollection(from: $start_date, to: $end_date) {
                contributionCalendar {
                    totalContributions
                }
            }
        }
    }'''
    variables = {'start_date': start_date, 'end_date': end_date, 'login': USER_NAME}
    request = simple_request(graph_commits.__name__, query, variables)
    if request:
        return int(request.json()['data']['user']['contributionsCollection']['contributionCalendar']['totalContributions'])
    return 0

def query_count(funct_id):
    """Counts how many times the GitHub GraphQL API is called"""
    global QUERY_COUNT
    QUERY_COUNT[funct_id] += 1

def create_dark_mode_svg(age_data, commit_data, star_data, repo_data, follower_data):
    """Create the dark mode SVG with terminal styling"""
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="900" height="500" viewBox="0 0 900 500">
  <defs>
    <style>
      .terminal-bg {{ fill: #0d1117; }}
      .terminal-text {{ fill: #c9d1d9; font-family: 'Consolas', 'Monaco', monospace; font-size: 14px; }}
      .key {{ fill: #ffd700; }}
      .value {{ fill: #7dd3fc; }}
      .highlight {{ fill: #3fb950; }}
      .comment {{ fill: #8b949e; }}
      .prompt {{ fill: #ffd700; font-weight: bold; }}
    </style>
  </defs>
  
  <!-- Terminal Background -->
  <rect width="900" height="500" class="terminal-bg" rx="12"/>
  
  <!-- Terminal Header -->
  <rect x="0" y="0" width="900" height="30" fill="#161b22" rx="12"/>
  <circle cx="20" cy="15" r="6" fill="#ff5f57"/>
  <circle cx="40" cy="15" r="6" fill="#ffbd2e"/>
  <circle cx="60" cy="15" r="6" fill="#28ca42"/>
  
  <!-- ASCII Art -->
  <text x="50" y="70" class="terminal-text">
    <tspan x="50" y="70">    ┌────────────────────────┐</tspan>
    <tspan x="50" y="90">    │  ●───●───●  NEURAL  │</tspan>
    <tspan x="50" y="110">   │  / \\ / \\ /   NETWORK │</tspan>
    <tspan x="50" y="130">   │ ●───●───●─────────●  │</tspan>
    <tspan x="50" y="150">   │  \\ / \\ / \\       /   │</tspan>
    <tspan x="50" y="170">   │   ●───●───●─────●    │</tspan>
    <tspan x="50" y="190">   │    \\ / \\ / \\   /     │</tspan>
    <tspan x="50" y="210">   │     ●───●───●       │</tspan>
    <tspan x="50" y="230">   │      \\ / \\ /        │</tspan>
    <tspan x="50" y="250">   │       ●───●  AI     │</tspan>
    <tspan x="50" y="270">   └────────────────────────┘</tspan>
  </text>
  
  <!-- Terminal Content -->
  <text x="350" y="70" class="terminal-text">
    <tspan x="350" y="70" class="prompt">raneem@althaqafi</tspan><tspan class="comment"> ~$ whoami</tspan>
    <tspan x="350" y="100" class="comment">└─╼ </tspan><tspan class="key">name:</tspan> <tspan class="value">Raneem Althaqafi</tspan>
    <tspan x="350" y="120" class="comment">└─╼ </tspan><tspan class="key">role:</tspan> <tspan class="value">AI Engineer &amp; Researcher</tspan>
    <tspan x="350" y="140" class="comment">└─╼ </tspan><tspan class="key">age:</tspan> <tspan class="value">{age_data}</tspan>
    <tspan x="350" y="160" class="comment">└─╼ </tspan><tspan class="key">location:</tspan> <tspan class="value">Riyadh, Saudi Arabia</tspan>
    
    <tspan x="350" y="190" class="prompt">raneem@althaqafi</tspan><tspan class="comment"> ~$ cat achievements.txt</tspan>
    <tspan x="350" y="210" class="comment">└─╼ </tspan><tspan class="highlight">🏆 World Champion:</tspan> <tspan class="value">Space Debris Detection (1st/495)</tspan>
    <tspan x="350" y="230" class="comment">└─╼ </tspan><tspan class="highlight">🤖 AI Innovation:</tspan> <tspan class="value">Arabic Metro Assistant (Siraj)</tspan>
    <tspan x="350" y="250" class="comment">└─╼ </tspan><tspan class="highlight">💓 Research:</tspan> <tspan class="value">rPPG Heartbeat Detection (94%)</tspan>
    <tspan x="350" y="270" class="comment">└─╼ </tspan><tspan class="highlight">🇸🇦 Impact:</tspan> <tspan class="value">Vision 2030 Contributor</tspan>
    
    <tspan x="350" y="300" class="prompt">raneem@althaqafi</tspan><tspan class="comment"> ~$ git status</tspan>
    <tspan x="350" y="320" class="comment">└─╼ </tspan><tspan class="key">repositories:</tspan> <tspan class="value">{repo_data}</tspan>
    <tspan x="350" y="340" class="comment">└─╼ </tspan><tspan class="key">stars_earned:</tspan> <tspan class="value">{star_data}</tspan>
    <tspan x="350" y="360" class="comment">└─╼ </tspan><tspan class="key">commits_2025:</tspan> <tspan class="value">{commit_data}</tspan>
    <tspan x="350" y="380" class="comment">└─╼ </tspan><tspan class="key">followers:</tspan> <tspan class="value">{follower_data}</tspan>
    
    <tspan x="350" y="410" class="prompt">raneem@althaqafi</tspan><tspan class="comment"> ~$ echo "motto"</tspan>
    <tspan x="350" y="430" class="comment">└─╼ </tspan><tspan class="value">"Building the future of AI, one neural network at a time"</tspan>
    
    <tspan x="350" y="460" class="prompt">raneem@althaqafi</tspan><tspan class="comment"> ~$ </tspan><tspan class="highlight">█</tspan>
  </text>
</svg>'''
    return svg_content

def create_light_mode_svg(age_data, commit_data, star_data, repo_data, follower_data):
    """Create the light mode SVG with terminal styling"""
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="900" height="500" viewBox="0 0 900 500">
  <defs>
    <style>
      .terminal-bg {{ fill: #ffffff; }}
      .terminal-text {{ fill: #24292f; font-family: 'Consolas', 'Monaco', monospace; font-size: 14px; }}
      .key {{ fill: #0969da; }}
      .value {{ fill: #8250df; }}
      .highlight {{ fill: #1a7f37; }}
      .comment {{ fill: #6f7781; }}
      .prompt {{ fill: #0969da; font-weight: bold; }}
    </style>
  </defs>
  
  <!-- Terminal Background -->
  <rect width="900" height="500" class="terminal-bg" rx="12" stroke="#d1d9e0" stroke-width="2"/>
  
  <!-- Terminal Header -->
  <rect x="0" y="0" width="900" height="30" fill="#f6f8fa" rx="12"/>
  <circle cx="20" cy="15" r="6" fill="#ff5f57"/>
  <circle cx="40" cy="15" r="6" fill="#ffbd2e"/>
  <circle cx="60" cy="15" r="6" fill="#28ca42"/>
  
  <!-- ASCII Art -->
  <text x="50" y="70" class="terminal-text">
    <tspan x="50" y="70">    ┌────────────────────────┐</tspan>
    <tspan x="50" y="90">    │  ●───●───●  NEURAL  │</tspan>
    <tspan x="50" y="110">   │  / \\ / \\ /   NETWORK │</tspan>
    <tspan x="50" y="130">   │ ●───●───●─────────●  │</tspan>
    <tspan x="50" y="150">   │  \\ / \\ / \\       /   │</tspan>
    <tspan x="50" y="170">   │   ●───●───●─────●    │</tspan>
    <tspan x="50" y="190">   │    \\ / \\ / \\   /     │</tspan>
    <tspan x="50" y="210">   │     ●───●───●       │</tspan>
    <tspan x="50" y="230">   │      \\ / \\ /        │</tspan>
    <tspan x="50" y="250">   │       ●───●  AI     │</tspan>
    <tspan x="50" y="270">   └────────────────────────┘</tspan>
  </text>
  
  <!-- Terminal Content -->
  <text x="350" y="70" class="terminal-text">
    <tspan x="350" y="70" class="prompt">raneem@althaqafi</tspan><tspan class="comment"> ~$ whoami</tspan>
    <tspan x="350" y="100" class="comment">└─╼ </tspan><tspan class="key">name:</tspan> <tspan class="value">Raneem Althaqafi</tspan>
    <tspan x="350" y="120" class="comment">└─╼ </tspan><tspan class="key">role:</tspan> <tspan class="value">AI Engineer &amp; Researcher</tspan>
    <tspan x="350" y="140" class="comment">└─╼ </tspan><tspan class="key">age:</tspan> <tspan class="value">{age_data}</tspan>
    <tspan x="350" y="160" class="comment">└─╼ </tspan><tspan class="key">location:</tspan> <tspan class="value">Riyadh, Saudi Arabia</tspan>
    
    <tspan x="350" y="190" class="prompt">raneem@althaqafi</tspan><tspan class="comment"> ~$ cat achievements.txt</tspan>
    <tspan x="350" y="210" class="comment">└─╼ </tspan><tspan class="highlight">🏆 World Champion:</tspan> <tspan class="value">Space Debris Detection (1st/495)</tspan>
    <tspan x="350" y="230" class="comment">└─╼ </tspan><tspan class="highlight">🤖 AI Innovation:</tspan> <tspan class="value">Arabic Metro Assistant (Siraj)</tspan>
    <tspan x="350" y="250" class="comment">└─╼ </tspan><tspan class="highlight">💓 Research:</tspan> <tspan class="value">rPPG Heartbeat Detection (94%)</tspan>
    <tspan x="350" y="270" class="comment">└─╼ </tspan><tspan class="highlight">🇸🇦 Impact:</tspan> <tspan class="value">Vision 2030 Contributor</tspan>
    
    <tspan x="350" y="300" class="prompt">raneem@althaqafi</tspan><tspan class="comment"> ~$ git status</tspan>
    <tspan x="350" y="320" class="comment">└─╼ </tspan><tspan class="key">repositories:</tspan> <tspan class="value">{repo_data}</tspan>
    <tspan x="350" y="340" class="comment">└─╼ </tspan><tspan class="key">stars_earned:</tspan> <tspan class="value">{star_data}</tspan>
    <tspan x="350" y="360" class="comment">└─╼ </tspan><tspan class="key">commits_2025:</tspan> <tspan class="value">{commit_data}</tspan>
    <tspan x="350" y="380" class="comment">└─╼ </tspan><tspan class="key">followers:</tspan> <tspan class="value">{follower_data}</tspan>
    
    <tspan x="350" y="410" class="prompt">raneem@althaqafi</tspan><tspan class="comment"> ~$ echo "motto"</tspan>
    <tspan x="350" y="430" class="comment">└─╼ </tspan><tspan class="value">"Building the future of AI, one neural network at a time"</tspan>
    
    <tspan x="350" y="460" class="prompt">raneem@althaqafi</tspan><tspan class="comment"> ~$ </tspan><tspan class="highlight">█</tspan>
  </text>
</svg>'''
    return svg_content

def perf_counter(funct, *args):
    """Calculates the time it takes for a function to run"""
    start = time.perf_counter()
    funct_return = funct(*args)
    return funct_return, time.perf_counter() - start

def formatter(query_type, difference, funct_return=False):
    """Prints a formatted time differential"""
    print(f'{query_type:<23}: {difference:.4f} {"s" if difference > 1 else "ms" if difference < 1 else "s"}')
    return funct_return

if __name__ == '__main__':
    """
    Raneem Althaqafi Dynamic GitHub Profile Generator
    """
    print('🚀 Generating dynamic GitHub profile...')
    print('Calculation times:')
    
    # Get user data
    user_data, user_time = perf_counter(user_getter, USER_NAME)
    OWNER_ID, acc_date = user_data
    formatter('account data', user_time)
    
    # Calculate age (adjust birth date as needed)
    age_data, age_time = perf_counter(daily_readme, datetime.datetime(1995, 1, 1))  # Adjust your birth date here
    formatter('age calculation', age_time)
    
    # Get GitHub stats
    repo_data, repo_time = perf_counter(graph_repos_stars, 'repos', ['OWNER'])
    formatter('repositories', repo_time)
    
    star_data, star_time = perf_counter(graph_repos_stars, 'stars', ['OWNER'])
    formatter('stars', star_time)
    
    commit_data, commit_time = perf_counter(graph_commits)
    formatter('commits', commit_time)
    
    follower_data, follower_time = perf_counter(follower_getter, USER_NAME)
    formatter('followers', follower_time)
    
    # Create SVG files
    print('\n📝 Creating SVG files...')
    
    # Generate SVG content
    dark_svg = create_dark_mode_svg(age_data, commit_data, star_data, repo_data, follower_data)
    light_svg = create_light_mode_svg(age_data, commit_data, star_data, repo_data, follower_data)
    
    # Write SVG files
    with open('dark_mode.svg', 'w', encoding='utf-8') as f:
        f.write(dark_svg)
    
    with open('light_mode.svg', 'w', encoding='utf-8') as f:
        f.write(light_svg)
    
    print('✅ SVG files generated successfully!')
    print(f'📊 Stats: {repo_data} repos, {star_data} stars, {commit_data} commits, {follower_data} followers')
    print(f'🔥 Total GitHub API calls: {sum(QUERY_COUNT.values())}')
    
    total_time = user_time + age_time + repo_time + star_time + commit_time + follower_time
    print(f'⏱️  Total execution time: {total_time:.4f}s') 