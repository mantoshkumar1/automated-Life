import os
import csv
import time
# import win32file
import shutil
from utility.logger_util.setup_logger import logger


class BackupGooglePhoto:
    def __init__(self, src_dir_path_list, dest_dir_path: str):
        #
        # list all the parent directories of your video/image files.
        self.src_dir_path_list = src_dir_path_list

        #
        # this is where, your processed files will be stored.
        self._dest_dir_path = dest_dir_path

        #
        # This is the CSV file where all the records of the image/video images will
        # be stored. This CSV is the most important part of this application. In this
        # CSV file, we write the source path of each video/image files with their
        # supposedly calculated destination path. And the fourth column of this CSV is
        # "is rearranged". While recursively  traversing the source directory path, we
        # will write "no" for each traversed videos/image files.
        # Later on, when we will start migrating files from one place to another,
        # then we will write "yes" for each video/image files. This was necessary
        # because external hard-disks kept crashing due to excess memory read and write.
        #
        # to write into file: use 'write_row_to_csv'
        # to read from this file: use 'read_row_from_from_csv'
        self._csv_file_path = os.path.join(self._dest_dir_path, "file_indices.csv")

    def write_row_to_csv(self, source_path, dest_path, file_size, is_rearranged):  # being used
        """Function to write copy information to CSV file"""
        # By setting newline='' when opening the file, we are telling Python to use
        # the default line terminator, which is the newline character.
        with open(self._csv_file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                # Write header row if file is empty
                writer.writerow(
                    ["Source File Path", "Destination File Path", "File size (MB)", "Is rearranged"])
            writer.writerow([source_path, dest_path, file_size, is_rearranged])

    @staticmethod
    def wait_until_relocation(src_path, dst_path):  # being used
        # Get the initial size of the source file
        src_size = os.path.getsize(src_path)

        # Wait until the [size of the Relocated file == size of Source file]
        while True:
            dst_size = os.path.getsize(dst_path)
            if dst_size >= src_size:
                break
            time.sleep(30)

    def create_temp_file(self, file_path: str):
        file_name = f'copy_of_{os.path.basename(file_path)}'
        destination_file_path = os.path.join(self._dest_dir_path, file_name)
        shutil.copy2(file_path, destination_file_path)
        return destination_file_path

    def process_csv_and_rearrange_files(self, do_copy: bool = True):  # being used
        """
        :param do_copy: True if copy; False if move.
        :return:
        """
        temp_csv_file = self.create_temp_file(self._csv_file_path)
        with open(self._csv_file_path, 'r') as csv_file, \
                open(temp_csv_file, 'w', newline='') as temp_csv:
            reader = csv.reader(csv_file)
            writer = csv.writer(temp_csv)

            for row in reader:
                src_path = row[0]
                dest_path = row[1]
                file_size = row[2]
                is_relocated = row[3]

                if is_relocated.lower() == 'no':
                    is_relocated = 'yes'

                    if do_copy:
                        self.copy_path(src_path, dest_path)
                    else:
                        self.move_path(src_path, dest_path)

                updated_row = [src_path, dest_path, file_size, is_relocated]
                writer.writerow(updated_row)

        self.move_path(temp_csv_file, self._csv_file_path)
        print(f"Relocation status updated and saved to '{self._csv_file_path}'.")

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

    @staticmethod
    def is_file_storable(src_file_path):  # being used
        excluded_extensions = {'.html', '.xml', '.txt', '.json', '.pdf'}
        file_extension = os.path.splitext(src_file_path)[1].lower()
        return file_extension not in excluded_extensions

    @staticmethod
    def get_files_and_folders(directory: str) -> list:  # being used
        paths = []

        for root, dirs, files in os.walk(directory):
            for dir in dirs:
                subfolder_path = os.path.join(root, dir)
                paths.append(subfolder_path)

            for file in files:
                file_path = os.path.join(root, file)
                paths.append(file_path)

        return paths

    def recursive_directory_traverse_and_index(self, src_path, initial_src_dir):  # being used
        """Define a function to recursively traverse the directory tree and build the
        indices of source files in a CSV

        :param src_path:os.listdir will throw NotADirectoryError if it's not a directory
        :param initial_src_dir:
        """
        if os.path.isfile(src_path):
            file_src_path = src_path
            if self.is_file_storable(file_src_path):
                file_size = os.path.getsize(file_src_path) / 1000000  # MB
                file_relative_path = os.path.relpath(file_src_path, initial_src_dir)
                file_dest_path = os.path.join(self._dest_dir_path, file_relative_path)

                self.write_row_to_csv(
                    source_path=file_src_path, dest_path=file_dest_path,
                    # pay close attention to the value of 'is_rearranged', it's
                    # 'no'. This will be written in the CSV file.
                    file_size=file_size, is_rearranged='no'
                )

            return

        for path in self.get_files_and_folders(directory=src_path):
            self.recursive_directory_traverse_and_index(path, initial_src_dir)

    @staticmethod
    def buffered_file_copy(source_file, destination_file, buffer_size=50):  # being used
        """
        Copies a file from the source path to the destination path using a buffered
        approach.


        Why Buffered Approach:
        The buffered approach is employed to efficiently handle large files by reading
        and writing the file in manageable chunks. This approach offers several
        advantages:

        1. Memory Efficiency: By reading and writing the file in smaller chunks, the
        buffered approach reduces the memory footprint required during the file copy
        operation. It prevents excessive memory consumption, particularly when dealing
        with large files, and helps avoid system slowdowns due to high memory usage.

        2. Performance Optimization: The buffered approach improves overall performance
        by mitigating potential bottlenecks associated with disk I/O operations. By
        controlling the buffer size, you can find an optimal balance that maximizes
        copying speed without overwhelming system resources.

        3. Flexibility and Adaptability: The buffer size can be adjusted based on the
        specific requirements of your system and the characteristics of the files being
        processed. This flexibility allows you to optimize the file copy operation for
        your particular environment, hardware, and file sizes.

        :param source_file: (str) Path to the source file to be copied.
        :param destination_file: (str) Path to the destination file.
        :param buffer_size: (int) Buffer size in MB for reading and writing the file.
        :raises: FileNotFoundError: If the source file does not exist.
        """
        target_dir = os.path.dirname(destination_file)
        os.makedirs(target_dir, exist_ok=True)

        buffer_size = buffer_size * 1024 * 1024  # MB
        with open(source_file, 'rb') as src, open(destination_file, 'wb') as dest:
            while True:
                buffer = src.read(buffer_size)
                if not buffer:
                    break
                dest.write(buffer)

    @staticmethod
    def delete_path(path):  # being used
        try:
            os.remove(path) if os.path.isfile(path) else os.rmdir(path)
        except OSError as e:
            print(f"Error occurred while deleting {path}: {e}")

        # wait until path is deleted (deletion may take time)
        while os.path.exists(path):
            time.sleep(10)

    @staticmethod
    def copy_path(src_path, dest_path):  # being used
        try:
            BackupGooglePhoto.buffered_file_copy(src_path, dest_path)
            shutil.copystat(src_path, dest_path)
        except OSError as e:
            print(f"Error occurred while copying {src_path}: {e}")

        if os.path.isfile(dest_path):
            BackupGooglePhoto.wait_until_relocation(src_path, dest_path)

    @staticmethod
    def move_path(src_path, dest_path):  # being used
        try:
            BackupGooglePhoto.buffered_file_copy(src_path, dest_path)
        except OSError as e:
            print(f"Error occurred while moving {src_path}: {e}")

        if os.path.isfile(dest_path):
            BackupGooglePhoto.wait_until_relocation(src_path, dest_path)

        BackupGooglePhoto.delete_path(src_path)

    def index_source_files(self):  # being used
        self.delete_path(self._csv_file_path)
        for src_dir_path in self.src_dir_path_list:
            self.recursive_directory_traverse_and_index(src_path=src_dir_path,
                                                        initial_src_dir=src_dir_path)

    def rearrange_multimedia_resources(self, do_indexing=True, do_copy=True):  # being used
        """

        :param do_indexing:
        :param do_copy: True if copy; False if move.
        :return:
        """
        os.makedirs(self._dest_dir_path, exist_ok=True)

        if do_indexing:
            self.index_source_files()

        self.process_csv_and_rearrange_files(do_copy=do_copy)
