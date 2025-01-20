# Copyright 2024 State Cloud.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""markdown_utils"""
import os


class MarkdownTableManager:
    """
    Manages Markdown tables in a specified file, allowing loading, modification, and saving of table data in Markdown format.
    It supports loading existing tables from the file, adding new tables, and saving changes back to the file.
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.tables = {}
        if os.path.exists(file_path):
            self._load_existing_tables()

    def _load_existing_tables(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            sections = content.split('\n\n')
            for section in sections:
                lines = section.strip().split('\n')
                if len(lines) < 2:
                    continue
                header_line = lines[1]
                header_cells = header_line.strip('|').split('|')
                headers = [cell.strip() for cell in header_cells]
                table_name = lines[0].strip('# ')
                table = MarkdownTable()
                table.headers = headers
                # 0926 fix: make sure no spaces before and after row
                table.rows = [[item.strip() for item in line.strip('|').split('|')] for line in lines[3:]]
                self.tables[table_name] = table

    def get_table(self, table_name, overwrite=False):
        """
        Retrieves the table with the specified name. If the table doesn't exist or overwrite is requested, a new table is created.
        """
        if table_name not in self.tables or overwrite:
            self.tables[table_name] = MarkdownTable()
        return self.tables[table_name]

    def save_to_file(self):
        """
        Saves all tables to the specified file in markdown format.
        Each table is written with its name followed by its content.
        """
        with open(self.file_path, 'w', encoding='utf-8') as file:
            for table_name, table in self.tables.items():
                file.write(table.to_markdown(table_name))
                file.write('\n\n')


class MarkdownTable:
    """A class that represents a Markdown table with headers and rows. 
    It provides methods to add headers, rows, and columns, 
    as well as convert the table into a markdown formatted string."""
    def __init__(self):
        self.headers = []
        self.rows = []

    def add_column(self, header, content=None):
        """Adds a new column to the table with the given header and optional content."""
        if content is None:
            content = []
        self.headers.append(header)
        for i, row in enumerate(self.rows):
            if i < len(content):
                row.append(content[i])
            else:
                row.append("")
        for i in range(len(self.rows), len(content)):
            new_row = [""] * (len(self.headers) - 1)
            new_row.append(content[i])
            self.rows.append(new_row)

    def add_row(self, content=None):
        """Adds a new row to the table with the provided content."""
        if content is None:
            content = []
        content = list(map(str, content))
        new_row = content + [""] * (len(self.headers) - len(content))
        self.rows.append(new_row)

    def add_header(self, headers):
        """Adds new headers to the table."""
        self.headers.extend(headers)
        for row in self.rows:
            row.extend([""] * (len(headers) - len(row)))

    def add_columns_from_dict(self, columns_dict):
        """Adds multiple columns from a dictionary."""
        for header, content in columns_dict.items():
            self.add_column(header, content)

    def to_markdown(self, table_name=None):
        """Converts the table into a markdown formatted string."""
        markdown = f"### {table_name}\n" if table_name else ""
        markdown += "| " + " | ".join(self.headers) + " |\n"
        markdown += "| " + " | ".join(["---"] * len(self.headers)) + " |\n"
        for row in self.rows:
            markdown += "| " + " | ".join(row) + " |\n"
        return markdown


if __name__ == '__main__':
    _table = MarkdownTable()
    _table.add_header(["Name", "Age"])
    _table.add_row(["Alice", "30"])
    _table.add_row(["Bob", "25"])
    _table.add_column("City", ["New York", "Los Angeles"])
    print(_table.to_markdown())
