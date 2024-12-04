from flask import Blueprint, render_template, request, jsonify
import json

# Create a blueprint for the search server
search = Blueprint("search", __name__)

# Load search index (assuming it's a JSON file)
#with open("search_index.json") as f:
    #search_index = json.load(f)

@search.route("/", methods=["GET"])
def index():
    """Home page."""
    return render_template("index.html")

@search.route("/search", methods=["GET"])
def search_results():
    """Search results page."""
    query = request.args.get("q", "").lower()
    results = []

    if query:
        # Search logic: Match query with indexed terms
        for term, docs in search_index.items():
            if query in term:
                for doc in docs:
                    results.append({
                        "url": doc["url"],
                        "title": doc["title"],
                        "snippet": doc["snippet"][:150] + "..."  # Truncate snippet
                    })

    # Render the results page
    return render_template("results.html", query=query, results=results)
