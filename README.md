# Google Maps Scraper UI

## Description
Google Maps Scraper UI is a graphical user interface designed to simplify the use of the powerful [Google Maps Scraper](https://github.com/gosom/google-maps-scraper) developed by [gosom](https://github.com/gosom). This tool allows you to visually select business categories and locations, configure search parameters, and manage data extraction jobs intuitively, without needing to use the command line.

## How to Use

### Prerequisites

1.  **Start the Google Maps Scraper API**
    * Navigate to the `API` folder included in this repository.
    * Run the `.exe` executable file.
    * A command-line (CMD) window will open, and the API will start automatically.
    * The API will be accessible at `http://localhost:8080` (or the port indicated in the CMD window).
    * **IMPORTANT**: Do not close the command-line window during the entire process. It must remain open for the API to function.

2.  **Verify the API is Running**
    * Open your web browser and navigate to the address from the command-line window (e.g., `http://localhost:8080`).
    * You should see the web interface of the Google Maps Scraper.
    * **NOTE**: You do not need to modify any settings from this web interface. All configuration will be handled through our desktop application.

### Using the Google Maps Scraper UI

1.  **Launch the Application**
    > For the best experience, it is recommended to use the application in full-screen mode.

    * Run `scraper_gui.py`.
    * The graphical user interface will open, displaying several tabs.

2.  **General Configuration (Configuration Tab)**

     ![Configuration Tab](images/config_tab.png)
    * **API Host**: Keep the default value (`http://localhost:8080`) or adjust it if the API is running on a different port.
    * **Job Name**: Enter a descriptive name for your extraction job.
    * **Radius (meters)**: Define the search radius around each location (e.g., `10000` for 10km).
    * **Depth**: Specify how many results you want to extract (higher values yield more results but take longer).
    * **Max Time (minutes)**: Set a time limit for each job.
    * **Wait Time (minutes)**: Set the maximum time to wait for a job to finish.

4.  **Select Categories and Keywords (Categories & Keywords Tab)**
    ![Categories Tab](images/categories_tab.png)
    * Check the boxes for the business categories you want to search for.
    * Use the "Select All" or "Deselect All" buttons for convenience.
    * The keywords associated with the selected categories will appear in the list on the right.
    * **Add New Category**: You can create new categories using the form on the right.
    * **Add Keywords to Category**: You can add new keywords to an existing category.

5.  **Select Locations (Locations Tab)**
    ![Locations Tab](images/locations_tab.png)
    * Check the boxes for the locations where you want to search.
    * Click "View Selected Locations Info" to see detailed information for the chosen locations.
    * **Add New Location**: You can add new locations using the form on the right.
    * If you need coordinates, use the "Open Map to Get Coordinates" button.

6.  **Summary and Execution (Execution Tab)**
    ![Execution Tab](images/execution_tab.png)
    * Click "Update Summary" to review a summary of the job you are about to run.
    * Carefully check all the configured parameters.
    * When ready, click "Run Job".
    * Confirm the execution when prompted.
    * The progress and logs will be displayed at the bottom.

7.  **Monitor the Execution**
    * Status messages will appear in the logs area.
    * You can cancel the execution at any time with the "Cancel" button.
    * Upon completion, you will be notified of the total number of completed jobs.
    * **IMPORTANT**: Do not start a new job until the UI confirms that the current job has been successfully submitted to the API.

8.  **Download Results**
    * **IMPORTANT**: The Google Maps Scraper CMD window must remain open.
    * **CSV Files**: The results for each job are saved as CSV files in the `API/webdata` directory.
    * You can also download them directly from the web interface at `http://localhost:8080`. From there, you can view and download the results once they are ready (status will be 'ok' and highlighted in green). If the status is 'Working' or 'pending', the job is still in progress.
    * **NOTE**: Do not close the CMD window until you have downloaded all your results.

## Installation

### 1. Install the Google Maps Scraper API

#### Option 1: Use the Included Executable (Recommended)
1.  The Google Maps Scraper executable is already included in the `API` folder of this repository.
2.  Simply run the `.exe` file within that folder to start the API.
3.  A command-line window will open, and the API will launch automatically.
4.  No further configuration is necessary.

#### Option 2: Download the Latest Version (If you need to update)
If you prefer to download the latest version or the included executable does not work:

1.  Download the latest release of Google Maps Scraper from [GitHub](https://github.com/gosom/google-maps-scraper/releases/tag/v1.8.0).
2.  Unzip the downloaded file into a folder of your choice.
3.  Run the included executable:
    * On Windows: Double-click the `.exe` file.
    * On macOS/Linux: Use the command `./google-maps-scraper`.
4.  A command-line window will open, and the API will start automatically.
5.  The API will be available at `http://localhost:8080` (or the port shown in the CMD).

**IMPORTANT**: Keep the command-line window open throughout the entire process.

### 2. Install the Google Maps Scraper UI

1.  Download the files from this repository.
2.  Ensure you have Python 3.6 or higher installed.
3.  Install the required dependencies:
    ```bash
    pip install tkinter requests
    ```
4.  Create the necessary folders if they do not exist:
    ```bash
    mkdir -p keywords location
    ```
5.  Run the application:
    ```bash
    python scraper_gui.py
    ```

## File Structure

-   `scraper_gui.py`: The main application file containing the graphical user interface.
-   `keywords/`: A directory containing text files with keywords, organized by category.
-   `location/`: A directory containing text files with location information (coordinates and zoom level).
-   `API/`: A directory containing the Google Maps Scraper executable.

## Common Use Cases

### 1. Searching for Restaurants in Madrid

To find all restaurants in Madrid:

1.  In the **Configuration** tab:
    * Set the radius to `10000` meters.
    * Set the depth to `15`.
    * Name the job "Restaurants_Madrid".

2.  In the **Categories & Keywords** tab:
    * Select "restaurants" or create a new category.
    * Ensure keywords like "restaurant", "food", "dining", etc., are included.

3.  In the **Locations** tab:
    * Select "Madrid" or create a new location with Madrid's coordinates.
    * If it doesn't exist, you can create it with this data:
        * Name: Madrid
        * Zoom: 12
        * Latitude: 40.4167754
        * Longitude: -3.7037902

4.  In the **Execution** tab:
    * Update the summary to verify the settings.
    * Run the job.
    * Wait for it to finish and go to `http://localhost:8080` to download the results.

### 2. Searching for Multiple Services Across Various Locations

To search for plumbers, electricians, and carpenters in several cities:

1.  In the **Categories & Keywords** tab:
    * Select the categories: "plumbing", "electricians", and "carpentry".
    * Create these categories if they don't already exist.

2.  In the **Locations** tab:
    * Select multiple locations of interest (e.g., Valencia, Barcelona, Seville).

3.  In the **Execution** tab:
    * You will see that multiple jobs will be generated (one for each combination of category and location).
    * For example: 3 categories × 3 locations = 9 jobs.

This approach allows you to gather comparative data on different services across various geographic areas in a single operation.

### 3. Specific Data Extraction for Market Research

For more detailed market analysis:

1.  Create highly specific categories:
    * For example: "vegetarian_restaurants", "24h_gyms", "organic_stores".
    * Add precise keywords that target the exact type of business.

2.  Adjust the depth:
    * Use higher values (15-20) for more exhaustive results.
    * Keep in mind that higher values will take longer to process.

3.  Refine the radius:
    * For dense urban areas, a smaller radius (e.g., 5000m) may be sufficient.
    * For rural areas or regional searches, increase the radius (e.g., 20000m or more).

With this data, you can identify market niches, analyze competition, and uncover business opportunities with precision.

## Tips for Better Results

-   **Be specific with your keywords**: The more precise they are, the better the results.
-   **Balance the depth**: A very high depth will yield more results but will take more time.
-   **Divide large areas**: For very large cities, consider dividing them into zones and running separate searches.
-   **Check partial results**: You can visit `http://localhost:8080` while jobs are running to see partial results.
-   **Save your configurations**: Note down the settings that yield good results to reuse them in the future.

## Credits and Acknowledgements

This graphical interface is a companion tool for the excellent [Google Maps Scraper](https://github.com/gosom/google-maps-scraper) developed by [gosom](https://github.com/gosom). The original scraper provides a robust API for extracting data from Google Maps, while this interface makes it accessible to non-technical users.

Special thanks to:
-   The original author of Google Maps Scraper for creating and maintaining such a useful tool.
-   All contributors who have helped improve this project.
-   The user community for providing valuable feedback.

## Legal Disclaimer

This software is provided "as is", without warranty of any kind. Use this tool in accordance with Google's terms of service and the applicable laws in your jurisdiction. Data scraping may be subject to legal restrictions in some cases.

