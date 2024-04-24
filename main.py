from web_functions import ams_df, karriere_df
import time


def jobs_scraping():
    print("Welcome to jobs_scraping for ams.at and karriere.at!")
    print(
        "Since the jobs on these Websites are located in Austria, only Austrian cities (written in German, e.g. Graz, Wien) are valid location inputs!"
    )
    print(
        "Job Names/Fields can also be written in English, e.g. Data Analyst, Data Science."
    )
    print(
        "You can choose from either of the websites and decide if the output should be printed in the terminal or saved as csv_file via providing a filename!"
    )
    waiting_seconds = 1.8  # Waiting for website to load.
    while True:
        decision = input("On which website do you want to see jobs? [ams,karriere]: ")
        while not (decision == "ams" or decision == "karriere"):
            print(
                f'The input {decision} was not valid. Pick either "ams" or "karriere"! '
            )
            decision = input(
                "On which website do you want to look for jobs? [ams,karriere]: "
            )
        job_field = input("Choose your job field, e.g. Data Science, Data Analyst: ")
        location = input(
            "Choose your desired Austrian location (written in German), e.g. Wien, Graz: "
        )
        filename = input(
            "Should the output be saved as a filename? If so, enter a filename, else just enter!: "
        )
        if decision == "karriere":
            karriere_df(job_field, location, waiting_seconds, filename)
        else:
            ams_df(job_field, location, waiting_seconds, filename)
        time.sleep(3.0)

        further = input("Do you want to continue? [y/n] ")
        if further != "y":
            break


def main():
    jobs_scraping()
    """location = "Steiermark"
    job = 'Data Science'
    waiting_seconds = 1.5
    ams_df(job, location, waiting_seconds, "ams.csv")
    karriere_df(job, location, waiting_seconds)"""


if __name__ == "__main__":
    main()
