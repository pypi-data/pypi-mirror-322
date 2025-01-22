from .api import ipl_common
from . import auth


class Client:
    def __init__(self, api_key=None, scheme=None, host=None, api_version=None):
        self._config = auth.Config(
            api_key=api_key, scheme=scheme, host=host, api_version=api_version
        )
        self._ipl_config: ipl_common.Config = {
            "host": self._config.get_url(),  # This includes scheme and API version path prefix.
            "headers": self._config.get_headers(),
        }

    def status(self, job_id):
        path = "ipl/jobs/{}/status"
        return ipl_common.status(self._ipl_config, path, job_id)

    def wait(self, job_id, interval=10):
        path = "ipl/jobs/{}/status"
        return ipl_common.wait(self._ipl_config, path, job_id, interval)

    def decompose(
        self, file, testgen_lang, organization, callback, doc_gen, parent_job_id
    ):
        path = "ipl/decompose"
        return ipl_common.decompose(
            self._ipl_config,
            path,
            file,
            testgen_lang,
            organization,
            callback,
            doc_gen,
            parent_job_id,
        )

    def data(self, job_id, file=None):
        path = "ipl/jobs/{}/data"
        return ipl_common.data(self._ipl_config, path, job_id, file)

    def simulator(self, zone, file):
        path = "ipl/simulator/create"
        return ipl_common.simulator(self._ipl_config, zone, path, file)

    def list_jobs(self, limit=10, job_type=None):
        path = "ipl/jobs"
        return ipl_common.list_jobs(self._ipl_config, path, limit, job_type)

    def unsat_analysis(self, file, organization, callback):
        path = "ipl/unsat-analysis/jobs"
        return ipl_common.unsat_analysis(
            self._ipl_config, path, file, organization, callback
        )

    def log_analysis_builder(
        self, file, organization=None, callback=None, decomp_job_id=None
    ):
        path = "ipl/log-analysis-builder/jobs"
        return ipl_common.log_analysis_builder(
            self._ipl_config, path, file, organization, callback, decomp_job_id
        )

    def cancel(self, job_id):
        path = "ipl/jobs/{}/cancel"
        return ipl_common.cancel(self._ipl_config, path, job_id)

    def validate(
        self, file: str | None = None, model: str | None = None, organization=None
    ):
        path = "ipl/validate"
        return ipl_common.validate(self._ipl_config, path, file, model, organization)
