import os
import json
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

import mvp  # your pipeline module

UPLOAD_FOLDER = "uploads"
SNAPSHOT_FOLDER = "snapshots_out"
INDEX_FOLDER = os.path.join(SNAPSHOT_FOLDER, "index")

ALLOWED_EXTENSIONS = {"pdf", "docx", "eml"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["SNAPSHOT_FOLDER"] = SNAPSHOT_FOLDER

CORS(app)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SNAPSHOT_FOLDER, exist_ok=True)
os.makedirs(INDEX_FOLDER, exist_ok=True)


# ================= HELPERS =================

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ================= UPLOAD =================

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No filename"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Unsupported file type"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    try:
        # 🔥 Run full agent pipeline
        outputs = mvp.process_file(file_path)

        results = []
        for role, path in outputs:
            results.append({
                "role": role,
                "snapshot_file": os.path.basename(path)
            })

        return jsonify({
            "message": "Processed successfully",
            "doc_id": filename,
            "snapshots": results,
            "status": "success"
        })

    except Exception as e:
        return jsonify({
            "error": "Processing failed",
            "details": str(e)
        }), 500


# ================= DOWNLOAD SNAPSHOT =================

@app.route("/snapshots/<path:filename>")
def get_snapshot(filename):
    return send_from_directory(
        app.config["SNAPSHOT_FOLDER"],
        filename,
        as_attachment=True
    )


# ================= QUERY =================

@app.route("/query", methods=["POST"])
def query_docs():
    """
    JSON:
    {
        "query": "your question",
        "doc_id": "optional filename"
    }
    """

    data = request.get_json(force=True)
    query = (data.get("query") or "").strip()
    doc_id = (data.get("doc_id") or "").strip()

    if not query:
        return jsonify({"error": "query is required"}), 400

    if not os.path.exists(INDEX_FOLDER):
        return jsonify({"error": "No index found. Upload a document first."}), 400

    chunks = []

    try:
        if doc_id:
            idx_path = os.path.join(INDEX_FOLDER, f"{os.path.splitext(doc_id)[0]}.chunks.json")

            if not os.path.exists(idx_path):
                return jsonify({"error": f"No index for doc_id={doc_id}"}), 400

            with open(idx_path, "r", encoding="utf-8") as f:
                chunks = json.load(f)

        else:
            # 🔥 multi-doc query
            for fn in os.listdir(INDEX_FOLDER):
                if fn.endswith(".chunks.json"):
                    with open(os.path.join(INDEX_FOLDER, fn), "r", encoding="utf-8") as f:
                        chunks.extend(json.load(f))

        # 🔥 AGENTIC ANSWER
        result = mvp.answer_query(query, chunks)

        return jsonify({
            "query": query,
            "answer": result.get("answer"),
            "confidence": result.get("confidence"),
            "citations": result.get("citations"),
            "status": "success"
        })

    except Exception as e:
        return jsonify({
            "error": "Query failed",
            "details": str(e)
        }), 500


# ================= HEALTH CHECK =================

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "running",
        "upload_folder": UPLOAD_FOLDER,
        "snapshot_folder": SNAPSHOT_FOLDER
    })


# ================= RUN =================

if __name__ == "__main__":
    app.run(debug=True, port=5000)