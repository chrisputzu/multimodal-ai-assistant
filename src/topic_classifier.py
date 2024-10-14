import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score

async def classify_intent(user_message: str) -> str:
    """
    Classifies the intent of a given message using a trained model.

    Args:
        user_message (str): The input message to classify.

    Returns:
        str: The predicted intent label.

    Notes:
        - The model is trained on a custom dataset with input text and corresponding labels.
    """
    csv_path = Path('training_set_classifier/data_training_classifier.csv')
    df = pd.read_csv(csv_path)
    df.columns = ['text', 'label']
    
    X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42)
    
    model = make_pipeline(TfidfVectorizer(), MultinomialNB())
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    print("Accuracy:", accuracy_score(y_test, y_pred))
    label = model.predict([user_message])[0]

    return label
