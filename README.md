# Calendar/Task Tracker App
## Group 2 Spring 2024
## Members
- Moses Tulepkalev
- Loe Malbanan
- Austin Byrd
- Nick Chesi
- Reilly Gardner
- Deepkia Bajaj

## Replit/Git guide for the group

### Overview
This is a guide for our group for how to develop using git/github and replit. The branching model being adopted is essentially trunk based development (read up on it if you want, but i'll kinda explain it here).
If you have any questions on the git structure or if replit is being a pain feel free to message Moses over discord

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
This is for us to decide on, what code standards should we have, if any (maybe some would be nice). Stuff like
- File structure
- Varaible/method naming
- Comment standards
- Zen of Python (Austin put this in)
