# English Retrieval Backend: RAG + MongoDB + Gemini 1.5 Pro + Semantic Router + Reflection


This demo will be presented at Google I/O Extended Surabaya 2024


- [Slide](https://docs.google.com/presentation/d/1-noqqG8xCfIzS3H1lmG6dpJ-xROcdM54rATWxe7cxhM/edit?usp=sharing)

- [Code](https://colab.research.google.com/drive/1WU_XGl4jGcrMQq-1zhDUsTDcpsVxflXD?usp=sharing) to build Vector Search
- [Code](https://colab.research.google.com/drive/1x4Yd7bRLbJoUePKF6pctncIvejrfkn3F?usp=sharing) to run RAG pipeline in Google Colab

![](https://storage.googleapis.com/mle-courses-prod/users/61b869ca9c3c5e00292bb42d/private-files/dd582970-3da7-11ef-bf69-71eafa46c86b-Screen_Shot_2024_07_09_at_11.00.59.png)


#### Chatbot Architecture

![](https://storage.googleapis.com/mle-courses-prod/users/61b869ca9c3c5e00292bb42d/private-files/f8928780-3da7-11ef-a9c5-539ef4fa11ba-Screen_Shot_2024_07_09_at_11.01.45.png)


#### Demo

![](https://storage.googleapis.com/mle-courses-prod/users/61b6fa1ba83a7e37c8309756/private-files/4e600bd0-48e6-11ef-bf69-71eafa46c86b-452670670_7898243190231450_1194215039024506002_n.jpg)


### Set up

#### 1. Installation
This code requires Python >= 3.9.


```
pip install -r requirements.txt
```

#### 2. Environment Variables

Create a file named .env and add the following lines, replacing placeholders with your actual values:

```
MONGODB_URI=
EMBEDDING_MODEL=
DB_NAME=
DB_COLLECTION=
GEMINI_KEY=
```

- MONGODB_URI: URI of your MongoDB Atlas instance.
- EMBEDDING_MODEL: Name of the embedding model you're using for text embedding.
- DB_NAME: Name of the database in your MongoDB Atlas.
- DB_COLLECTION: Name of the collection within the database.
- GEMINI_KEY: Your key to access the Gemini API.

#### 3. Data

Sample data [here](https://drive.google.com/file/d/1s1WQ2wLW7TKK0fhHH74OZu9E3XlWTfsS/view?usp=sharing)

Make sure you create a Vector Search Index. [Follow this video](https://youtu.be/jZ4hN4evesg?si=ZbXAMlQ4dsBQU_oI&t=2076).

#### 4. Edit your Prompt in serve.py

In the serve.py file, you can see that we used the prompt like this. This prompt was enhanced by adding information about your products to it.

```
Become a sales consultant for a phone store. Customer's question: {query}\nAnswer the question based on the following product information: {source_information}.
```

- query: Query from the user.
- source_information: Information we get from our database.

The full prompt will look like this:

```
Become a sales consultant for a phone store. Customer's question: Could you provide more detailed information about the Tracfone Samsung A15 4G?
Answer the question based on the following product information:
 1) Name: Tracfone Samsung A15 4G , 128 GB, LTE, 6GB RAM, Black - Prepaid Smartpone [Locked to Tracfone Wireless}, Price: $149.00, Rating: 4.0
 2) Name: Tracfone Samsung Galaxy A14, 5G, 64GB, Black - Prepaid Smartphone [Locked to Tracfone], Price: $99.88, Rating: 4.1
 3) Name: AT&T Samsung Galaxy A15 5G, 128GB, 4GB RAM, Black - Prepaid Smartphone, Price: $139.00, Rating: 2.9
 4) Name: AT&T Samsung Galaxy A15 5G, 128GB, 4GB RAM, Black - Prepaid Smartphone, Price: $139.00, Rating: 2.9
 5) Name: Tracfone Motorola moto g 5G (2024), 64GB, Gray - Prepaid Smartphone [Locked to Tracfone], Price: $99.88, Rating: 3.8
 6) Name: AT&T Samsung Galaxy A14 5G, 64GB Black - Prepaid Smartphone, Price: $69.88, Rating: 3.7
 7) Name: AT&T Samsung Galaxy A14 5G, 64GB Black - Prepaid Smartphone, Price: $69.88, Rating: 3.7
 8) Name: Tracfone BLU View 5, 64GB, Black - Prepaid Smartphone [Locked to Tracfone], Price: $29.88, Rating: 3.4
 9) Name: Tracfone BLU View 5 Pro, 64GB, Black - Prepaid Smartphone [Locked to Tracfone], Price: $69.88, Rating: 3.8
 10) Name: Tracfone Motorola moto g Play 4G (2024), 64GB, Black - Prepaid Smartphone [Locked to Tracfone], Price: $49.88, Rating: 3.8.

```

The prompt is then fed to LLMs.

#### 5. Run server

```
python serve.py
```

#### 6. Testing API

Testing on web-app. [Link](https://github.com/bangoc123/protonx-ai-app-UI)

