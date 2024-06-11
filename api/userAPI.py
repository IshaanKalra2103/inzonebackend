import uuid
from flask import Blueprint, request, jsonify
from firebase_admin import firestore

# Initialize Firestore client
db = firestore.client()
user_ref = db.collection("users")

# Define a Flask Blueprint for the user API
userAPI = Blueprint("userAPI", __name__)

# Helper function to get user document reference and snapshot
def get_user_document(user_email):
    user_doc_ref = user_ref.document(user_email)
    return user_doc_ref, user_doc_ref.get()

# Route to add a new user
@userAPI.route("/users", methods=["POST"])
def add_user():
    try:
        data = request.json
        user_email = data.get("email")
        user_doc_ref, user_doc = get_user_document(user_email)

        # Check if the user already exists
        if user_doc.exists:
            return jsonify({"error": "User already exists"}), 400

        # Create user data dictionary
        user_data = {
            "age": data.get("age"),
            "ai": data.get("ai"),
            "bio": data.get("bio"),
            "categories": data.get("categories"),
            "chats": data.get("chats", []),
            "email": user_email,
            "family": data.get("family", []),
            "firstName": data.get("firstName"),
            "followers": data.get("followers", []),
            "following": data.get("following", []),
            "gender": data.get("gender"),
            "lastName": data.get("lastName"),
            "parent": data.get("parent"),
            "uid": str(uuid.uuid4()),
            "user_name": data.get("user_name"),
        }

        # Save user data to Firestore
        user_doc_ref.set(user_data)
        return jsonify({"success": True, "uid": user_data["uid"]}), 200
    except Exception as e:
        return f"An exception occurred: {e}", 500

# Route to get all users
@userAPI.route("/users", methods=["GET"])
def get_users():
    try:
        users = user_ref.get()
        users_list = [user.to_dict() for user in users]
        return jsonify(users_list), 200
    except Exception as e:
        return f"An exception occurred: {e}", 500

# Route to get a specific user by email
@userAPI.route("/users/<user_email>", methods=["GET"])
def get_user(user_email):
    try:
        user_doc_ref, user_doc = get_user_document(user_email)
        if user_doc.exists:
            return jsonify(user_doc.to_dict()), 200
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return f"An exception occurred: {e}", 500

# Route to update user information
@userAPI.route("/users/<user_email>", methods=["PUT"])
def update_user(user_email):
    try:
        data = request.json
        user_doc_ref, user_doc = get_user_document(user_email)

        # Check if the user exists
        if not user_doc.exists:
            return jsonify({"error": "User not found"}), 404

        user_data = user_doc.to_dict()

        # Update user fields
        user_data.update(
            {
                "age": data.get("age", user_data.get("age")),
                "ai": data.get("ai", user_data.get("ai")),
                "bio": data.get("bio", user_data.get("bio")),
                "categories": data.get("categories", user_data.get("categories")),
                "chats": data.get("chats", user_data.get("chats")),
                "email": data.get("email", user_data.get("email")),
                "family": data.get("family", user_data.get("family")),
                "firstName": data.get("firstName", user_data.get("firstName")),
                "followers": data.get("followers", user_data.get("followers")),
                "following": data.get("following", user_data.get("following")),
                "gender": data.get("gender", user_data.get("gender")),
                "lastName": data.get("lastName", user_data.get("lastName")),
                "parent": data.get("parent", user_data.get("parent")),
                "user_name": data.get("user_name", user_data.get("user_name")),
            }
        )

        # Save updated user data to Firestore
        user_doc_ref.set(user_data)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An exception occurred: {e}", 500

# Route to get a user's followers and following
@userAPI.route("/users/<user_email>/followers_following", methods=["GET"])
def get_user_followers_following(user_email):
    try:
        user_doc_ref, user_doc = get_user_document(user_email)
        if user_doc.exists:
            user_data = user_doc.to_dict()
            return (
                jsonify(
                    {
                        "followers": user_data.get("followers", []),
                        "following": user_data.get("following", []),
                    }
                ),
                200,
            )
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return f"An exception occurred: {e}", 500

# Route to add a follower or following
@userAPI.route("/users/<user_email>/followers_following", methods=["POST"])
def add_follower_or_following(user_email):
    try:
        data = request.json
        addition_type = data.get("type")
        new_entry = {
            "email": data.get("email"),
            "name": data.get("name"),
            "profileImage": data.get("profileImage"),
            "verified": data.get("verified"),
        }

        user_doc_ref, user_doc = get_user_document(user_email)
        if user_doc.exists:
            user_data = user_doc.to_dict()
            if addition_type == "followers":
                user_data.setdefault("followers", []).append(new_entry)
            elif addition_type == "following":
                user_data.setdefault("following", []).append(new_entry)
            else:
                return jsonify({"error": "Invalid addition type"}), 400

            user_doc_ref.set(user_data)
            return jsonify({"success": True}), 200
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return f"An exception occurred: {e}", 500

# Route to remove a follower or following
@userAPI.route("/users/remove/<user_email>", methods=["DELETE"])
def remove_follower_or_following(user_email):
    try:
        data = request.json
        other_email = data.get("other_email")
        removal_type = data.get("type")

        user_doc_ref, user_doc = get_user_document(user_email)
        if user_doc.exists:
            user_data = user_doc.to_dict()
            if removal_type == "followers":
                user_data["followers"] = [
                    f
                    for f in user_data.get("followers", [])
                    if f["email"] != other_email
                ]
            elif removal_type == "following":
                user_data["following"] = [
                    f
                    for f in user_data.get("following", [])
                    if f["email"] != other_email
                ]
            else:
                return jsonify({"error": "Invalid removal type"}), 400

            user_doc_ref.set(user_data)
            return jsonify({"success": True}), 200
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return f"An exception occurred: {e}", 500

# Route to batch add followers or following
@userAPI.route("/users/<user_email>/batch_followers_following", methods=["POST"])
def batch_add_followers_or_following(user_email):
    try:
        data = request.json
        additions = data.get("additions", [])
        addition_type = data.get("type")  # 'followers' or 'following'

        if addition_type not in ["followers", "following"]:
            return jsonify({"error": "Invalid addition type"}), 400

        user_doc_ref, user_doc = get_user_document(user_email)
        if not user_doc.exists:
            return jsonify({"error": "User not found"}), 404

        user_data = user_doc.to_dict()

        if addition_type not in user_data:
            user_data[addition_type] = []

        user_data[addition_type].extend(additions)

        # Ensure no duplicates by converting to a list of unique items
        user_data[addition_type] = list(
            {v["email"]: v for v in user_data[addition_type]}.values()
        )

        user_doc_ref.set(user_data)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An exception occurred: {e}", 500
