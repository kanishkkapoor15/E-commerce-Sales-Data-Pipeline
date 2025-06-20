Over the past few days, I worked on designing and deploying a real-time data engineering pipeline — starting from a dummy API to storing structured data in an Amazon S3 bucket. Here’s a quick breakdown of what I accomplished:

🔹 Step-by-Step Journey:

📦 Designed a FastAPI Microservice to simulate eCommerce order data on-demand.
⚙️ Built a Kafka Producer to extract data from the API and publish it to a Kafka topic.
📥 Created a Kafka Consumer that listens and processes the real-time stream.
🔁 Streamed data with Apache Spark, consuming from Kafka and applying transformations.
☁️ Stored clean data into AWS S3, organizing it as structured .json files.
🛠️ Working to automate the entire workflow with Apache Airflow (Docker integration next!).

🛤️ This mini-project helped me solidify my concepts of:

Event streaming
Stream processing
Cloud storage integration
Real-world ETL pipeline design

👇 Here’s a visual flow of the architecture:

<img width="991" alt="Screenshot 2025-06-16 at 9 26 28 PM" src="https://github.com/user-attachments/assets/ee3cba86-bdca-4b60-9408-aebe2cd0e49e" />

💡 Technologies Used: Kafka · FastAPI · Apache Spark · Amazon S3 · Python · Airflow


