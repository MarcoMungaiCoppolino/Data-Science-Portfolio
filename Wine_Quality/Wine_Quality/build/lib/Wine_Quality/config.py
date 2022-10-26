# config.py

# In projectname/projectname/config.py, we place in special paths and variables 
# that are used acrossed the project. 
# Then, in our notebooks, we can easily import these variables and not worry 
# about custom strings littering our code. 
"""
from pathlib import Path  # pathlib is seriously awesome!

data_dir = Path('/path/to/some/logical/parent/dir')
data_path = data_dir / 'my_file.csv'  # use feather files if possible!!!

customer_db_url = 'sql:///customer/db/url'
purchases_db_url = 'sql:///purchases/db/url'"""