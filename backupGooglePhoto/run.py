from backupGooglePhoto.app.backup_google_album import BackupGooglePhoto

# list all the parent directories of your video/image files.
src_dir_path_list = [r"C:\Users\MANTKUMAR\Downloads\working-data-google-photo", ]

# This is where, your processed files will be stored.
dest_dir_path = r"C:\Users\MANTKUMAR\Downloads\experiment_output"

backup_Gphoto = BackupGooglePhoto(src_dir_path_list, dest_dir_path)
backup_Gphoto.rearrange_multimedia_resources(do_indexing=True, do_copy=True)


