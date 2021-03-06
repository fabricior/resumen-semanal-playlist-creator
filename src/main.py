from response_processor import add_all_videos_to_playlist


def main():
    print('\n' * 2)
    resumen_semanal_video_id = input("Ingresá el Id del video del Resumen Semanal (el Id es lo que está despues del v= en la url del navegador. Ejemplo: ywRiAQuM65U )\n")

    playlist_id = input("Ingresá el Id tu playlist a la cual le querés agregar todos los videos de la descripción (El XXXXXXXXX que está despues del list= en la url del navegador: PLidK0Jb0r6CL3cF98ZglWO3oqJNqKv2Xt )\nSi queres que se cree una nueva playlist privada, dejalo en blanco.")
    
    print('\n' * 2)

    print('Ahora vamos a necesitar autorizar esta aplicación para que pueda acceder a tus videos de Youtube. Seguí las instrucciones de abajo.\n')

    playlist_id = add_all_videos_to_playlist(resumen_semanal_video_id, playlist_id)
    
    print(f'\nListo! Ya podes mirar el playlist con id "{playlist_id}" en Youtube.\n')

if __name__ == "__main__":
    main()