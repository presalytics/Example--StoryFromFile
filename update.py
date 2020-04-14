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
