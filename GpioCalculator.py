import tkinter as tk
from tkinter import ttk
import os
import sys

VERSION = "v1.0"
MAINTAINER = "machangbao110@sina.com"


def resource_path(relative_path):
    """
    PyInstaller & normal python compatible resource path
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class GPIOCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GpioCalculator")
        self.resizable(False, False)

        # ========== icon (optional) ===========
        try:
            icon_path = resource_path("icon.ico")
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception:
            pass
        # ======================================

        self.create_vars()
        self.create_widgets()
        self.update_soc_ui()
        self.update_calc_mode()

    # ================= variables =================

    def create_vars(self):
        self.soc = tk.StringVar(value="i.MX")
        self.mode = tk.StringVar(value="Forward")

        self.group = tk.StringVar()
        self.port = tk.StringVar()
        self.index = tk.StringVar()
        self.gpio_num = tk.StringVar()

        self.export_mode = tk.StringVar(value="export")
        self.result_gpio = None

    # ================= UI =================

    def create_widgets(self):
        self.main = ttk.Frame(self)
        self.main.pack(padx=8, pady=6, fill="x")

        self.create_soc_frame()
        self.create_mode_frame()
        self.create_calculation_frame()
        self.create_export_frame()
        self.create_footer()

    def create_soc_frame(self):
        f = ttk.LabelFrame(self.main, text="SoC Mode")
        f.pack(fill="x", pady=4)

        for soc in ["i.MX", "Rockchip", "Allwinner"]:
            ttk.Radiobutton(
                f, text=soc, value=soc,
                variable=self.soc, command=self.update_soc_ui
            ).pack(side="left", padx=8)

    def create_mode_frame(self):
        f = ttk.LabelFrame(self.main, text="Calculation Mode")
        f.pack(fill="x", pady=4)

        for m in ["Forward", "Backward"]:
            ttk.Radiobutton(
                f, text=m, value=m,
                variable=self.mode, command=self.update_calc_mode
            ).pack(side="left", padx=8)

    # ================= Calculation =================

    def create_calculation_frame(self):
        self.calc = ttk.LabelFrame(self.main, text="Calculation")
        self.calc.pack(fill="x", pady=4)

        self.fw_row = ttk.Frame(self.calc)
        self.fw_row.pack(anchor="w")

        self.cb_group = self._combo(self.fw_row, "Group", self.group)
        self.cb_port = self._combo(self.fw_row, "Port", self.port)
        self.cb_index = self._combo(self.fw_row, "Index", self.index)

        self.lbl_fw_result = ttk.Label(self.calc, foreground="blue")
        self.lbl_fw_result.pack(anchor="w", pady=4)

        self.bw_row = ttk.Frame(self.calc)
        ttk.Label(self.bw_row, text="GPIO Number", width=12).pack(side="left")
        ttk.Entry(self.bw_row, textvariable=self.gpio_num, width=12).pack(side="left")

        self.lbl_bw_result = ttk.Label(self.calc, foreground="blue")

        for v in [self.group, self.port, self.index]:
            v.trace_add("write", lambda *_: self.calc_forward())
        self.gpio_num.trace_add("write", lambda *_: self.calc_backward())

    def _combo(self, parent, label, var):
        f = ttk.Frame(parent)
        f.pack(side="left", padx=4)
        ttk.Label(f, text=label).pack(anchor="w")
        cb = ttk.Combobox(f, textvariable=var, width=10, state="normal")
        cb.pack()
        return cb

    # ================= Export =================

    def create_export_frame(self):
        self.export = ttk.LabelFrame(self.main, text="Export Command")
        self.export.pack(fill="x", pady=4)

        r = ttk.Frame(self.export)
        r.pack(anchor="w")

        for t in ["export", "export low", "export high", "export input"]:
            ttk.Radiobutton(
                r, text=t, value=t,
                variable=self.export_mode,
                command=self.update_export_cmd
            ).pack(side="left", padx=6)

        out = ttk.Frame(self.export)
        out.pack(fill="x", pady=4)

        self.cmd = tk.Text(out, height=2, width=46)
        self.cmd.pack(side="left", padx=(0, 4))
        self.cmd.config(state="disabled")

        ttk.Button(out, text="Copy", command=self.copy_cmd).pack(side="left")

    # ================= Footer =================

    def create_footer(self):
        ttk.Label(
            self,
            text=f"GpioCalculator {VERSION} | Maintainer: {MAINTAINER}",
            foreground="gray"
        ).pack(pady=4)

    # ================= State Reset =================

    def reset_state(self):
        self.group.set("")
        self.port.set("")
        self.index.set("")
        self.gpio_num.set("")
        self.export_mode.set("export")
        self.result_gpio = None

        self.cmd.config(state="normal")
        self.cmd.delete("1.0", "end")
        self.cmd.config(state="disabled")

        self.lbl_fw_result.config(text="")
        self.lbl_bw_result.config(text="")

    def set_first_valid_values(self):
        for cb, var in [
            (self.cb_group, self.group),
            (self.cb_port, self.port),
            (self.cb_index, self.index),
        ]:
            values = cb["values"]
            if values:
                var.set(values[0])

    # ================= Logic =================

    def update_soc_ui(self):
        self.reset_state()

        soc = self.soc.get()
        for w in self.fw_row.winfo_children():
            w.pack_forget()

        if soc == "Rockchip":
            self.cb_group.master.pack(side="left")
            self.cb_port.master.pack(side="left")
            self.cb_index.master.pack(side="left")
            self.cb_group["values"] = [f"GPIO{i}" for i in range(8)]
            self.cb_port["values"] = list("ABCD")
            self.cb_index["values"] = list(range(8))

        elif soc == "i.MX":
            self.cb_group.master.pack(side="left")
            self.cb_index.master.pack(side="left")
            self.cb_group["values"] = [f"GPIO{i}" for i in range(1, 9)]
            self.cb_index["values"] = list(range(32))

        else:
            self.cb_port.master.pack(side="left")
            self.cb_index.master.pack(side="left")
            self.cb_port["values"] = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            self.cb_index["values"] = list(range(32))

        self.set_first_valid_values()

        if self.mode.get() == "Backward":
            self.gpio_num.set("0")
            self.calc_backward()

    def update_calc_mode(self):
        self.reset_state()

        self.fw_row.pack_forget()
        self.lbl_fw_result.pack_forget()
        self.bw_row.pack_forget()
        self.lbl_bw_result.pack_forget()

        if self.mode.get() == "Forward":
            self.fw_row.pack(anchor="w")
            self.lbl_fw_result.pack(anchor="w", pady=4)
        else:
            self.bw_row.pack(anchor="w")
            self.lbl_bw_result.pack(anchor="w", pady=4)
            self.gpio_num.set("0")
            self.calc_backward()

        self.set_first_valid_values()

    # ---------- Calculation ----------

    def calc_forward(self):
        try:
            soc = self.soc.get()

            if soc == "Rockchip":
                g = int(self.group.get().replace("GPIO", ""))
                p = ord(self.port.get()) - ord("A")
                i = int(self.index.get())
                gpio = g * 32 + p * 8 + i
            elif soc == "i.MX":
                g = int(self.group.get().replace("GPIO", "")) - 1
                i = int(self.index.get())
                gpio = g * 32 + i
            else:
                p = ord(self.port.get()) - ord("A")
                i = int(self.index.get())
                gpio = p * 32 + i

            self.result_gpio = gpio
            self.lbl_fw_result.config(text=f"GPIO = {gpio}")
            self.update_export_cmd()
        except Exception:
            pass

    def calc_backward(self):
        try:
            gpio = int(self.gpio_num.get())
            self.result_gpio = gpio
            soc = self.soc.get()

            if soc == "Rockchip":
                g = gpio // 32
                p = (gpio % 32) // 8
                i = gpio % 8
                name = f"GPIO{g}_{chr(ord('A')+p)}{i}"
            elif soc == "i.MX":
                g = gpio // 32 + 1
                i = gpio % 32
                name = f"GPIO{g}_IO{i:02d}"
            else:
                p = gpio // 32
                i = gpio % 32
                name = f"P{chr(ord('A')+p)}{i}"

            self.lbl_bw_result.config(text=name)
            self.update_export_cmd()
        except Exception:
            pass

    # ---------- Export ----------

    def update_export_cmd(self):
        if self.result_gpio is None:
            return

        gpio = self.result_gpio
        mode = self.export_mode.get()

        if mode == "export":
            cmd = f"echo {gpio} > /sys/class/gpio/export"
        elif mode == "export low":
            cmd = (
                f"echo {gpio} > /sys/class/gpio/export\n"
                f"echo low > /sys/class/gpio/gpio{gpio}/direction"
            )
        elif mode == "export high":
            cmd = (
                f"echo {gpio} > /sys/class/gpio/export\n"
                f"echo high > /sys/class/gpio/gpio{gpio}/direction"
            )
        else:
            cmd = (
                f"echo {gpio} > /sys/class/gpio/export\n"
                f"cat /sys/class/gpio/gpio{gpio}/value"
            )

        self.cmd.config(state="normal")
        self.cmd.delete("1.0", "end")
        self.cmd.insert("end", cmd)
        self.cmd.config(state="disabled")

    def copy_cmd(self):
        self.clipboard_clear()
        self.clipboard_append(self.cmd.get("1.0", "end").strip())


if __name__ == "__main__":
    GPIOCalculator().mainloop()
