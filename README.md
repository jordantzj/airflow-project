**Data pipeline orchestration using Airflow hosted on EC2**

<img width="919" alt="Screenshot 2024-10-10 at 12 17 24 PM" src="https://github.com/user-attachments/assets/d3c873a9-f9a4-4d10-8d1e-408212969129">

In this project, I used Airflow to orchestrate a data pipeline where the Python scripts will extract comments from a Youtube video and then load it into a MongoDB collection. This app is being hosted on a Ubuntu EC2 instance.

**Instructions** (Assuming Airflow and Mongodb are installed, requirements can be found in requirements.txt)
1) Spin up your EC2 instance and edit your inbound rule to allow TCP connections from port 22 (for SSH), 27017 (for MongoDB), 8080 (for Airflow Webserver)
   a) Platform: Ubuntu
   b) Instance type: t2.medium
2) Copy the public address of your EC2 instance and paste it in the .env file which should be in the dags folder.
3) Get your Youtube data API key from here: https://developers.google.com/youtube/v3/getting-started (can be found in your Google Developers Console)
4) Enter API key in the .env file
   Example of your .env file:
   API_KEY ="AHFIHUIEFHU89345NJK5"
   IP_ADDRESS="10.326.131.5"
5) mkdir airflow to create the main folder of this project and clone this repo into the airflow folder (directory should be home/ubuntu/airflow/dags)
6) In the root directory, enter this command to start Airflow, "nohup airflow webserver --port 8080 > airflow-web.log 2>&1 & nohup airflow scheduler > airflow-scheduler.log 2>&1 &" and this command to start MongoDB., "sudo systemctl start mongod"
7) Create a connection in MongoDB compass, replace "localhost" with your EC2 instance public IP address.
8) Go to Airflow UI by typing "http//<EC2_IP_ADDRESS>:8080"
9) Trigger DAG in the Airflow UI and refresh your MongoDB to see the youtube comments :)

Here's a video for more clarity:
https://youtu.be/4s4Fx8_vMC4
