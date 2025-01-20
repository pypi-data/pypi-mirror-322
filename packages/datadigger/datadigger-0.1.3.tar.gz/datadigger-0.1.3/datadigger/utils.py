# datadigger/utils.py
from typing import Union, Optional, List, Any
from bs4 import BeautifulSoup
import re
import pandas as pd
import csv
import os


def create_directory(directory_name: str) -> None:
    """
    Creates a directory if it doesn't already exist.
    
    Args:
    - directory_name (str): The name of the directory to create.

    Returns:
    - None
    """
    try:
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
    except OSError as error:
        print(f"Error: {error}")


def standardized_string(string: str = None) -> str:
    """
    Standardizes a string by:
    - Replacing `\n`, `\t`, and `\r` with spaces.
    - Removing HTML tags.
    - Replacing multiple spaces with a single space.
    - Stripping leading/trailing spaces.

    Args:
    - string (str, optional): The string to be standardized. Defaults to None.

    Returns:
    - str: The standardized string, or an empty string if input is None.
    """
    if string is not None:
        string = str(string)
        string = string.replace("\\n", " ").replace("\\t", " ").replace("\\r", " ")
        string = re.sub(r"<.*?>", " ", string)  # Remove HTML tags
        string = re.sub(r"\s+", " ", string)  # Collapse multiple spaces into one
        string = string.strip()  # Strip leading/trailing spaces
        return string
    else:
        print("None value is passed")
        return ""



def remove_common_elements(remove_in: Union[list, tuple, set] = None, remove_by: Union[list, tuple, set] = None) -> list:
    """
    Removes elements from `remove_in` that are present in `remove_by`.

    Args:
    - remove_in (Union[list, tuple, set], optional): The collection from which elements will be removed. Defaults to None.
    - remove_by (Union[list, tuple, set], optional): The collection containing elements to remove from `remove_in`. Defaults to None.

    Returns:
    - list: A list containing elements from `remove_in` that are not in `remove_by`.
    """
    if remove_in is not None and remove_by is not None:
        # Ensure both collections are sets for efficient difference operation
        set_a = remove_in
        set_b = remove_by

        if not isinstance(set_a, set):
            set_a = set(set_a)
        if not isinstance(set_b, set):
            set_b = set(set_b)

        set_a.difference_update(set_b)  # Remove elements from set_a that are in set_b
        return list(set_a)  # Return the result as a list

    else:
        missing_args = []
        if remove_in is None:
            missing_args.append('remove_in')
        if remove_by is None:
            missing_args.append('remove_by')

        print(f"Value not passed for: {', '.join(missing_args)}")
        return []


def save_to_csv(list_data: Optional[List[list]] = None, column_header_list: Optional[List[str]] = None, output_file_path: Optional[str] = None, sep: str = ",") -> None:
                
    """
    Saves data to a CSV file. If the file exists, it appends the data; otherwise, it creates a new file.
    
    Args:
    - list_data (Optional[List[list]], optional): The data to be saved in the CSV file. Defaults to None.
    - column_header_list (Optional[List[str]], optional): The column headers for the CSV file. Defaults to None.
    - output_file_path (Optional[str], optional): The path to the output CSV file. Defaults to None.
    - sep (str, optional): The delimiter used in the CSV file. Defaults to "," (comma).

    Returns:
    - None: This function doesn't return anything. It performs a side effect (writing to a file).
    """
    if list_data and column_header_list and output_file_path:
        try:
            # Check if the file exists
            if os.path.exists(output_file_path):
                # Append data to the file if it exists
                pd.DataFrame(list_data, columns=column_header_list).to_csv(output_file_path, index = False, header = False, sep = sep, encoding = "utf-8", quoting = csv.QUOTE_ALL, quotechar = '"', mode = "a")
                                                                            
            else:
                # Create a new file and write data
                pd.DataFrame(list_data, columns=column_header_list).to_csv(output_file_path, index = False, header = True, sep = sep, encoding = "utf-8", quoting = csv.QUOTE_ALL, quotechar = '"', mode = "w")
                                                                            
        except Exception as e:
            print(f"save_to_csv: {e.__class__} - {str(e)}")
    else:
        missing_args = []
        if list_data is None:
            missing_args.append('list_data')
        if column_header_list is None:
            missing_args.append('column_header_list')
        if output_file_path is None:
            missing_args.append('output_file_path')

        print(f"Data not saved due to missing arguments: {', '.join(missing_args)}")



def read_csv(csv_file_path: str, get_value_by_col_name: Optional[str] = None, filter_col_name: Optional[str] = None, inculde_filter_col_values: Optional[List[str]] = None, exclude_filter_col_values: Optional[List[str]] = None, sep: str = ",") -> Union[List[str], pd.DataFrame]:
             
    """
    Reads a CSV file and returns values from a specific column based on various filters.
    
    Args:
    - csv_file_path (str): Path to the CSV file.
    - get_value_by_col_name (Optional[str]): The column name from which to fetch values.
    - filter_col_name (Optional[str]): The column name to apply filters.
    - inculde_filter_col_values (Optional[List[str]]): List of values to include in the filter.
    - exclude_filter_col_values (Optional[List[str]]): List of values to exclude from the filter.
    - sep (str, optional): The delimiter used in the CSV file. Defaults to "," (comma).
    
    Returns:
    - Union[List[str], pd.DataFrame]: A list of values if filtering, or the full DataFrame if no filtering.
    """
    
    if not os.path.exists(csv_file_path):
        print("read_csv: csv_file_path does not exist.")
        return []
    
    urls = []
    
    try:
        # Try to read CSV with error handling and the specified separator
        df = pd.read_csv(csv_file_path, header=0, sep=sep, encoding='utf-8', on_bad_lines='skip', dtype=object).fillna("")
        
        if get_value_by_col_name and filter_col_name:
            # If we are filtering by include values
            if inculde_filter_col_values:
                for value in inculde_filter_col_values:
                    filtered_df = df[df[filter_col_name] == str(value)]
                    urls.extend(filtered_df[get_value_by_col_name].tolist())
            
            # If we are filtering by exclude values
            elif exclude_filter_col_values:
                for value in exclude_filter_col_values:
                    filtered_df = df[df[filter_col_name] != str(value)]
                    urls.extend(filtered_df[get_value_by_col_name].tolist())
        
        elif get_value_by_col_name and not filter_col_name:
            # If just getting values from a single column without filters
            urls.extend(df[get_value_by_col_name].tolist())
        
        elif not get_value_by_col_name and not filter_col_name:
            # If no filters or specific column is provided, return the entire DataFrame
            return df
        
        else:
            print("========= Arguments are not proper =========")
            return []
    
    except Exception as e:
        print(f"Error reading CSV: {str(e)}")
        return []

    # Return unique values (set removes duplicates) as a list
    return list(set(urls))



def process_json_list_to_dict(json_obj: list = None) -> Union[list, dict]:
    if isinstance(json_obj, list):
        for json_obj_value in json_obj:
            if isinstance(json_obj_value, dict):
                return json_obj_value
    else:
        return json_obj  

def get_json_content(json_obj: Union[list,dict] = None, keys: list = None) -> Any:
    """
    Extract values from a JSON object (dict or list) using a list of keys.

    Args:
    - json_obj (Union[dict, list]): The JSON object (either a dictionary or a list).
    - keys (List[str]): A list of keys to access nested values.

    Returns:
    - Any: The extracted value, or an empty string if not found. 
    """

    if json_obj is not None and keys is not None:
        for key in keys:
            try:
                if isinstance(json_obj, dict):
                    json_obj = json_obj[key]
                elif isinstance(json_obj, list):
                    json_obj = process_json_list_to_dict(json_obj=json_obj)
                    if isinstance(json_obj, dict):
                        json_obj = json_obj[key]
            except Exception as error:
                print(error)
                
        return standardized_string(json_obj) if isinstance(json_obj, (int, float, str)) else json_obj if json_obj else ""
    else:
        return ""


def get_selector_content(soup_obj: Optional[BeautifulSoup], css_selector_ele: Optional[str] = None, css_selector: Optional[str] = None, attr: Optional[str] = None ) -> Optional[Union[str, List[BeautifulSoup]]]:
    """
    Extracts content from a BeautifulSoup object based on CSS selectors and attributes.

    Parameters:
        soup_obj (Optional[BeautifulSoup]): The BeautifulSoup object to search in.
        css_selector_ele (Optional[str]): CSS selector to get a list of matching elements.
        css_selector (Optional[str]): CSS selector to get a single element's content.
        attr (Optional[str]): Attribute name to extract from the selected element.

    Returns:
        Optional[Union[str, List[BeautifulSoup]]]: Extracted content based on the specified criteria.
            - If `css_selector_ele` is provided, returns a list of elements.
            - If `css_selector` is provided with or without `attr`, returns text or attribute value.
            - If no specific selector or attribute is provided, returns the text content of the soup object.
            - Returns `None` if no matching elements are found or inputs are invalid.
    """
    if soup_obj is None:
        return None  # No soup object provided.

    try:
        # Return a list of matching elements if `css_selector_ele` is provided.
        if css_selector_ele is not None and css_selector is None and attr is None:
            return soup_obj.select(css_selector_ele)

        # Return the text content of the first matching element for `css_selector`.
        elif css_selector is not None and css_selector_ele is None and attr is None:
            element = soup_obj.select_one(css_selector)
            return standardized_string(element.text) if element else None

        # Return the value of the specified attribute for `css_selector`.
        elif css_selector is not None and attr is not None and css_selector_ele is None:
            element = soup_obj.select_one(css_selector)
            return standardized_string(element.get(attr, "")) if element else None

        # Return the value of the specified attribute from the `soup_obj` directly.
        elif attr is not None and css_selector_ele is None and css_selector is None:
            return standardized_string(soup_obj.get(attr, ""))

        # Return the text content of the entire `soup_obj` if no selectors or attributes are provided.
        elif attr is None and css_selector_ele is None and css_selector is None:
            return standardized_string(soup_obj.text)
        else:
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None



def save_file( directory: str = None, content: str = None, file_name: str = None, mode: str = "w", encoding: str = "utf-8" ) -> None:
    """
    Saves content to a file in the specified directory with the given file name.

    Args:
        directory (str, optional): The path to the directory where the file will be saved. Defaults to None.
        content (str, optional): The content to save in the file. Defaults to None.
        file_name (str, optional): The name of the file (including its extension). Defaults to None.
        mode (str, optional): The file open mode. Defaults to "w" (write mode).
                              Use "a" for appending to an existing file.
        encoding (str, optional): The encoding to use for the file. Defaults to "utf-8".

    Returns:
        None

    Raises:
        ValueError: If required arguments are missing or an invalid mode is provided.
        OSError: If there is an issue creating the directory or writing the file.
        Exception: For any other unexpected errors.
    """
    try:
        # Validate required arguments
        if directory is None:
            raise ValueError("The 'directory' argument must be provided.")
        if content is None:
            raise ValueError("The 'content' argument must be provided.")
        if file_name is None:
            raise ValueError("The 'file_name' argument must be provided.")

        # Ensure the mode is valid for text files
        if mode not in {"w", "a"}:
            raise ValueError(f"Invalid mode: {mode}. Allowed modes are 'w' (write) or 'a' (append).")

        # Ensure the directory exists
        os.makedirs(directory, exist_ok=True)

        # Create the full file path
        file_path = os.path.join(directory, file_name)

        # Write or append the content to the file
        with open(file_path, mode, encoding=encoding) as file:
            file.write(content)

        action = "appended to" if mode == "a" else "written to"
        print(f"Content successfully {action} the file: {file_path}")
    except ValueError as ve:
        print(f"Value Error: {ve}")
        raise
    except OSError as os_error:
        print(f"Directory or file operation failed: {os_error}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

def read_file(file_path: str, encoding: str = "utf-8") -> str:
    """
    Reads the content of a file and returns it as a string.

    Args:
        file_path (str): The full path to the file to read.
        encoding (str, optional): The encoding to use when reading the file. Defaults to "utf-8".

    Returns:
        str: The content of the file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        OSError: If there is an issue accessing the file.
        Exception: For any other unexpected errors.
    """
    try:
        # Ensure the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")

        # Read and return the file content
        with open(file_path, "r", encoding=encoding) as file:
            content = file.read()
            print(f"Content successfully read from: {file_path}")
            return content
    except FileNotFoundError as fnfe:
        print(f"File Not Found Error: {fnfe}")
        raise
    except OSError as os_error:
        print(f"File operation failed: {os_error}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise
