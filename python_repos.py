import requests
import pygal

from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS
## adapted from Python Crash Course by Eric Matthes, ISBN-13: 978-1-59327-603-4
#Visualization of the most starred projects on Github using python

# make an API call and store the response
url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
r = requests.get(url)

# test for a successful response before proceeding
assert(r.status_code == 200)

# store API response in a variable
response_dict = r.json()
print("Total respositories:", response_dict['total_count'])

# explore information about the repositories
repo_dicts = response_dict['items']

# create dictionary of desired values from repositories
names, plot_dicts = [], []
for repo_dict in repo_dicts:
    names.append(repo_dict['name'])

    # get description if one is exists
    description = repo_dict['description']
    if not description:
        description = 'No description provided'

    plot_dict = {
        'value': repo_dict['stargazers_count'],
        'label': description,
        'xlink': repo_dict['html_url'],
    }
    plot_dicts.append(plot_dict)

# make visualization using pygal
my_style = LS('#121225', base_style=LCS)
my_style.title_font_size = 24
my_style.label_font_size = 14
my_style.major_label_font_size = 18

my_config = pygal.Config()
my_config.x_label_rotation = 45
my_config.show_legend = False
my_config.truncate_label = 15
my_config.show_y_guides = False
my_config.width = 1000
my_config.y_title = 'Number of Stars'

chart = pygal.Bar(my_config, style=my_style)
chart.title = 'Most-Starred Python Projects on GitHub'
chart.x_labels = names
chart.add('', plot_dicts)
chart.render_to_file('python_repos.svg')
