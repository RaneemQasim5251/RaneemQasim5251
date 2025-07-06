import datetime
from dateutil import relativedelta
import requests
import os
from lxml import etree
import time
import hashlib

# GitHub Personal Access Token
# You'll need to set these environment variables:
# export ACCESS_TOKEN=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
# export USER_NAME=RaneemQasim5251
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
    """Create a simple, GitHub-compatible dark mode SVG"""
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="600" viewBox="0 0 1000 600">
<rect width="1000" height="600" fill="#0d1117" rx="10"/>
<rect x="0" y="0" width="1000" height="25" fill="#161b22" rx="10"/>
<circle cx="15" cy="12" r="4" fill="#ff5f57"/>
<circle cx="30" cy="12" r="4" fill="#ffbd2e"/>
<circle cx="45" cy="12" r="4" fill="#28ca42"/>

<text x="50" y="60" fill="#c9d1d9" font-family="monospace" font-size="16">
<tspan x="50" y="60" fill="#ffd700">raneem@althaqafi</tspan><tspan fill="#8b949e"> ~$ whoami</tspan>
<tspan x="50" y="85" fill="#8b949e">└─╼ </tspan><tspan fill="#ffd700">name:</tspan><tspan fill="#7dd3fc"> Raneem Althaqafi</tspan>
<tspan x="50" y="105" fill="#8b949e">└─╼ </tspan><tspan fill="#ffd700">role:</tspan><tspan fill="#7dd3fc"> AI Engineer &amp; Researcher</tspan>
<tspan x="50" y="125" fill="#8b949e">└─╼ </tspan><tspan fill="#ffd700">age:</tspan><tspan fill="#7dd3fc"> {age_data}</tspan>
<tspan x="50" y="145" fill="#8b949e">└─╼ </tspan><tspan fill="#ffd700">location:</tspan><tspan fill="#7dd3fc"> Riyadh, Saudi Arabia</tspan>

<tspan x="50" y="175" fill="#ffd700">raneem@althaqafi</tspan><tspan fill="#8b949e"> ~$ cat achievements.txt</tspan>
<tspan x="50" y="195" fill="#8b949e">└─╼ </tspan><tspan fill="#3fb950">🏆 World Champion:</tspan><tspan fill="#7dd3fc"> Space Debris (1st/495)</tspan>
<tspan x="50" y="215" fill="#8b949e">└─╼ </tspan><tspan fill="#3fb950">🤖 AI Innovation:</tspan><tspan fill="#7dd3fc"> Arabic Metro AI (Siraj)</tspan>
<tspan x="50" y="235" fill="#8b949e">└─╼ </tspan><tspan fill="#3fb950">💓 Research:</tspan><tspan fill="#7dd3fc"> rPPG Heartbeat (94%)</tspan>
<tspan x="50" y="255" fill="#8b949e">└─╼ </tspan><tspan fill="#3fb950">🇸🇦 Impact:</tspan><tspan fill="#7dd3fc"> Vision 2030 Contributor</tspan>

<tspan x="50" y="285" fill="#ffd700">raneem@althaqafi</tspan><tspan fill="#8b949e"> ~$ git status</tspan>
<tspan x="50" y="305" fill="#8b949e">└─╼ </tspan><tspan fill="#ffd700">repos:</tspan><tspan fill="#7dd3fc"> {repo_data}</tspan><tspan fill="#8b949e"> │ </tspan><tspan fill="#ffd700">stars:</tspan><tspan fill="#7dd3fc"> {star_data}</tspan>
<tspan x="50" y="325" fill="#8b949e">└─╼ </tspan><tspan fill="#ffd700">commits:</tspan><tspan fill="#7dd3fc"> {commit_data}</tspan><tspan fill="#8b949e"> │ </tspan><tspan fill="#ffd700">followers:</tspan><tspan fill="#7dd3fc"> {follower_data}</tspan>

<tspan x="50" y="355" fill="#ffd700">raneem@althaqafi</tspan><tspan fill="#8b949e"> ~$ echo "Building AI future"</tspan>
<tspan x="50" y="375" fill="#8b949e">└─╼ </tspan><tspan fill="#7dd3fc">"One neural network at a time" ✨</tspan>

<tspan x="50" y="405" fill="#ffd700">raneem@althaqafi</tspan><tspan fill="#8b949e"> ~$ system_status</tspan>
<tspan x="50" y="425" fill="#8b949e">└─╼ </tspan><tspan fill="#00ff00">MATRIX_MODE: ACTIVATED</tspan>
<tspan x="50" y="445" fill="#8b949e">└─╼ </tspan><tspan fill="#00ff00">NEURAL_NETWORK: ONLINE</tspan>
<tspan x="50" y="465" fill="#8b949e">└─╼ </tspan><tspan fill="#00ff00">AI_CORE: READY</tspan>

<tspan x="50" y="485" fill="#ffd700">raneem@althaqafi</tspan><tspan fill="#8b949e"> ~$ </tspan><tspan fill="#3fb950">█</tspan>
</text>

<rect x="0" y="580" width="1000" height="20" fill="#0d1117" opacity="0"/>
</svg>'''
    return svg_content

def create_light_mode_svg(age_data, commit_data, star_data, repo_data, follower_data):
    """Create a simple, GitHub-compatible light mode SVG"""
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="600" viewBox="0 0 1000 600">
<rect width="1000" height="600" fill="#ffffff" stroke="#d1d9e0" stroke-width="2" rx="10"/>
<rect x="0" y="0" width="1000" height="25" fill="#f6f8fa" rx="10"/>
<circle cx="15" cy="12" r="4" fill="#ff5f57"/>
<circle cx="30" cy="12" r="4" fill="#ffbd2e"/>
<circle cx="45" cy="12" r="4" fill="#28ca42"/>

<text x="50" y="60" fill="#24292f" font-family="monospace" font-size="16">
<tspan x="50" y="60" fill="#0969da">raneem@althaqafi</tspan><tspan fill="#6f7781"> ~$ whoami</tspan>
<tspan x="50" y="85" fill="#6f7781">└─╼ </tspan><tspan fill="#0969da">name:</tspan><tspan fill="#8250df"> Raneem Althaqafi</tspan>
<tspan x="50" y="105" fill="#6f7781">└─╼ </tspan><tspan fill="#0969da">role:</tspan><tspan fill="#8250df"> AI Engineer &amp; Researcher</tspan>
<tspan x="50" y="125" fill="#6f7781">└─╼ </tspan><tspan fill="#0969da">age:</tspan><tspan fill="#8250df"> {age_data}</tspan>
<tspan x="50" y="145" fill="#6f7781">└─╼ </tspan><tspan fill="#0969da">location:</tspan><tspan fill="#8250df"> Riyadh, Saudi Arabia</tspan>

<tspan x="50" y="175" fill="#0969da">raneem@althaqafi</tspan><tspan fill="#6f7781"> ~$ cat achievements.txt</tspan>
<tspan x="50" y="195" fill="#6f7781">└─╼ </tspan><tspan fill="#1a7f37">🏆 World Champion:</tspan><tspan fill="#8250df"> Space Debris (1st/495)</tspan>
<tspan x="50" y="215" fill="#6f7781">└─╼ </tspan><tspan fill="#1a7f37">🤖 AI Innovation:</tspan><tspan fill="#8250df"> Arabic Metro AI (Siraj)</tspan>
<tspan x="50" y="235" fill="#6f7781">└─╼ </tspan><tspan fill="#1a7f37">💓 Research:</tspan><tspan fill="#8250df"> rPPG Heartbeat (94%)</tspan>
<tspan x="50" y="255" fill="#6f7781">└─╼ </tspan><tspan fill="#1a7f37">🇸🇦 Impact:</tspan><tspan fill="#8250df"> Vision 2030 Contributor</tspan>

<tspan x="50" y="285" fill="#0969da">raneem@althaqafi</tspan><tspan fill="#6f7781"> ~$ git status</tspan>
<tspan x="50" y="305" fill="#6f7781">└─╼ </tspan><tspan fill="#0969da">repos:</tspan><tspan fill="#8250df"> {repo_data}</tspan><tspan fill="#6f7781"> │ </tspan><tspan fill="#0969da">stars:</tspan><tspan fill="#8250df"> {star_data}</tspan>
<tspan x="50" y="325" fill="#6f7781">└─╼ </tspan><tspan fill="#0969da">commits:</tspan><tspan fill="#8250df"> {commit_data}</tspan><tspan fill="#6f7781"> │ </tspan><tspan fill="#0969da">followers:</tspan><tspan fill="#8250df"> {follower_data}</tspan>

<tspan x="50" y="355" fill="#0969da">raneem@althaqafi</tspan><tspan fill="#6f7781"> ~$ echo "Building AI future"</tspan>
<tspan x="50" y="375" fill="#6f7781">└─╼ </tspan><tspan fill="#8250df">"One neural network at a time" ✨</tspan>

<tspan x="50" y="405" fill="#0969da">raneem@althaqafi</tspan><tspan fill="#6f7781"> ~$ system_status</tspan>
<tspan x="50" y="425" fill="#6f7781">└─╼ </tspan><tspan fill="#00ff00">MATRIX_MODE: ACTIVATED</tspan>
<tspan x="50" y="445" fill="#6f7781">└─╼ </tspan><tspan fill="#00ff00">NEURAL_NETWORK: ONLINE</tspan>
<tspan x="50" y="465" fill="#6f7781">└─╼ </tspan><tspan fill="#00ff00">AI_CORE: READY</tspan>

<tspan x="50" y="485" fill="#0969da">raneem@althaqafi</tspan><tspan fill="#6f7781"> ~$ </tspan><tspan fill="#1a7f37">█</tspan>
</text>

<rect x="0" y="580" width="1000" height="20" fill="#ffffff" opacity="0"/>
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
    age_data, age_time = perf_counter(daily_readme, datetime.datetime(2001, 3, 16))  # Born March 16, 2001
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
