## API Keys

The `keys.txt` file contains private API keys. Follow these steps to configure it:

1. **Create `keys.txt`**:
   - Copy `keys.template.txt` to `keys.txt`.
   - Replace the placeholder values in `keys.txt` with your actual API keys.

2. **Ensure Security**:
   - **Important**: Do not share `keys.txt` publicly. It contains sensitive information.

3. **Add `keys.txt` to `.gitignore`**:
   - Ensure `keys.txt` is listed in your `.gitignore` file to prevent it from being tracked by Git.

## Database Configuration

You need to configure the `DATABASE_URL` for your database connection. Follow these steps:

1. **Create `database.config`**:
   - Copy `database.config.template` to `database.config`.
   - Update the `DATABASE_URL` in `database.config` with your database connection details.

2. **Add `database.config` to `.gitignore`**:
   - Ensure `database.config` is listed in your `.gitignore` file to prevent it from being tracked by Git.

### Example `keys.template.txt`

```plaintext
# Replace with your actual API keys
your_api_key_1_here
your_api_key_2_here
.
.
.
