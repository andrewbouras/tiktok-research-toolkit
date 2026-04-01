from __future__ import annotations

import threading
import webbrowser
from pathlib import Path
from tkinter import StringVar, Tk, filedialog, messagebox, simpledialog
from tkinter import ttk

from .config import load_runtime
from .dashboard.app import create_app
from .legacy import import_legacy_workspace
from .workspace import init_demo_workspace, init_study_workspace


class DesktopLauncher:
    def __init__(self) -> None:
        self.root = Tk()
        self.root.title("TikTok Research Toolkit")
        self.workspace_var = StringVar(value="")
        self._build()

    def _build(self) -> None:
        frame = ttk.Frame(self.root, padding=18)
        frame.grid(sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        ttk.Label(frame, text="TikTok Research Toolkit", font=("", 16, "bold")).grid(row=0, column=0, sticky="w")
        ttk.Label(
            frame,
            text="Choose a workspace folder, then start with a demo, a blank study, or a legacy import.",
            wraplength=520,
        ).grid(row=1, column=0, sticky="w", pady=(6, 14))

        workspace_row = ttk.Frame(frame)
        workspace_row.grid(row=2, column=0, sticky="ew")
        workspace_row.columnconfigure(0, weight=1)
        ttk.Entry(workspace_row, textvariable=self.workspace_var).grid(row=0, column=0, sticky="ew")
        ttk.Button(workspace_row, text="Choose Workspace", command=self.choose_workspace).grid(row=0, column=1, padx=(8, 0))

        actions = ttk.Frame(frame)
        actions.grid(row=3, column=0, sticky="ew", pady=(14, 0))
        for index, (label, command) in enumerate(
            [
                ("Try Demo Study", self.init_demo),
                ("Create New Study", self.init_study),
                ("Import Existing Study", self.import_legacy),
                ("Open Dashboard", self.open_dashboard),
            ]
        ):
            ttk.Button(actions, text=label, command=command).grid(row=0, column=index, padx=(0 if index == 0 else 8, 0))

    def choose_workspace(self) -> None:
        selected = filedialog.askdirectory(title="Choose a workspace folder")
        if selected:
            self.workspace_var.set(selected)

    def require_workspace(self) -> Path:
        workspace = self.workspace_var.get().strip()
        if not workspace:
            raise RuntimeError("Choose a workspace directory first.")
        return Path(workspace)

    def init_demo(self) -> None:
        try:
            runtime = init_demo_workspace(self.require_workspace())
        except Exception as exc:
            messagebox.showerror("Demo workspace failed", str(exc))
            return
        messagebox.showinfo("Demo workspace ready", f"Created demo workspace at:\n{runtime.paths.root}")

    def init_study(self) -> None:
        study_name = simpledialog.askstring("Study name", "Study name:", initialvalue="TikTok Research Study")
        if not study_name:
            return
        try:
            runtime = init_study_workspace(self.require_workspace(), study_name)
        except Exception as exc:
            messagebox.showerror("Study workspace failed", str(exc))
            return
        messagebox.showinfo("Study workspace ready", f"Created study workspace at:\n{runtime.paths.root}")

    def import_legacy(self) -> None:
        try:
            workspace = self.require_workspace()
        except Exception as exc:
            messagebox.showerror("Workspace required", str(exc))
            return
        workbook = filedialog.askopenfilename(title="Choose workbook", filetypes=[("Excel workbook", "*.xlsx")])
        if not workbook:
            return
        metadata_json = filedialog.askopenfilename(title="Choose metadata JSON", filetypes=[("JSON", "*.json")])
        transcripts_dir = filedialog.askdirectory(title="Choose transcripts directory")
        replacement_json = filedialog.askopenfilename(title="Choose replacement candidates JSON", filetypes=[("JSON", "*.json")])
        database = filedialog.askopenfilename(title="Choose existing SQLite database", filetypes=[("SQLite database", "*.sqlite3")])
        llm_scores_dir = filedialog.askdirectory(title="Choose LLM scores directory")
        try:
            runtime = import_legacy_workspace(
                workspace,
                workbook_path=Path(workbook),
                metadata_json_path=Path(metadata_json) if metadata_json else None,
                transcripts_dir=Path(transcripts_dir) if transcripts_dir else None,
                replacement_candidates_path=Path(replacement_json) if replacement_json else None,
                database_path=Path(database) if database else None,
                llm_scores_dir=Path(llm_scores_dir) if llm_scores_dir else None,
            )
        except Exception as exc:
            messagebox.showerror("Legacy import failed", str(exc))
            return
        messagebox.showinfo("Legacy import complete", f"Imported legacy study into:\n{runtime.paths.root}")

    def open_dashboard(self) -> None:
        try:
            runtime = load_runtime(self.require_workspace())
        except Exception as exc:
            messagebox.showerror("Dashboard failed", str(exc))
            return
        port = int(runtime.raw_config["study"].get("port", 5173))
        app = create_app(runtime)

        def run_server() -> None:
            app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)

        thread = threading.Thread(target=run_server, daemon=True)
        thread.start()
        url = f"http://127.0.0.1:{port}"
        webbrowser.open(url)
        messagebox.showinfo("Dashboard running", f"Dashboard started at:\n{url}")

    def run(self) -> None:
        self.root.mainloop()


def main() -> int:
    DesktopLauncher().run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
