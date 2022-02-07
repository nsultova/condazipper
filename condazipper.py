"""
Creates an environment.yml for conda combining the best of both worlds. 
You need to provide two different environment.yml files, which have to be created by using:
"conda env export --from-history > env_from_history.yml"
and
"conda env export --no-builds > env_no_builds.yml"
..within the conda environment you wish to migrate.

IMPORTANT: As for now this only works with first-generation cona-environments - this means if the environment has already been created by 
an env.ymf file which was exported the default way, export --from-history just displays what a default export would look like, thus we cannot 
use it for determining the top-level dependencies anymore
"""

import yaml
import argparse

parser = argparse.ArgumentParser(description='''
                                                Creates an environment.yml for conda combining the best of both worlds. 
                                                You need to provide two different environment.yml files, which have to be created by using:
                                                "conda env export --from-history > env_from_history.yml"
                                                and
                                                "conda env export --no-builds > env_no_builds.yml"
                                                ..within the conda environment you wish to migrate.
                                             ''')

parser.add_argument('-fh', '--from-history', required=True, type=str,
    help='''
            Provide a conda environment.yml which has been exported by using "conda env export --from-history > env_from_history.yml"
    ''')
    
parser.add_argument('-nb', '--no-builds', required=True, type=str,
    help='''
            Provide a conda environment.yml which has been exported by using "conda env export --no-builds > env_no_builds.yml"
    ''')
 
args = parser.parse_args()
env_from_history = args.from_history
env_no_builds = args.no_builds

with open (env_from_history) as f:
    from_history = yaml.full_load(f)

with open (env_no_builds) as f:
    no_builds = yaml.full_load(f)

#Extract the dependencies section from each file
dep_from_history = from_history['dependencies']
dep_no_builds = no_builds['dependencies']

#Extract the pip part if present
#TODO..how to determine toplevel packages in pip part?
try:
    pip_part = dep_no_builds[-1]['pip']
    dep_no_builds = dep_no_builds[:-1]
except:
    print("No additional packages installed via pip. Skipping..")
    pip_part = None

#Create assignment between top-level dependencies
#How to code this more elegant? filter(), map()..
dep_matches = []
for _, elem_no_builds in enumerate(dep_no_builds):
        for _, elem_from_history in enumerate(dep_from_history):
            if elem_from_history in elem_no_builds:
                dep_matches.append(elem_no_builds)
    

#Add pip part if present
if pip_part is not None:
    dep_matches.append({'pip': pip_part})

#reconstruct modified env.yml
dict_file = {'name' : from_history['name'],
            'channels' : from_history['channels'],
            'dependencies' : dep_matches
}

print(dict_file)

with open(r'env_modified.yml', 'w') as file:
    documents = yaml.dump(dict_file, file, sort_keys=False)

#TODO
"""
* find if there is a more elegant way for filtering
* find a solution for edge cases in pip
* build a cli interface 
* parametrize
* Think about how tests should look like
"""