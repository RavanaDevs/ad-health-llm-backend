from flask import Flask, request, jsonify, render_template
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

app = Flask(__name__)


llm = ChatGroq(
    temperature=0,
    groq_api_key="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",
    model_name="llama-3.1-70b-versatile"
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_titles', methods=['POST'])
def generate_titles():
    data = request.json
    location = data.get('location')
    category = data.get('category')
    price = data.get('price')
    city = data.get('city')

    prompt_extract = PromptTemplate(
        input_variables=["Location", "category", "price", "city"],
        template="Give me 5 titles for the description using five words or below: \"{Location}, {city}, {price}, {category}\""
    )

    formatted_prompt = prompt_extract.format(
        Location=location,
        category=category,
        price=price,
        city=city
    )

    response = llm.invoke(formatted_prompt)

    response_text = response.content if hasattr(response, 'content') else str(response)
    titles = [title.strip() for title in response_text.split('\n') if title.strip()]

    return jsonify({"titles": titles})

if __name__ == '__main__':
    app.run(debug=True)
