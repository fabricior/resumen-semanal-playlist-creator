from responseDumpExample import python_response

def _extractDescriptionFrom(response: dict) -> str:
    desc = response['items'][0]['snippet']['description']
    return desc

def _extractSectionsFrom(description: str) -> list:
    import re
    # Last section is not matched. Assuming it is "Grand Finale" so it is fine to not include it.
    result = re.findall(r"([0-9][0-9]:[0-5][0-9].+?(?=[0-9][0-9]:[0-5][0-9]))", description, re.DOTALL)

    # we don't need "intro" section either
    result.pop(0)

    return result

def _classifySectionParts(section: str) -> dict:
    lines =  [x for x in section.split('\n') if x]

    title = lines[0]
    video_description = lines[1]
    youtube_link = lines[2]

    return { 'sectionTitle': title, 'videoDescription': video_description, 'link': youtube_link  }

def process(response : dict) -> dict:
    description = _extractDescriptionFrom(response)
    sections = _extractSectionsFrom(description)
    final_sections = map(_classifySectionParts, sections) 
    return final_sections

##### TEST CODE - REMOVE
for section in process(python_response()):
    print(section)
##### TEST CODE - REMOVE    




