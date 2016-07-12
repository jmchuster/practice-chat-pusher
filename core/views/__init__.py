from .index import index
from .auth import auth
from .public_room import message, new

#
#
#
#
# # GET /
# @require_http_methods(['GET'])
# def index(request):
#     # draws the initial page
#     # draws the list of public channels, along with their user counts
#     # draws the friends list, pending friend requests, who's online and offline
#
# # GET /public_rooms/1/messages
# @require_http_methods(['GET'])
# def public_room_messages(request):
#     # gets you back the most recent 100 messages on public channel 1
#
# # POST /public_rooms/1/messages
# def post_public_room_messages(request):
#     # you send a message to everyone else in the room
#     # also stored in db
#     # also stored in redis
#
# # POST /public_rooms
# @require_http_methods(['POST'])
# def create_public_room(request):
#     # pass in a room name, and we'll pass back the id of the new public room, so you can open it up
#
# # GET /private_rooms/1/messages
# @require_http_methods(['GET'])
# def private_room_messages(request):
#     # gets you back the most recent 100 messages on private channel 1
#
# # POST /private_rooms/1/messages
# def post_private_room_message(request):
#     # you send a message to everyone else in the room
#     # also stored in db
#     # also stored in redis
#
# # POST /private_rooms
# def create_private_room(request):
#     # pass in a room name and a list of users, and we'll pass back the id of the new private room, so you can open it up
#
# # POST /private_rooms/1
# def update_private_room(request):
#     # pass in an updated room name and/or updated list of users
#     # delete if you pass in delete=True
#
# # POST /auth
# @require_http_methods(['GET'])
# def auth(request):
#     # trying to get access to a private or presence channel
#
# # GET /private_chats/1/messages
# @require_http_methods(['GET'])
# def private_chat_messages(request):
#     # gets you back the most recent 100 messages that you had with user 1
#
# def post_private_chat_message(request):
#     # you send a message to the user
#     # also stored in db
#     # also stored in redis
#
#
#
#
#
#
# @require_http_methods(['GET', 'POST'])
# def chat(request):
#     if request.method == 'GET':
#         return render(request, 'chat.html', { 'pusher_app_key': os.environ.get('PUSHER_APP_KEY') })
#     elif request.method == 'POST':
#         message = request.POST.get('message', '').strip()
#         if len(message) == 0:
#             return JsonStatus.Noop()
#
#         username = request.POST.get('username', '').strip() or 'anonymous'
#
#         pusher = Pusher(
#           app_id=os.environ.get('PUSHER_APP_ID'),
#           key=os.environ.get('PUSHER_APP_KEY'),
#           secret=os.environ.get('PUSHER_APP_SECRET')
#         )
#
#         pusher.trigger('presence-chat_channel', 'message_event', {
#             'username': username,
#             'message': message,
#             'timestamp': datetime.utcnow().isoformat()
#         })
#         return JsonStatus.Ok()
#
# @require_http_methods(['POST'])
# def auth(request):
#     pusher = Pusher(
#         app_id=os.environ.get('PUSHER_APP_ID'),
#         key=os.environ.get('PUSHER_APP_KEY'),
#         secret=os.environ.get('PUSHER_APP_SECRET')
#     )
#
#     user_id = request.COOKIES.get('user_id') or uuid.uuid4().hex
#
#     auth = pusher.authenticate(
#         channel=request.POST.get('channel_name', ''),
#         socket_id=request.POST.get('socket_id', ''),
#         custom_data={
#             'user_id': user_id,
#             'user_info': {
#                 'username': 'anon_' + str(hash(user_id) % 1000) # semi-random number up to 1000
#             }
#         })
#
#     response = JsonResponse(auth)
#     response.set_cookie('user_id', user_id, httponly=True)
#     return response
