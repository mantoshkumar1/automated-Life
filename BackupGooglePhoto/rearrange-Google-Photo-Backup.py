import os
import csv
import sys
import time
# import win32file
import shutil
import traceback
from utility.logger_util.setup_logger import logger


class RearrageGooglePhotoBackup:
    def __init__(self):
        #
        # list all the parent directories of your video/image files.
        self.src_dir_path_list = [
            r"C:\Users\MANTKUMAR\Desktop\experiment\input",
        ]

        #
        # this is where, your processed files will be stored.
        self._dest_dir_path = r"C:\Users\MANTKUMAR\Desktop\experiment\output"

        #
        # This is the CSV file where all the records of the image/video images will
        # be stored. This CSV is the most important part of this application. In this
        # CSV file, we write the source path of each video/image files with their
        # supposedly calculated destination path. And the third column of this CSV is
        # "is copied". While recursively  traversing the source directory path, we will
        # write "no" for each traversed videos/image files.
        # Later on, when we will start migrating files from one place to another,
        # then we will write "yes" for each video/image files. This was necessary
        # because external hard-disks kept crashing due to excess memory read and write.
        #
        # to write into file: use 'write_row_to_csv'
        # to read from this file: use 'read_row_from_from_csv'
        self._csv_file_path = os.path.join(self._dest_dir_path, "file_copy_info.csv")

        #
        # In this log file, all the failed copy/move operation are logged. This log
        # file will only record the source path of the failed copy/move operation.
        self._failed_relocation_path_log = os.path.join(self._dest_dir_path, 'failed-relocations-paths.log')

    def write_row_to_csv(self, source_path, dest_path, is_copied):
        """Function to write copy information to CSV file"""
        # By setting newline='' when opening the file, we are telling Python to use
        # the default line terminator, which is the newline character.
        with open(self._csv_file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                # Write header row if file is empty
                writer.writerow(
                    ["Source File Path", "Destination File Path", "Copied?"])
            writer.writerow([source_path, dest_path, is_copied])

    def read_row_from_from_csv(self):
        """A generator function to read copy information from CSV file one row at
        a time.

        This CSV contains all information related to image/video files are stored. The rows of the CSV are
        (source-path, destination-path, 'is-copied').
        """
        with open(self._csv_file_path, 'r+', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # skip header row
            for row in reader:
                yield row

    def process_csv_and_rearrange_files(self):
        # Open CSV file for reading
        with open(self._csv_file_path, 'r') as file:
            # Create CSV reader object
            reader = csv.reader(file)
            # Skip header row
            next(reader)
            # Loop through each row
            for row in reader:
                source_path, dest_path, is_copied = row

                # Check if file was already copied
                if is_copied.lower() == 'yes':
                    continue

                # Copy the file
                success = self.move_or_copy_file(
                    src_path=source_path, dest_path=dest_path, do_copy=True)

                if not success:
                    continue

                # Open CSV file for writing
                with open(self._csv_file_path, 'w') as outfile:
                    # Create CSV writer object
                    writer = csv.writer(outfile)

                    # # Write header row
                    # writer.writerow(
                    #     ["Source File Path", "Destination File Path",
                    #      "Copied?"])
                    #

                    # Write modified rows to CSV
                    for r in reader:
                        if r == row:
                            writer.writerow([source_path, dest_path, 'YES'])
                        # else:
                        #     writer.writerow(r)
                        #

    @staticmethod
    def create_dir(dir_path) -> bool:
        """Create the destination directory if it doesn't exist"""
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
            logger.info(f"Created destination directory {dir_path}")
        return True

    @staticmethod
    def write_to_file(filename, content):
        with open(filename, 'w') as file:
            file.write(content)

    # @staticmethod
    # def read_from_file(filename):
    #     with open(filename, 'r') as file:
    #         content = file.read()
    #     return content


    # def reconnect_external_disk(self, drive_letter):
    #     volume_path = r'\\.\%s:' % drive_letter
    #
    #     handle = win32file.CreateFile(volume_path, win32file.GENERIC_READ,
    #                                   win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE,
    #                                   None, win32file.OPEN_EXISTING, 0, None)
    #     win32file.DeviceIoControl(handle, win32file.FSCTL_DISMOUNT_VOLUME, None, None)
    #     win32file.DeviceIoControl(handle, win32file.FSCTL_LOCK_VOLUME, None, None)
    #
    #     # Wait for a few seconds
    #     time.sleep(30)
    #
    #     win32file.DeviceIoControl(handle, win32file.FSCTL_UNLOCK_VOLUME, None, None)
    #     win32file.CloseHandle(handle)


    def move_or_copy_file(self, src_path, dest_path, do_copy=True) -> bool:
        max_attempt = 3
        for i in range(1, max_attempt+1):
            try:
                # shutil.copy or shutil.move returns file's destination.
                # This destination may be a directory.
                # import pdb;pdb.set_trace()
                self.create_dir(dir_path=os.path.dirname(dest_path))
                copy_function = shutil.copy if do_copy else shutil.move
                copy_function(src_path, dest_path)
                return True
            except Exception as e:
                logger.warning(f"Attempt {i}/{max_attempt}: source file={src_path} failed to {'copy' if do_copy else 'move'}")
                logger.warning(f"Error: {traceback.format_exc()}")
                time.sleep(5)

        logger.error(f"source file={src_path} failed to {'copy' if do_copy else 'move'}")
        self.write_to_file(filename=self._failed_relocation_path_log, content=src_path)
        return False

    # def move_file(self, src_path, dest_dir, do_copy=True):
    #     filename = os.path.basename(src_path)
    #     src_file_parent_dir = os.path.dirname(src_path)
    #     src_file_parent_folder_name = os.path.basename(src_file_parent_dir)
    #     dest_dir = os.path.join(dest_dir, src_file_parent_folder_name)
    #     create_dst_path(dest_dir)
    #     dest_file_path = os.path.join(dest_dir, filename)
    #     dest_base, dest_ext = os.path.splitext(dest_file_path)
    #     i = 1
    #     while os.path.exists(dest_file_path):
    #         dest_file_path = f"{dest_base}_{i}{dest_ext}"
    #         i += 1
    #         print(f"Duplicate file found: {filename}")
    #
    #
    #
    #         with open(failed_log_path, "w") as file:
    #             max_retries = 3
    #             print(
    #                 f"Failed to copy {src_path} to {dest_path}. {max_retries} attempts failed")
    #             file.write(f"{src_path}\n")
    #
    #     dest_file_list = []
    #     perform_oper(src_path, dest_file_path, do_copy)
    #     dest_file_list.append(dest_file_path)
    #
    #     # Move the corresponding JSON file as well
    #     src_json_path = src_path + ".json"
    #     if os.path.exists(src_json_path):
    #         dest_dir_path = os.path.dirname(dest_file_path)
    #         json_file_name = os.path.basename(src_json_path)
    #         dest_file_path = os.path.join(dest_dir_path, json_file_name)
    #         perform_oper(src_json_path, dest_file_path, do_copy)
    #         dest_file_list.append(dest_file_path)
    #
    #     return dest_file_list

    def is_file_image_type(self, src_file_path):
        exclude_file_types = {'.html', '.xml', '.txt', '.json'}
        if os.path.splitext(src_file_path)[1].lower() in exclude_file_types:
            return False
        return True

    def get_src_dst_path(self, src_path, dest_dir) -> dict:
        """Don't know at this stage, what I might return more, so returning dict.
        This way, it will not break any existing feature if something new gets added
        in the returned dict"""
        filename = os.path.basename(src_path)
        src_file_parent_dir = os.path.dirname(src_path)
        src_file_parent_folder_name = os.path.basename(src_file_parent_dir)
        dest_dir = os.path.join(dest_dir, src_file_parent_folder_name)

        dest_file_path = os.path.join(dest_dir, filename)

        # dest_base, dest_ext = os.path.splitext(dest_file_path)
        # i = 1
        # while os.path.exists(dest_file_path):
        #     logger.info(f"Duplicate file found: {dest_file_path}")
        #     dest_file_path = f"{dest_base}_{i}{dest_ext}"
        #     i += 1

        return {
            'src_path': src_path,
            'dst_path': dest_file_path
        }

    def traverse_directory_tree(self, src_path):
        """Define a function to recursively traverse the directory tree"""
        # Loop through all files and directories in the current directory
        for file_name in os.listdir(src_path):
            file_path = os.path.join(src_path, file_name)
            if os.path.isfile(file_path):
                if self.is_file_image_type(src_file_path=file_path):
                    src_dst_path_dict = self.get_src_dst_path(src_path=file_path, dest_dir=self._dest_dir_path)
                    file_src_path, file_dst_path = src_dst_path_dict['src_path'],  src_dst_path_dict['dst_path']

                    self.write_row_to_csv(
                        source_path=file_src_path, dest_path=file_dst_path,
                        # pay close attention to the value of 'is_copied', it's 'no'.
                        # This will be written in the CSV file.
                        is_copied='NO'
                    )
                logger.debug(f"skipping not-image type file: {file_path}")

            elif os.path.isdir(file_path):
                # Recursively traverse the sub-directory
                self.traverse_directory_tree(src_path=file_path)

    def reindex_csv(self):
        try:
            shutil.rmtree(path=self._dest_dir_path)
        except Exception as e:
            logger.error(f'failed to delete target directory: '
                         f'{self._dest_dir_path}')
            # logger.error(f'Exception: {traceback.format_exc()}')

        for src_dir_path in self.src_dir_path_list:
            self.traverse_directory_tree(src_path=src_dir_path)

    def get_user_input(self):
        intentional_messing_around = 0
        if not os.path.exists(path=self._dest_dir_path):
            return 'y'

        while True:
            print("***************************************************************")
            print(f"You are going to delete the target directory: {self._dest_dir_path}.")
            print("This operation is irreversible.")
            print("***************************************************************")
            response = input(f"Do you want to continue:? (y/n): ").lower()
            if response in {'y', 'n'}:
                return response

            intentional_messing_around += 1
            if intentional_messing_around > 3:
                print("Stop, you will lose this game... It's endless darkness here. "
                      "Now try again")
            if intentional_messing_around > 10:
                sys.exit("Now, also re-execute the application again!")

            print("Invalid input. Please enter 'y' or 'n'.")

    def rearrange_multimedia_resources(self):
        # Traverse the directory tree starting from the root directory
        # user_input = self.get_user_input()
        user_input = 'y'
        self.create_dir(dir_path=self._dest_dir_path)
        import pdb;
        pdb.set_trace()
        if user_input == 'y':
            self.reindex_csv()

        self.process_csv_and_rearrange_files()


rearrange_Gphoto = RearrageGooglePhotoBackup()
rearrange_Gphoto.rearrange_multimedia_resources()






