<div align="center">
    <h1>ML Horizon</h1>
</div>
<div align="center">
    <p>:star: Your gatway to AI knowledge. :star:</p>
</div>

## Table of Contents
- [Introduction](#Introduction)
- [Features](#features)
- [Installation](#installation)

# Introduction
**ML Horizon** is an educational knowledge-sharing platform dedicated to empowering users of all ages and skill levels to learn **Machine Learning (ML)** and **Artificial Intelligence (AI)** on their terms. In a rapidly evolving field like ML/AI, it can be challenging for learners to find a path that suits their goals, knowledge level, and interests. ML Horizon bridges this gap by offering a **customizable learning experience** that caters to each user’s unique journey, ensuring they get precisely the knowledge they need without the distraction of irrelevant content.

# Features
1. **AI-Powered Chatbot**: Equipped with an extensive knowledge base curated from reputable, high-quality sources, the chatbot allows users to ask specific questions and dive deep into technical concepts. This feature empowers users to get personalized answers and guidance on complex topics in real-time.

2. **Customized Project Generator**: Tailored to each user’s coding ability, experience level, and interests, the project generator designs unique projects that align with the user’s goals. The generated projects cover various algorithms, applications, and skill levels, giving users a practical outlet to apply their knowledge.

3. **Personalized Programming Support**: ML Horizon includes a **Coding Assistant** that provides guidance when users encounter challenges during implementation. Rather than completing the work for them, the assistant offers contextual hints and step-by-step support, encouraging users to reach solutions independently.

## How does it work?

### Knowledge Base | Atlas Search | Reranking
This platform featuring a RAG-integrated AI Agent that is compatible with a comprehensive knowledgebase. This knowledgebase generated through an AI-based data pipeline, predicting user's questions, search up high quality relevent information in the internet in conjucntion with its own knowledge and store the answer in a database. This AI has the capability to provide accurate and up to date information instead of other ai provider that has a huge gap in knowledge. As this database is estabilished, a hybird-retriever is built using atlas vector search and atlas query search. The combined result is then passed into cohere reanker for the best result. 

### Usage of Sonnet V2 
The use of sonnet v2 not only increases the overall quality of the responses, but also provide a strong reasoning ability allowing us to turn our imagenation into practice, enabling excellent customization functionality.

### LangChain Integration
Lastly, LangChain is the ultimate technology that enables the smooth progress of ML Horizon. The flexibility and countless pre-built functions not only ease up the AI framework designing process but assuring a seamless integration of all different services like AWS and mongodb atlas. 

# Installation
**IMPORTANT NOTE**: Since different parts of the application requires a series of API, please ensure to follow online tutorial to aquire them in pior of testing. 

1. After getting all the api keys, install all the dependencies in local environment or virtual environment
```bash
pip install -r requirement.txt
```

2. Store all the api keys in a .env file and make sure the api key name matches the name that is being used in the repository.

3. Run the app.py file in the backend 

# License
This project is licensed under the MIT License - see the [LICENSE](License) file for details.

# Disclaimer
The COT RAG System is intended for educational purposes only. The creator assumes no responsibility for any consequences arising from it use. Users are advised to comply with appropriate terms of service of relevant usage and adhere to all applicable laws, regulartions, and ethical guidlines.