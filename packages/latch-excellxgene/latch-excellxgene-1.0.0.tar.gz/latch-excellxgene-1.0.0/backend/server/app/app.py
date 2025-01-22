import datetime
import logging
from functools import wraps
from http import HTTPStatus

from flask import (
    Flask,
    current_app,
    make_response,
    jsonify,
    Response,
    render_template,
    Blueprint,
    request,
    send_from_directory,
    session,
    after_this_request,
    stream_with_context,
    send_file,
    send_from_directory
)
from flask_restful import Api, Resource
import backend.server.common.rest as common_rest
from backend.common.errors import DatasetAccessError, RequestException
from backend.server.common.health import health_check
from backend.common.utils.utils import Float32JSONEncoder
import os

webbp = Blueprint("webapp", "backend.server.common.web", template_folder="templates")

ONE_WEEK = 7 * 24 * 60 * 60

   
def auth0_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = 'excxg_profile' in session
        # return 401 if token is not passed
        if not token and current_app.hosted_mode:
            return jsonify({'message' : 'Authorization missing.'}), 401
  
        return  f(*args, **kwargs)
  
    return decorated

def desktop_mode_only(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if current_app.hosted_mode:
            return jsonify({'message' : 'Feature only available in desktop mode.'}), 401
  
        return  f(*args, **kwargs)
  
    return decorated    

def hosted_mode_only(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_app.hosted_mode:
            return jsonify({'message' : 'Feature only available in hosted mode.'}), 401
  
        return  f(*args, **kwargs)
  
    return decorated    

def _cache_control(always, **cache_kwargs):
    """
    Used to easily manage cache control headers on responses.
    See Werkzeug for attributes that can be set, eg, no_cache, private, max_age, etc.
    https://werkzeug.palletsprojects.com/en/1.0.x/datastructures/#werkzeug.datastructures.ResponseCacheControl
    """

    def inner_cache_control(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            response = make_response(f(*args, **kwargs))
            if not always and not current_app.app_config.server_config.app__generate_cache_control_headers:
                return response
            if response.status_code >= 400:
                return response
            for k, v in cache_kwargs.items():
                setattr(response.cache_control, k, v)
            return response

        return wrapper

    return inner_cache_control


def cache_control(**cache_kwargs):
    """ config driven """
    return _cache_control(False, **cache_kwargs)


def cache_control_always(**cache_kwargs):
    """ always generate headers, regardless of the config """
    return _cache_control(True, **cache_kwargs)


@webbp.route("/", methods=["GET"])
def dataset_index():
    app_config = current_app.app_config

    dataset_config = app_config.get_dataset_config()
    scripts = dataset_config.app__scripts
    inline_scripts = dataset_config.app__inline_scripts

    try:
        args = {"SCRIPTS": scripts, "INLINE_SCRIPTS": inline_scripts}
        return render_template("index.html", **args)

    except DatasetAccessError as e:
        return common_rest.abort_and_log(
            e.status_code, f"Invalid dataset: {e.message}", loglevel=logging.INFO, include_exc_info=True
        )


@webbp.errorhandler(RequestException)
def handle_request_exception(error):
    return common_rest.abort_and_log(error.status_code, error.message, loglevel=logging.INFO, include_exc_info=True)


def requires_authentication(func):
    @wraps(func)
    def wrapped_function(self, *args, **kwargs):
        auth = current_app.auth
        if auth.is_user_authenticated():
            return func(self, *args, **kwargs)
        else:
            return make_response("not authenticated", HTTPStatus.UNAUTHORIZED)

    return wrapped_function


def rest_get_data_adaptor(func):
    @wraps(func)
    def wrapped_function(self):
        try:
            return func(self, current_app.data_adaptor)
        except DatasetAccessError as e:
            return common_rest.abort_and_log(
                e.status_code, f"Invalid dataset: {e.message}", loglevel=logging.INFO, include_exc_info=True
            )

    return wrapped_function


class HealthAPI(Resource):
    @cache_control_always(no_store=True)
    def get(self):
        config = current_app.app_config
        return health_check(config)


class SchemaAPI(Resource):
    @cache_control(public=True, max_age=ONE_WEEK)
    @rest_get_data_adaptor
    def get(self, data_adaptor):
        return common_rest.schema_get(data_adaptor)

class InitializeUserAPI(Resource):
    @cache_control(public=True, max_age=ONE_WEEK)
    @rest_get_data_adaptor
    def get(self, data_adaptor):
        return common_rest.initialize_user(data_adaptor)

class ConfigAPI(Resource):
    @cache_control(public=True, max_age=ONE_WEEK)
    @rest_get_data_adaptor
    def get(self, data_adaptor):
        return common_rest.config_get(current_app.app_config, data_adaptor)


class UserInfoAPI(Resource):
    @cache_control_always(no_store=True)
    @rest_get_data_adaptor
    def get(self, data_adaptor):
        return common_rest.userinfo_get(current_app.app_config, data_adaptor)


class AnnotationsObsAPI(Resource):
    @cache_control(public=True, max_age=ONE_WEEK)
    @rest_get_data_adaptor
    def get(self, data_adaptor):
        return common_rest.annotations_obs_get(request, data_adaptor)

    @requires_authentication
    @cache_control(no_store=True)
    @auth0_token_required
    @rest_get_data_adaptor
    def put(self, data_adaptor):
        return common_rest.annotations_obs_put(request, data_adaptor)

class UserInfoAuth0API(Resource):
    @cache_control(public=True, max_age=ONE_WEEK)
    def get(self):
        if 'excxg_profile' in session:
            return make_response(jsonify({"response": session['excxg_profile']}), HTTPStatus.OK)
        else:
            return make_response(jsonify({"response": None}), HTTPStatus.OK)            

class HostedModeAPI(Resource):
    @cache_control(public=True, max_age=ONE_WEEK)
    @rest_get_data_adaptor
    def get(self, data_adaptor):
        def _get_user_id(data_adaptor):
            annotations = data_adaptor.dataset_config.user_annotations        
            userID = f"{annotations._get_userdata_idhash(data_adaptor)}"       
            return userID        
        return make_response(jsonify({"response": current_app.hosted_mode,
                                      "cxgMode": _get_user_id(data_adaptor).split('/')[-1].split('\\')[-1]}),
                                      HTTPStatus.OK)


class JointModeAPI(Resource):
    @cache_control(public=True, max_age=ONE_WEEK)
    @rest_get_data_adaptor
    def get(self, data_adaptor):    
        return make_response(jsonify({"response": data_adaptor._joint_mode}),HTTPStatus.OK)

class SwitchCxgModeAPI(Resource):
    @cache_control(public=True, max_age=ONE_WEEK)
    @rest_get_data_adaptor
    @auth0_token_required
    def get(self, data_adaptor):
        return common_rest.switch_cxg_mode(request, data_adaptor)


class SendFileAPI(Resource):
    @cache_control(public=True, max_age=ONE_WEEK)
    @rest_get_data_adaptor
    @auth0_token_required
    def get(self,data_adaptor):
        field = request.args.get("path", None)
        os.remove(field)
        return make_response()

class AnnotationsVarAPI(Resource):
    @cache_control(public=True, max_age=ONE_WEEK)
    @rest_get_data_adaptor
    def get(self, data_adaptor):
        return common_rest.annotations_var_get(request, data_adaptor)

    @requires_authentication
    @cache_control(no_store=True)
    @auth0_token_required
    @rest_get_data_adaptor
    def put(self, data_adaptor):
        return common_rest.annotations_var_put(request, data_adaptor)


class DataVarAPI(Resource):
    @cache_control(no_store=True)
    @rest_get_data_adaptor
    @auth0_token_required
    def put(self, data_adaptor):
        return common_rest.data_var_put(request, data_adaptor)

    @cache_control(public=True, max_age=ONE_WEEK)
    @rest_get_data_adaptor
    def get(self, data_adaptor):
        return common_rest.data_var_get(request, data_adaptor)


class ColorsAPI(Resource):
    @cache_control(public=True, max_age=ONE_WEEK)
    @rest_get_data_adaptor
    def get(self, data_adaptor):
        return common_rest.colors_get(data_adaptor)


class DiffExpObsAPI(Resource):
    @cache_control(no_store=True)
    @rest_get_data_adaptor
    @auth0_token_required
    def post(self, data_adaptor):
        return common_rest.diffexp_obs_post(request, data_adaptor)

class PreprocessAPI(Resource):
    @cache_control(no_store=True)
    @rest_get_data_adaptor
    @auth0_token_required
    @desktop_mode_only
    def put(self, data_adaptor):
        return common_rest.preprocess_put(request, data_adaptor)


class LayoutObsAPI(Resource):
    @cache_control(public=True, max_age=ONE_WEEK)
    @rest_get_data_adaptor
    def get(self, data_adaptor):
        return common_rest.layout_obs_get(request, data_adaptor)

class LayoutObsJointAPI(Resource):
    @cache_control(public=True, max_age=ONE_WEEK)
    @rest_get_data_adaptor
    def get(self, data_adaptor):
        return common_rest.layout_obs_get_joint(request, data_adaptor)

class SankeyPlotAPI(Resource):
    @cache_control(no_store=True)
    @rest_get_data_adaptor
    def put(self, data_adaptor):
        return common_rest.sankey_data_put(request, data_adaptor)

class OutputAPI(Resource):
    @cache_control(no_store=True)
    @rest_get_data_adaptor
    def put(self, data_adaptor):
        return common_rest.output_data_put(request, data_adaptor)

class DownloadAnndataAPI(Resource):
    @cache_control(no_store=True)
    @rest_get_data_adaptor
    @auth0_token_required
    def put(self, data_adaptor):
        return common_rest.save_data_put(request, data_adaptor)

class DownloadMetadataAPI(Resource):
    @cache_control(no_store=True)
    @rest_get_data_adaptor
    def put(self, data_adaptor):
        return common_rest.save_metadata_put(request, data_adaptor)

class DownloadVarMetadataAPI(Resource):
    @cache_control(no_store=True)
    @rest_get_data_adaptor
    def put(self, data_adaptor):
        return common_rest.save_var_metadata_put(request, data_adaptor)

class DownloadGenedataAPI(Resource):
    @cache_control(no_store=True)
    @rest_get_data_adaptor
    def put(self, data_adaptor):
        return common_rest.save_genedata_put(request, data_adaptor)

class DeleteObsAPI(Resource):
    @cache_control(no_store=True)
    @rest_get_data_adaptor
    @auth0_token_required
    def put(self, data_adaptor):
        return common_rest.delete_obs_put(request, data_adaptor)

class RenameObsAPI(Resource):
    @cache_control(no_store=True)
    @rest_get_data_adaptor
    @auth0_token_required
    def put(self, data_adaptor):
        return common_rest.rename_obs_put(request, data_adaptor)

class RenameDiffAPI(Resource):
    @cache_control(no_store=True)
    @rest_get_data_adaptor
    @auth0_token_required
    def put(self, data_adaptor):
        return common_rest.rename_diff_put(request, data_adaptor)

class DeleteDiffAPI(Resource):
    @cache_control(no_store=True)
    @rest_get_data_adaptor
    @auth0_token_required
    def put(self, data_adaptor):
        return common_rest.delete_diff_put(request, data_adaptor)

class RenameSetAPI(Resource):
    @cache_control(no_store=True)
    @rest_get_data_adaptor
    @auth0_token_required
    def put(self, data_adaptor):
        return common_rest.rename_set_put(request, data_adaptor)

class DeleteSetAPI(Resource):
    @cache_control(no_store=True)
    @rest_get_data_adaptor
    @auth0_token_required
    def put(self, data_adaptor):
        return common_rest.delete_set_put(request, data_adaptor)

class RenameGeneSetAPI(Resource):
    @cache_control(no_store=True)
    @rest_get_data_adaptor
    @auth0_token_required
    def put(self, data_adaptor):
        return common_rest.rename_geneset_put(request, data_adaptor)

class DeleteGeneSetAPI(Resource):
    @cache_control(no_store=True)
    @rest_get_data_adaptor
    @auth0_token_required
    def put(self, data_adaptor):
        return common_rest.delete_geneset_put(request, data_adaptor)        

class DeleteObsmAPI(Resource):
    @cache_control(no_store=True)
    @rest_get_data_adaptor
    @auth0_token_required
    def put(self, data_adaptor):
        return common_rest.delete_obsm_put(request, data_adaptor)

class UploadVarMetadata(Resource):
    @rest_get_data_adaptor
    @cache_control(no_store=True)
    @auth0_token_required
    def post(self, data_adaptor):
        return common_rest.upload_var_metadata_post(request, data_adaptor)
   
class RenameObsmAPI(Resource):
    @cache_control(no_store=True)
    @rest_get_data_adaptor
    @auth0_token_required
    def put(self, data_adaptor):
        return common_rest.rename_obsm_put(request, data_adaptor)

class LeidenClusterAPI(Resource):
    @cache_control(no_store=True)
    @rest_get_data_adaptor
    @auth0_token_required
    def put(self, data_adaptor):
        return common_rest.leiden_put(request, data_adaptor)

class ReembedParametersObsmAPI(Resource):
    @cache_control(no_store=True)
    @rest_get_data_adaptor
    def put(self, data_adaptor):
        return common_rest.reembed_parameters_obsm_put(request, data_adaptor)

class GeneInfoAPI(Resource):
    @cache_control(public=True, max_age=ONE_WEEK)
    @rest_get_data_adaptor
    @requires_authentication
    def get(self, data_adaptor):
        return common_rest.gene_info_get(request, data_adaptor)

class DiffGroupInfo(Resource):
    @cache_control(public=True, max_age=ONE_WEEK)
    @rest_get_data_adaptor
    @requires_authentication    
    def get(self, data_adaptor):
        return common_rest.diff_group_get(request, data_adaptor)

class DiffStatsInfo(Resource):
    @cache_control(public=True, max_age=ONE_WEEK)
    @rest_get_data_adaptor
    @requires_authentication
    def get(self, data_adaptor):
        return common_rest.diff_stats_get(request, data_adaptor)        

class DiffGenesInfo(Resource):
    @cache_control(public=True, max_age=ONE_WEEK)
    @rest_get_data_adaptor
    @requires_authentication    
    def get(self, data_adaptor):
        return common_rest.diff_genes_get(request, data_adaptor)    
    
    @requires_authentication
    @cache_control(no_store=True)
    @rest_get_data_adaptor
    @auth0_token_required
    def put(self, data_adaptor):
        return common_rest.diff_genes_put(request, data_adaptor)            


class ResetToRootFolder(Resource):
    @requires_authentication
    @cache_control(no_store=True)
    @rest_get_data_adaptor
    @auth0_token_required
    def put(self, data_adaptor):
        return common_rest.reset_to_root_folder(request, data_adaptor)

class AdminRestartMP(Resource):
    @cache_control(public=True, max_age=ONE_WEEK)
    @rest_get_data_adaptor
    @requires_authentication
    @auth0_token_required
    def get(self, data_adaptor):
        return common_rest.admin_restart_get(request, data_adaptor)


class GeneInfoBulkAPI(Resource):
    @requires_authentication
    @cache_control(no_store=True)
    @rest_get_data_adaptor
    def put(self, data_adaptor):
        return common_rest.gene_info_bulk_put(request, data_adaptor)

class ReembedParametersAPI(Resource):
    @cache_control(public=True, max_age=ONE_WEEK)
    @rest_get_data_adaptor
    def get(self, data_adaptor):
        return common_rest.reembed_parameters_get(request, data_adaptor)

    @requires_authentication
    @cache_control(no_store=True)
    @rest_get_data_adaptor
    @auth0_token_required
    def put(self, data_adaptor):
        return common_rest.reembed_parameters_put(request, data_adaptor)

class GenesetsAPI(Resource):
    @cache_control(public=True, max_age=ONE_WEEK)
    @rest_get_data_adaptor
    def get(self, data_adaptor):
        return common_rest.genesets_get(request, data_adaptor)

    @requires_authentication
    @cache_control(no_store=True)
    @rest_get_data_adaptor
    @auth0_token_required
    def put(self, data_adaptor):
        return common_rest.genesets_put(request, data_adaptor)

class GenesetsRenameAPI(Resource):
    @requires_authentication
    @cache_control(no_store=True)
    @rest_get_data_adaptor
    @auth0_token_required
    def put(self, data_adaptor):
        return common_rest.genesets_rename_put(request, data_adaptor)


class SummarizeVarAPI(Resource):
    @rest_get_data_adaptor
    @cache_control(public=True, max_age=ONE_WEEK)
    def get(self, data_adaptor):
        return common_rest.summarize_var_get(request, data_adaptor)

    @rest_get_data_adaptor
    @cache_control(no_store=True)
    @auth0_token_required
    def post(self, data_adaptor):
        return common_rest.summarize_var_post(request, data_adaptor)


def get_api_base_resources(bp_base):
    """Add resources that are accessed from the api url"""
    api = Api(bp_base)

    # Diagnostics routes
    api.add_resource(HealthAPI, "/health")
    return api


def get_api_dataroot_resources(bp_dataroot):
    """Add resources that refer to a dataset"""
    api = Api(bp_dataroot)

    def add_resource(resource, url):
        """convenience function to make the outer function less verbose"""
        api.add_resource(resource, url)

    # Initialization routes
    add_resource(SchemaAPI, "/schema")
    add_resource(InitializeUserAPI, "/initialize")
    add_resource(SendFileAPI, "/downloadCallback")
    add_resource(ConfigAPI, "/config")
    add_resource(UserInfoAPI, "/userinfo")
    add_resource(UserInfoAuth0API, "/userInfo")
    add_resource(HostedModeAPI, "/hostedMode")
    add_resource(JointModeAPI, "/jointMode")
    add_resource(GeneInfoAPI, "/geneInfo")
    add_resource(GeneInfoBulkAPI, "/geneInfoBulk")
    add_resource(ResetToRootFolder,"/resetToRoot")
    add_resource(AdminRestartMP, "/adminRestart")
    add_resource(SwitchCxgModeAPI,"/switchCxgMode")
    add_resource(UploadVarMetadata, "/uploadVarMetadata")    
    # Data routes
    add_resource(AnnotationsObsAPI, "/annotations/obs")
    add_resource(AnnotationsVarAPI, "/annotations/var")
    add_resource(DataVarAPI, "/data/var")
    add_resource(GenesetsAPI, "/genesets")
    #add_resource(GenesetsRenameAPI, "/genesets/rename")
    
    add_resource(ReembedParametersAPI, "/reembed-parameters")
    add_resource(ReembedParametersObsmAPI, "/reembed-parameters-obsm")

    #add_resource(SankeyPlotAPI, "/sankey")
    #add_resource(OutputAPI, "/output")
    #add_resource(DownloadAnndataAPI, "/downloadAnndata")
    add_resource(DownloadMetadataAPI, "/downloadMetadata")
    add_resource(DownloadVarMetadataAPI, "/downloadVarMetadata")
    add_resource(DownloadGenedataAPI, "/downloadGenedata")
    #add_resource(LeidenClusterAPI, "/leiden")
    add_resource(DeleteObsmAPI, "/layout/obsm")
    add_resource(RenameObsmAPI, "/layout/rename")
    
    add_resource(DeleteObsAPI, "/annotations/delete")
    add_resource(RenameObsAPI, "/annotations/rename")
    add_resource(RenameDiffAPI, "/renameDiffExp")  
    add_resource(DeleteDiffAPI, "/deleteDiffExp") 
    add_resource(RenameSetAPI, "/renameSet")  
    add_resource(DeleteSetAPI, "/deleteSet") 
    add_resource(RenameGeneSetAPI, "/renameGeneSet")  
    add_resource(DeleteGeneSetAPI, "/deleteGeneSet")         
    add_resource(DiffGroupInfo, "/diffExpPops") 
    add_resource(DiffStatsInfo, "/diffExpStats")   
    add_resource(DiffGenesInfo, "/diffExpGenes")  
    #add_resource(PreprocessAPI, "/preprocess")
    add_resource(SummarizeVarAPI, "/summarize/var")
    # Display routes
    add_resource(ColorsAPI, "/colors")
    # Computation routes
    #add_resource(DiffExpObsAPI, "/diffexp/obs")
    add_resource(LayoutObsAPI, "/layout/obs")
    add_resource(LayoutObsJointAPI, "/layout/jemb")
    return api


class Server:
    @staticmethod
    def _before_adding_routes(app, app_config):
        """ will be called before routes are added, during __init__.  Subclass protocol """
        pass

    def __init__(self, app_config):
        self.app = Flask(__name__, static_folder=None)
        self._before_adding_routes(self.app, app_config)
        self.app.json_encoder = Float32JSONEncoder
        server_config = app_config.server_config

        # enable session data
        self.app.permanent_session_lifetime = datetime.timedelta(days=50 * 365)

        # Config
        secret_key = server_config.app__flask_secret_key
        self.app.config.update(SECRET_KEY=secret_key)

        self.app.register_blueprint(webbp)

        api_version = "/api/v0.2"
        api_path = "/"

        bp_base = Blueprint("bp_base", __name__, url_prefix=api_path)
        base_resources = get_api_base_resources(bp_base)
        self.app.register_blueprint(base_resources.blueprint)

        bp_api = Blueprint("api", __name__, url_prefix=f"{api_path}{api_version}")
        resources = get_api_dataroot_resources(bp_api)
        self.app.register_blueprint(resources.blueprint)
        self.app.add_url_rule(
            "/static/<path:filename>",
            "static_assets",
            view_func=lambda filename: send_from_directory("../common/web/static", filename),
            methods=["GET"],
        )

        self.app.data_adaptor = server_config.data_adaptor
        self.app.app_config = app_config

        auth = server_config.auth
        self.app.auth = auth
        if auth.requires_client_login():
            auth.add_url_rules(self.app)
        auth.complete_setup(self.app)
