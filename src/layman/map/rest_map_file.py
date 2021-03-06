import json
import os
from flask import Blueprint, jsonify, current_app as app, g

from layman.http import LaymanError
from layman.util import check_username_decorator
from layman.common.filesystem.util import get_user_dir
from . import util
from layman.authn import authenticate
from layman.authz import authorize


bp = Blueprint('rest_map_file', __name__)


@bp.before_request
@authenticate
@authorize
@check_username_decorator
@util.check_mapname_decorator
def before_request():
    pass


@bp.route('/maps/<mapname>/file', methods=['GET'])
def get(username, mapname):
    app.logger.info(f"GET Map File, user={g.user}")

    # raise exception if map does not exist
    map_info = util.get_complete_map_info(username, mapname)

    if 'path' in map_info['file']:
        userdir = get_user_dir(username)
        file_path = map_info['file']['path']
        file_path = os.path.join(userdir, file_path)
        with open(file_path) as json_file:
            data = json.load(json_file)
            data['user'] = util.get_map_owner_info(username)
            data['groups'] = util.get_groups_info(username, mapname)
            return jsonify(data), 200

    raise LaymanError(27, {'mapname': mapname})



