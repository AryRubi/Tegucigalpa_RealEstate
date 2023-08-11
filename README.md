
# Real Estate Data Scraper for Tegucigalpa, Honduras

## Introduction

This project is focused on filling a significant data gap in the real estate domain of Tegucigalpa, Honduras. In the absence of pre-built datasets, the project scrapes information from various real estate websites using Python scripts. AWS services, including Lambda and S3, have been instrumental in scheduling and automating the tasks of data extraction, transformation, and cleaning. The processed data is then visualized in a Power BI dashboard, offering a comprehensive view of trends and patterns in real estate. This dashboard serves as a valuable tool for understanding real estate dynamics in the region.

## Note on AWS and Local Execution

The current project is executed on AWS for automation and scalability. However, the files uploaded to this GitHub repository are run locally. Therefore, some configurations and dependencies specific to the AWS environment may not be present in this repository.

## Project Structure

### Web Scraping

The web scraping codes available in this repository don't have the real URLs. The actual URLs have been kept private for privacy reasons, to maintain the secrecy of the source webpages.

### Data Transformation

The transformed data is saved as CSV files in the `housing3` folder. The CSV files in the `transform` folder are only found in the `housing3` folder, as the other two folders contain URLs, and it is intended to keep the source webpages secret.

## Getting Started

1. **Clone the repository**: Clone this repository to your local machine and navigate to the project directory.
2. **Install Dependencies**: Run `pip install -r requirements.txt` to install all necessary dependencies.
3. **Configuration**: Update the configuration files with your local settings.
4. **Run the Scripts**: Execute the Python scripts to start scraping and transforming the data.

## Visualization with Power BI

The processed data can be visualized in a Power BI dashboard. You can click the following link to see it: [Link text Here]([https://link-url-here.org](https://app.powerbi.com/view?r=eyJrIjoiZmU2MTM5OTktMjYxOS00MDM3LWI5YTEtNTI2YTU1YjA5ODUzIiwidCI6IjgwZjQ1ODhmLTllY2EtNGRjZC1hMzQwLTgyMDFmYWEzNTAyMCIsImMiOjl9))

## Contributing

If you have any suggestions or improvements, feel free to open an issue or submit a pull request.

## Contact

For any further questions or inquiries, please reach out via [email](mailto:ary.rubi@hotmail.com).

---

*Disclaimer: This repository and its contents are intended for educational and informational purposes. Always comply with the terms and conditions of the websites you are scraping.*
