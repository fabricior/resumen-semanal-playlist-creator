def add_video_playlist(youtube_api, playlistId, videoId):
    body = dict(
        snippet=dict(
            playlistId=playlistId,
            resourceId={"kind": "youtube#video", "videoId": videoId},
            position=0,
        )
    )

    request = youtube_api.playlistItems().insert(part="snippet", body=body)

    return request.execute()

def create_playlist(youtube_api, title, description, privacyStatus):
    body = dict(
        snippet=dict(
            title=title,
            description=description,
            privacyStatus=privacyStatus,
        ),
        status=dict(
            privacyStatus=privacyStatus,
        ),
    )

    request = youtube_api.playlists().insert(part="snippet,status", body=body)

    return request.execute()
