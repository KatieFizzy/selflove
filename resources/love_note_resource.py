
from flask_restful import Resource, reqparse
from models.love_note_model import LoveNoteModel
from auth.auth import requires_auth

class LoveNote(Resource):

    method_decorators = [requires_auth]

    parser = reqparse.RequestParser()

    parser.add_argument('body',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('user_id',
                        type=int,
                        required=True,
                        help="Every item needs a user_id."
                        )



    def get(self, id):
        love_note = LoveNoteModel.find_by_id(id)
        if love_note:
            return love_note.json()
        return {'message': 'Item not found'}, 404

    def post(self):
        data = LoveNote.parser.parse_args()


        if LoveNoteModel.find_by_body(data.body):
            return {'message': "An note with body {}' already exists.".format(data.body)}, 400

        data = LoveNote.parser.parse_args()

        love_note = LoveNoteModel( **data)

        try:
            love_note.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return love_note.json(), 201

    def delete(self, id):
        love_note = LoveNoteModel.find_by_id(id)
        if love_note:
            love_note.delete_from_db()
            return {'message': 'Note deleted.'}
        return {'message': 'Note not found.'}, 404

    def put(self, id):
        data = LoveNote.parser.parse_args()

        love_note = LoveNoteModel.find_by_id(id)

        if love_note:
            love_note.title = data['title']
            love_note.body = data['body']
        else:
            love_note = LoveNoteModel(**data)

        love_note.save_to_db()

        return love_note.json()



class LoveNoteList(Resource):
    def get(self):
        return {'love_notes': list(map(lambda x: x.json(), LoveNoteModel.query.all()))}

