
def chat_serializer(chat) -> dict:
    return {
        '_id': str(chat["_id"]),
        'user_id': chat["user_id"],
        'prompt': chat["prompt"],
        'generated': chat["generated"],
        'created_at': chat["created_at"],
    }
    
def chats_serializer(chats, user_id) -> list:
    return [
        {
            '_id': str(chat["_id"]),
            'user_id': chat["user_id"],
            'prompt': chat["prompt"],
            'generated': chat["generated"],
            'created_at': chat["created_at"],
        }
        for chat in chats
        if chat["user_id"] == user_id
    ]