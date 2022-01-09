from response_processor import add_all_videos_to_playlist


def main():
    resumen_semanal_video_id = input("Ingresá el Id del video del Resumen Semanal (el Id es lo que está despues del v= en la url del navegador. Ejemplo: ywRiAQuM65U\n")

    playlist_id = input("Ingresá el Id tu playlist a la cual le querés agregar todos los videos de la descripción. El (XXXXXXXXX que está despues del list= en la url del navegador: PLidK0Jb0r6CL3cF98ZglWO3oqJNqKv2Xt\n")

    add_all_videos_to_playlist(resumen_semanal_video_id, playlist_id)
    
    print("Listo!")

if __name__ == "__main__":
    main()