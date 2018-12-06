import os
import sys

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse

# ensure module is found in path
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)
sys.path.insert(0, os.path.abspath(BASE_DIR))

from same_thing.db import get_connection_to_latest, is_cluster_membership, sorted_cluster
from same_thing.sink import DBP_GLOBAL_MARKER, DBP_GLOBAL_PREFIX

db = get_connection_to_latest(max_retries=12, read_only=True)
app = Starlette(debug='--debug' in sys.argv)


@app.route('/lookup/', methods=['GET'])
def lookup(request: Request) -> JSONResponse:
    uri = request.query_params.get('uri')
    if not uri:
        return JSONResponse({
            'uri': 'The `uri` parameter must be provided.'
        }, status_code=400)

    normalized_uri = uri.lstrip(DBP_GLOBAL_PREFIX)
    if normalized_uri.startswith(DBP_GLOBAL_MARKER):
        normalized_uri = normalized_uri[len(DBP_GLOBAL_MARKER):].encode('utf8')
    else:
        normalized_uri = db.get(uri.encode('utf8'))
        if not normalized_uri:
            return not_found(uri)

    value_bytes = db.get(normalized_uri)
    if not value_bytes:
        return not_found(uri)
    elif not is_cluster_membership(value_bytes):
        normalized_uri = value_bytes
        value_bytes = db.get(value_bytes)

    singletons, local_ids = sorted_cluster(value_bytes)

    response_fields = {
        'global': f"{DBP_GLOBAL_PREFIX}{DBP_GLOBAL_MARKER}{normalized_uri.decode('utf8')}",
        'locals': local_ids,
        'cluster': singletons,
    }

    meta = request.query_params.get('meta')
    if not (meta and meta == 'off'):
        response_fields['meta'] = {
            'documentation': 'http://dev.dbpedia.org/Global%20IRI%20Resolution%20Service',
            'github': 'https://github.com/dbpedia/dbp-same-thing-service',
            'license': 'http://purl.org/NET/rdflicense/cc-by3.0',
            'license_comment': 'Free service provided by DBpedia. Usage and republication of data implies that you '
                               'attribute either http://dbpedia.org as the source or reference the latest general '
                               'DBpedia paper or the specific paper mentioned in the GitHub Readme.',
            'comment': """
                The service resolves any IRI to its cluster and displays the global IRI and its cluster members.
                Cluster members can change over time as the DBpedia community, data providers and professional services curate the linking space. 
    
                Usage note: 
                1. Save the first global id AND the local IRI that seems most appropriate. 
                   It is recommended that you become a data provider, in which case the local IRI would be your IRI.  
                2. Use the global ID to access anything DBpedia.
                3. Use the stored local ID to update and revalidate linking and clusters.
            """,
        }

    return JSONResponse(response_fields)


def not_found(uri: str) -> JSONResponse:
    return JSONResponse({
        'uri': uri
    }, status_code=404)
