from typing import Any
import os

class CSVMaker:
    def __init__(self):
        pass

    def column_writer(self, data: list, file: str) -> str:
        """
        Write the data to a CSV file.
        Args:
            data (list): The data to be written to the CSV file.
            file (str): The path to the CSV file.
        Returns:
            str: The path to the CSV file.
        """

        if not data:  # Check if the data list is empty
            print("No data provided to write.")
            return file  # You might want to handle this differently

        file = os.path.abspath(file)
        with open(file, 'w') as f:
            if type(data[0]) == list:
                for line in zip(*data):
                    f.write(','.join(str(x) for x in line) + '\n')
            else:
                for line in data:
                    if isinstance(line, (list, tuple)):
                        f.write(','.join(str(x) for x in line) + '\n')
                    else:
                        f.write(str(line) + '\n')  # Treat single values (e.g., int or float) correctly

        return file

