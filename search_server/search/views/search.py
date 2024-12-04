from flask import Blueprint, render_template, request
from search import model

# Create a Blueprint for search routes
search_bp = Blueprint('search_bp', __name__)

@search_bp.route("/")
def show_index():
    """Display the search homepage."""
    import search  # Move the import here to avoid circular import issue
    connection = search.model.get_db()

    # Query the documents table
    cur = connection.execute("SELECT docid, title, summary, url FROM documents LIMIT 10")
    documents = cur.fetchall()

    context = {"documents": documents}
    return render_template("index.html", **context)

@search_bp.route("/search")
def search():
    """Handle search queries."""
    # Retrieve query parameters
    query = request.args.get("q", "")
    pagerank_weight = request.args.get("pagerank_weight", 0.5)

    # Validate the query
    if not query:
        return render_template(
            "results.html",
            query=query,
            results=[],
            error="Please enter a search term."
        )

    # Access the database
    connection = model.get_db()

    # Execute a query to search the database
    cur = connection.execute(
        "SELECT docid, title, summary, url FROM documents WHERE title LIKE ? OR summary LIKE ? LIMIT 10",
        (f"%{query}%", f"%{query}%")
    )
    results = cur.fetchall()

    # Render the results page
    return render_template(
        "results.html",
        query=query,
        pagerank_weight=pagerank_weight,
        results=results
    )

@search_bp.route("/results")
def results():
    return render_template("results.html")
