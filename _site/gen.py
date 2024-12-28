import openai
import os
from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from openai import OpenAI
import re

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Ensure the API key is set in your environment

class Author(BaseModel):
    name: str
    description: str

class AuthorCollection(BaseModel):
    authors: List[Author]

class Quote(BaseModel):
    text: str
    author: str 

class QuoteCollection(BaseModel):
    quotes: list[Quote]

def get_buddhist_quotes():
    # Make the API call to OpenAI's chat completion endpoint
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "I need some buddhist quotes."},
            {"role": "system", "content": "Dont repeat quotes."},
            {"role": "user", "content": "I need 50 buddhist quotes."},
        ],
        response_format=QuoteCollection,
    )

    # Get the response content properly (fixing the TypeError)
    response_content = completion.choices[0].message.parsed
    return response_content


def get_author_quotes(author, num=2):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "I need some quotes from the following authors."},
            {"role": "system", "content": "Dont repeat quotes."},
            {"role": "user", "content": f"I need up to {num} quotes from the author, {author}"},
        ],
        response_format=QuoteCollection,
    )

    # Get the response content properly (fixing the TypeError)
    response_content = completion.choices[0].message.parsed
    return response_content

def get_authors_quotes(authors, num=2):
    all_quotes={}
    for author in authors:
        pattern = r'[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s-]'
        pattern=r'[^a-zA-Z0-9\s\-_À-ÿ\u0100-\u017F\u0400-\u04FF]'
        author_name=re.sub(pattern, '', author.name)
        print(f"Getting quotes for {author_name}")
        try:
            quotes=get_author_quotes(author_name, num=num)
            all_quotes[author_name]=quotes
        except Exception as e:
            print(f"exception: ",e)

    return all_quotes


def get_buddhist_authors(num):
    # Make the API call to OpenAI's chat completion endpoint
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "I need a list of people associated with buddhism"},
            {"role": "system", "content": "Dont repeat people."},
            {"role": "user", "content": "I need up to {num} people who have written, spoken, or communicated directly on buddhism"},
        ],
        response_format=AuthorCollection,
    )

    # Get the response content properly (fixing the TypeError)
    response_content = completion.choices[0].message.parsed
    return response_content


def get_subject_authors(subject, num=2):
    # Make the API call to OpenAI's chat completion endpoint
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"I need a list of people associated with {subject} and a brief description about the person"},
            {"role": "system", "content": "Dont repeat people, ensure they are associated directly with the subject"},
            {"role": "user", "content": f"I need up to {num} people who have written, spoken, or communicated directly on {subject}"},
        ],
        response_format=AuthorCollection,
    )

    # Get the response content properly (fixing the TypeError)
    response_content = completion.choices[0].message.parsed
    return response_content




from genpage import *

# Call the function to write the quote to a Jekyll page

def write_quote_collection(collection, subject="unknown", ): 
    for quote in collection:
        pattern = r'[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s-]'
        pattern=r'[^a-zA-Z0-9\s\-_À-ÿ\u0100-\u017F\u0400-\u04FF]'
        author_name=re.sub(pattern, '', quote.author)
        write_quote_to_jekyll_page(subject, quote.text, author_name)
        #create_author_index(quote.author, subject, description="No Description" )
        #create_subject_index(subject)

def write_subject(subject):
    authors=get_subject_authors(subject, num=10).authors
    create_subject_index(subject)
    #authors=get_buddhist_authors().authors
    print (type(authors))
    if authors:
        print("Subject Authors:", len(authors))
        for author in authors:
            pattern = r'[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s-]'
            pattern=r'[^a-zA-Z0-9\s\-_À-ÿ\u0100-\u017F\u0400-\u04FF]'
            author_name=re.sub(pattern, '', author.name)
            print('*'*40)
            print(author_name)
            clean_description=re.sub(r'"', r'\\"', author.description)
            create_author_index(author_name, subject, description=clean_description )
    else:
        print("Failed to retrieve valid authors.")
        return

    quotes=get_authors_quotes(authors, num=10)
    for k,v in quotes.items():
        print(quotes[k].quotes)
        write_quote_collection(quotes[k].quotes, subject=subject)


# Main function to execute the script and print the results
def main():
    #subjects=["buddhism", "science", "computers", "politics", "farming", "nature"]
    subjects = [
    "Love", "Friendship", "Happiness", "Wisdom", "Success", "Motivation", "Perseverance",
    "Gratitude", "Hope", "Faith", "Kindness", "Forgiveness", "Courage", "Change", "Freedom",
    "Self-discipline", "Focus", "Growth", "Mindfulness", "Resilience", "Creativity",
    "Ambition", "Patience", "Confidence", "Authenticity", "Self-love", "Determination",
    "Balance", "Positivity", "Vision", "Courageous living", "Grit", "Self-empowerment",
    "Family", "Parenthood", "Marriage", "Trust", "Compromise", "Respect", 
    "Mother and daughter", "Father and son", "Sibling", "Generations", "Unity", "Parenting",
    "Togetherness", "Nurturing", "Caregiving", "Support", "Generosity", "Solidarity",
    "Joy", "Sadness", "Anger", "Fear", "Empathy", "Compassion", "Contentment", "Grief",
    "Happiness", "Sad", "Loneliness", "Excitement", "Love for self", "Regret", "Hopefulness",
    "Angst", "Insecurity", "Excitement", "Fulfillment", "Elation", "Peace of mind",
    "Truth", "Morality", "Existence", "Free will", "Knowledge", "Justice", "Beauty", "Time",
    "Friedrich Nietzsche", "Aristotle", "Socrates", "Plato", "Epicurus", "Stoicism", "Hedonism",
    "Ethics", "Logic", "Self-awareness", "Wisdom in living", "Philosophy of life", "Metaphysics",
    "Community", "Leadership", "Equality", "Diversity", "Tradition", "Education",
    "Art", "Technology", "Politics", "Black History Month", "Women empowerment",
    "Human rights", "Sustainability", "Activism", "Civic duty", "Progress", "Civil rights",
    "Social justice", "Solidarity", "Collectivism", "Environmentalism", "Equality for all", "Rights",
    "Seasons", "Animals", "Oceans", "Mountains", "Conservation", "Sustainability",
    "Flower", "Ocean", "Sunset", "Rain", "Forest", "Desert", "Wildlife", "Nature's beauty",
    "Climate change", "Eco-friendliness", "Biodiversity", "Earth", "Landscapes", "Ecosystem",
    "Teamwork", "Leadership", "Innovation", "Discipline", "Balance", "Entrepreneurship",
    "Risk-taking", "Inspirational for work", "Motivational for success", "Productivity", "Efficiency",
    "Creativity in work", "Collaboration", "Work-life balance", "Focus at work",
    "Entrepreneurial mindset", "Corporate culture", "Professional growth", "Ambition in career",
    "Prayer", "Faith", "Redemption", "Humility", "Afterlife", "Destiny", "Bible",
    "Inspirational Bible verses", "Christian", "God", "Islamic", "Spirituality", "Soul", "Heaven", "Faithfulness",
    "Hope", "Divine intervention", "Peace", "Salvation", "Compassionate love", "Gratitude to the divine",
    "Hinduism", "Buddhism", "Judaism", "Christianity", "Islam", "Sikhism", "Taoism", "Confucianism",
    "Shintoism", "Jainism", "Zoroastrianism", "Bahá'í Faith", "Indigenous spirituality", "New Age spirituality",
    "Kabbalah", "Yoga", "Meditation", "Sufism", "Mysticism", "Transcendentalism", "Reincarnation",
    "Enlightenment", "Spiritual awakening", "Inner peace", "Divinity", "Sacred texts", "Faith practices", 
    "Rituals", "Spiritual healing", "Prayer and meditation", "Faith and devotion", "Spiritual growth",
    "Adventure", "Travel", "Humor", "Dreams", "Nostalgia", "Music", "Food", "Sports",
    "Books", "History", "Science", "Space", "Health", "Fitness", "Art of war",
    "Movie", "Famous", "Funny", "Disney", "Anime",
    "Comedy", "Drama", "Thriller", "Romance", "Action", "Sci-fi", "Horror", "Fantasy",
    "Cultural trends", "TV shows", "Streaming services", "Documentaries", "Entertainment industry",
    "Perseverance", "Motivational", "Positive", "Encouraging", "Uplifting", "Powerful", "Never give up", "Strength",
    "Resilience", "Determination", "Hope", "Endurance", "Overcoming obstacles", "Courage under pressure",
    "Personal growth", "Self-improvement", "Mental fortitude", "Grit and resolve", "Emotional resilience",
    "Hard work", "Discipline in life", "Facing adversity", "Triumph over fear", "Overcoming doubt"
    ]

    for subject in subjects:
        print("subject...",subject)
        write_subject(subject)
    
if __name__ == "__main__":
    main()
