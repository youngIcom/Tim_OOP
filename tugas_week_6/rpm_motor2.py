import serial
import tkinter as tk
from tkinter import messagebox
import time

SERIAL_PORT = '/dev/ttyUSB0'  # Ganti dengan port kamu
BAUD_RATE = 9600

class MonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kontrol Motor & Servo")
        self.root.geometry("700x500")
        self.root.configure(bg="white")

        try:
            self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
            time.sleep(2)  # Tunggu koneksi stabil
        except Exception as e:
            messagebox.showerror("Serial Error", f"Gagal membuka port serial:\n{e}")
            self.ser = None

        self.setup_ui()

    def setup_ui(self):
        header = tk.Label(self.root, text="SISTEM MONITOR & TRACKER", font=("Arial", 14, "bold"), bg="white")
        header.pack()

        main_frame = tk.Frame(self.root, bg="#f0f0f0", padx=10)
        main_frame.pack(fill="both", expand=True)

        # Frame Kiri: Motor
        left_frame = tk.Frame(main_frame, bg="#f0f0f0")
        left_frame.pack(side="top", padx=0, fill="y")

        self.entry_pwm, self.status_pwm = self._create_input(left_frame, "Motor DC (PWM 0-255)", self.kirim_pwm)

        # Frame Kanan: Motor
        right_frame = tk.Frame(main_frame, bg="#f0f0f0")
        right_frame.pack(side="top", padx=10, pady=10, fill="y")

        self.entry_rpm, self.status_rpm = self._create_input(right_frame, "RPM Motor DC (0-255)", self.kirim_pwm)

        # Frame Kanan: Servo
        bottom_frame = tk.Frame(main_frame, bg="#f0f0f0")
        bottom_frame.pack(side="top", padx=10, pady=10)

        self.entry_servo, self.status_servo = self._create_input(bottom_frame, "Motor Servo (Angle 0-180)", self.kirim_servo)

    def _create_input(self, parent, label_text, send_command):
        frame = tk.Frame(parent, bg="#f0f0f0")
        frame.pack(pady=10, fill="x")

        label = tk.Label(frame, text=label_text, bg="#f0f0f0")
        label.pack(side="top", anchor="w")

        entry = tk.Entry(frame)
        entry.pack(side="left", padx=(0, 10), fill="x", expand=True)

        status_label = tk.Label(frame, text="Menunggu input...", bg="#f0f0f0")
        status_label.pack(side="bottom", padx=(5, 0))

        button = tk.Button(frame, text="Kirim", command=lambda: send_command(entry, status_label))
        button.pack(side="right", padx=10)

        return entry, status_label

    def kirim_pwm(self, entry, status_label):
        if not self.ser or not self.ser.is_open:
            messagebox.showerror("Serial Error", "Port serial belum terbuka!")
            return
        try:
            pwm = int(entry.get())
            if not (0 <= pwm <= 255):
                raise ValueError("Nilai PWM harus 0-255")
            command = f"M{pwm}\n"
            self.ser.write(command.encode())
            self.ser.flush()
            status_label.config(text=f"PWM Motor: {pwm}")
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def kirim_servo(self, entry, status_label):
        if not self.ser or not self.ser.is_open:
            messagebox.showerror("Serial Error", "Port serial belum terbuka!")
            return
        try:
            angle = int(entry.get())
            if not (0 <= angle <= 180):
                raise ValueError("Sudut servo harus 0-180")
            command = f"S{angle}\n"
            self.ser.write(command.encode())
            self.ser.flush()
            status_label.config(text=f"Sudut Servo: {angle}")
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = MonitorApp(root)
    root.mainloop()
