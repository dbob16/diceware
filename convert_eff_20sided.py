import ttkbootstrap as ttk 
from tkinter import filedialog

def main():
    window = ttk.Window(title="Dilan's 20 sided EFF Converter", themename="cyborg")
    v_filein = ttk.StringVar(window)
    v_fileout = ttk.StringVar(window)

    # Commands
    def cmd_fileinbrowse():
        filepath = filedialog.askopenfilename()
        v_filein.set(filepath)

    def cmd_fileoutbrowse():
        filepath = filedialog.asksaveasfilename()
        v_fileout.set(filepath)

    def cmd_convert():
        readfile = open(v_filein.get(), "r")
        with open(v_fileout.get(), "w") as writefile:
            for line in readfile.readlines():
                line = line.split()
                seq, word = line[0], line[1]
                seq = seq.replace("-", " ")
                seq = seq.split()
                nseq = ""
                for digit in seq:
                    if len(digit) < 2:
                        digit = f"0{digit}"
                    nseq += digit
                writefile.write(f"{nseq}  {word}\n")
        v_filein.set("")
        v_fileout.set("")

    def cmd_close():
        window.destroy()

    # Frames
    frm_files = ttk.Frame(window)
    frm_files.pack(side="top", padx=4, pady=4)

    frm_buttons = ttk.Frame(window)
    frm_buttons.pack(side="top", padx=4, pady=4)

    # File Controls
    lbl_inputfile = ttk.Label(frm_files, text="Input File")
    lbl_inputfile.grid(row=0, column=0, padx=4, pady=4)

    txt_inputfile = ttk.Entry(frm_files, width=25, textvariable=v_filein)
    txt_inputfile.grid(row=0, column=1, padx=4, pady=4)

    btn_browseinfile = ttk.Button(frm_files, text="Browse", command=cmd_fileinbrowse)
    btn_browseinfile.grid(row=0, column=2, padx=4, pady=4)

    lbl_outputfile = ttk.Label(frm_files, text="Output File")
    lbl_outputfile.grid(row=1, column=0, padx=4, pady=4)

    txt_outputfile = ttk.Entry(frm_files, width=25, textvariable=v_fileout)
    txt_outputfile.grid(row=1, column=1, padx=4, pady=4)

    btn_browseoutfile = ttk.Button(frm_files, text="Browse", command=cmd_fileoutbrowse)
    btn_browseoutfile.grid(row=1, column=2, padx=4, pady=4)

    # Button Controls
    btn_convert = ttk.Button(frm_buttons, text="Convert", command=cmd_convert)
    btn_convert.grid(row=0, column=0, padx=4, pady=4)

    btn_close = ttk.Button(frm_buttons, text="Close", bootstyle="secondary", command=cmd_close)
    btn_close.grid(row=0, column=1, padx=4, pady=4)

    window.mainloop()

if __name__ == "__main__":
    main()