import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import shutil
import subprocess
import sys

try:
    import yt_dlp
except Exception:
    try:
        subprocess.run(["pip", "install", "yt-dlp"])
        import yt_dlp
    except Exception:
        subprocess.run(["py", "-m", "pip", "install", "yt-dlp"])
        import yt_dlp


def check_ffmpeg(root):
    if shutil.which("ffmpeg") is None:
        answer = messagebox.askyesno(
            "ffmpeg not found",
            "ffmpeg is required for MP3 conversion and video merging but was not found.\n\nInstall it now via winget? (requires Windows Package Manager)"
        )
        if answer:
            subprocess.run(["winget", "install", "--id", "Gyan.FFmpeg", "-e"], shell=True)
            messagebox.showinfo("ffmpeg", "Installation complete. Please relaunch the app.")
            root.destroy()
            sys.exit(0)
        else:
            messagebox.showwarning("ffmpeg", "MP3 conversion and video merging may not work without ffmpeg.")


def is_playlist(url):
    with yt_dlp.YoutubeDL({"quiet": True, "ignoreerrors": True}) as ydl:
        info = ydl.extract_info(url, download=False)
        return info and info.get("_type") == "playlist" and len(info.get("entries", [])) > 1


def build_ydl_opts(folder, alias, fmt, progress_hook):
    name = alias.strip() if alias.strip() else "%(title)s"
    if fmt == "mp3":
        return {
            "format": "bestaudio/best",
            "outtmpl": f"{folder}/{name}.%(ext)s",
            "ignoreerrors": True,
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
            "progress_hooks": [progress_hook],
        }
    return {
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "outtmpl": f"{folder}/{name}.%(ext)s",
        "merge_output_format": "mp4",
        "ignoreerrors": True,
        "progress_hooks": [progress_hook],
    }


def _on_progress(d, log, set_progress):
    if d["status"] == "downloading":
        pct = d.get("_percent_str", "0%").strip().replace("%", "")
        try:
            set_progress(float(pct))
        except ValueError:
            pass
        log(d["filename"].split("/")[-1] + " - downloading")
    elif d["status"] == "finished":
        set_progress(100)
        log(d["filename"].split("/")[-1] + " - finished")


def start_download(url_var, folder_var, alias_var, fmt_var, status_var, progress_var, playlist_var, progress_bar, btn):
    url = url_var.get().strip()
    folder = folder_var.get().strip()
    if not url or not folder:
        messagebox.showwarning("Missing info", "Please provide both a URL and a save folder.")
        return

    btn.config(state="disabled")
    progress_var.set(0)
    playlist_var.set("")
    status_var.set("Fetching info...")

    def run():
        try:
            playlist = is_playlist(url)
            if playlist:
                progress_bar.grid_remove()
                with yt_dlp.YoutubeDL({"quiet": True, "ignoreerrors": True}) as ydl:
                    info = ydl.extract_info(url, download=False)
                entries = [e for e in info.get("entries", []) if e]
                total = len(entries)
                downloaded = [0]

                def on_finish(d):
                    if d["status"] == "finished":
                        downloaded[0] += 1
                        playlist_var.set(f"{downloaded[0]} / {total} videos downloaded")

                opts = build_ydl_opts(folder, alias_var.get(), fmt_var.get(), on_finish)
                status_var.set("Downloading playlist...")
                with yt_dlp.YoutubeDL(opts) as ydl:
                    ydl.download([url])
            else:
                progress_bar.grid()
                opts = build_ydl_opts(folder, alias_var.get(), fmt_var.get(),
                                      lambda d: _on_progress(d, status_var.set, progress_var.set))
                with yt_dlp.YoutubeDL(opts) as ydl:
                    ydl.download([url])
            status_var.set("Done!")
        except Exception as e:
            status_var.set("Error")
            messagebox.showerror("Download failed", str(e))
        finally:
            btn.config(state="normal")

    threading.Thread(target=run, daemon=True).start()


def browse_folder(folder_var):
    path = filedialog.askdirectory()
    if path:
        folder_var.set(path)


def build_ui():
    root = tk.Tk()
    check_ffmpeg(root)
    root.title("Youtube Media Fetcher")
    root.resizable(False, False)

    url_var = tk.StringVar()
    folder_var = tk.StringVar()
    alias_var = tk.StringVar()
    fmt_var = tk.StringVar(value="mp4")
    status_var = tk.StringVar(value="Idle")
    progress_var = tk.DoubleVar(value=0)
    playlist_var = tk.StringVar(value="")

    pad = {"padx": 10, "pady": 5}

    tk.Label(root, text="Video / Playlist URL:").grid(row=0, column=0, sticky="w", **pad)
    tk.Entry(root, textvariable=url_var, width=50).grid(row=0, column=1, columnspan=2, **pad)

    tk.Label(root, text="Save folder:").grid(row=1, column=0, sticky="w", **pad)
    tk.Entry(root, textvariable=folder_var, width=40).grid(row=1, column=1, **pad)
    tk.Button(root, text="Browse", command=lambda: browse_folder(folder_var)).grid(row=1, column=2, **pad)

    tk.Label(root, text="Alias (optional):").grid(row=2, column=0, sticky="w", **pad)
    tk.Entry(root, textvariable=alias_var, width=50).grid(row=2, column=1, columnspan=2, **pad)

    tk.Label(root, text="Output format:").grid(row=3, column=0, sticky="w", **pad)
    ttk.Combobox(root, textvariable=fmt_var, values=["mp4", "mp3"], state="readonly", width=10).grid(row=3, column=1, sticky="w", **pad)

    btn = tk.Button(root, text="Download", width=20)
    btn.config(command=lambda: start_download(url_var, folder_var, alias_var, fmt_var, status_var, progress_var, playlist_var, progress_bar, btn))
    btn.grid(row=4, column=0, columnspan=3, pady=10)

    tk.Label(root, textvariable=status_var, fg="blue").grid(row=5, column=0, columnspan=3, **pad)
    tk.Label(root, textvariable=playlist_var, fg="green").grid(row=6, column=0, columnspan=3)
    progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100, length=400)
    progress_bar.grid(row=7, column=0, columnspan=3, padx=10, pady=(0, 10))

    root.mainloop()


if __name__ == "__main__":
    build_ui()
