# condazipper
Creates an environment.yml for conda combining the best of both worlds. 

Hacky script for pain relief.^^

You need to provide two different environment.yml files, which have to be created by using:
"conda env export --from-history > env_from_history.yml"
and
"conda env export --no-builds > env_no_builds.yml"
..within the conda environment you wish to migrate.

IMPORTANT: As for now this only works with first-generation cona-environments - this means if the environment has already been created by 
an env.ymf file which was exported the default way, export --from-history just displays what a default export would look like, thus we cannot 
use it for determining the top-level dependencies anymore
