import queue
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, scrolledtext

import excel_concat as core


class TextRedirector:
    """Redireciona sys.stdout para uma fila lida pela thread da UI."""

    def __init__(self, q):
        self.q = q

    def write(self, s):
        self.q.put(s)

    def flush(self):
        pass


def run_pipeline(q, arquivos):
    sys.stdout = TextRedirector(q)
    try:
        core.main(generate=True, validate=True, arquivos=arquivos)
    except SystemExit as e:
        q.put(f"\n[ERRO] {e.code}\n")
    except Exception as e:
        q.put(f"\n[ERRO] {e}\n")
    finally:
        sys.stdout = sys.__stdout__
        q.put(None)


def main():
    root = tk.Tk()
    root.title("RNC Concat")
    root.geometry("700x600")

    tk.Label(root, text=f"Saída: {core.OUTPUT_FILE}").pack(anchor="w", padx=8, pady=(8, 0))

    origem = tk.StringVar(value="manual")
    arquivos_selecionados = []
    label_selecao = tk.Label(root, text="Nenhum arquivo selecionado.", fg="gray")

    def escolher_arquivos():
        caminhos = filedialog.askopenfilenames(
            title="Selecionar arquivos .xlsx", filetypes=[("Excel", "*.xlsx")]
        )
        if caminhos:
            arquivos_selecionados[:] = [Path(c) for c in caminhos]
            label_selecao.config(text=f"{len(arquivos_selecionados)} arquivo(s) selecionado(s).")

    frame_origem = tk.LabelFrame(root, text="Arquivos de entrada")
    frame_origem.pack(fill="x", padx=8, pady=8)

    tk.Radiobutton(
        frame_origem, text=f"Pasta {core.INPUT_DIR}", variable=origem, value="pasta"
    ).pack(anchor="w")
    frame_manual = tk.Frame(frame_origem)
    frame_manual.pack(fill="x")
    tk.Radiobutton(frame_manual, text="Selecionar arquivos manualmente", variable=origem, value="manual").pack(
        side="left"
    )
    tk.Button(frame_manual, text="Escolher arquivos...", command=escolher_arquivos).pack(side="left", padx=8)
    label_selecao.pack(anchor="w", padx=24)

    log = scrolledtext.ScrolledText(root, state="disabled")
    log.pack(fill="both", expand=True, padx=8, pady=8)

    btn = tk.Button(root, text="Executar")
    btn.pack(pady=(0, 8))

    q = queue.Queue()

    def poll():
        try:
            while True:
                item = q.get_nowait()
                if item is None:
                    btn.config(state="normal")
                    continue
                log.config(state="normal")
                log.insert("end", item)
                log.see("end")
                log.config(state="disabled")
        except queue.Empty:
            pass
        root.after(100, poll)

    def start():
        if origem.get() == "manual" and not arquivos_selecionados:
            label_selecao.config(text="Selecione ao menos um arquivo antes de executar.", fg="red")
            return

        arquivos = arquivos_selecionados if origem.get() == "manual" else None
        btn.config(state="disabled")
        log.config(state="normal")
        log.delete("1.0", "end")
        log.config(state="disabled")
        threading.Thread(target=run_pipeline, args=(q, arquivos), daemon=True).start()

    btn.config(command=start)
    poll()
    root.mainloop()


if __name__ == "__main__":
    main()
