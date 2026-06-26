from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('notes.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, content TEXT)')
    conn.commit()
    conn.close()

@app.route('/notes', methods=['GET'])
def get_notes():
    conn = get_db_connection()
    notes = conn.execute('SELECT * FROM notes').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in notes]), 200

@app.route('/notes', methods=['POST'])
def add_note():
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({'error': 'Title tidak boleh kosong!'}), 400
        
    conn = get_db_connection()
    conn.execute('INSERT INTO notes (title, content) VALUES (?, ?)', (data['title'], data.get('content', '')))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Catatan berhasil ditambahkan'}), 201

@app.route('/notes/<int:id>', methods=['DELETE'])
def delete_note(id):
    conn = get_db_connection()
    note = conn.execute('SELECT * FROM notes WHERE id = ?', (id,)).fetchone()
    if note is None:
        conn.close()
        return jsonify({'error': 'Catatan tidak ditemukan'}), 404
        
    conn.execute('DELETE FROM notes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Catatan berhasil dihapus'}), 200

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)