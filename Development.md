### Homebrew formula
The Homebrew tap/formula process is the combination of two GitHub repositorysitories. 

 - The First GitHub repository contains the functionality package (socios).

 - The second GitHub repository contains the homebrew formula with the ruby file (homebrew-socios).

### Homebrew Directory list
The homebrew package uses the below folder path to configuration.  
**Formula** – The package definition uses the path
`/usr/local/Homebrew/Library/Taps/homebrew/homebrew-core/Formula/socios.rb`

**Keg** - The installation prefix of a Formula uses the path 
`/usr/local/Cellar/Socios/v1.0.0`

**Cellar** - All Kegs are installed in path 
`/usr/local/Cellar`

**Tap** - A GitHub repository of Formulae and/or commands uses the path `/usr/local/Homebrew/Library/Taps/homebrew/homebrew-core`

### creating the Homebrew tap/formula
- git clone https://github.com/repository-url

- After cloning the repository switch into that cloned repository folder and place the script packages in that repository(Socios) and start the commit in GitHub using the below commands in terminal

        git add .
        git commit -am "first commit"
        git push -u origin main
        git tag v1.0.0
        git push origin v1.0.0
	
- Commit am(a- automatically stage all tracked modified file before the commit, m- message of the commit)
- Create the second repository for the ruby formula file in GitHub called “homebrew-socios”. Then clone that repository into our machine using the git clone command.
- Switch into that new repository folder to create the formula 
- Then, we need to copy the compressed tar.gz file link from the GitHub release and create the ruby file formula by running the below command in terminal.

        brew create http://github.com/repository.tar.gz

- The above command will generate the default formula file in a ruby format for our socios packages (Need to edit this default formula).
- Copy the default formula to the document folder then open it with Nano editor to add the below lines in the ruby formula file .
    1. bin.install "socios"
    2. prefix.install Dir["lib"]

- Then upload this file into the new GitHub repository using the below commands

        git add .
        git commit -am "formula"
        git push -u origin main
		
- Once completed the above procedures, we can able to download and use our socios packages by using the below commands.

        brew tap SociOS-Linux/socios
        brew install Socios
		
- Then we can check the functions of Socios using the below commands

        socios --help
        socios --version
	
