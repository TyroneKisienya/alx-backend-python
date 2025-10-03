# MySQL CSV Data Importer

A Python script that reads user data from a CSV file and imports it into a MySQL database, handling duplicates and missing values gracefully.

## Features

- Automatic database and table creation
- CSV data import with validation
- Duplicate prevention using primary keys
- Automatic UUID generation for missing user IDs
- Skip rows with missing required fields
- Environment variable configuration support

## Prerequisites

- Python 3.x
- MySQL Server
- Required Python packages:
  - `mysql-connector-python`

## Installation

1. Install the required Python package:
```bash
pip install mysql-connector-python
```

2. Ensure you have a MySQL server running and accessible.

## Configuration

The script uses environment variables for database configuration. You can set these or use the defaults:

| Environment Variable | Default Value | Description |
|---------------------|---------------|-------------|
| `MYSQL_HOST` | `localhost` | MySQL server hostname |
| `SERVERPORT` | `3306` | MySQL server port |
| `MYSQL_USER` | `ALX` | Database username |
| `MYSQL_PASSWORD` | `password` | Database password |

### Setting Environment Variables

**Linux/Mac:**
```bash
export MYSQL_HOST=localhost
export MYSQL_USER=your_username
export MYSQL_PASSWORD=your_password
export SERVERPORT=3306
```

**Windows (Command Prompt):**
```cmd
set MYSQL_HOST=localhost
set MYSQL_USER=your_username
set MYSQL_PASSWORD=your_password
set SERVERPORT=3306
```

## CSV File Format

The script expects a CSV file named `user_data.csv` in the same directory with the following columns:

- `user_id` (optional - auto-generated if missing)
- `name` (required)
- `email` (required)
- `age` (required)

### Example CSV Format

```csv
user_id,name,email,age
123e4567-e89b-12d3-a456-426614174000,John Doe,john@example.com,25.50
,Jane Smith,jane@example.com,30.00
```

## Database Schema

The script creates the following:

**Database:** `ALX_prodev`

**Table:** `user_data`

| Column | Type | Constraints |
|--------|------|-------------|
| user_id | CHAR(50) | PRIMARY KEY, NOT NULL |
| name | VARCHAR(100) | NOT NULL |
| email | VARCHAR(250) | NOT NULL |
| age | DECIMAL(5,2) | NOT NULL |

## Usage

1. Place your `user_data.csv` file in the same directory as the script.

2. Run the script:
```bash
python3 script_name.py
```

or make it executable:
```bash
chmod +x script_name.py
./script_name.py
```

## How It Works

1. **Connect to MySQL Server** - Establishes connection using configured credentials
2. **Create Database** - Creates `ALX_prodev` database if it doesn't exist
3. **Connect to Database** - Reconnects specifically to the `ALX_prodev` database
4. **Create Table** - Creates `user_data` table if it doesn't exist
5. **Read CSV** - Loads data from `user_data.csv`
6. **Insert Data** - Imports rows while:
   - Generating UUIDs for missing user_ids
   - Skipping rows with missing name or email
   - Preventing duplicate entries by checking existing user_ids
   - Handling errors gracefully

## Output Messages

The script provides feedback during execution:

- `Connection successful` - MySQL server connection established
- `ALX_prodev created successfully` - Database created or already exists
- `Table created successfully` - Table created or already exists
- `Skipping the row {...} with missing values` - Row skipped due to missing required fields
- `Failed to insert row: ...` - Error during insertion of a specific row
- `Inserted X new rows` - Summary of successful insertions
- `Done.` - Script completed successfully

## Error Handling

- Missing CSV file - Raises `FileNotFoundError`
- Database connection issues - Prints error and raises exception
- Invalid data types - Skips row and continues
- Duplicate user_ids - Skips duplicate entries
- Missing required fields (name/email) - Skips row with warning message

## Troubleshooting

**Connection Issues:**
- Verify MySQL server is running
- Check environment variables or default credentials
- Ensure MySQL user has CREATE and INSERT permissions

**CSV Not Found:**
- Verify `user_data.csv` exists in the script directory
- Check file name spelling (case-sensitive on Linux/Mac)

**Data Not Inserting:**
- Check CSV format matches expected columns
- Ensure required fields (name, email, age) are present
- Review console output for specific error messages

## Security Notes

- Never commit files containing passwords to version control
- Use environment variables for sensitive configuration
- Consider using `.env` files with `python-dotenv` for local development
- Ensure proper database user permissions (principle of least privilege)

## Author
Skai