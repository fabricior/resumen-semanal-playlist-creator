import re
from youtube_auth import get_authenticated_youtube_api
from youtube_video_info_fetcher import get_video_info, get_video_info_from_dummy
from youtube_playlist_manager import add_video_playlist

def _extract_description_rom(response: dict) -> str:
    desc = response['items'][0]['snippet']['description']
    return desc

def _extract_sections_from(description: str) -> list:
    # Last section is not matched. Assuming it is "Grand Finale" so it is fine to not include it.
    result = re.findall(r"([0-9][0-9]:[0-5][0-9].+?(?=[0-9][0-9]:[0-5][0-9]))", description, re.DOTALL)

    # we don't need "intro" section either
    result.pop(0)

    return result

def _extract_video_id_from_link(link):
    video_id = re.search(r'(?<=v=)[^&#]+', link).group(0)
    return video_id

def _get_section_videos(youtube_links_and_descriptions_raw: list) -> list:    
    def is_you_tube_link(element: str) -> bool:
        return element.find('youtube.com') != -1 or element.find('youtu.be') != -1

    result = []
    current_element = { 'video_links': [] }

    for description_or_video in youtube_links_and_descriptions_raw:        
        if not is_you_tube_link(description_or_video):            
            if 'description' in current_element:
                result.append(current_element);                
                current_element = { 'video_links': [] }

            current_element['description'] = description_or_video
        else:
            video_id = _extract_video_id_from_link(description_or_video)            
            current_element['video_links'].append({ 'link': description_or_video, 'video_id': video_id })

    return result

def _classify_section_parts(section: str) -> dict:
    lines =  [x for x in section.split('\n') if x]

    sectionTitle = lines[0]
    links_and_descriptions = _get_section_videos(lines[1:])

    return { 'sectionTitle': sectionTitle, 'links_and_descriptions': links_and_descriptions }

def process(response : dict) -> dict:
    description = _extract_description_rom(response)
    sections = _extract_sections_from(description)
    final_sections = map(_classify_section_parts, sections) 
    return final_sections

##### TEST CODE - REMOVE

playlist_id = 'PLidK0Jb0r6CKuC9aUEaY7ZnB2KLHLygXN'


youtube_api = get_authenticated_youtube_api()
video_info = get_video_info(youtube_api)

print('\n' * 5)
print(video_info)
print('\n' * 5)
sections = process(video_info)
for section in sections:    
    print('\n=========================================================\n')
    print(section.get('sectionTitle'))
    print('\n=========================================================\n')
    for x in section.get('links_and_descriptions'):
        print('\n\t-----------------------------------------------------\n')
        print('\t' + x.get('description'))
        for y in x.get('video_links'):
            print('\t' + y.get('link'))
            add_video_playlist(youtube_api, playlist_id, y.get('video_id'))
##### TEST CODE - REMOVE    




