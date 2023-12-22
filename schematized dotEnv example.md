# Schema example
This is an example of a schema file for a dotEnv file.

## Schema file
example with description

```
# dotEnv schema
# CliVersion: 0.1
# ---
# Name: example
# Description: example schema
# Version: 0.1
# Author: author
# License: MIT
# ---

# Header:       this is a Header to display in CLI
# Section:      this is a section
# Subsection:   this is a subsection
# Message:      this is a comment
# Space      <- this is a space


# Field:
# - Name:         this is a field name
# - Example:      this is an example value
# - Description:  this is a description
# - Hint:         this is a hint
# - Type:         this is a type
# - Required:     [True|False] this is a required field - default False
# - Regex:        this is a regex - default None
# - Generate:     [True|False] this is a generated value - default False
# - User:         [True|False] user input - default True
FIELD_NAME=Default_value
```

## Example of use
example with values

```
# dotEnv schema
# CliVersion: 0.1
# ---
# Name: Django Shop
# Description: Django Shop settings for production
# Version: 1.5
# Author: XYZ
# License: MIT
# ---
# Header:       Django Shop settings
# Section:      Database
# Subsection:   Postgres
# Field:
# Name:         Database name
# Example:      django_shop
# Description:  Name of the database
# Type:         String
# Required:     True
# Regex:        ^[a-zA-Z0-9_]*$
DB_NAME=django_shop_db

# Field:
# Name:         Database user
# Example:      django_shop_user
# Description:  Name of the database user
# Type:         String
# Required:     True
# Regex:        ^[a-zA-Z0-9_]*$
DB_USER=django_shop_user

# Field:
# Name:         Database password
# Description:  Password of the database user
# Type:         Password
# Generate:     True
DB_PASSWORD=django_shop_password

# Field:
# Name:         Database host
# Example:      localhost | 192.168.1.1 | domain.com
# Description:  Host of the database
# Type:         String
# Required:     True
# Regex:        ^[a-zA-Z0-9_]*$
DB_HOST=

# Section:      Email
# Subsection:   SMTP
# Field:
# Name:         Email host
# Example:      localhost
# Description:  Host of the email server
# Type:         String
# Required:     True
# Regex:        ^[a-zA-Z0-9_]*$
EMAIL_HOST=localhost

```