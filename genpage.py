import os
from datetime import datetime
import re

# Function to create a Jekyll page from a quote
def write_quote_to_jekyll_page(subject, quote, author):
    # Get current date in the format required by Jekyll (_posts/YYYY-MM-DD-title.md)
    date_str = datetime.now().strftime("%Y-%m-%d")
    title = f"{author} - {quote[:40].rsplit(' ', 1)[0].rstrip()}"
    pattern=pattern = r'[^a-zA-ZáéíóúÁÉÍÓÚñÑ\s-]'
    pattern=r'[^a-zA-Z0-9\s\-_À-ÿ\u0100-\u017F\u0400-\u04FF]'
    title = re.sub(pattern, '', title)
    filename = f"{date_str}-{title}.md"  # Format the filename in Jekyll format
    
    # Create the content for the Jekyll page
    content = f"""---
layout: post
title: "{title}"
date: {date_str} 12:00:00 -0000
author: {author}
quote: "{quote}"
subject: {subject}
permalink: /{subject}/{author}/{title}
---

{quote}

- {author}
"""
    
    output_dir="quotes/"+subject+"/"+author+"/_posts"
    posts_dir = output_dir.replace(" ", "-")

    # Ensure the output directory exists
    os.makedirs(posts_dir, exist_ok=True)
    
    # Write the content to a markdown file
    file_path = os.path.join(posts_dir, filename)
    with open(file_path, "w") as file:
        file.write(content)
    
    print(f"Quote written to {file_path}")



def create_subject_index(subject):
    output_dir="quotes/"+subject
    os.makedirs(output_dir, exist_ok=True)

    # Define the file path
    file_path = os.path.join(output_dir, "index.md")

    # Create the content for the index.md file
    content = f"""---
title: {subject}
subject: "{subject}"
permalink: /{subject}
---

Welcome to the page of {subject}
"""

    # Write the content to the file
    with open(file_path, "w") as file:
        file.write(content)

    print(f"subject page created: {file_path}")
  

def create_author_index(author_name, subject, description="No Description" ):
    # Ensure the output directory exists
    output_dir="quotes/"+subject+"/"+author_name
    author_dir = output_dir.replace(" ", "-")
    os.makedirs(author_dir, exist_ok=True)

    # Define the file path
    file_path = os.path.join(author_dir, "index.md")

    # Create the content for the index.md file
    content = f"""---
layout: author
title: {author_name}
description: "{description}"
subject: "{subject}"
parent: {subject}
permalink: /{subject}/authors/{author_name.replace(" ", "-")}/
---

Welcome to the page of {author_name}! Here you can find their quotes.
"""

    # Write the content to the file
    with open(file_path, "w") as file:
        file.write(content)

    print(f"Author page created: {file_path}")
