from flask import jsonify, request, Blueprint

from downloads.auth import authorizer
from downloads.models import Download

api = Blueprint('api', __name__)


@api.route('/', methods=['GET'])
@authorizer
def api_index():
    return jsonify({
        "success": True,
        "downloads": Download.count()
    })


@api.route('/download/', methods=['POST'])
@authorizer
def api_download():
    files = request.get_json().get("files", [])
    result = []

    for file in files:
        download = Download.loads(file)
        download.save()

        result.append(Download.dumps(download))

    return jsonify({
        "success": True,
        "files": result
    }), 201


@api.route('/download/retry/', methods=['post'])
@authorizer
def download_retry_all():
    Download.retry_all()
    return jsonify({"success": True})


@api.route('/download/<hash>/retry/', methods=['post'])
@authorizer
def download_retry_single(hash):
    download = Download.get_by_hash(hash)
    if not download:
        return jsonify({"success": False}), 404

    download.failed = 0
    download.retries = 0
    download.save()

    return jsonify({"success": True})


@api.route('/download/status/', methods=['POST'])
@authorizer
def download_status_bulk():
    files = request.get_json().get("files", [])
    downloads = Download.list_by_hash(files)

    return jsonify({
        "success": True,
        "files": {
            download.hash: Download.dumps(download)
            for download in downloads
        }
    })


@api.route('/download/<hash>/', methods=['GET'])
@authorizer
def download_status_single(hash):
    download = Download.get_by_hash(hash)
    if not download:
        return jsonify({"success": False}), 404

    return jsonify({
        "success": True,
        "file": Download.dumps(download)
    })
