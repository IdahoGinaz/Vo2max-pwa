from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from fitparse import FitFile
from flask_cors import CORS
import zipfile, io, os

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 30 * 1024 * 1024

def extract_fit_from_zip(fobj):
    z = zipfile.ZipFile(fobj)
    for name in z.namelist():
        if name.lower().endswith('.fit'):
            return io.BytesIO(z.read(name))
    return None

def parse_vo2_from_fit_bytes(data_bytes):
    ff = FitFile(io.BytesIO(data_bytes))
    vo_val = None
    for msg in ff.get_messages():
        try:
            for field in msg:
                fdn = getattr(field, 'field_definition_number', None)
                fname = getattr(field, 'name', None)
                if fdn == 7 or (isinstance(fname, str) and fname.lower() in ('unknown_7', 'unknown 7', 'unknown-7')):
                    vo_val = field.value
                    break
            if vo_val is not None:
                break
        except Exception:
            continue
    return vo_val

@app.route('/', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'no file part'}), 400
    f = request.files['file']
    if f.filename == '':
        return jsonify({'error': 'no filename'}), 400
    filename = secure_filename(f.filename)
    data = f.read()
    fit_bytes = None
    if filename.lower().endswith('.zip'):
        fit_stream = extract_fit_from_zip(io.BytesIO(data))
        if not fit_stream:
            return jsonify({'error': 'no .fit inside zip'}), 400
        fit_bytes = fit_stream.read()
    elif filename.lower().endswith('.fit'):
        fit_bytes = data
    else:
        return jsonify({'error': 'unsupported file type'}), 400

    try:
        vo_raw = parse_vo2_from_fit_bytes(fit_bytes)
    except Exception as e:
        return jsonify({'error': 'parse_failed', 'message': str(e)}), 500

    if vo_raw is None:
        return jsonify({'found': False, 'message': 'VO2 field not found'}), 200

    try:
        vo2 = (float(vo_raw) * 3.5) / 65536
    except Exception:
        return jsonify({'error': 'invalid_vo_value', 'raw': vo_raw}), 500

    return jsonify({'found': True, 'vo2': round(vo2, 3), 'raw': vo_raw}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
