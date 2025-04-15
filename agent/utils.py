import os
import json

def save_img(img, img_ext):
    if not os.path.exists("temp"):
        os.mkdir("temp")

    file_name = os.path.join("temp", str(len(os.listdir("temp"))) + "." + img_ext)
    img.save(file_name)

    return file_name

def json_to_blog_html(json_input: str, output_file: str = "blog_post.html") -> str:
    data = json.loads(json_input)
    
    # Extract content
    headline = data.get("headline", "")
    introduction = data.get("introduction", "")
    body = data.get("body", [])
    conclusion = data.get("conclusion", "")

    # Build HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{headline}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 2rem auto;
                padding: 1rem;
                background-color: #f9f9f9;
                color: #333;
            }}
            h1 {{
                color: #004080;
            }}
            p {{
                margin-bottom: 1rem;
            }}
        </style>
    </head>
    <body>
        <h1>{headline}</h1>
        <p>{introduction}</p>
    """

    for paragraph in body:
        html_content += f"<p>{paragraph}</p>\n"

    html_content += f"<p><strong>{conclusion}</strong></p>\n"

    html_content += """
    </body>
    </html>
    """

    # Save to file
    # with open(output_file, "w", encoding="utf-8") as f:
    #     f.write(html_content.strip())

    return html_content.strip()