# backend/utils/store_embeddings.py
from langchain_text_splitters import RecursiveCharacterTextSplitter
from google.genai import types
from common import index, genai_client, EMBED_MODEL
import uuid

CHUNK_SIZE = 400
CHUNK_OVERLAP = 50

def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    return splitter.split_text(text)

def store_embeddings_in_pinecone(text):
    chunks = chunk_text(text)
    for i, chunk in enumerate(chunks):
        doc_id = generate_unique_uuid()
        emb = genai_client.models.embed_content(
            model=EMBED_MODEL,
            contents=chunk,
            config=types.EmbedContentConfig(output_dimensionality=1536)
        ).embeddings[0].values
        index.upsert(vectors=[(f"{doc_id}", emb, {"text": chunk})])
        print(f"Index Inserted {i}")
    print(f"✅ Stored {len(chunks)} chunks for {doc_id}")

def generate_unique_uuid():
    return str(uuid.uuid4())

'''# Local test
if __name__ == "__main__":
    sample_text = """
    1. Data science is the study of data to extract meaningful insights.
    2. It combines statistics, computer science, and domain knowledge.
    3. The goal is to turn raw data into actionable knowledge.
    4. It involves data collection, cleaning, analysis, and visualization.
    5. Data scientists use programming languages like Python and R.
    6. Python is popular for its simplicity and vast libraries.
    7. Libraries like Pandas, NumPy, and Scikit-learn are essential.
    8. R is favored for statistical modeling and data visualization.
    9. SQL is used to query structured databases.
    10. Data can be structured, semi-structured, or unstructured.
    11. Structured data fits neatly into tables.
    12. Unstructured data includes text, images, and videos.
    13. Semi-structured data includes JSON and XML formats.
    14. Data preprocessing is crucial for accurate analysis.
    15. It includes handling missing values and outliers.
    16. Exploratory Data Analysis (EDA) reveals patterns and trends.
    17. Visualization tools include Matplotlib, Seaborn, and Plotly.
    18. Machine learning is a core part of data science.
    19. It enables predictive modeling and pattern recognition.
    20. Supervised learning uses labeled data.
    21. Common supervised algorithms: Linear Regression, Decision Trees.
    22. Unsupervised learning finds hidden patterns in unlabeled data.
    23. Examples include K-Means and Hierarchical Clustering.
    24. Reinforcement learning optimizes decisions through trial and error.
    25. Deep learning uses neural networks for complex tasks.
    26. TensorFlow and PyTorch are popular deep learning frameworks.
    27. Natural Language Processing (NLP) analyzes text data.
    28. NLP tasks include sentiment analysis and language translation.
    29. Computer vision interprets image and video data.
    30. Big data refers to extremely large datasets.
    31. Hadoop and Spark are used for big data processing.
    32. Data lakes store raw data in native formats.
    33. Data warehouses store structured, cleaned data.
    34. Cloud platforms like AWS, Azure, and GCP support data science.
    35. Data science lifecycle includes problem definition and data acquisition.
    36. It continues with data preparation and modeling.
    37. Model evaluation ensures accuracy and reliability.
    38. Deployment integrates models into production systems.
    39. Monitoring ensures models remain effective over time.
    40. Feature engineering improves model performance.
    41. It involves creating new variables from raw data.
    42. Dimensionality reduction simplifies data without losing information.
    43. PCA and t-SNE are common techniques.
    44. Data ethics ensures responsible use of data.
    45. It includes privacy, fairness, and transparency.
    46. Bias in data can lead to unfair outcomes.
    47. Data governance manages data quality and access.
    48. Version control tools like Git track code changes.
    49. Jupyter Notebooks are popular for interactive coding.
    50. Collaboration tools include GitHub and Google Colab.
    51. A/B testing compares two versions of a product.
    52. It helps optimize user experience and performance.
    53. Time series analysis deals with data over time.
    54. ARIMA and Prophet are used for forecasting.
    55. Data science is used in healthcare for diagnostics.
    56. In finance, it predicts stock trends and fraud detection.
    57. In retail, it enhances customer segmentation and inventory management.
    58. In marketing, it personalizes campaigns and predicts churn.
    59. In transportation, it optimizes routes and logistics.
    60. In sports, it analyzes player performance and strategy.
    61. In education, it supports adaptive learning systems.
    62. In agriculture, it predicts crop yields and pest outbreaks.
    63. Data scientists need strong communication skills.
    64. They must explain technical results to non-technical stakeholders.
    65. Business acumen helps align data insights with goals.
    66. Data storytelling combines visuals and narratives.
    67. Dashboards present real-time data insights.
    68. Tools like Tableau and Power BI are widely used.
    69. Data science is evolving with generative AI.
    70. Multimodal models handle text, image, and audio together.
    71. Ethics in AI is a growing concern.
    72. Data science roles include analyst, engineer, and scientist.
    73. Analysts focus on reporting and visualization.
    74. Engineers build data pipelines and infrastructure.
    75. Scientists develop models and conduct experiments.
    76. Data science requires continuous learning.
    77. MOOCs and bootcamps offer accessible training.
    78. Certifications validate skills and knowledge.
    79. Kaggle is a platform for data science competitions.
    80. It helps build portfolios and gain experience.
    81. Open-source datasets support learning and experimentation.
    82. Common sources: UCI, Google Dataset Search, Data.gov.
    83. Data science projects follow CRISP-DM or OSEMN frameworks.
    84. CRISP-DM stands for Cross-Industry Standard Process for Data Mining.
    85. OSEMN stands for Obtain, Scrub, Explore, Model, Interpret.
    86. Model accuracy is measured using metrics like RMSE and F1-score.
    87. Confusion matrix shows true vs predicted classifications.
    88. ROC curve visualizes classification performance.
    89. Overfitting occurs when a model learns noise.
    90. Regularization techniques prevent overfitting.
    91. Cross-validation ensures model generalization.
    92. Hyperparameter tuning optimizes model settings.
    93. Grid search and random search are common methods.
    94. Ensemble methods combine multiple models.
    95. Examples: Random Forest, Gradient Boosting.
    96. Data science is transforming industries globally.
    97. It empowers decision-making and innovation.
    98. The future includes AI-driven automation and real-time analytics.
    99. Responsible data science builds trust and impact.
    100. Its a powerful blend of science, art, and strategy.
    """
    
    store_embeddings_in_pinecone(sample_text)'''
