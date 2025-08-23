import embedding_index


query = "Who works in Mumbai?"
results = embedding_index.query(query, top_k=3)

for res in results:
    print(f"{res['text']} | Source: {res['source_file']} | Distance: {res['distance']}")


"""
1. “Who works in Mumbai?”

Answer: Priya, the data analyst.

2. “Which team handles food delivery data?”

Answer: Ravi (backend developer) and Priya (data analyst) work together on real-time food delivery data from Zomato and Swiggy.

3. “Who manages projects in Bangalore?”

Answer: Amit, the project manager.

4. “What does Ravi enjoy outside of work?”

Answer: Reading technology blogs, contributing to open-source projects, and participating in hackathons.

5. “What tools does Priya use for analytics?”

Answer: Excel and Python, along with advanced analytics techniques including machine learning and predictive modeling.
"""