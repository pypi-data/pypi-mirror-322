from __future__ import annotations

import re
import xml.dom.minidom
import xml.parsers.expat
from typing import ClassVar

from qtoolkit.core.data_objects import QJob, QJobInfo, QResources, QState, QSubState
from qtoolkit.core.exceptions import CommandFailedError, OutputParsingError
from qtoolkit.io.pbs_base import PBSIOBase

# https://wiki.nikhil.io/Ancient_Sysadmin_Stuff/Sun_Grid_Engine_States/
# https://manpages.ubuntu.com/manpages/jammy/en/man5/sge_status.5.html
# Jobs Status:
#     'qw' - Queued and waiting,
#     'w' - Job waiting,
#     's' - Job suspended,
#     't' - Job transferring and about to start,
#     'r' - Job running,
#     'h' - Job hold,
#     'R' - Job restarted,
#     'd' - Job has been marked for deletion,
#     'Eqw' - An error occurred with the job.
# 'z' - finished
#
# Category     State     SGE Letter Code
# Pending:     pending     qw
# Pending:     pending, user hold     qw
# Pending:     pending, system hold     hqw
# Pending:     pending, user and system hold     hqw
# Pending:     pending, user hold, re-queue     hRwq
# Pending:     pending, system hold, re-queue     hRwq
# Pending:     pending, user and system hold, re-queue     hRwq
# Pending:     pending, user hold     qw
# Pending:     pending, user hold     qw
# Running     running     r
# Running     transferring     t
# Running     running, re-submit     Rr
# Running     transferring, re-submit     Rt
# Suspended     job suspended     s, ts
# Suspended     queue suspended     S, tS
# Suspended     queue suspended by alarm     T, tT
# Suspended     all suspended with re-submit     Rs, Rts, RS, RtS, RT, RtT
# Error     all pending states with error     Eqw, Ehqw, EhRqw
# Deleted     all running and suspended states with deletion     dr, dt, dRr, dRt,
#                                                                ds, dS, dT, dRs,
#                                                                dRS, dRT


class SGEState(QSubState):
    # Job states
    FINISHED = "z"
    QUEUED_WAITING = "qw"
    WAITING = "w"
    JOB_SUSPENDED = "s"
    TRANSFERRING = "t"
    RUNNING = "r"
    HOLD = "hqw"
    RESTARTED = "R"
    DELETION = "d"
    ERROR_PENDING = "Eqw"
    ERROR_PENDING_HOLD = "Ehqw"
    ERROR_PENDING_HOLD_REQUEUE = "EhRqw"
    DELETION_RUNNING = "dr"
    DELETION_TRANSFERRING = "dt"
    DELETION_RUNNING_RESUBMIT = "dRr"
    DELETION_TRANSFERRING_RESUBMIT = "dRt"
    DELETION_SUSPENDED_JOB = "ds"
    DELETION_SUSPENDED_QUEUE = "dS"
    DELETION_SUSPENDED_ALARM = "dT"
    DELETION_SUSPENDED_RESUBMIT_JOB = "dRs"
    DELETION_SUSPENDED_RESUBMIT_QUEUE = "dRS"
    DELETION_SUSPENDED_RESUBMIT_ALARM = "dRT"

    @property
    def qstate(self) -> QState:
        return _STATUS_MAPPING[self]  # type: ignore


_STATUS_MAPPING = {
    SGEState.FINISHED: QState.DONE,
    SGEState.QUEUED_WAITING: QState.QUEUED,
    SGEState.WAITING: QState.QUEUED,
    SGEState.HOLD: QState.QUEUED_HELD,
    SGEState.ERROR_PENDING: QState.FAILED,
    SGEState.ERROR_PENDING_HOLD: QState.FAILED,
    SGEState.ERROR_PENDING_HOLD_REQUEUE: QState.FAILED,
    SGEState.RUNNING: QState.RUNNING,
    SGEState.TRANSFERRING: QState.RUNNING,
    SGEState.RESTARTED: QState.RUNNING,
    SGEState.JOB_SUSPENDED: QState.SUSPENDED,
    SGEState.DELETION: QState.FAILED,
    SGEState.DELETION_RUNNING: QState.FAILED,
    SGEState.DELETION_TRANSFERRING: QState.FAILED,
    SGEState.DELETION_RUNNING_RESUBMIT: QState.FAILED,
    SGEState.DELETION_TRANSFERRING_RESUBMIT: QState.FAILED,
    SGEState.DELETION_SUSPENDED_JOB: QState.SUSPENDED,
    SGEState.DELETION_SUSPENDED_QUEUE: QState.SUSPENDED,
    SGEState.DELETION_SUSPENDED_ALARM: QState.SUSPENDED,
    SGEState.DELETION_SUSPENDED_RESUBMIT_JOB: QState.SUSPENDED,
    SGEState.DELETION_SUSPENDED_RESUBMIT_QUEUE: QState.SUSPENDED,
    SGEState.DELETION_SUSPENDED_RESUBMIT_ALARM: QState.SUSPENDED,
}


class SGEIO(PBSIOBase):
    header_template: str = """
#$ -cwd $${cwd}
#$ -q $${queue}
#$ -N $${job_name}
#$ -P $${device}
#$ -l $${select}
#$ -l h_rt=$${walltime}
#$ -l s_rt=$${soft_walltime}
#$ -pe $${model}
#$ -binding $${place}
#$ -W group_list=$${group_list}
#$ -M $${mail_user}
#$ -m $${mail_type}
#$ -o $${qout_path}
#$ -e $${qerr_path}
#$ -p $${priority}
#$ -r $${rerunnable}
#$ -t $${array}
$${qverbatim}"""

    SUBMIT_CMD: str | None = "qsub"
    CANCEL_CMD: str | None = "qdel"
    system_name: str = "SGE"
    default_unit: str = "M"
    power_labels: ClassVar[dict] = {"k": 0, "m": 1, "g": 2, "t": 3}
    _qresources_mapping: ClassVar[dict] = {
        "queue_name": "queue",
        "job_name": "job_name",
        "priority": "priority",
        "output_filepath": "qout_path",
        "error_filepath": "qerr_path",
        "project": "group_list",
    }

    def __init__(self, get_job_executable: str = "qstat"):
        super().__init__()
        self.get_job_executable = get_job_executable

    def extract_job_id(self, stdout):
        match = re.search(r'Your job (\d+) \(".*?"\) has been submitted', stdout)
        if not match:
            raise OutputParsingError("Failed to parse job ID from stdout")
        return match.group(1)

    def extract_job_id_from_cancel(self, stderr):
        match = re.search(r"qdel: job (\d+) deleted", stderr)
        if not match:
            raise OutputParsingError("Failed to parse job ID from stdout")
        return match.group(1)

    def _get_jobs_list_cmd(
        self, job_ids: list[str] | None = None, user: str | None = None
    ) -> str:
        if job_ids:
            raise ValueError("Querying by job IDs is not supported for SGE.")

        command = self._get_qstat_base_command()

        if user:
            command.append(f"-u {user}")

        return " ".join(command)

    def parse_job_output(self, exit_code, stdout, stderr) -> QJob | None:  # aiida style
        # TODO at the moment the command for a single job is not available
        # check if this should be removed as well.
        if exit_code != 0:
            msg = f"command {self.get_job_executable or 'qacct'} failed: {stderr}"
            raise CommandFailedError(msg)
        if isinstance(stdout, bytes):
            stdout = stdout.decode()
        if isinstance(stderr, bytes):
            stderr = stderr.decode()

        # Check for specific error messages in stderr or stdout
        error_patterns = [
            re.compile(
                r"Primary job\s+terminated normally, but\s+(\d+)\s+process returned a non-zero exit code",
                re.IGNORECASE,
            ),
            re.compile(
                r"mpiexec detected that one or more processes exited with non-zero status",
                re.IGNORECASE,
            ),
            re.compile(r"An error occurred in MPI_Allreduce", re.IGNORECASE),
            re.compile(
                r"Error: mca_pml_ucx_send_nbr failed: -25, Connection reset by remote peer",
                re.IGNORECASE,
            ),
            re.compile(r"mpi_errors_are_fatal", re.IGNORECASE),
        ]

        for pattern in error_patterns:
            if pattern.search(stderr) or pattern.search(stdout):
                msg = f"command {self.get_job_executable or 'qacct'} failed: {stderr}"
                raise CommandFailedError(msg)

        if not stdout.strip():
            return None

        # Check if stdout is in XML format
        try:
            xmldata = xml.dom.minidom.parseString(stdout)  # noqa: S318
            job_info = xmldata.getElementsByTagName("job_list")[0]
            job_id = job_info.getElementsByTagName("JB_job_number")[
                0
            ].firstChild.nodeValue  # type: ignore
            job_name = job_info.getElementsByTagName("JB_name")[0].firstChild.nodeValue  # type: ignore
            owner = job_info.getElementsByTagName("JB_owner")[0].firstChild.nodeValue  # type: ignore
            state = job_info.getElementsByTagName("state")[0].firstChild.nodeValue  # type: ignore
            queue_name = job_info.getElementsByTagName("queue_name")[
                0
            ].firstChild.nodeValue  # type: ignore
            slots = job_info.getElementsByTagName("slots")[0].firstChild.nodeValue  # type: ignore
            tasks = job_info.getElementsByTagName("tasks")[0].firstChild.nodeValue  # type: ignore

            sge_state = SGEState(state)
            job_state = sge_state.qstate

            try:
                cpus = int(slots)
                nodes = int(tasks)
                threads_per_process = int(cpus / nodes)
            except ValueError:
                cpus = None
                nodes = None
                threads_per_process = None

            return QJob(
                name=job_name,
                job_id=job_id,
                state=job_state,
                sub_state=sge_state,
                account=owner,
                queue_name=queue_name,
                info=QJobInfo(
                    nodes=nodes, cpus=cpus, threads_per_process=threads_per_process
                ),
            )
        except Exception:
            # Not XML, fallback to plain text
            job_info_dict: dict = {}
            for line in stdout.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    job_info_dict[key.strip()] = value.strip()

            try:
                cpus = int(job_info_dict.get("slots", 1))
                nodes = int(job_info_dict.get("tasks", 1))
                threads_per_process = int(cpus / nodes)
            except ValueError:
                cpus = None
                nodes = None
                threads_per_process = None

            state_str = job_info_dict.get("state")
            sge_state = SGEState(state_str) if state_str else None
            job_state = sge_state.qstate

            return QJob(
                name=job_info_dict.get("job_name"),
                job_id=job_info_dict.get("job_id"),
                state=job_state,
                sub_state=sge_state,
                account=job_info_dict.get("owner"),
                queue_name=job_info_dict.get("queue_name"),
                info=QJobInfo(
                    nodes=nodes, cpus=cpus, threads_per_process=threads_per_process
                ),
            )

    def _get_element_text(self, parent, tag_name):
        elements = parent.getElementsByTagName(tag_name)
        if elements:
            return elements[0].childNodes[0].data.strip()
        return None

    def _safe_int(self, value: str | None) -> int | None:
        if value is None:
            return None
        try:
            return int(value)
        except ValueError:
            return None

    def _get_qstat_base_command(self) -> list[str]:
        return ["qstat", "-ext", "-urg", "-xml"]

    def _get_job_ids_flag(self, job_ids_str: str) -> str:
        raise NotImplementedError("Querying by job IDs is not supported for SGE.")

    def _get_job_cmd(self, job_id: str):
        raise NotImplementedError("Querying by job IDs is not supported for SGE.")

    def parse_jobs_list_output(self, exit_code, stdout, stderr) -> list[QJob]:
        if exit_code != 0:
            msg = f"command {self.get_job_executable or 'qacct'} failed: {stderr}"
            raise CommandFailedError(msg)
        if isinstance(stdout, bytes):
            stdout = stdout.decode()
        if isinstance(stderr, bytes):
            stderr = stderr.decode()

        try:
            xmldata = xml.dom.minidom.parseString(stdout)  # noqa: S318
        except xml.parsers.expat.ExpatError as exc:
            raise OutputParsingError("XML parsing of stdout failed") from exc

        # Ensure <job_info> elements exist
        # (==> xml file created via -u option,
        # tag doesn't exist when created with -j option)
        root_element = xmldata.documentElement
        if root_element.tagName != "job_info":
            raise OutputParsingError(
                f"Unexpected root element '{root_element.tagName}', expected 'job_info'. "
                f"Ensure -u option was used for generating the xml file."
            )

        job_elements = xmldata.getElementsByTagName("job_list")

        jobs_list = []

        for job_element in job_elements:
            qjob = QJob()
            qjob.job_id = self._get_element_text(job_element, "JB_job_number")
            job_state_string = self._get_element_text(job_element, "state")

            try:
                sge_job_state = SGEState(job_state_string)
            except ValueError as exc:
                raise OutputParsingError(
                    f"Unknown job state {job_state_string} for job id {qjob.job_id}"
                ) from exc

            qjob.sub_state = sge_job_state
            qjob.state = sge_job_state.qstate
            qjob.username = self._get_element_text(job_element, "JB_owner")
            qjob.name = self._get_element_text(job_element, "JB_name")

            info = QJobInfo()
            info.nodes = self._safe_int(
                self._get_element_text(job_element, "num_nodes")
            )
            info.cpus = self._safe_int(self._get_element_text(job_element, "num_proc"))
            info.memory_per_cpu = self._convert_memory_str(
                self._get_element_text(job_element, "hard resource_list.mem_free")
            )
            info.partition = self._get_element_text(job_element, "queue")
            info.time_limit = self._convert_str_to_time(
                self._get_element_text(job_element, "hard resource_list.h_rt")
            )

            qjob.info = info

            jobs_list.append(qjob)

        return jobs_list

    @staticmethod
    def _convert_str_to_time(time_str: str | None) -> int | None:
        if time_str is None:
            return None

        parts = time_str.split(":")
        if len(parts) == 3:
            hours, minutes, seconds = parts
        elif len(parts) == 2:
            hours, minutes = "0", parts[0]
            seconds = parts[1]
        elif len(parts) == 1:
            hours, minutes, seconds = "0", "0", parts[0]
        else:
            raise OutputParsingError(f"Invalid time format: {time_str}")

        try:
            return int(hours) * 3600 + int(minutes) * 60 + int(seconds)
        except ValueError as exc:
            raise OutputParsingError(f"Invalid time format: {time_str}") from exc

    def _add_soft_walltime(self, header_dict: dict, resources: QResources):
        header_dict["soft_walltime"] = self._convert_time_to_str(
            resources.time_limit * 0.99
        )

    def sanitize_options(self, options):
        if "job_name" in options:
            options = dict(options)
            options["job_name"] = re.sub(r"[\s/@*\\:]", "_", options["job_name"])
        return options
