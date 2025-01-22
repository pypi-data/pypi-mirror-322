import os
import sys
import subprocess
import json
from steam_sdk.data.DataSettings import DataSettings, Condor
import getpass

class DriverFiQuS:
    """
        Class to drive FiQuS models
    """
    def __init__(self, FiQuS_path: str = '', path_folder_FiQuS_input: str = None, path_folder_FiQuS_output: str = None, GetDP_path: str = None, verbose: bool = False, htcondor_settings: Condor() = None) -> object:
        """

        :param FiQuS_path: full path to fiqus module
        :type FiQuS_path: str
        :param path_folder_FiQuS_input: full path to FiQuS input folder, i.e. where the input file .yaml is
        :type path_folder_FiQuS_input: str
        :param path_folder_FiQuS_output: full path to FiQuS output folder. This is typically where the same as the path_folder_FiQuS_input
        :type path_folder_FiQuS_output: str
        :param GetDP_path: full path to GetDP executable, with the executable name and extension
        :type GetDP_path: str
        :param verbose: if set to True more logs are printed to the console
        :type verbose: bool
        """
        self.FiQuS_path = FiQuS_path
        self.path_folder_FiQuS_input = path_folder_FiQuS_input
        self.path_folder_FiQuS_output = path_folder_FiQuS_output
        self.GetDP_path = GetDP_path
        self.verbose = verbose

        if htcondor_settings:
            self.htcondor_settings = htcondor_settings

        if self.FiQuS_path == 'pypi':
            import fiqus
            self.FiQuS_path = os.path.dirname(os.path.dirname(fiqus.__file__))

        if self.verbose:
            print('FiQuS path =               {}'.format(self.FiQuS_path))
            print('path_folder_FiQuS_input =  {}'.format(self.path_folder_FiQuS_input))
            print('path_folder_FiQuS_output = {}'.format(self.path_folder_FiQuS_output))
            print('GetDP_path =               {}'.format(self.GetDP_path))
            if self.htcondor_settings:
                print('htcondor_settings =    {}'.format(self.htcondor_settings))


    def run_FiQuS(self, sim_file_name: str, return_summary: bool = False):
        """
        Method to run FiQuS with a given input file name. The run type is specified in the input file.
        :param return_summary: summary of relevant parameters
        :rtype return_summary: dict
        :param sim_file_name: name of the input file (without .yaml) that must be inside the path_folder_FiQuS_input specified in the initialization
        :type sim_file_name: str
        """
        if 'pypi' in self.FiQuS_path:
            from fiqus.MainFiQuS import MainFiQuS
            try:
                MainFiQuS(
                    input_file_path=os.path.join(self.path_folder_FiQuS_input, sim_file_name + '.yaml'),
                    model_folder=self.path_folder_FiQuS_output,
                    GetDP_path=self.GetDP_path,
                    fds=DataSettings(),
                )
            except Exception as e:
                print(f"Error: {e}")
        else:
            call_commands_list = [
                sys.executable,
                os.path.join(self.FiQuS_path, 'fiqus', 'MainFiQuS.py'),
                os.path.join(self.path_folder_FiQuS_input, sim_file_name + '.yaml'),
                '-o', self.path_folder_FiQuS_output,
                '-g', self.GetDP_path,
            ]
            if self.verbose:
                command_string = " ".join(call_commands_list)
                print(f'Calling MainFiQuS via Python Subprocess.call() with: {command_string}')
            try:
                result = subprocess.call(call_commands_list, shell=False)
            except subprocess.CalledProcessError as e:
                # Handle exceptions if the command fails
                print("Error:", e)
                if result != 0:
                    raise _error_handler(call_commands_list, result, "Command failed.")
                return result
            except subprocess.CalledProcessError as e:
                # Handle exceptions if the command fails
                raise _error_handler(call_commands_list, e.returncode, e.stderr)
            
        if return_summary:
            summary = json.load(open(f"{os.path.join(self.path_folder_FiQuS_output, sim_file_name)}.json"))
            return summary
        
    def run_FiQuS_htcondor(self):
        import htcondor
        username = getpass.getuser()
        first_letter = username[0]
        col = htcondor.Collector()
        credd = htcondor.Credd()
        credd.add_user_cred(htcondor.CredTypes.Kerberos, None)
        sub = htcondor.Submit()

        root_folder_to_be_returned = folders_to_be_returned[0]
        if root_folder_to_be_returned == "Geometry":
            eos_output_folder = os.path.dirname(geometry_folder)
            eos_base_name = os.path.basename(geometry_folder)
            copy_eos_folder = ""
            relative_input_folder = ""
        elif root_folder_to_be_returned == "Mesh":
            eos_output_folder = os.path.dirname(mesh_folder)
            eos_base_name = os.path.basename(mesh_folder)
            copy_eos_folder = f"-c {geometry_folder}"
            relative_input_folder = ""
        elif root_folder_to_be_returned == "Solution":
            eos_output_folder = os.path.dirname(solution_folder)
            eos_base_name = os.path.basename(solution_folder)
            copy_eos_folder = f"-c {mesh_folder}"
            relative_input_folder = f"-p {os.path.basename(geometry_folder)}"

        relative_output_folder = os.path.relpath(os.path.join(eos_output_folder, eos_base_name), os.path.join(base_path_model_files, input_file_name))



        sub['executable'] = "fiqus/utils/call_mainfiqus_htcondor.sh"
        sub['arguments'] = f"-f {os.getcwd()} -i {input_file_path} -m {fdm_path} -s {fds_path} -o {eos_output_folder} -r {relative_output_folder} {copy_eos_folder} {relative_input_folder}"
        sub['error'] = fds.htcondor.error
        sub['output'] = fds.htcondor.output
        sub['log'] = fds.htcondor.log
        sub['request_cpus'] = str(fds.htcondor.request_cpus)
        if fds.htcondor.request_memory:
            sub['request_memory'] = fds.htcondor.request_memory
        if fds.htcondor.request_disk:
            sub['request_disk'] = fds.htcondor.request_disk

        if fds.htcondor.singularity_image_path:
            sub['+SingularityImage'] = f"\"{fds.htcondor.singularity_image_path}\""
        elif fds.htcondor.cerngetdp_version:
            sub['+SingularityImage'] = '"/cvmfs/unpacked.cern.ch/gitlab-registry.cern.ch/steam/steam-fiqus-dev-public-docker:' + f"{fds.htcondor.cerngetdp_version}\""
        else:
            sub['+SingularityImage'] = '"/cvmfs/unpacked.cern.ch/gitlab-registry.cern.ch/steam/steam-fiqus-dev-public-docker:latest/"'
        # get access to eos in singularity container
        sub['+SingularityBind'] = "'/eos:/eos'"

        sub['should_transfer_files'] = 'YES'
        sub['when_to_transfer_output'] = 'ON_EXIT_OR_EVICT'
        sub['preserve_relative_paths'] = True
        sub['+MaxRuntime'] = fds.htcondor.max_run_time
        sub['output_destination'] = f"root://eosuser.cern.ch//eos/user/{first_letter}/{username}/{fds.htcondor.eos_relative_output_path}/$(Cluster)"
        sub['MY.SendCredential'] = True
        sub['+BigMemJob'] = fds.htcondor.big_mem_job
        sub['environment'] = f"CONDOR_JOB_ID=$(Cluster)"

        schedd = htcondor.Schedd()
        result = schedd.submit(sub)

        cluster_id = result.cluster()

class _error_handler(Exception):
    def __init__(self, command, return_code, stderr):
        self.command = command
        self.return_code = return_code
        self.stderr = stderr
        super().__init__(f"Command '{command}' failed with return code {return_code}. Error: {stderr}")
