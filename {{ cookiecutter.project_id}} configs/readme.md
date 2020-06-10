# Configuration files for {{cookiecutter.project_title}}

In this folder you find the configuration files generated based on the cookiecutter. 

Now you need to **check** the configuration files and add them to the files where the configuration is needed.

Depending on your needs you only use the relevant evironments. Probably you initially only need production as you work with production data. Development can later be added when needed.

1. Create a new repo in [dat-repo-control-config](https://github.com/vwt-digital-config/dat-repo-control-config) 
	1. Check the contents of `dat-repo-control-config/data-catalog-snippet.json`.
	2. The content must be added to the data-catalog.json of the repo control. 
	3. Commit and push the repo.
2. Create a new project in [DAT Deployment Config](https://github.com/vwt-digital-config/dat-deployment-config)
  1. Check the contents of `dat-deployment-config/prod-projects-snippet.json`.
  2. The content must be added to the projects.json of the correct environment. 
  3. Commit and push the repo.
  4. Link the project to the github repo (ask: Eric, Bernie or Daimy)
3. Add the project files to [{{cookiecutter.project_id}}-config](https://github.com/vwt-digital-config/{{cookiecutter.project_id}}-config)
	1. Check the contents of `{{cookiecutter.project_id}}-config`.  
    It should contain:
    1. Config for both prod and dev.  
       The config creates one storage bucket. If you need more: copy paste the one that is created and change the fields accordingly.
    2. A basic notebook
    4. A initial readme.md
    5. A licence 
	3. Add all this to the newly created repo