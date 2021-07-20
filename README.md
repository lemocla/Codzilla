# **MS3 - Codzilla**

## **Introduction** 

[include screenshots of project on responsive devices]

Codizilla -  an online meetup-planning platform - was created for educational purposes only as part of the Code Institute’s full stack development course.

Using the principles of UX design, this fully responsive and interactive website was developed using HTML, CSS, JavaScript, Python, Flask and MongoDB. 

View live project here [link to deployed link]

## **Table of content** 

  - [UX Design](#ux-design)
    - [Strategy](#strategy)
    - [User stories](#user-stories)
    - [Scope](#scope)
    - [Structure](#structure)
    - [Skeleton](#skeleton)
    - [Design](#design)
  - [Features](#features)
    - [Existing features](#existing-features)
    - [Features left to implement](#features-left-to-implement)
  - [Technologies Used](#technology-used)
    - [Languages](#languages)
    - [Database](#database)
    - [Libraries, frameworks and other technologies](#libraries-frameworks-and-other-technologies)
  - [Testing](#testing)
  - [Deployment](#deployment)
    - [Deployment of the page](#deployment-of-the-page)
    - [How to run the code locally](#how-to-run-the-code-locally)
   - [Credits](#credits)
     - [Code](#code)
     - [Content](#content)
     - [Media](#media)
     - [Acknowledgment](#acknowledgments)


# **UX DESIGN**

- ## **Strategy** 

    Codizilla is an online event-planning platform, aimed at developers who, regardless of their experience, want to organise and participate in meetups in order to extend their skills, network and portfolio around:
    - a group or open-source project, 
    - a study group to learn and expand on a specific language or framework 
    - a working group to help each others with cvs and cover letters or
    - a drink to simply meet and socialize    
    
    The site owner, as a remote student on a full-stack development course, appreciates that it can be a lonely process and has enjoyed meeting with fellow students on the course, working and socializing together on an array of projects. 

    **Site owner goal**

    - To provide an easy and engaging community platform where users can create and join meetups
    - To expand on software development skills using Python, Flask and MongoDB
    - To create a minimum viable product that can be further developed with additional features   

    **User goals** 

    - To access a user-friendly website across multiple devices 
    - To build a community with other developers around shared-interests and collaborative projects by joining and/or organising meetups. 


- ## **User stories** 

    **As a new user:** 
    - I want a responsive website so that I can access it on different devices.
    - I want to easily navigate across the site so that I can find the information I need.
    - I want to search events without having to register so that I can assess if this website is for me
    - I want to view a details for an event so that I can see all the practical information 
    - I want to sign-up on the website so that I can join or organise an event
    - I want to read about how to use this website so that I can make the most of the features on offer.  

    **As a returning user:** 
    - I want to login on the website so that I can make use of all the features on the website 
    - I want to be able to edit my profile so that I can update my personal information
    - I want to set my preferences for my notification so that I don’t miss important information
    - I want to reset my password if I forgot it so that I can access my account
    - I want to be able to delete my profile so that my personal information is removed from the website        

    **As an event organiser:**
    - I want to create a group so that my events are easier to find
    - I want to easily create an event so that I can start meeting with other users
    - I want to view events that I have created so that I can manage my events
    - I want to post an answer to a question about a meetup I’m organising so that I can offer more details about the event.   

    **As a meetup participant:**
    - I want to easily join an event so that I can start meeting other users 
    - I want to be able to ask a question about the event  so that I can get more details about the event
    - I want to cancel my participation to an event
    - I want to view the events that I am planning to attend    

    **As a frequent user:**
    - I want to contact the site owner so that I can make queries about the website
    - I want to be able to edit an event so that I can reschedule or update details about the event
    - I want to be able to cancel an event so that attendees can get notified of the cancellation
    - I want to be able to delete an event so that I can manage my account more effectively
    - I want to view important notifications about my events so that I keep up-to-date.


- ## **Scope** 

    - ### **Feature trade-off**

        ![features tradeoff](documentation/scope/features_tradeoff.png)

        This website will be developed as a minimal viable product with room for future improvements and releases incorporating additional features.

    - ### **Functional requirements**
        - To be able to sign-up using email address and secure password
        - To be able to login 
        - To be able to add/view/edit/delete profile information and preferences
        - To be able to reset password 
        - To be able to add/view/edit/delete an event 
        - To be able to add/view/edit/delete a group
        - To be able to cancel an event 
        - To be able to search events according to keyword and set of criteria
        - To be able to sort meetup according to a set of criteria 
        - To be able to display search results 
        - To be able to add/view/edit/delete a question 
        - To be able to add/view/edit/delete an answer 
        - To be able to notify users when an event is about to take place, when an event has been changed or cancelled and when a question has been asked / answered
        - To be able to share events on social media
        - To be able to store and retrieve images 
        - To be able to contact the site owner 
        - To receive feedback for important actions: create - update - delete
        - Page 404 Not Found
        - Page 500 Internal Server Error page 

	- ### **Non functional requirements**
	
      - Display event location on a map
      - Display profile and event images 

    - ### **Content requirements**
        - Clear and concise information on how how to use the website 
        - Forms for user input 
        - Engaging text and headings throughout to display relevant user input such as profile page, events and groups as well as questions and answers
        - Background images to provide visually appealing and engaging interface
        - Icons for interactive and visual elements 

    - ### **Constraints**
	
      **Technical skills:**   
      The site owner is still learning Python, Flask and MongoD, which may impact on the successful implementation of the planned features. 

      **Time:**     
      Implementing features using new technical skills will require time and careful planning. 

- ## **Structure**

    - ### **Information architecture**

         ![website architecture](documentation/structure/architecture.png)
         Link to document (png format) [here](documentation/structure/architecture.png)

    - ### **Website workflow**

        ![website workflow](documentation/structure/workflow.png)
         Link to document (png format) [here](documentation/structure/workflow.png) 

    - ### **Organisation of functionality and content**

      **Header:** Logo and a collapsible menu for guest users. Once users are logged in, they will have access to certain functionality such as notification and add an event. Users will also have easy access to their profile, their events as well as their groups.   

      **Homepage:** Search option, information about and on how to use the website as well as a carousel of upcoming events,
    
      **Footer:** Contact form and useful links
    
      **All events and groups:** list of all events with search and sort option. Each event card will include important information: event title, date & time, location, number of attendees.
    
      **Event and group detail pages:** display all the information relevant event / group
    
      **Profile page:** to display all the relevant information about a user
    
      **View my events pages:** to display a summary of all the events organised as well events the user is attending / interested in.

      **View my group page:** to display a summary of all the groups for which the user is either a member or an organiser. 

      Other pages will have the primary purpose to collect information add/ edit information stored on the database such as user profile, events and groups.

    - ### **Interaction design**

        - Collapsible menu
        - Modal forms for editing profile and contact us page 
        - Buttons and content cards with hovering effects 
        - Icons with hovering effect

    - ### **Database structure**

        Database structure was designed using [diagram.io](https://dbdiagram.io). 

        ![database architecture](documentation/structure/db_structure.png)

        Link to document (png format) [here](documentation/structure/db_structure.png) 


- ## **Skeleton**

    **Homepage wireframe** 

    ![Homepage](documentation/wireframes/homepage_user_in.png)
    Link to homepage wireframe (png format) [here](ocumentation/wireframes/homepage_guest_user.png) 

    Please find below links to a selection of wireframe for this project. 
    - [Sign in page wireframe](documentation/wireframes/login_page.png) 
    - [Sign up page wireframe](documentation/wireframes/sign_up_page.png) 
    - [Complete profile wireframe](documentation/wireframes/complete_profile.png) 
    - [Profile completed wireframe](documentation/wireframes/profile_completed.png) 
    - [All events and groups wireframe](documentation/wireframes/all_events_and_groups.png) 
    - [Add / edit an event wireframe](documentation/wireframes/create_edit_event.png) 
    - [Add / edit a group wireframe](documentation/wireframes/create_a_group.png) 
    - [Profile page](documentation/wireframes/profile_page.png)
    - [Edit profile modals wireframe](documentation/wireframes/profile_edit_modals.png) 
    - [My events wireframe](documentation/wireframes/my_events.png) 
    - [My groups wireframe](documentation/wireframes/my_groups.png) 
    - [Notification](documentation/wireframes/notification.png) 

    Please find all the wireframes in pdf format [here](documentation/wireframes/wireframes_all.pdf)

    #### **Difference to design**

    #### **Limitations** 

- ## **Design** 

    The website will feature a simple, modern and engaging design, with minimum colours and imagery to keep the emphasis on the events and information displayed.

    - #### **Imagery**

    - #### **Colour scheme**

      The website will use the following colour palette, which was customed made using  and checked for accessibility using [Adobe Color](https://color.adobe.com/create/color-wheel) 
      ![color palette](documentation/design/colours.png)

      Colours will be used sparingly throughout the website. 

      The colour blue will be used for icons and buttons to inform users with regards to their interest and participation into groups and events. 
      
      Fuchsia will be used for the logo and was selected for its bright and bold appearance offering a striking contrast with the blue. It will also be used to hightlight certain text elements. 

    - #### **Typography**

      The website will use the following fronts from [Google](https://fonts.google.com/):
      - Open sans for the text throughout due its friendly appearance and being easy to read. 
      - Roboto for headings as it complements Open sans very nicely 
      - Tourney for the logo for its technological aspect. 

    - #### **Icons**
      Icons by [font-awesome](https://fontawesome.com/) will be used in the navigation bar to allow user to quickly access functionalities offered by the website once logged-in. 

    - #### **Styling**

      - Horizontal lines to structure and make the content of the website easy to read.
      - Rounded edge borders and buttons for a more user friendly and inviting interface.

    - #### **Difference to design** 

# **FEATURES**

  - ## **Existing features**

  - ## **Features left to implement**

# **TECHNOLOGY USED**

  - ## **Languages**
    - HTML
    - CSS
    - Javascript 
    - Python 

  - ## **Database**
    - MongoDB

  - ## **Libraries frameworks and other technologies**
    - Flask
    - Heroku 
    - PyMongo 
    - Jinja


# **TESTING** 

 - ## **Intro** 

 - ## **Code validation** 
    - #### **W3C HTML Code Validator**
    - #### **W3C CSS Jigsaw Validator**
    - #### **JSHint validator**
    - #### **Python 8**

 - ## **User stories** 

 - ## **Responsiveness and compatibility** 

 - ## **Testing performance**

 - ## **Testing accessibility - wave report**

  - ## **Interesting issues and know bugs**
    - #### **Interesting issues**
    - #### **Known bugs**

# **DEPLOYMENT**

  This website was developed on Gitpod using the Code Institute student template with changes frequently committed to git then pushed onto GitHub from the Gitpod terminal.
  
  The application is deployed on Heroku with the repository hosted on Github
  
  - ## **Prerequisite**
    - Have an account with MongoDB and get a connection string 
    - Have an account with Heroku 
  - ## **To use the code locally** 

    To use this project, you can either fork or clone the local repository on gitHug as follows, then go to the deployment section to configure and deploy the app on Heroku.
 
    - ### **Forking local repository** 
      You can make a copy of the GitHub Repository by "forking" the original repository onto your own account, where changes can be made without affecting the original repository by following the following steps: 

      - Log onto Github
      - Navigate to the GitHub repository : https://github.com/lemocla/Codzilla
      - Click on the fork icon (located on top right of the page at the same level of repository name)

      ![forking](documentation/deployment/fork.png)
 
      - You should now have a copy of this repository into your GitHub account.
	    - To make a change, clone the file into your local IDE

      For more information on how to fork a repository, please check this [github documentation](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo). 
      

    - ### **Cloning the repository into your local IDE** 

      - Log into GitHub and navigate to the GitHub repository: https://github.com/lemocla/Codzilla
      - Above the repository folder and file content, click “Code”
      - Select from one of the following options:  

        ![cloning](documentation/deployment/cloning.png)

        #### **Clone the files using url** 
          - Copy the url
          - Create a repository in GitHub and a workspace in your IDE
          - Open the terminal and type: ``$ git clone https://github.com/lemocla/Codzilla``
          - All the files should have been imported in your workspace

	      #### **Download zip files**
          - Create a repository in GitHub and a workspace in your IDE
          - Unzip the folder
          - Upload the files into your workspace

      You can find all the steps to follow according to your chosen method in this [GitHub documentation](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository-from-github/cloning-a-repository) on how to clone a repository.

  - ## **Prepare for deployment**
	
    - ### **Get connection string with MongoDB**

      - Click on project
      - Click on connect
        ![mongo_connect](documentation/deployment/mongodb_connect.png)
      - Select connect your application (make sure python & version 3.6 selected)
        ![mongo connect app](documentation/deployment/mongodb_connect_app.png)
      - Copy link & change db name & password (make sure you use the password for user access and not your login details)
        ![mongo connect app](documentation/deployment/mongodb_connection_string.png)
        

    - ### **Set local environment** 

      - Create env.py file in the route directory by entering touch env.py in your command line interface
      - Add the following to your env.py
 
            import os   
            os.environ.setdefault("IP", "0.0.0.0")    
            os.environ.setdefault("PORT", "5000")   
            os.environ.setdefault("SECRET_KEY", "your_secret_key")   
            os.environ.setdefault("MONGO_URI", "Your_Mongo_connection_string")   
            os.environ.setdefault("MONGO_DBNAME", "Your_DB_Name")

      - Add your env.py and ‘pycache/’ directory to .gitignore 

    - ### **Requirements.txt and Procfile**

      - Create a requirements.txt file, which will list all of the Python dependencies by typing the following in the command line interface:    
            ``$ pip freeze > requirements.txt``   
 
      - Create a Procfile, which is a specific type of file that tells Heroku how to run our project by typing the following the command line interface:    
            ``$ echo web: python app.py > Procfile``     
       (Make sure to write Procfile with a capital P and to remove blank line in the Procfile)
    
      - Add and commit the requirement.txt and procfile then push to GitHub

  - ##  **Deployment on Heroku**

    - Log onto Heroku and click the create new app button
      ![Heroku add app](documentation/deployment/heroku_add.png)
    - Enter a unique name for your application
    - Select the region closest to you      
    - Set your deployment method to 'GitHub'
      ![Heroku connect github](documentation/deployment/heroku_connect.png)
    - Search for the repository you wish to deploy from 
    - Enable automatic deploy 
      ![Heroku github setting](documentation/deployment/heroku_github.png)

    - Set environment in Heroku App 
      - Go to settings, then click on reveal config vars
      - Enter your key value pairs as per your env.py file (without the inverted commas)
        ![Heroku variable](documentation/deployment/heroku_variable.png)


# **CREDITS** 

- ## **Code**
- ## **Content**
- ## **Media**
- ## **Acknowledgments** 
