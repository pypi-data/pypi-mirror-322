from transformers import pipeline

# Load the pipeline for text classification
classifier = pipeline("zero-shot-classification", model="typeform/distilbert-base-uncased-mnli")

# Define the possible intents
candidate_labels = ["complaint", "feedback", "appointment","travel","agenda","taskmanagement","religion","fire test"]

def determine_intent(user_input):
    result = classifier(user_input, candidate_labels)
    print(result)
    return result["labels"][0]  # The intent with the highest score

# Example user input
user_input = '''
    Playing with matches is dangerous.
    Can you book me a meeting, its about flying to paris
    '''

# Determine the intent
for i in range(10):
    intent = determine_intent(user_input)
    print(f"User intent: {intent}")