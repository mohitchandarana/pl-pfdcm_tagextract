#
# pfdcm_tagextract ds ChRIS plugin app
#
# (c) 2021 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

import os

from chrisapp.base import ChrisApp
import      pudb
import      pfmisc
import      subprocess
import      pfdicom_tagExtract

Gstr_title = """


        __    _                 _                        _                  _   
       / _|  | |               | |                      | |                | |  
 _ __ | |_ __| | ___ _ __ ___  | |_ __ _  __ _  _____  _| |_ _ __ __ _  ___| |_ 
| '_ \|  _/ _` |/ __| '_ ` _ \ | __/ _` |/ _` |/ _ \ \/ / __| '__/ _` |/ __| __|
| |_) | || (_| | (__| | | | | || || (_| | (_| |  __/>  <| |_| | | (_| | (__| |_ 
| .__/|_| \__,_|\___|_| |_| |_| \__\__,_|\__, |\___/_/\_\\__|_|  \__,_|\___|\__|
| |                         ______        __/ |                                 
|_|                        |______|      |___/                                  


"""

Gstr_synopsis = """

(Edit this in-line help for app specifics. At a minimum, the 
flags below are supported -- in the case of DS apps, both
positional arguments <inputDir> and <outputDir>; for FS and TS apps
only <outputDir> -- and similarly for <in> <out> directories
where necessary.)

    NAME

       pfdcm_tagextract.py 

    SYNOPSIS

        python pfdcm_tagextract.py                                         \\
            [-h] [--help]                                               \\
            [--json]                                                    \\
            [--man]                                                     \\
            [--meta]                                                    \\
            [--savejson <DIR>]                                          \\
            [-v <level>] [--verbosity <level>]                          \\
            [--version]                                                 \\
            <inputDir>                                                  \\
            <outputDir> 

    BRIEF EXAMPLE

        * Bare bones execution

            docker run --rm -u $(id -u)                             \
                -v $(pwd)/in:/incoming -v $(pwd)/out:/outgoing      \
                mchandarana/pl-pfdcm_tagextract:3.0.0 pfdcm_tagextract                        \
                /incoming /outgoing

    DESCRIPTION

        `pfdcm_tagextract.py` ...

    ARGS

        [-i] [--inputFile] <inputFile>
        An optional <inputFile> specified relative to the <inputDir>. If
        specified, then do not perform a directory walk, but convert only
        this file.
        
        [-e] [--extension] <DICOMextension>
        An optional extension to filter the DICOM files of interest from the
        <inputDir>

        [-o] [--outputFileStem] <outputFileStem>
        The output file stem to store data. This should *not* have a file
        extension, or rather, any "." in the name are considered part of
        the stem and are *not* considered extensions.

        [-t] [--outputFileType] <outputFileType>
        A comma specified list of output types. These can be:

            o <type>    <ext>       <desc>
            o raw       -raw.txt    the raw internal dcm structure to string
            o json      .json       a json representation
            o html      .html       an html representation with optional image
            o dict      -dict.txt   a python dictionary
            o col       -col.txt    a two-column text representation (tab sep)
            o csv       .csv        a csv representation

        Note that if not specified, a default type of 'raw' is assigned.

        [-h] [--help]
        If specified, show help message and exit.
        
        [--json]
        If specified, show json representation of app and exit.
        
        [--man]
        If specified, print (this) man page and exit.

        [--meta]
        If specified, print plugin meta data and exit.
        
        [--savejson <DIR>] 
        If specified, save json representation file to DIR and exit. 
        
        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.
        
        [--version]
        If specified, print version number and exit. 
"""


class Pfdcm_tagextract(ChrisApp):
    """
    An app to ...
    """
    PACKAGE                 = __package__
    TITLE                   = 'A ChRIS plugin app'
    CATEGORY                = ''
    TYPE                    = 'ds'
    ICON                    = ''   # url of an icon image
    MIN_NUMBER_OF_WORKERS   = 1    # Override with the minimum number of workers as int
    MAX_NUMBER_OF_WORKERS   = 1    # Override with the maximum number of workers as int
    MIN_CPU_LIMIT           = 1000 # Override with millicore value as int (1000 millicores == 1 CPU core)
    MIN_MEMORY_LIMIT        = 200  # Override with memory MegaByte (MB) limit as int
    MIN_GPU_LIMIT           = 0    # Override with the minimum number of GPUs as int
    MAX_GPU_LIMIT           = 0    # Override with the maximum number of GPUs as int

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """
        self.add_argument("--noJobLogging",
                            help        = "Turn off per-job logging to file system",
                            type        = bool,
                            dest        = 'noJobLogging',
                            action      = 'store_true',
                            optional    = True,
                            default     = True)

        self.add_argument("--verbose",
                            type        = str,
                            optional    = True,
                            help        = "verbosity level for app",
                            dest        = 'verbose',
                            default     = "1")
        
        self.add_argument('-i', '--inputFile',
                            dest        = 'inputFile',
                            type        = str,
                            optional    = True,
                            help        = 'name of the input file within the inputDir',
                            default     = ''
                        )

        self.add_argument('-e', '--extension',
                            dest        = 'extension',
                            type        = str,
                            optional    = True,
                            help        = 'extension of the inputFile in inputDir',
                            default     = 'dcm'
                        )

        self.add_argument('-o', '--outputFileStem',
                            dest        = 'outputFileStem',
                            type        = str,
                            optional    = True,
                            help        = 'output file stem name without extension',
                            default     = '\'%_md5|6_PatientID-%PatientAge\''
                        )

        self.add_argument('-t', '--outputFileType',
                            dest        = 'outputFileType',
                            type        = str,
                            optional    = True,
                            help        = 'extension of the outputFile in outputDir',
                            default     = 'raw'
                        )


    def job_run(self, str_cmd):
        """
        Running some CLI process via python is cumbersome. The typical/easy
        path of
                            os.system(str_cmd)
        is deprecated and prone to hidden complexity. The preferred
        method is via subprocess, which has a cumbersome processing
        syntax. Still, this method runs the `str_cmd` and returns the
        stderr and stdout strings as well as a returncode.
        Providing readtime output of both stdout and stderr seems
        problematic. The approach here is to provide realtime
        output on stdout and only provide stderr on process completion.
        """
        d_ret       : dict = {
            'stdout':       "",
            'stderr':       "",
            'cmd':          "",
            'cwd':          "",
            'returncode':   0
        }
        str_stdoutLine  : str   = ""
        str_stdout      : str   = ""

        p = subprocess.Popen(
                    str_cmd.split(),
                    stdout      = subprocess.PIPE,
                    stderr      = subprocess.PIPE,
        )

        # Realtime output on stdout
        str_stdoutLine  = ""
        str_stdout      = ""
        while True:
            stdout      = p.stdout.readline()
            if p.poll() is not None:
                break
            if stdout:
                str_stdoutLine = stdout.decode()
                if int(self.args['verbosity']):
                    print(str_stdoutLine, end = '')
                str_stdout      += str_stdoutLine
        d_ret['cmd']        = str_cmd
        d_ret['cwd']        = os.getcwd()
        d_ret['stdout']     = str_stdout
        d_ret['stderr']     = p.stderr.read().decode()
        d_ret['returncode'] = p.returncode
        if int(self.args['verbosity']) and len(d_ret['stderr']):
            print('\nstderr its here: \n%s' % d_ret['stderr'])
        return d_ret

    def job_stdwrite(self, d_job, str_outputDir, str_prefix = ""):
        """
        Capture the d_job entries to respective files.
        """
        if not self.args['noJobLogging']:
            for key in d_job.keys():
                with open(
                    '%s/%s%s' % (str_outputDir, str_prefix, key), "w"
                ) as f:
                    f.write(str(d_job[key]))
                    f.close()
        return {
            'status': True
        }

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """

        options.verbosity   = options.verbose
        self.args           = vars(options)
        self.__name__       = "pfdcm_tagextract"
        self.dp             = pfmisc.debug(
                                 verbosity   = int(self.args['verbosity']),
                                 within      = self.__name__
                             )

        print(Gstr_title)
        print('Version: %s' % self.get_version())

        inputfilepath = os.path.join(options.inputdir, options.inputFile)
       
        html_cmd = ''

        if 'html' in options.outputFileType:
            html_cmd = '--useIndexhtml'
        
        if '' == options.inputFile:
            str_cmd = 'pfdicom_tagExtract -I %s -e %s -O %s -o %s %s -t %s' % (options.inputdir, options.extension, options.outputdir, 
                                                                        options.outputFileStem, html_cmd, options.outputFileType)
        else:
            str_cmd = 'pfdicom_tagExtract -I %s -e %s -i %s -O %s -o %s %s -t %s' % (options.inputdir, options.extension, options.inputFile,
                                                                        options.outputdir, options.outputFileStem, html_cmd, options.outputFileType)

        print("Running %s..." % str_cmd)

        d_job = self.job_run(str_cmd)

        self.job_stdwrite(
                d_job, options.outputdir,
                'logs-%s-' % (options.inputFile)
            )


    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)
