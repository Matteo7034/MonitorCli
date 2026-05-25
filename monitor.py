import psutil
import time
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Static
from utils import format_bytes

class MonitorWidget(Static):
    def on_mount(self):
        self.set_interval(1,self.update_stats)

    def update_stats(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        #battery = psutil.battery()
        uptime_seconds = time.time() - psutil.boot_time()
        uptime_hours = uptime_seconds // 3600

        text = (
            f"[b][green]CPU:[/b][/green] {cpu}%\n"
            f"[b][yellow]RAM:[/b][/yellow] {ram.percent}% ({format_bytes(ram.used)} / {format_bytes(ram.total)}\n"
            f"[b][pink]DISK:[/b][/pink] {disk.percent}% ({format_bytes(disk.used)} / {format_bytes(disk.total)}\n"
            f"[b][red]UPTIME:[/b][/red] {int(uptime_hours)} hours\n"
        )
        self.update(text)


class ProcessWidget(Static):
    def on_mount(self):
        self.set_interval(1,self.update_process)
    def update_process(self):
        process = sorted(
            psutil.process_iter(['pid','name','cpu_percent']),
            key=lambda p: p.info['cpu_percent'],
            reverse=True 
        )[:6]

        text = "[b][orange]Top 6 CPU Processes[/b][/orange]\n\n"
        for p in process:
            text += f"{p.info['pid']} - {p.info['name']} - {p.info['cpu_percent']}%\n"
    
        self.update(text)

class SystemMonitor(App):
    CSS = """
    Screen{
        layout: vertical;
    }
    #root{
        height: 1fr;
        width: 100%;
    }
    .panel {
        width: 1fr;
        height: 1fr;
        padding: 2;
        border: round green;
    }
    Static {
        border: round green;
        padding: 1;
    }
    """
    def compose(self) -> ComposeResult:
        with Vertical(id="root"):
            with Horizontal():
                with Vertical(classes="panel"):
                       yield MonitorWidget()
                with Vertical(classes="panel"):
                       yield ProcessWidget()
if __name__ == "__main__":
    SystemMonitor().run()

