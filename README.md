# power10

Python scraper for the Power of 10 Athletics Results [website](https://www.thepowerof10.info/) utilising Pandas.

## Usage

1. Create and activate a new virtual environment:

    ```bash
    python -m venv .venv --prompt .
    ```

    ```bash
    source .venv/bin/activate
    ```

1. Install the required dependencies:

    ```bash
    python -m pip install -r requirements.txt
    ```

1. Specify the events, genders and years you want to scrape in the `main.py` script by updating the `required_events`, `required_genders` and `required_years` variables. The below example will scrape the 100m, 200m and 400m events for both male and female athletes in the year 2020:

    ```python
    required_events = [100, 200, 400]
    required_genders = ["W", "M"]
    required_years = [2020]
    ```

1. Run the script:

    ```bash
    python main.py
    ```

1. The results for each event will be saved to a CSV file in the `results` directory.

### Notes

Event, gender and year codes can be found by examining the url parameters of the Power of 10 [results page](https://www.thepowerof10.info/results/resultslookup.aspx).

For example, the following events correspond to the url parameters:
- 100m: 100
- 200m: 200
- 400m: 400
- 800m: 800
- 1500m: 1500
- 3000m: 3000
- 5000m: 5000
