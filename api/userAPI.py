import uuid
from flask import Blueprint, request, jsonify
from firebase_admin import firestore

db = firestore.client()
user_Ref = db.collection('user')

userAPI = Blueprint('userAPI', __name__)

# @userAPI.route('/add', method = ['POST'])
# def create():
#     try:
#         id = uuid.uuid4
#         user_Ref.document(id).set(request.json)
#         return jsonify({"success": True}), 200
#     except Exception as e:
#         return f"An exception occured: {e}"
                
@userAPI.route('/users')
def get_users():
    try:
        users_ref = db.collection('users')
        users = users_ref.get()

        users_list = []
        for user in users:
            users_list.append(user.to_dict())

        return jsonify(users_list), 200
    except Exception as e:
        return f"An exception occurred: {e}", 500
    
@userAPI.route('/users/<user_email>', methods=['GET'])
def get_user(user_email):
    try:
        user_ref = db.collection('users').document(user_email)
        user_doc = user_ref.get()
        if user_doc.exists:
            user_data = user_doc.to_dict()
            return jsonify(user_data), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return f"An exception occurred: {e}", 500
    
@userAPI.route('/users/follow/<user_email>', methods=['GET'])
def get_user_following(user_email):
    try:
        user_ref = db.collection('users').document(user_email)
        user_doc = user_ref.get()
        if user_doc.exists:
            user_data = user_doc.to_dict()
            if "followers" in user_data and "following" in user_data:
                return jsonify({"followers": user_data["followers"], "following": user_data["following"]}), 200
            else:
                return jsonify({"error": "User document does not have 'followers' or 'following' field"}), 404
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return f"An exception occurred: {e}", 500
    
@userAPI.route('/users/add/<user_email>', methods=['POST'])
def add_follower_or_following(user_email):
    try:
        data = request.json
        other_email = data.get("email")
        other_name = data.get("name")
        other_profile_image = data.get("profileImage")
        other_verified = data.get("verified")
        addition_type = data.get("type")  # 'follower' or 'following'

        user_ref = db.collection('users').document(user_email)
        user_doc = user_ref.get()
        
        if user_doc.exists:
            user_data = user_doc.to_dict()

            new_entry = {
                "email": other_email,
                "name": other_name,
                "profileImage": other_profile_image,
                "verified": other_verified
            }

            if addition_type == "follower":
                if "followers" not in user_data:
                    user_data["followers"] = []
                user_data["followers"].append(new_entry)
            elif addition_type == "following":
                if "following" not in user_data:
                    user_data["following"] = []
                user_data["following"].append(new_entry)
            else:
                return jsonify({"error": "Invalid addition type"}), 400

            user_ref.set(user_data)
            return jsonify({"success": True}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return f"An exception occurred: {e}", 500



@userAPI.route('/users/remove/<user_email>', methods=['DELETE'])
def remove_follower_or_following(user_email):
    try:
        data = request.json
        other_email = data.get("other_email")
        removal_type = data.get("type")  # 'follower' or 'following'

        user_ref = db.collection('users').document(user_email)
        user_doc = user_ref.get()
        
        if user_doc.exists:
            user_data = user_doc.to_dict()

            if removal_type == "follower" and "followers" in user_data:
                user_data["followers"] = [f for f in user_data["followers"] if f["email"] != other_email]
            elif removal_type == "following" and "following" in user_data:
                user_data["following"] = [f for f in user_data["following"] if f["email"] != other_email]
            else:
                return jsonify({"error": "Invalid removal type or missing field"}), 400

            user_ref.set(user_data)
            return jsonify({"success": True}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return f"An exception occurred: {e}", 500


    



