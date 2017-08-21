The solution is a single file called loan_summary.py that can be invoked from the command line or a cron.

>>python loan_summary.py

The same directory that contains the file also contains a folder called data_files.  When it runs it will take any files in there, process it into a summary file and create an output file in the completed_files directory.  It will also move the original data file into the same directory.

I chose the Python programming language because for me it is the simplest as well as easiest to use language.

Scaling considerations:  Since the program builds the output in RAM before writing it to a file very very large files might become problematic.  However the file would need to be very big indeed before this becomes a problem.

In a production environment I would probably set this up as a file called by a cron.  Hence the directory setup and not relying on a file.  That way a second cron can just scp the file into the proper directory.