""" Basic modules """
import os 
import math
from datetime import datetime

""" Async io """
import asyncio

""" Import nodus """
import nodus

""" Rich and Textual for UI """
from rich.text import Text

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, Grid, ScrollableContainer
from textual.widgets import Header, Footer, Button, Static, DataTable, Label
from textual.screen import ModalScreen

""" Definitions """
__COLUMNS__ = [('ID','job_id',{'width':5}), 
               ('PID','pid',{'width':8}), 
               ('Nodus Session ID', 'nodus_session_id', {'width':40}),
               ('Parent Caller', 'parent_caller', {'width':50}), 
               ('Job Name', 'job_name', {'width':30}), 
               ('Status', 'status', {'width':15}), 
               ('Start Time', 'timestamp', {'width':20}), 
               ('End Time', 'completion_time', {'width':20}),
               ('Runtime', None, {'width':15}),
               ('Priority', 'priority', {'width':10}),
               ('Log','log_path', {'width':50}),
               ('Command', 'command', {'width':50}),
               ('Script Path', 'script_path', {'width':50})]


class WarningModal(ModalScreen):
    def __init__(self, message: str):
        super().__init__()
        self.message = message  # Custom message

    def compose(self) -> ComposeResult:
        # Center the content vertically and horizontally
        yield Vertical(
            Label(f"⚠️ {self.message}", id="warning-message"),
            Button("Close", id="close-button"),
            id="warning-container"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "close-button":
            self.app.pop_screen()  # Close the modal when "Close" is clicked

""" Job list widget """
class JobList(DataTable):
    def __init__(self, job_manager: nodus.manager.JobManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # set params 
        self.job_manager = job_manager
        self.selected_row_index = None  # Store the index of the selected row
        

        # First column is status (icon)
        self.add_column(" ", width=3)
        for column in __COLUMNS__:
            self.add_column(column[0], **column[2])
        
        # Enables row selection
        self.cursor_type = "row"  

        # Our job list will be a list of tuples that we can pass directly to the DataTable widget. 
        # This means we need to keep track of what each column represents in the tuple.
        self.jobs_column_map = self._init_column_map()

        # also, init a couple of vars that we will use to keep track of which rows have to be updated 
        self.job_id_list = []
        self.row_indices = {}
        self.jobs = []
        self.jobs_dict = {}
    
    async def on_mount(self):
        """Set up the UI and start the refresh process."""
        self.refresh_task = asyncio.create_task(self.refresh_table())

    def _init_column_map(self):
        cursor = self.job_manager.conn.cursor()

        # Execute a query to get the column names
        cursor.execute("PRAGMA table_info(jobs)")

        # Fetch the results
        columns = [row[1] for row in cursor.fetchall()]

        # The deal is that when we run "fetch_jobs" we get a list of tuples, where each tuple represents a job,
        # and the order of the values corresponds to __COLUMNS__. However, when we fetch the jobs from the database,
        # they are represented in a different order, following "columns". 
        # When we constantly fetch, we will have to check if the jobs have changed or not, in order to decide 
        # if we need to update them or not. But to do this, we need to be able to know which index in the tuple
        # corresponds to each parameter we want to check. 

        # So, we create a dictionary that maps the column names to the index in the tuple.
        column_map = {}
        for i, column in enumerate(columns):
            for j, col in enumerate(__COLUMNS__):
                if col[1] == column:
                    column_map[column] = j
                    break
        
        return column_map
        
    def cleanup_job(self, job):
        # First get vars 
        completion_time = job['End Time']
        completion_time = completion_time if completion_time else "N/A"
        pid = job['PID']
        parent_caller = job['Parent Caller']
        job_name = job['Job Name']
        timestamp = job['Start Time']
        log_path = job['Log']
        priority = job['Priority']
        command = job['Command']
        script_path = job['Script Path']

        # Now compute runtime
        runtime = "N/A"
        if completion_time != "N/A" and timestamp:
            runtime = nodus.utils.compute_runtime(timestamp, completion_time)

        # Now update the job
        job['Runtime'] = runtime

        # If completion_time is None, display "N/A"
        job['End Time'] = completion_time
        # If PID is None, display "N/A"
        job['PID'] = pid if pid else "N/A"
        # If parent_caller is None, display "N/A"
        parent_caller = parent_caller if parent_caller else "N/A"
        # If parent_caller is too long, truncate it
        job['Parent Caller'] = parent_caller[:47] + "..." if len(parent_caller) > 50 else parent_caller
        # If job_name is None, display "N/A"
        job_name = job_name if job_name else "N/A"
        # If job_name is too long, truncate it
        job['Job Name'] = job_name #[:17] + "..." if len(job_name) > 20 else job_name

        # If log_path is None, N/A
        original_log_path = f'{log_path}'
        log_path = log_path if log_path else "N/A"
        # If log_path is too long, truncate it
        if len(log_path) > 50:
            lp = log_path.split(os.sep)[-1]
            log_path = f'…{os.sep}{lp[:25]}…{lp[-24:]}' if len(lp) > 50 else f"…{os.sep}{lp}"
        job['Log'] = log_path

        # If command is None, display "N/A"
        command = command if command else "N/A"
        job['Command'] = command[:47] + "..." if len(command) > 50 else command

        # if priority is None, display "N/A"
        job['Priority'] = priority if priority else "N/A"

        # if script_path is None, display "N/A"
        script_path = script_path if script_path else "N/A"
        # if script_path is too long, truncate it
        job['Script Path'] = script_path[:47] + "..." if len(script_path) > 50 else script_path

        return job, original_log_path

    async def fetch_jobs(self):
        #connection = sqlite3.connect(self.db_path)
        cursor = self.job_manager.conn.cursor()
        fields = ', '.join([f[1] for f in __COLUMNS__ if f[1] is not None])
        cursor.execute(f"SELECT {fields} FROM jobs ORDER BY timestamp DESC")
        jobs = cursor.fetchall()

        # convert jobs to dict 
        jobs = [dict(zip([f[0] for f in __COLUMNS__ if f[1] is not None], job)) for job in jobs]

        # Now compute runtime
        jobs_out = []
        opaths = []
        jobs_dict = {}
        for job in jobs:
            # clean up 
            job, opath = self.cleanup_job(job)
            jobs_dict[job['ID']] = {**{kw: job[kw] for kw in job if kw != 'Log'}, 'Log': opath}
            # Transform back into tuple
            _j = ()
            for column in __COLUMNS__:
                _j += (job[column[0]],)
            jobs_out.append(_j)
            opaths.append(opath)
        # Add jobs_dict to self for future use 
        return jobs_out, opaths, jobs_dict

    def get_status_icon(self, status):
        """Return a colored light icon based on job status."""
        if status == "completed":
            return Text("●", style="#00ff00")  # Green light
        elif status == "running":
            return Text("●", style="#00ffff")  # Cyan light for active jobs
        elif status == "errored":
            return Text("●", style="#ff0000")  # Red light
        elif status in ("pending", "waiting"):
            # yellow color 
            return Text("●", style="#ffff00")  # Yellow light
        return Text("●", style="#1f1f1f")  # Default gray light

    async def on_row_selected(self, event):
        row_data = event.row_key
        # Handle selection (e.g., display details in another panel)
        print(f"Selected Job: {row_data}")
        self.selected_row_index = event.row_index

    async def refresh_table(self):
        """Efficiently update the table with changed jobs."""
        while True:
            # Fetch the latest jobs
            new_jobs, new_log_paths, new_jobs_dict = await self.fetch_jobs()

            # Easy check:
            if new_jobs == self.jobs:
                # No changes, skip the rest
                await asyncio.sleep(2)
                continue

            # Initialize the position of each row, by PID
            new_row_indices = {}
            # And the opposite of the above, by row index
            new_job_id_list = [] 

            # Init jobs_dict (by job_id)
            new_jobs_by_id = {}
            new_jobs_log_paths = {}

            # Since we might have to add new rows, keep track of the offset (new_row added)
            offset = 0
            njobs = len(self.jobs_dict)

            # Now populate the table with the new jobs
            for irow, (new_job, new_log_path, new_job_dict) in enumerate(zip(new_jobs, new_log_paths, new_jobs_dict)):
                # Get this job's pid 
                job_id = new_job[self.jobs_column_map['job_id']]
                # Get the status too 
                new_status = new_job[self.jobs_column_map['status']]

                # Let's try to find this job in the current jobs list
                row_index = self._find_row_index_by_id(job_id)
                if row_index is not None:
                    # Check if data has changed 
                    if self.jobs_dict[job_id] != new_job:
                        # If it has changed, update the row 
                        if row_index == irow:
                            # The row didn't change position, so just update its contents
                            self._update_row(row_index, new_job, new_status)
                        else:
                            # If the row is not in the right position, we have to move it
                            # Now, this is seems a bit tricky, but here's the deal: 
                            # at this point we are basically looping through every row incrementally,
                            # which means that if at this point we have to move a row, we can do so 
                            # by simply removing it, and adding it again. This works because this won't affect
                            # any rows that we already added, and by doing so we theoretically can be sure that 
                            # any rows in future iterations will also be moved. So at the end, this row that's now
                            # being eliminated and re-added at the end of the stck, will end up at the right position
                            # in the table.
                            row_key = list(self.rows.items())[row_index][0]
                            self.remove_row(row_key)
                            # Add it back (to the end)
                            icon = self.get_status_icon(new_status)
                            self.add_row(icon, *new_job)
                        
                else:
                    icon = self.get_status_icon(new_status)
                    self.add_row(icon, *new_job)
                    row_index = njobs + offset 
                    offset += 1

                # Add to row_indices
                new_row_indices[job_id] = irow
                # Add to pid_list
                new_job_id_list.append(job_id)
                # Add to jobs_dict
                new_jobs_by_id[job_id] = new_job
                new_jobs_log_paths[job_id] = new_log_path
            
            # Now we can set these variables in self, to be used later to check 
            # if we need to update jobs or not 
            self.job_id_list = new_job_id_list
            self.row_indices = new_row_indices

            # also store the job data 
            self.jobs_by_id = new_jobs_by_id
            self.jobs_log_paths = new_jobs_log_paths

            # Update jobs (for easy checking if they have changed in the future)
            self.jobs = new_jobs
            self.jobs_dict = new_jobs_dict

            # Now remove rows that are not in the new jobs list
            # for irow, job_id in enumerate(job_id_list):
            #     if job_id not in row_indices:
            #         self.remove_row(irow)


            # Preserve scroll position
            await asyncio.sleep(2)

    def _find_row_index_by_id(self, job_id):
        """Find the row index of a job by its ID."""
        if job_id in self.row_indices:
            return self.row_indices[job_id]
        return None

    def _update_row(self, row_index, updated_job, updated_status):
        """Update the content of an existing row without flickering."""
        icon = self.get_status_icon(updated_status)
        updated_data = (icon,) + updated_job
        for i, data in enumerate(updated_data):
            self.update_cell_at((row_index, i), data)

    def kill(self, row_index):
         # Get job_id
        job_id = self.job_id_list.pop(row_index)
        # Get job 
        job = self.jobs_dict[job_id]

        # Get pid 
        job_pid = job['PID']

        # Check if job is still running
        self.app.push_screen(WarningModal(f"Killing process with pid: {job_pid}"))
        process_killed = nodus.utils.kill_process(job_pid)
        # If process_killed is False, show an error message to user
        # Make sure to delete the previous confirmation popup 
        if not process_killed: 
            self.app.push_screen(WarningModal("Failed to kill the process!"))
        else:
            self.app.push_screen(WarningModal(f"Process with pid {job_pid} was killed"))
        
    def delete(self, row_index):
        
        # Get job_id
        job_id = self.job_id_list.pop(row_index)
        # Pop job at self.jobs (Same index)
        job = self.jobs.pop(row_index)
        # Remove from self.jobs_dict
        self.jobs_dict.pop(job_id)

        # We need to update the list of indices now 
        # First, remove entry for this job_id
        irow = self.row_indices.pop(job_id)
        # Now, for any job that has an index greater than irow, we need to decrement it by 1
        for jid in self.row_indices:
            if self.row_indices[jid] > irow:
                self.row_indices[jid] -= 1

        # Now remove row from table
        row = list(self.rows.items())[row_index][0]        
        self.remove_row(row)

        # And finally remove from database 
        cursor = self.job_manager.conn.cursor()
        cursor.execute(f"DELETE FROM jobs WHERE job_id = {job_id}")
        self.job_manager.conn.commit()

        
    def rerun(self, row_index):
        # Get job_id
        job_id = self.job_id_list.pop(row_index)
        # Get job 
        job = self.jobs_dict[job_id]

        # Check if job is still running
        if job['Status'] != 'completed' and job['Status'] != 'errored':
            # Display a warning popup warning the user that the job is still running and it cannot be rerun
            self.app.push_screen(WarningModal("Job is still running (or pending) and cannot be rerun. Please wait before trying to re-run again."))

        # Make sure we have a command or a script path
        if not job['Command'] and not job['Script Path']:
            # Display a warning popup warning the user that the job is still running and it cannot be rerun
            self.app.push_screen(WarningModal("Job does not have a command or script path so it cannot be run. Please check the job details."))

        # Now rerun the job 
        self.job_manager.rerun_job(job_id)
    

class JobDetails(Static):
    """A widget to display details of a selected job."""
    def update_details(self, job):
        """Update the displayed job details."""
        if job:
            self.update(
                f"Job ID: {job['ID']}\n"
                f"Name: {job['Job Name']}\n"
                f"PID: {job['PID']}\n"
                f"Priority: {job['Priority']}\n"
                f"Status: {job['Status']}\n"
                f"Start Time: {job['Start Time']}\n"
                f"End Time: {job['End Time']}\n"
                f"Runtime: {job['Runtime']}\n"
                f"Parent Caller: {job['Parent Caller']}\n"
                f"Nodus Session ID: {job['Nodus Session ID']}\n"
                f"Log: {job['Log']}\n"
                f"Command: {job['Command']}\n"
                f"Script Path: {job['Script Path']}\n"
            )

        else:
            self.update("No job selected.")

class JobLog(Static):
    _log = None
    
    """A widget to display the log of a selected job."""
    def compose(self) -> ComposeResult:
        with Vertical() as vertical:
            vertical.styles.padding = 1

            # Log title
            self.log_title = Static("No log selected.")
            self.log_title.styles.background = "purple"
            self.log_title.styles.margin = 0
            yield self.log_title

            # Scrollable container for the log content
            with ScrollableContainer() as scroll_view:
                scroll_view.border_title = "Log Content"
                scroll_view.styles.border = ('solid', 'black')
                scroll_view.styles.border_title_align = 'left'
                scroll_view.styles.background = "#F0F0D7"
                scroll_view.styles.color = "black"
                self.log_scroll_view = scroll_view

                # The log content widget (inside the scrollable area)
                self.log_content = Static("")
                self.log_content.styles.padding = 0
                yield self.log_content

    async def on_mount(self):
        """Set up the UI and start the refresh process."""
        self.refresh_task = asyncio.create_task(self.refresh_log())

    async def refresh_log(self):
        """Update the table with the latest jobs."""
        while True:
            if self._log is not None:
                # Update the displayed log
                self.update_details(self._log)
            await asyncio.sleep(2)

    def update_details(self, log):
        """Update the displayed job log."""
        log_content = ""
        if log:
            if not os.path.exists(log):
                self.log_title.update(f"Log not found: {log}")
                self._log = None
                return
            self.log_title.update(f"Log: {log}")
            # Read content of log 
            with open(log, 'r') as f:
                log_content = f.read()
            self._log = log
            log_content = self.add_line_numbers(log_content)
            # self.log_line_numbers.update(lines)
            self.log_content.update(log_content)
        else:
            self.log_title.update("No log selected.")
        self.log_scroll_view.visible = (log_content != "")
        # Move scroll_view to bottom 
        self.smart_scroll_to_bottom()

    def smart_scroll_to_bottom(self):
        # Get the current vertical scroll position and maximum scrollable height
        current_y = self.log_scroll_view.scroll_y
        max_y = self.log_scroll_view.virtual_size.height - self.log_scroll_view.size.height

        # Allow a small margin to account for floating-point inaccuracies
        if current_y >= max_y - 5:
            # User is at the bottom, auto-scroll
            self.log_scroll_view.scroll_to(y=self.log_scroll_view.virtual_size.height, animate=False)
        else:
            # User has scrolled up, don't auto-scroll
            pass

    def add_line_numbers(self, text: str) -> str:
        """Prepend line numbers to each line in the log content."""
        lines = text.split("\n")

        nsp = math.log(len(lines)) + 1

        # find closest odd number 
        nsp = int(math.ceil(nsp) // 2 * 2 + 1) + 1

        numbered_lines = ["[black on #AAB99A]{}[/][black on #F0F0D7]{}[/]".format(str(i).center(nsp), line) for i, line in enumerate(lines)]
        return "\n".join(numbered_lines)

class NodusApp(App):
    TITLE = "Nodus Dashboard"
    BINDINGS = [
        ("q", "quit", "Quit"), #("r", "refresh", "Refresh"), #("d", "toggle_dark", "Toggle Dark Mode"),
        ("k", "kill", "Kill selected job entry"),
        ("escape", "unfocus_selected", "Unfocus selected job entry"),
        ("d", "delete_job_entry", "Delete selected job entry from db"),
        ("r", "rerun_job", "Rerun selected job entry")
    ]
    CSS = """
    Vertical {
        padding: 0 ;
    }
    Container {
        padding: 0;  /* Dotted border for the main containers */
        width: 100%;
    }
    #job_list_group {
        height: 55%;
    }
    #job_bottom_group {
        height: 45%;
    }
    #job_details_group {
        height: 100%;
        width: 35%;
    }
    #job_log_group {
        height: 100%;
        width: 65%;
    }
    #warning-container {
        width: 50%;
        height: auto;
        background: darkred;
        border: solid red;
        padding: 2;
        align: center middle;          /* Fully center the container */
        content-align: center middle;  /* Center content inside the container */
    }

    #warning-message {
        color: white;
        text-align: center;
        padding-bottom: 1;
    }

    #close-button {
        align: center middle;  /* Center the button */
    }
    """

    def __init__(self, db_path: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dark = False
        self.db_path = db_path
        # Setup the db 
        # Create Nodus Session
        self.session = nodus.NodusSession()
        self.db = self.session.add_nodus_db(db_path = self.db_path)
        # Get jm 
        self.jm = self.db.job_manager


    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        # Create the main layout with two groups: JobList and JobDetails
        with Vertical() as vertical:
            vertical.styles.padding = 0
            with Container(id="job_list_group") as c1:
                # Set container style
                c1.border_title=f"Job List from database @ {self.db_path}"
                c1.styles.border = ('round', 'white')
                c1.styles.border_title_align = 'left'
                c1.styles.padding = 1

                self.job_list = JobList(self.jm)
                yield self.job_list

            with Horizontal(id = "job_bottom_group") as h:
                h.styles.padding = 0

                with Container(id="job_details_group") as c2:
                    # Set container style
                    c2.border_title="Job Details"
                    c2.styles.border = ('round', 'white')
                    c2.styles.border_title_align = 'left'
                    c2.styles.padding = 1

                    self.job_details = JobDetails("No job selected.")
                    yield self.job_details
                
                with Container(id="job_log_group") as c3:
                    # Set container style
                    c3.border_title="Job Log"
                    c3.styles.border = ('round', 'white')
                    c3.styles.border_title_align = 'left'
                    c3.styles.padding = 0

                    self.job_log = JobLog()
                    yield self.job_log

    """ Easily update job details on panels """
    def show_selected_job_at_row(self, row_index):
        # Make sure we are within boundaries
        if row_index >= 0 and row_index < len(self.job_list.job_id_list):
            selected_job_id = self.job_list.job_id_list[row_index]
            # Get the job
            selected_job = self.job_list.jobs_dict[selected_job_id] if selected_job_id in self.job_list.jobs_dict else None
            if selected_job is not None:
                self.job_details.update_details(selected_job)
                # Update log view
                self.job_log.update_details(selected_job['Log'] if selected_job else None)  

    async def on_data_table_row_selected(self, event: DataTable.RowSelected):
        """Handle row selection and update job details."""
        row_index = event.cursor_row
        self.show_selected_job_at_row(row_index)

    def on_key(self, event):
        """Handle keyboard arrow keys for navigation."""
        if event.key in ("up", "down"):
            current_row = self.job_list.cursor_row or 0

            # Move the cursor
            new_row = current_row
            if event.key == "up" and current_row > 0:
                # self.job_list.move_cursor(row=current_row-1)
                new_row = current_row - 1
            elif event.key == "down" and current_row < len(self.job_list.jobs_dict) - 1:
                # self.job_list.move_cursor(row=current_row+1)
                new_row = current_row + 1

            self.show_selected_job_at_row(new_row)
            
    async def on_mount(self):
        """Set up the UI and start the refresh process."""
        self.refresh_task = asyncio.create_task(self.refresh_title())

    async def refresh_title(self):
        """Update the window title with the last update time."""
        while True:
            last_update_time = datetime.now()
            current_time = last_update_time.strftime('%H:%M:%S')
            self.title = f"Nodus Job Manager (Standalone Mode) - {current_time} (Updating every 2s)"
            await asyncio.sleep(2)

    def action_quit(self) -> None:
        self.exit()

    # def action_toggle_dark(self) -> None:
    #     self.dark = not self.dark

    def action_kill(self):
        current_row = self.job_list.cursor_row
        if current_row is not None:
            self.job_list.kill(current_row)

    def action_delete_job_entry(self):
        """Custom action to delete the selected job."""
        current_row = self.job_list.cursor_row

        if current_row >= 0 and current_row < len(self.job_list.job_id_list):
            # Delete 
            self.job_list.delete(current_row)
            # Make sure we set the cursor to the next row (below)
            if current_row < len(self.job_list.job_id_list):
                self.job_list.move_cursor(row=current_row)
                # Update details 
                self.show_selected_job_at_row(current_row)
            else:
                self.job_list.move_cursor(row=None)
                self.job_details.update_details(None)
                self.job_log.update_details(None)
            

    def action_rerun_job(self):
        """Custom action to delete the selected job."""
        current_row = self.job_list.cursor_row
        if current_row is not None:
            self.job_list.rerun(current_row)

    def action_unfocus_selected(self):
        # TODO: THIS DOESN'T WORK
        self.job_list.move_cursor(row=None)
        self.job_list.selected_row_index = -1        
        self.job_details.update_details(None)
        self.job_log.update_details(None)

def run_ui(db_path: str = None):
    if db_path is not None:
        if not os.path.isfile(db_path): 
            # Roll back 
            db_path = nodus.__nodus_db_path__
    else:
        db_path = nodus.__nodus_db_path__

    app = NodusApp(db_path)
    app.run()