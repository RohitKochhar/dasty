# Imports ---------------------------------------------------------------------
import quart

# App setup -------------------------------------------------------------------
app = quart.Quart(__name__)

# Globals ---------------------------------------------------------------------
users = [
    {"id": 0, "name": "Alice"},
    {"id": 1, "name": "Bob"},
    {"id": 2, "name": "Charlie"},
]

# Routes ----------------------------------------------------------------------
@app.route('/')
async def handle_get_root():
    """
    Resets the users global variable
    """
    global users 
    users = [{"id": 0, "name": "Alice"}, {"id": 1, "name": "Bob"}, {"id": 2, "name": "Charlie"}]

    return 'OK'

@app.route('/healthz')
async def handle_get_healthz():
    """
    Returns a health check
    """
    return "OK"

@app.route('/readyz')
async def handle_get_readyz():
    """
    Returns a readiness check
    """
    return "OK"

@app.route('/users', methods=['GET'])
async def handle_get_users():
    """
    Returns a set of users
    """
    return {"users": users}

@app.route('/users/id=<int:id>', methods=['GET'])
async def handle_get_users_id(id):
    """
    Returns a user with the specified id
    """
    for user in users:
        if user["id"] == id:
            return {"user": user}
    return {"message": f"User {id} not found"}, 404

@app.route('/users/name=<name>', methods=['GET'])
async def handle_get_users_name(name):
    """
    Returns a user with the specified name
    """
    for user in users:
        if user["name"] == name:
            return {"user": user}
    return {"message": f"User {name} not found"}, 404

@app.route('/users/name=<name>', methods=['POST'])
async def handle_post_users(name):
    """
    Adds a new user
    """
    user = {"id": len(users) + 1, "name": name}
    users.append(user)
    return {"users": user}

@app.route('/users/name=<name>', methods=['DELETE'])
async def handle_delete_users(name):
    """
    Deletes a user
    """
    # Get the index of the user with the specified name
    for user in users:
        if user["name"] == name:
            users.remove(user)
            return {"message": f"Deleted user {name}"}, 200
    return {"message": f"User {name} not found"}, 404

# Run the app -----------------------------------------------------------------
if __name__ == "__main__":
        app.run(host='0.0.0.0', port=2396)
