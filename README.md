# ETL Pipeline with Apache Airflow

## **Project Overview**
This repository demonstrates an ETL (Extract, Transform, Load) pipeline built with Apache Airflow to automate the process of fetching school data from an API, transforming the data, and loading it into a PostgreSQL database. 

## **Key Features**
- **Data Extraction**: Fetch school data from the [School Data API](https://api-sekolah-indonesia.vercel.app/sekolah?page=1&perPage=5000).
- **Data Transformation**:
  - Filter for SMA schools with status "N" (National/State-owned).
  - Add a new `school_address` column combining school name and address.
  - Convert `lintang` (latitude) and `bujur` (longitude) to numeric values.
  - Remove rows with invalid or missing coordinates.
- **Data Loading**: Insert transformed data into a PostgreSQL database, creating the target table if it does not exist.
- **Automation**: Schedule daily execution of the ETL process using Apache Airflow.

## **Technologies Used**
- **Apache Airflow**: Workflow orchestration and task scheduling.
- **PostgreSQL**: Target database for storing the transformed data.
- **Python**: Task definitions, data extraction, and transformations.

## **ETL Pipeline Workflow**
1. **Extract**: Fetch raw school data in JSON format from the API.
2. **Transform**: Clean, filter, and format the data using Python and Pandas.
3. **Load**: Store the transformed data into a PostgreSQL database.

## **Airflow DAG Design**
The DAG consists of the following tasks:
- **fetch_data_from_api**: Extracts data from the API.
- **transform_data**: Applies transformations to clean and prepare the data.
- **load_data_to_database**: Loads the transformed data into PostgreSQL.

### **DAG Workflow**
```
fetch_data_from_api → transform_data → load_data_to_database
```

## **Setup and Installation**

### Prerequisites
- PostgreSQL database setup and running

### Steps
1. Clone this repository:
   ```
   git clone <repository-url>
   cd <repository-name>
   ```

2. Configure the PostgreSQL connection in Airflow:
   - Go to Airflow UI → Admin → Connections.
   - Add a new connection with ID `postgres` and provide the database details.

3. Deploy the DAG by placing the script in the Airflow `dags` folder.

4. Trigger the DAG from the Airflow UI to start the ETL process.

## **File Structure**
```
├── dags
│   ├── api_to_database_dag.py  # Airflow DAG script
├── README.md                   # Project documentation
```

## **API Information**
- **Endpoint**: [School Data API](https://api-sekolah-indonesia.vercel.app/sekolah)
- **Data Format**: JSON

## **Expected Outputs**
- A PostgreSQL table named `target_table` containing transformed data with the following columns:
  - `school_address`
  - `lintang` (latitude)
  - `bujur` (longitude)
  - Other relevant school details

## **Screenshots**
1. **DAG Testing in Airflow**
   ![DAG Testing](https://github.com/hijirdella/ETL-Pipeline-Airflow-School-API/blob/b50aae3448c98116a0190cdd2a5d843f41216085/Documentation/DAG%20Testing.jpg)

2. **Success Load in Database**
   ![Database Load](https://github.com/hijirdella/ETL-Pipeline-Airflow-School-API/blob/b50aae3448c98116a0190cdd2a5d843f41216085/Documentation/Success%20Load%20in%20Database.jpg)

3. **Transformed Data**
   ![Transformed Data](https://github.com/hijirdella/ETL-Pipeline-Airflow-School-API/blob/b50aae3448c98116a0190cdd2a5d843f41216085/Documentation/Transformed%20Data.jpg)

## **Benefits of the ETL Pipeline**
- Automates the data ingestion process for consistent updates.
- Ensures data quality through validation and transformations.
- Provides a scalable and modular workflow for future extensions.

## **Contributors**
- Hijir Della Wirasti
  - LinkedIn: [https://www.linkedin.com/in/hijirdella/](https://www.linkedin.com/in/hijirdella/)

## **Special Thanks to My Mentor**
- Mohamad Ikhsan Nurulloh: [https://www.linkedin.com/in/mohamad-ikhsan-nurulloh/](https://www.linkedin.com/in/mohamad-ikhsan-nurulloh/)


