from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
# from sentence_transformers import SentenceTransformer
# from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

llm = ChatGroq(
    temperature=0,
    groq_api_key="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",
    model_name="llama-3.1-70b-versatile"
)

# model=SentenceTransformer("sentence-transformers/bert-base-nli-mean-tokens")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_titles', methods=['POST'])
@cross_origin()
def generate_titles():
    data = request.json

    title_generation_prompt = '''
Generate five enhanced and engaging titles for a property listing to attract potential buyers or renters. Use the following parameters to improve the existing title provided:

- Title: {title}
- Description: {description}
- Price: {price}
- Search Keywords: {search_keywords}

Each generated title should be clear, concise, and make the property appealing for online searches. Tailor the titles to highlight unique features and competitive advantages related to the description, price, and keywords, maximizing searchability and appeal for potential customers. 

Give only titles. do not provide any other details or descriptions. Do not number the titles and add additional characters from the beginig and end.
'''

    title = data.get('title')
    description = data.get('description')
    price = data.get('price')
    search_keywords = data.get('search_keywords')

    prompt_extract = PromptTemplate(
        input_variables=["title", "description", "price", "search_keywords"],
        template=title_generation_prompt
    )

    formatted_prompt = prompt_extract.format(
        title=title,
        description=description,
        price=price,
        search_keywords=search_keywords
    )

    response = llm.invoke(formatted_prompt)

    response_text = response.content if hasattr(response, 'content') else str(response)
    titles = [title.strip() for title in response_text.split('\n') if title.strip()]

    return jsonify({"titles": titles})

# @app.route('/check-similarity', methods=['POST'])
# @cross_origin()
# def check_similarity():
#     data = request.json

#     title = data.get("title")
#     description = data.get("description")

#     sentencevec1=model.encode(title)
#     sentencevec2=model.encode(description)

#     sim = cosine_similarity([sentencevec1],[sentencevec2])

@app.route('/check-similarity', methods=['POST'])
@cross_origin()
def check_similarity():
    sim_check_prompt = """
    Given a title and a description, analyze the similarity between the two texts on a scale from 0 to 100, where 0 means no similarity and 100 means identical. Only respond with a single integer from 0 to 100, based on their thematic and contextual closeness.

    Title: "{title}"
    Description: "{description}"
    """
    data = request.json

    title = data.get("title")
    description = data.get("description")
    
    prompt_extract = PromptTemplate(
        input_variables=["title", "description"],
        template=sim_check_prompt
    )

    formatted_prompt = prompt_extract.format(
        title=title,
        description=description
    )

    response = llm.invoke(formatted_prompt)

    response_text = response.content if hasattr(response, 'content') else str(response)
    titles = [title.strip() for title in response_text.split('\n') if title.strip()]

    return jsonify({"similarity": titles})

if __name__ == '__main__':
    app.run(debug=True)
