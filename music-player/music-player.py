import os
import random
import pygame
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, Scrollbar, ttk, BooleanVar, Checkbutton
from mutagen.mp3 import MP3
from mutagen.wave import WAVE


class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter Music Player")
        self.root.geometry("680x550")
        self.root.resizable(False, False)

        pygame.mixer.init()

        self.music_files = []
        self.current_index = None
        self.is_paused = False
        self.repeat_enabled = BooleanVar(value=False)
        self.shuffle_enabled = BooleanVar(value=False)
        self.track_length = 0
        self.user_seeking = False

        self._setup_widgets()
        self._setup_timers()

    def _setup_widgets(self):
        tk.Label(self.root, text="Playlist", font=(
            "Helvetica", 14)).pack(pady=10)

        frame = tk.Frame(self.root)
        frame.pack()

        self.listbox = Listbox(frame, width=60, height=15)
        self.listbox.pack(side="left", fill="y")

        scrollbar = Scrollbar(frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        self.listbox.bind("<Double-Button-1>", lambda e: self.play_music())

        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        tk.Button(control_frame, text="Load Files",
                  command=self.load_music_files, width=12).grid(row=0, column=0, padx=5)
        tk.Button(control_frame, text="Play", command=self.play_music,
                  width=12).grid(row=0, column=1, padx=5)
        tk.Button(control_frame, text="Pause", command=self.pause_music,
                  width=12).grid(row=0, column=2, padx=5)
        tk.Button(control_frame, text="Unpause", command=self.unpause_music,
                  width=12).grid(row=0, column=3, padx=5)
        tk.Button(control_frame, text="Stop", command=self.stop_music,
                  width=12).grid(row=0, column=4, padx=5)

        nav_frame = tk.Frame(self.root)
        nav_frame.pack(pady=5)
        tk.Button(nav_frame, text="⏮ Previous", command=self.play_previous,
                  width=12).grid(row=0, column=0, padx=5)
        tk.Button(nav_frame, text="⏭ Next", command=self.play_next,
                  width=12).grid(row=0, column=1, padx=5)

        option_frame = tk.Frame(self.root)
        option_frame.pack(pady=5)

        Checkbutton(option_frame, text="Shuffle",
                    variable=self.shuffle_enabled).pack(side="left", padx=10)
        Checkbutton(option_frame, text="Repeat",
                    variable=self.repeat_enabled).pack(side="left", padx=10)

        playlist_frame = tk.Frame(self.root)
        playlist_frame.pack(pady=10)
        tk.Button(playlist_frame, text="💾 Save Playlist",
                  command=self.save_playlist, width=16).grid(row=0, column=0, padx=5)
        tk.Button(playlist_frame, text="📂 Load Playlist",
                  command=self.load_playlist, width=16).grid(row=0, column=1, padx=5)

        volume_frame = tk.Frame(self.root)
        volume_frame.pack(pady=10)
        tk.Label(volume_frame, text="Volume:").pack(side="left")
        self.volume_slider = ttk.Scale(
            volume_frame, from_=0, to=100, orient="horizontal", length=200, command=self.set_volume)
        self.volume_slider.set(70)
        self.volume_slider.pack(side="left", padx=10)
        self.set_volume(70)

        # Progress bar and time labels
        self.progress_frame = tk.Frame(self.root)
        self.progress_frame.pack(pady=10)

        self.time_label = tk.Label(self.progress_frame, text="00:00")
        self.time_label.pack(side="left", padx=5)

        self.progress_bar = ttk.Scale(
            self.progress_frame, from_=0, to=100, orient="horizontal", length=400)
        self.progress_bar.pack(side="left")
        self.progress_bar.bind("<ButtonPress-1>", self.start_seek)
        self.progress_bar.bind("<ButtonRelease-1>", self.end_seek)

        self.total_label = tk.Label(self.progress_frame, text="00:00")
        self.total_label.pack(side="left", padx=5)

    def _setup_timers(self):
        self.root.after(1000, self.update_progress)
        self.root.after(1000, self._check_music_end)

    def load_music_files(self):
        files = filedialog.askopenfilenames(title="Select Music Files",
                                            filetypes=[("Audio Files", "*.mp3 *.wav")])
        for file in files:
            if file not in self.music_files:
                self.music_files.append(file)
                self.listbox.insert(tk.END, os.path.basename(file))

    def save_playlist(self):
        if not self.music_files:
            messagebox.showinfo("Nothing to Save", "No playlist to save.")
            return
        file = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file:
            with open(file, 'w') as f:
                for path in self.music_files:
                    f.write(f"{path}\n")
            messagebox.showinfo(
                "Playlist Saved", "Playlist saved successfully.")

    def load_playlist(self):
        file = filedialog.askopenfilename(
            title="Open Playlist", filetypes=[("Text Files", "*.txt")])
        if file:
            try:
                with open(file, 'r') as f:
                    paths = [line.strip()
                             for line in f if os.path.isfile(line.strip())]
                self.music_files.clear()
                self.listbox.delete(0, tk.END)
                for path in paths:
                    self.music_files.append(path)
                    self.listbox.insert(tk.END, os.path.basename(path))
                self.current_index = None
                self.stop_music()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load playlist:\n{e}")

    def play_music(self):
        try:
            selected = self.listbox.curselection()
            if not selected and self.current_index is None:
                messagebox.showwarning(
                    "No Selection", "Select a song or use Next/Shuffle.")
                return
            if selected:
                self.current_index = selected[0]

            filepath = self.music_files[self.current_index]
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.play()
            self.is_paused = False
            self.track_length = self.get_track_length(filepath)

            self.progress_bar.config(to=self.track_length)
            self.total_label.config(text=self.format_time(self.track_length))

            self.listbox.select_clear(0, tk.END)
            self.listbox.select_set(self.current_index)
        except Exception as e:
            messagebox.showerror("Playback Error", str(e))

    def get_track_length(self, filepath):
        try:
            if filepath.lower().endswith(".mp3"):
                return int(MP3(filepath).info.length)
            elif filepath.lower().endswith(".wav"):
                return int(WAVE(filepath).info.length)
        except:
            return 0

    def update_progress(self):
        if pygame.mixer.music.get_busy() and not self.user_seeking:
            current_pos = pygame.mixer.music.get_pos() // 1000
            self.progress_bar.set(current_pos)
            self.time_label.config(text=self.format_time(current_pos))
        self.root.after(1000, self.update_progress)

    def start_seek(self, event):
        self.user_seeking = True

    def end_seek(self, event):
        new_time = int(self.progress_bar.get())
        pygame.mixer.music.play(start=new_time)
        self.user_seeking = False

    def format_time(self, seconds):
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins:02}:{secs:02}"

    def pause_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.is_paused = True

    def unpause_music(self):
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False

    def stop_music(self):
        pygame.mixer.music.stop()
        self.is_paused = False
        self.progress_bar.set(0)
        self.time_label.config(text="00:00")

    def set_volume(self, val):
        try:
            pygame.mixer.music.set_volume(float(val) / 100)
        except:
            pass

    def play_next(self):
        if self.shuffle_enabled.get():
            self.play_random()
        elif self.music_files:
            self.current_index = (
                self.current_index + 1) % len(self.music_files) if self.current_index is not None else 0
            self.play_music()

    def play_previous(self):
        if self.music_files:
            self.current_index = (
                self.current_index - 1) % len(self.music_files) if self.current_index is not None else 0
            self.play_music()

    def play_random(self):
        if self.music_files:
            self.current_index = random.randint(0, len(self.music_files) - 1)
            self.play_music()

    def _check_music_end(self):
        if not pygame.mixer.music.get_busy() and self.current_index is not None and not self.is_paused:
            if self.repeat_enabled.get():
                self.play_music()
            elif self.shuffle_enabled.get():
                self.play_random()
            else:
                self.play_next()
        self.root.after(1000, self._check_music_end)


if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()
