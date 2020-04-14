# Example: Creating a Story From a PowerPoint File

This example shows users how to to automate updates to PowerPoint presentations (or other office documents, e.g., Excel Spreadsheets, Google Apps Slides) with just a few lines of code.  Any user with basic python skills and access to a device with a command line should be able follow the steps in this example and modify its code to suit their purpose.



This example is divied into three sections:

* [Setting Up The Environment](#Setting)

* [Creating A Story From The Command Line Interface](#creating)

* [Automating Updates](#Automating)

In this repository, there 2 files to get aquaited with prior to working through the example:

* `example.pptx` : This file is a dummy Open Office Xml (PowerPoint) document.  You can choose to use a different file if you'd like.  Just changes the references "example.pptx" in the code in this exercise.

* `update.py` : This file contains a script that pushes changes to `example.pptx` to the presalytics API service, allowing users to automate updates to thier shared stories.

---

# Setting up The Environment

To begin, clone this repository from github to an empty local folder of your choosing:

~~~~bash
git clone https://github.com/presalytics/Example--StoryFromFile.git
~~~~

Then, create a virtual environment and activate it:

~~~~bash
python -m virtualenv venv
source venv/bin/activate # venv\Scripts\activate.bat (Windows)
~~~~
> Note: If using Anaconda, you can also setup a conda environment to get going.


Install presalytics from the python package index:

~~~~bash
pip install presalytics
~~~~

Use the presaltyics command line interface (CLI) to confiure your workspace:

~~~~bash
presalytics config {YOUR_USERNAME}
~~~~

---

# Creating a Story from the Command Line Interface

Create a story using the following command

~~~~bash
presalytics create example.pptx --ooxml-file
~~~~

The command will open a browser window and prompt you to login to the api. After logging into, this action could take as long as 30 to complete.  Once completed, you should have a the story outline in file in your workspace called `story.yaml`:

~~~~yaml
additionalProperties:
outline_version: 0.3.1
description: ''
info:
createdBy: story_bot
dateCreated: '2020-04-14T00:26:57.068094+00:00'
dateModified: '2020-04-14T00:29:16.826351+00:00'
modifiedBy: ''
revision: '3'
revisionNotes: Created by via "create_outline_from_ooxml_file" method
outlineVersion: 0.3.1
pages:
- kind: widget-page
name: ' This Is an Example Page In a Story'
widgets:
- data:
    document_ooxml_id: bcf8c970-1ecf-417e-84f6-c3504d21ec59
    endpoint_id: Slides
    file_last_modified: '2020-04-14T07:09:43+00:00'
    filename: example.pptx
    object_name: ' This Is an Example Page In a Story'
    object_ooxml_id: c699a102-d405-43d4-91b6-2c3668376008
    previous_ooxml_version:
        document_ooxml_id: 17a36348-fbe9-4da0-8d20-678fad1b2ea1
        object_ooxml_id: 02b35e4a-4766-474d-ad8d-d367be9e5aec
    story_id: 5fb119c9-6c4c-482b-9f86-fe9755ccd6ac
    kind: ooxml-file-object
    name: ' This Is an Example Page In a Story'
storyId: 5fb119c9-6c4c-482b-9f86-fe9755ccd6ac
themes:
- data:
    always_refresh: false
    ooxml_theme_id: 487df31e-95a1-4546-9469-c7d127a3391b
kind: ooxml-theme
name: Blank
plugins:
- config:
    accent1: 199EC7
    accent2: FCB410
    accent3: EC555C
    accent4: 40BC86
    accent5: 1057FC
    accent6: BFBFBF
    background1: FFFFFF
    background2: F8F9FA
    bodyFont: Arial
    dark1: '000000'
    dark2: 199EC7
    followedHyperlink: 868E96
    headingFont: Overpass Heavy
    hyperlink: 1057FC
    light1: FFFFFF
    light2: F8F9FA
    name: esalytics
    text1: '000000'
    text2: 199EC7
    kind: style
    name: ooxml-theme
title: ' This Is an Example Page In a Story'
~~~~


---

# Automating Updates


Pushing an update to is straightforward -- just run the command:
   
~~~bash
python update.py
~~~~

The python script `update.py` reads the outline from `story.yaml` and replaces the widget on the first page with an image of the first slide in the `example.pptx` presentation.  Just update the presentatioThen, and run the script to push changes to the presalytics API service.

The comments in the script its walk through each step line by line:

~~~~python
# update.py
import os
import presalytics

# You can replace the filename below with a filename of your choice,
# just place the file in the same folder as this script
updated_file = os.path.join(os.path.dirname(__file__), "example.pptx" )

# Creates a client object that carries methods to interact with the Presalytics API
client = presalytics.Client()

# Each story contains an 'outline' with instructions for presaltyics to
outline = presalytics.StoryOutline.import_yaml('story.yaml')

# This command retrieves the presaltytics 'Story' object the the Story API
story = client.story.story_id_get(outline.story_id, include_relationships=True)

# Get reference to the document that was uploaded with the "presaltyics create Example2.pptx --ooxml-file" command
document_id = story.ooxml_documents[0].id

# Replaces the old file with a new one
updated_story = client.story.story_id_file_post(
    story.id, 
    replace_existing=True, 
    obsolete_id=document_id,
    file=updated_file
)

# Create as Story Outline object
updated_outline = presalytics.StoryOutline.load(updated_story.outline)

# Writes to the Story Outline to `story.yaml`
updated_outline.export_yaml('story.yaml')
~~~~

You can you the job scheduling tools native to your machine to automatically push updates to the presalytics API.  If you haven not used these tools before, here are some helpful links for different operating systems:

* Mac - [Crontab](https://medium.com/better-programming/https-medium-com-ratik96-scheduling-jobs-with-crontab-on-macos-add5a8b26c30)

* Windows - [Task Scheduler](https://towardsdatascience.com/automate-your-python-scripts-with-task-scheduler-661d0a40b279)

* Linux - [Crontab](https://opensource.com/article/17/11/how-use-cron-linux)

Teams of analysts typically pursue a more scalable use case that implements server-side job scheduler such as [Celery Beat](https://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html) or [Apache Airflow](https://airflow.apache.org/), where scripts can be written on local machines and pushed to a remote server for 24/7 scheduling, which enable stories, dashboards, presenations to be updates around the clock.  These solutions tend to be tailor-made for the resources and the skill-level of an anlytics team.   

If you have question about how to set one of these solutions up, we are happy walk you through.  Send us a question anytime at [inquires@presalytics.io](mailto:inquires@presalytics.io).



