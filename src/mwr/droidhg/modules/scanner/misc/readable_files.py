from mwr.droidhg.modules import common, Module

class ReadableFiles(Module, common.BusyBox, common.ClassLoader, common.FileSystem, common.Shell):

    name = "Find files in a folder, which are world-readable."
    description = "Find files in a folder, which are world-readable."
    examples = ""
    author = "MWR InfoSecurity (@mwrlabs)"
    date = "2012-12-17"
    license = "MWR Code License"
    path = ["scanner", "misc"]
    
    def add_arguments(self, parser):
        parser.add_argument("target", default="/dev", help="the target directory to search", nargs="?")

    def execute(self, arguments):
        if self.isBusyBoxInstalled():
            files = self.busyBoxExec("find %s \( -type b -o -type c -o -type f -o -type s \) -perm -o=r \-exec ls {} \;" % arguments.target)
            writable_files = []

            for f in iter(files.split("\n")):
                if not f.startswith('find: '):
                    writable_files.append(f)

            if len(writable_files) > 0:
                self.stdout.write("Found world-readable files:\n")
                for f in writable_files:
                    self.stdout.write("  %s\n" % f)
            else:
                self.stdout.write("No world-readable files found.")
        else:
            self.stderr.write("This command requires BusyBox to complete. Run tools.setup.busybox and then retry.\n")
            