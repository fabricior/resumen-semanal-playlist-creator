import datetime
import re
from youtube_auth import get_authenticated_youtube_api
from youtube_video_info_fetcher import get_video_info, get_video_info_from_dummy
from youtube_playlist_manager import add_video_playlist, create_playlist

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
    
    for description_or_video in youtube_links_and_descriptions_raw:        
        is_description = not is_you_tube_link(description_or_video)
        if is_description:
            result_item = { 'video_links': [], 'description': description_or_video }
            result.append(result_item);                            
        else:
            video_id = _extract_video_id_from_link(description_or_video)            
            result_item['video_links'].append({ 'link': description_or_video, 'video_id': video_id })

    return result

def _classify_section_parts(section: str) -> dict:
    lines =  [x for x in section.split('\n') if x]

    sectionTitle = lines[0]
    links_and_descriptions = _get_section_videos(lines[1:])

    return { 'sectionTitle': sectionTitle, 'links_and_descriptions': links_and_descriptions }

def _process_raw(response : dict) -> dict:
    description = _extract_description_rom(response)
    sections = _extract_sections_from(description)
    final_sections = map(_classify_section_parts, sections) 
    return final_sections

def add_all_videos_to_playlist(resumen_semanal_video_id: str, playlist_id: str):
    youtube_api = get_authenticated_youtube_api()

    if not playlist_id:
        current_date_to_iso_format = datetime.datetime.now().strftime("%Y-%m-%d")
        new_playist = create_playlist(youtube_api, 'Resumen Semanal ' + current_date_to_iso_format, ' Resumen Semanal' + current_date_to_iso_format, 'private')
        playlist_id = new_playist['id']

    resumen_semanal_video_info = get_video_info(youtube_api, resumen_semanal_video_id)        
    print('\n' * 5)
    sections = _process_raw(resumen_semanal_video_info)
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





