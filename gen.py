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


def get_author_quotes(author, subject, num=2):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"I need some poems from the following author: {author} "},
            {"role": "system", "content": "Dont repeat poems."},
            {"role": "system", "content": f"Ensure all poems are nature poems part of the poetic movement {subject}"},
            {"role": "user", "content": f"Please provide up to {num} poems from the author"},
        ],
        response_format=QuoteCollection,
    )

    # Get the response content properly (fixing the TypeError)
    response_content = completion.choices[0].message.parsed
    return response_content

def get_authors_quotes(authors, subject, num=2):
    all_quotes={}
    for author in authors:
        pattern = r'[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s-]'
        pattern=r'[^a-zA-Z0-9\s\-_À-ÿ\u0100-\u017F\u0400-\u04FF]'
        author_name=re.sub(pattern, '', author.name)
        print(f"Getting quotes for {author_name}")
        try:
            quotes=get_author_quotes(author_name, subject=subject num=num)
            all_quotes[author_name]=quotes
        except Exception as e:
            print(f"exception: ",e)

    return all_quotes


def get_subject_authors(subject, num=2):
    # Make the API call to OpenAI's chat completion endpoint
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"I need a list of poets with works in the {subject} and a brief description about the person"},
            {"role": "system", "content": "Dont repeat people, ensure they are associated directly with the subject"},
            {"role": "user", "content": f"I need up to {num} people who have written nature poems as a part of the movement: {subject}"},
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

    quotes=get_authors_quotes(authors, subject=subject, num=10)
    for k,v in quotes.items():
        print(quotes[k].quotes)
        write_quote_collection(quotes[k].quotes, subject=subject)


# Main function to execute the script and print the results
def main():
    subjects = [
    # Japanese Haiku Traditions (already included previously)
    "Early Haiku Masters (17th–18th centuries)",  # Japanese
    "Meiji Period Haiku (1868–1912)",  # Japanese
    "Taishō Period Haiku (1912–1926)",  # Japanese
    "Shiki's Modern Haiku Movement",  # Japanese
    "Classical Haiku (Bashō, Buson, Issa)",  # Japanese
    "Haikai no Renga Tradition",  # Japanese
    "Kyōka Haiku",  # Japanese
    "Kamakura Period Haiku",  # Japanese
    "Edo Period Haiku",  # Japanese
    "Haiku as a Popular Literary Form (Late 19th century)",  # Japanese
    "Haiku's Emergence in the West (Early 20th century)",  # Japanese
    "Haiku in the Meiji Enlightenment",  # Japanese
    "Early Modern Haiku (19th–early 20th century)",  # Japanese

    # Non-Japanese Haiku Traditions and Movements
    "Western Haiku Influence (1900–1930)",  # Non-Japanese
    "Imagist Movement and Haiku (Early 20th century)",  # Non-Japanese
    "Ezra Pound's Haiku Influence (1910s–1920s)",  # Non-Japanese
    "Paul-Louis Couchoud's Haiku (France, 1910s)",  # Non-Japanese
    "Haiku in the English-Speaking World (Early 20th century)",  # Non-Japanese
    "Haiku in American Poetry (Early 20th century)",  # Non-Japanese
    "Poets of the San Francisco Renaissance and Haiku (1910s–1930s)",  # Non-Japanese
    "The Influence of Haiku on Western Modernist Poets",  # Non-Japanese
    "Haiku in the French Avant-Garde (1910s–1920s)",  # Non-Japanese
    "Japanese Haiku and the Symbolist Movement (Late 19th–Early 20th century)",  # Non-Japanese
    "Haiku and the French Symbolist Poets (e.g., Verlaine, Mallarmé)",  # Non-Japanese
    "Haiku's Role in the British Modernist Poets' Works (Early 20th century)",  # Non-Japanese
    "The British Haiku Movement (1900–1930)",  # Non-Japanese
    "Haiku and the Futurist Movement in Italy (1910s)",  # Non-Japanese
    "Haiku and Minimalism in Western Art (1910s–1920s)",  # Non-Japanese
    "Haiku as Part of the Imagist Anthologies (1910s–1920s)",  # Non-Japanese
    "Transcendental Haiku (Emerson, Thoreau, etc.)",  # Non-Japanese
    "Dadaists and Haiku (1910s–1920s)",  # Non-Japanese
    "Haiku in the American Modernist Poets' Works",  # Non-Japanese
    "Haiku Influence on Gertrude Stein and the Parisian Avant-Garde (1910s)",  # Non-Japanese
    "Haiku in German Expressionism (1910s)",  # Non-Japanese
    "Haiku as a Literary Form in Early 20th Century Russia",  # Non-Japanese
    "Haiku and Its Reception in Eastern Europe (Early 20th century)",  # Non-Japanese
    "Haiku and the New York School Poets (1920s)",  # Non-Japanese
    "Haiku's Influence on Modernist Short-Form Poetry (1910s–1930s)",  # Non-Japanese
    "Haiku and its Use in Post-Impressionist Art and Literature (Early 20th century)",  # Non-Japanese
    "Influence of Haiku on American Beat Poets (late 1920s–1940s)"  # Non-Japanese
]


    for subject in subjects:
        print("subject...",subject)
        write_subject(subject)
    
if __name__ == "__main__":
    main()
