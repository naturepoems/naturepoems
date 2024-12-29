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
    title: str 

class QuoteCollection(BaseModel):
    quotes: list[Quote]


def get_author_quotes(author, subject, num=2):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"I need some nature poems from the following author: {author} "},
            {"role": "system", "content": f"In your response I need the poem title and the poem itself"},
            {"role": "system", "content": f"Ensure all poems are nature poems part of the poetic movement {subject}"},
            {"role": "system", "content": "If possible, preserve the poems original form - line breaks, punctuation, etc."},
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
        pattern = r'[<>:"/\\|?*\x00-\x1F]'
        author_name= re.sub(pattern, '', author_name)
        print(f"Getting quotes for {author_name}")
        try:
            quotes=get_author_quotes(author_name, subject=subject, num=num)
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
        pattern = r'[<>:"/\\|?*\x00-\x1F]'
        author_name = re.sub(pattern, '', author_name)
        write_quote_to_jekyll_page(subject, quote.text, author_name, quote.title)
        #create_author_index(quote.author, subject, description="No Description" )
        #create_subject_index(subject)

def write_subject(subject, num=10):
    authors=get_subject_authors(subject, num=num).authors
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

    quotes=get_authors_quotes(authors, subject=subject, num=num)
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
    "Haiku and the French Symbolist Poets",  # Non-Japanese
    "Haiku's Role in the British Modernist Poets' Works (Early 20th century)",  # Non-Japanese
    "The British Haiku Movement (1900–1930)",  # Non-Japanese
    "Haiku and the Futurist Movement in Italy (1910s)",  # Non-Japanese
    "Haiku and Minimalism in Western Art (1910s–1920s)",  # Non-Japanese
    "Haiku as Part of the Imagist Anthologies (1910s–1920s)",  # Non-Japanese
    "Transcendental Haiku",  # Non-Japanese
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

    subjects= [
    # Japanese Nature Haiku Movements
    "Early Haiku Masters (17th–18th centuries)",  # Japanese haiku focused on nature
    "Classical Haiku (Bashō, Buson, Issa)",  # Japanese haiku with deep nature themes
    "Shiki's Modern Haiku Movement",  # Haiku focusing on nature's simplicity
    "Kyōka Haiku",  # Humorous yet nature-focused Japanese haiku
    "Haikai no Renga Tradition",  # Collaborative renga focused on nature themes
    "Haiku as a Popular Literary Form (Late 19th century)",  # Emergence of nature-based haiku
    "Haiku in the Edo Period (1603–1868)",  # Traditional haiku with nature themes
    "Haiku in the Meiji Period (1868–1912)",  # Nature poetry as part of modernization
    "Haiku and Zen Buddhism",  # Zen influences on nature-centric haiku
    "Modern Japanese Haiku (20th century)",  # Post-World War II haiku with nature themes

    # Western Nature Poetry Movements
    "Romanticism (Late 18th–Mid-19th century)",  # Nature as the central theme in poetry
    "Transcendentalism (1830s–1850s)",  # American poets like Thoreau and Emerson, nature-focused
    "The Hudson River School Poets (19th century)",  # Nature-focused American poetry
    "Nature Poetry in the British Romantic Period (1800–1850)",  # Keats, Wordsworth, Shelley, nature-focused
    "The Pre-Raphaelite Brotherhood (1850s–1860s)",  # English poets with strong nature themes
    "American Nature Poets (19th century)",  # Emerson, Whitman, Dickinson (nature-centric poems)
    "Imagist Movement and Nature (Early 20th century)",  # Nature observed in concise, clear terms
    "Naturalism (Late 19th century)",  # Nature's harsh realities in poetry (e.g., Crane)
    "American Realism and Nature Poetry (Late 19th–Early 20th century)",  # Focus on nature's authenticity
    "The French Symbolist Movement (Late 19th century)",  # Nature seen as a symbol for deeper meanings
    "Haiku in the English-Speaking World (Early 20th century)",  # Nature-haiku influence in English
    "American Nature Haiku Movement (1910s–1930s)",  # Adoption of Japanese haiku in American nature poetry
    "British Nature Poetry (19th century)",  # Poets like John Clare, nature-centric verse
    "The Chicago Imagists (1920s–1930s)",  # A modernist group exploring nature through minimalist forms
    "Dadaism and Nature (1910s–1920s)",  # Experimental nature-focused poetry within the Dada movement
    "French Romanticism and Nature (Early 19th century)",  # Nature as a source of poetic inspiration in France
    "Futurism and Nature (Early 20th century)",  # Nature interpreted through new artistic lenses
    "The Haiku Influence on Modern Nature Poetry (1910s–1920s)",  # Western poets influenced by Japanese haiku's focus on nature
    "Post-Impressionist Poets and Nature (Late 19th–Early 20th century)",  # Nature explored through visual poetry
    "American Modernism and Nature (1910s–1930s)",  # Nature in the context of modern American poetry
    "Early Eco-Poetry and Nature (Early 20th century)",  # Emerging environmental themes in poetry

    # Expanded Western Nature Movements
    "The Bloomsbury Group and Nature (1910s–1930s)",  # Exploration of nature in the context of modernist thought
    "Victorian Nature Poetry (1837–1901)",  # Nature's complexities in Victorian literature
    "The Beat Generation and Nature (1940s–1950s)",  # A late influence of nature in poetry, connected with spirituality
    "The Nature Poets of the American South (19th–Early 20th century)",  # Focus on Southern landscapes and nature
    "Renaissance Nature Poetry (16th century)",  # Nature's symbolic and spiritual meaning in Renaissance poetry
    "Post-Romantic Nature in European Poetry (Mid 19th century)",  # Nature after the Romantic period in Europe
    "The Lake Poets and Nature (1790s–1820s)",  # William Wordsworth and others focused on nature’s spiritual influence
    "French Realism and Nature (Mid 19th century)",  # Nature’s representation of real life (e.g., Flaubert, Zola)
    "British Neo-Romanticism (Early 20th century)",  # Poets focusing on nature in a post-Romantic context
    "Modernist Nature Writing in Spain (1920s)",  # Early 20th-century Spanish poets reflecting on nature
    "The Nature and Animal Poetry Movement (19th–20th century)",  # Poets concerned with animals and their relationships with nature
    "Nature in New Zealand Poetry (Late 19th–Early 20th century)",  # Poetic focus on the landscape and environment
    "Scandinavian Nature Poetry (Late 19th century)",  # Nature as a theme in Swedish, Norwegian, and Danish poetry
    "Nature in Russian Symbolism (Late 19th century)",  # Russian poets incorporating nature into symbolic meaning
    "The Natural World in Early 20th Century Australian Poetry",  # Nature-focused poets in Australia
    "Canadian Nature Poets (Late 19th–Early 20th century)",  # Poets like Archibald Lampman focusing on Canadian landscapes
    "The Romantic Poets of the Iberian Peninsula (19th century)",  # Spanish and Portuguese poets with nature as a theme
    "Modern Nature Poetry in South America",  # Poets reflecting on the natural world in Latin America
    "African Nature Poets (19th–Early 20th century)",  # African poets using nature as a metaphor or focus
    "Modernist Nature Writing in Italy (Early 20th century)",  # Italian poets embracing nature in modernist contexts
    "The Nature Poets of the Baltic States (Early 20th century)",  # Poets from Estonia, Latvia, and Lithuania with nature-centric works
    "Modern Nature Poetry in Poland (Early 20th century)",  # Polish poets writing on nature through modernist lenses

    # Additional Expansions
    "Ecofeminist Poetry and Nature (Late 19th–Early 20th century)",  # Poetic focus on women's connection to nature
    "Anthropocentric Nature Poetry (Early 20th century)",  # Nature seen through the lens of human relations
    "Imagism's Influence on Nature (Early 20th century)",  # The Imagist movement's influence on nature poems in Europe and America
    "Ecosophy in Poetry (Early 20th century)",  # Environmental philosophy influencing poetry
    "Psychological Nature Poetry (20th century)",  # Nature as a reflection of human psychology in poetry
    "Romanticized Nature Poetry in Colonial Contexts (19th century)",  # Exploration of nature from colonial perspectives
    "Symbolist Nature Poetry (19th–20th century)",  # Nature as an expression of the subconscious and symbols
    "Lyrical Nature Writing (Late 19th–Early 20th century)",  # Poets using nature as a form of lyrical expression
    "The Nature of Childhood in Poetry (19th–Early 20th century)",  # Nature as seen through the eyes of children in literature
    "Nature as Political Allegory (Early 20th century)",  # Poets using nature as a metaphor for political movements and struggles
    "Nature and the Sublime in Literature (18th–19th century)",  # Nature viewed as awe-inspiring and sublime, especially in the romantic tradition
    "Mythological Nature Poetry (19th–20th century)",  # The use of myth and folklore to represent nature in poetry
    "The Wilds of Nature in Exploration Poetry (19th–Early 20th century)",  # Poets inspired by the exploration of wild, uncharted territories
    "Poetry of Environmental Crisis (Early 20th century)",  # Poets writing about environmental degradation and the loss of nature
    "Philosophical Nature Poetry (19th–Early 20th century)",  # Nature as a source of philosophical reflection and insight in poetry
    "Post-War Nature Poetry (Post-1930)",  # Late 20th-century poets grappling with nature after the World Wars
    "Futurist Nature Poetry (Early 20th century)",  # Poets influenced by Futurism that still explore nature through futuristic lenses
    ]
    subjects=[
    "Classical Haiku (Bashō, Buson, Issa)",  # Japanese haiku with deep nature themes
    "Shiki's Modern Haiku Movement",  # Haiku focusing on nature's simplicity
    "Kyōka Haiku",  # Humorous yet nature-focused Japanese haiku
    "Haikai no Renga Tradition",  # Collaborative renga focused on nature themes
    ]


    for subject in subjects:
        print("subject...",subject)
        write_subject(subject)
    
if __name__ == "__main__":
    main()
