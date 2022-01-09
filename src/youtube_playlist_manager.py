def add_video_playlist(youtube_api, playlistId, videoId):
    body = dict(
        snippet=dict(
            playlistId=playlistId,
            resourceId={"kind": "youtube#video", "videoId": videoId},
            position=0,
        )
    )

    request = youtube_api.playlistItems().insert(part="snippet", body=body)

    response = request.execute()

    print(response)
