from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "Banana", "content": "Yellow fruit."},
    {"id": 2, "title": "Apple", "content": "Keeps the doctor away."},
    {"id": 3, "title": "Cherry", "content": "Small red fruit."},
]


def validate_input_post(data):
    if "title" not in data or "content" not in data:
        return False
    return True


def find_post_by_id(id_num):
    for post in POSTS:
        if post["id"] == id_num:
            return post
    return None


def delete_post_by_id(id_num):
    for post in POSTS:
        if post["id"] == id_num:
            POSTS.remove(post)
            return POSTS
    return None


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "please check url"}), 404


@app.route('/api/posts', methods=['GET', 'POST'])
def handle_posts():
    if request.method == 'GET':
        return jsonify(POSTS)
    if request.method == 'POST':
        new_post = request.get_json()
        if not validate_input_post(new_post):
            return jsonify({"error": "invalid or missing post data"}), 404
        max_id = 0
        for post in POSTS:
            if post["id"] > max_id:
                max_id = post["id"]
                new_id = max_id + 1
                new_post["id"] = new_id
        POSTS.append(new_post)
        return jsonify(new_post), 201
    else:
        return jsonify(POSTS), 201


@app.route("/api/posts/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    if request.method == "DELETE":
        post = find_post_by_id(post_id)

        if post is None:
            return jsonify({"message": f"Post with id:{post_id} not found."}), 404

        delete_post_by_id(post_id)
        return jsonify({"message": f"Post {post_id} deleted successfully."})


@app.route("/api/posts/<int:post_id>", methods=["PUT"])
def update_post(post_id):
    if request.method == "PUT":
        post = find_post_by_id(post_id)

        if post is None:
            return jsonify({"message": f"Post with id_{post_id} not found."}), 404

        new_post = request.get_json()

        title = new_post.get("title")
        content = new_post.get("content")
        if title is not None:
            post["title"] = title


        if content is not None:
            post["content"] = content

        return jsonify(POSTS)


@app.route("/api/posts/search", methods=["GET"])
def search_post():
    search_term = request.args.get("query", "")
    results = []
    for post in POSTS:
        title = post["title"]
        content = post["content"]
        if search_term.lower() in title.lower() or search_term.lower() in content.lower():
            results.append(post)
    return jsonify(results)


@app.route("/api/posts/order", methods=["GET"])
def sort_posts():
    sort_by = request.args.get("sort","title")
    direction = request.args.get("direction", "asc")

    if sort_by not in ["title", "content"]:
        return jsonify({"error": "Invalid sort field"}), 400

    if direction not in ["asc", "desc"]:
        return jsonify({"error": "Invalid sort direction"}), 400

    reverse = direction == "desc"

    def get_sort_value(post):
        return post[sort_by].lower()

    sorted_posts = sorted(POSTS, key=get_sort_value, reverse=reverse)
    print(sorted_posts)
    return jsonify(sorted_posts)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)












