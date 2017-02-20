Project ideastorming
========================

# description

* this is an work of the university's course of databases (2011-2), remade in django 1.10. 
* the project is a web application that allows you to upload ideas of innovative projects, they will be qualified and repaired by the same community. also, the application allows you to search projects and generate rankings of the projects more interesting proposed and repaired by the community.

# functional requeriments 

* there must exist a process for the user can register, also a system for login and logout.
* the main page must have two columns
    * the first column must display twenty last published project. 
    * the second column must display twenty project most popular.
    * lastly must display a box for the login (or the user information if the user is already logged).
* each registered user must be can publish a project, this project must have:
    * title
    * summary ( max 100 words )
    * a level of investment required
    * comparative advantages in comparation with other projects
    * the project must have tags to be able to classify it.
* in the main page, the user will be able to access to the detail of the project, on this page will be able to see:
    * the detail information about the project
    * information about the author.
    * all the qualifications  that the project has.
* qualifications of the project.
    * all registered user logged must be able of qualify the project, attached a mark and add some note that explains some possibles improvements to the projects. 
* the user must be able to update the project for include all the improvements given by the community. 
    * in the moment of doing the update, the user must be able to mark the actual qualification for ignoring it and it doesn't add to the global mark. 
        * mark the comment like "add the idea to the project." (?)
    * also when the user makes a change to the project must update the last modification update and the updated project must appear like a new project.

# stack

* python 3.5
* django 1.10
* posgresql
* bootstrap + jquery


