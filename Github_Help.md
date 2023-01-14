Base (Main Program) = Dev
Branch = feature-buffett-indicator

# Download program from GITHUB Dev to LOCAL DESKTOP MACHINE
git clone git@github.com:rickblien/quantstacks-beta.git 

# Create a copy of Dev by Create a new branch name "feature-buffett-indicator"
git checkout -b feature-buffett-indicator

# Switch to Dev branch
git checkout Dev

# Switch to feature-buffett-indicator branch
git checkout feature-buffett-indicator

# Shows all branches
git branch

# Show changes between Dev and feature-buffett-indicator branch
git diff feature-buffett-indicator

# Upload program from LOCAL MACHINE to GITHUB feature-buffett-indicator branch
git add .
git status
git commit -m "Title: Added a new filename.py" -m "Description Box: DCF program"
git push -u origin feature-buffett-indicator

# Undo git add -all
git reset

# Undo git commit last commit
git reset HEAD

# Undo git commit 2 commit ago
git reset HEAD~1

# Undo specific git commit
git log
git reset 34j2hh5453256345345252

# Undo multiple consecutive git commit
git log
git reset --hard 34j2hh5453256345345252

# Merge feature-buffett-indicator branch to Dev (main)
git merge feature-buffett-indicator

# Delete a feature-buffett-indicator branch
git branch -d feature-buffett-indicator


