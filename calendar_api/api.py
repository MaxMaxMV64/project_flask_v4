from flask import Flask, request, jsonify
from .model import Event

app = Flask(__name__)


@app.route('/api/v1/calendar/events', methods=['POST'])
def add_event():
    data = request.get_json()
    try:
        Event.create(data['date'], data['title'], data['text'])
        return jsonify({'message': 'Event added successfully'}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Internal server error: {e}'}), 500


@app.route('/api/v1/calendar/events', methods=['GET'])
def list_events():
    events = Event.get_all_events()
    response = []
    for event in events:
        response.append({
            'id': event.id,
            'date': event.event_date,
            'title': event.title,
            'text': event.text
        })
    return jsonify(response), 200


@app.route('/api/v1/calendar/event/<int:event_id>', methods=['GET'])
def read_event(event_id):
    event = Event.get_event_by_id(event_id)
    if not event:
        return jsonify({'error': 'Event not found'}), 404
    return jsonify({
        'id': event.id,
        'date': event.event_date,
        'title': event.title,
        'text': event.text
    }), 200


@app.route('/api/v1/calendar/event/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    data = request.get_json()
    try:
        Event.update_event(event_id, data['title'], data['text'])
        return jsonify({'message': 'Event updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': f'Something went wrong: {e}'}), 500


@app.route('/api/v1/calendar/event/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    try:
        Event.delete_event(event_id)
        return jsonify({'message': 'Event deleted successfully'}), 204
    except Exception as e:
        return jsonify({'error': f'Something went wrong: {e}'}), 500