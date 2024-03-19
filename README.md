# Calendar/Task Tracker App
## Group 2 Spring 2024
## Members
- Moses Tulepkalev
- Loe Malbanan
- Austin Byrd
- Nick Chesi
- Reilly Gardner
- Deepkia Bajaj


## Python venv and pip setup for the group
This section will serve as a guide for setting up a python venv on your machine so that you can keep and update package dependencies that will be needed for this project.

1. Ensure your machine has python3 installed (note, repit uses python 3.10.11, the closer you can get to this version on your machine, the better)
2. Clone the repo to a folder on your machine
3. Open the group2-spring2024 folder in a bash terminal

- To create a venv
in the repo folder run
```bash
python3 -m venv venv
```
this creates a new venv in the venv folder
- To activate the venv
```bash
source venv/bin/activate
```
- To deactivate the venv
```bash
deactivate
```
- To install dependencies

When in your venv run
```bash
pip install -r requirements.txt
```

- To update dependencies

This should be done anytime you have to pip install anything for this project in the venv

In the venv run
```bash
pip freeze > requirements.txt
```
make sure to push the updated requirements.txt file with the code that uses the dependency
## Replit/Git guide for the group

### Overview
This is a guide for our group for how to develop using git/github and replit. The branching model being adopted is essentially trunk based development (read up on it if you want, but i'll kinda explain it here).
If you have any questions on the git structure or if replit is being a pain feel free to message Moses over discord

### Branching guidelines (post sprint 1)
To avoid having issues with interdepending code and having it work together you should only create branches off of main and not merge your branches into anyone else's branch or vice versa. If you need functionality that is not yet pushed into main then either help the person whose code yours is dependent on get theirs done or do something else in the meantime. Converesely, if you know your work is a prerequisite for otehr poeple's work please make an effort to get it done sooner rather than later. Also once your work is done and is tested and confirmed to work then don't hesitate in creating a PR to get it into main so that other people can start working on it.

### Migrations
Do not delete any migrations that are already in main, do not delete any migrations that other migrations are dependent on. We can resolve migration issues if they come up.
### Do not push directly to main
Unfortuantely due to us not having permissions over the repo we are unable to push protect our main branch. However, please do not push directly to main, this can cause divergent branches and lots of pain for everybody. Pushing to main can occasionally be done for something like single line changes in production but should generally be avoided, merge requests should be used instead.

### Don't develop on replit
As we all have learned, replit is a pain in many ways, so for a multitude of reasons, we should avoid writing code and pushing code from replit. Since replit is our deploy enviroment any code that is on there should be completely functional and ready for "release" (see [this section](#trunk-based-development-overview) for more). Since replit was set up using Moses' PAT and email any commits from github will be seen as from his account, makes it harder to track who did what. Our use of replit should basically consist of pulling main and running deployment on it, if we need to do any debugging of code on replit due to issues that arise on replit specifically it should be added to a branch (perhaps a replit specific branch, TBD).

### Trunk based development overview
In order to avoid code conflicts wherever possible as well as having code well organized, we use trunk based development (very good explanation on it [here](https://trunkbaseddevelopment.com/)).
All code development will be done on feature branches (will be branched off main for 99% of our cases).
Each feature bracnch should have the following properties:

- Worked on by only one person
- Created for development of one specific feature/story
- Ideally no/minimal conflicts with other feature branch (no two feature branches should be working on same task/story at once)

The reason we are using feature branches as opposed to pushing to trunk is because it allows for us to have [PR/MRs](#merge-requests-(pull-requests)) for review and CI/CD.

The trunk (main) branch should be in a fully functional state at all times, ideally we should be able to tag a release off it at any point

### Merge requests (Pull Requests)
In order to merge feature branches into the main branch, we will be making use of merge requests (called pull requests in GitHub, abbreviated MR and PR respectively). This has several advantages over manually merging into main. Most notably.

- Allowing changes to be viewed by other group members
- Allowing assigning of reviewers and comments from group members
- Allowing automatic tests to be run and certified before allowing merges to be pushed into main

Once the feature that you are working on is finished, create a pull request on github, all automated tasks should run and pass.
Write a good description of your changes as well as what story/task it fulfils(if applicable). Add reviewers if you want anyone specific to look over your code.

Once you are done with creating your PR it is usually a good idea to have at least a few of the other people look over it and leave comments though you should be able to force push it through yourself.

### Atomic Commits
To make commit history easier to look through and identify what was changed where, commits should ideally be atmoic (or at least something like that just please don't have one commit for changes for all 150 lines of code you changed). This means that each commit should be doing one thing, one template/view or one change. Generally the point is if you want to find out where a function/piece of code was created/should be changed it should be easy to find it.

### Rewriting History
If you want to do anything that rewrites git history (rebasing, squashing, etc.) make sure you are doing it on a branch no one else is on so that you dont mess things up for other people.

### Re-using branches
If you plan on re-using a branch after it is merged into main, make sure to rebase it off of main before you restart devleopment on that branch

### Comments/Code standards
#### Imports
If you added imports to a file, then before committing and pushing, run the "Organize inputs" VS code command, this helps avoid merge conflicts from import order and stuff like that, it's a small issue but also really easy to fix.

This is for us to decide on, what code standards should we have, if any (maybe some would be nice). Stuff like
- File structure
- Varaible/method naming
- Comment standards
- Zen of Python (Austin put this in)
