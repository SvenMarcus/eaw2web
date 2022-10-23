from rich.progress import Progress, TaskID


class RichProgressReporter:
    def __init__(self, progress_bar: Progress, current_file: Progress) -> None:
        self.bar = progress_bar
        self.file = current_file
        self.task_id = TaskID(-1)

    def begin(self, filename: str) -> None:
        self.task_id = self.file.add_task(f"Processing {filename}")

    def finish(self) -> None:
        self.file.advance(self.task_id, 100)
        self.bar.advance(TaskID(0), 1)
