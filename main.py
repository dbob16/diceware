import sqlite3 as sql 
import ttkbootstrap as ttk
import random as r
from tkinter import filedialog

def create_conn():
    conn = sql.connect("app.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS 'tablelist' (tablename TEXT PRIMARY KEY)")
    conn.commit()
    return conn, cur

def main():
    window = ttk.Window(title="Dilan's Diceware", themename="cyborg")
    # Vars
    v_lookup = ttk.StringVar(window)
    v_txt_lookup = ttk.IntVar(window)
    v_wordlist = []
    v_output = ttk.StringVar(window)

    # Commands
    def cmd_refresh_cb():
        tablelist = []
        conn, cur = create_conn()
        cur.execute("SELECT tablename FROM 'tablelist' ORDER BY tablename ASC")
        for tablename in cur.fetchall():
            tablelist.append(tablename)
        cb_tablename.config(values=tablelist)
        if len(tablelist) > 0:
            cb_tablename.set(tablelist[0])
        else:
            cb_tablename.set("No Tables Available")

    def cmd_import_table():
        window = ttk.Toplevel(title="Table Importer")
        # Variables
        v_filepath = ttk.StringVar(window)
        v_tablename = ttk.StringVar(window)

        # Commands
        def cmd_close_window():
            window.destroy()

        def cmd_browse():
            filepath = filedialog.askopenfilename()
            v_filepath.set(filepath)
            window.focus()

        def cmd_save_table():
            conn, cur = create_conn()
            cur.execute(f"REPLACE INTO 'tablelist' (tablename) VALUES ('{v_tablename.get()}')")
            cur.execute(f"DROP TABLE IF EXISTS '{v_tablename.get()}'")
            cur.execute(f"CREATE TABLE '{v_tablename.get()}' (seq INT PRIMARY KEY, word TEXT)")
            conn.commit()
            f = open(v_filepath.get(), "r")
            for line in f.readlines():
                line_split = line.split()
                seq, word = line_split[0], line_split[1]
                cur.execute(f"REPLACE INTO '{v_tablename.get()}' VALUES ({seq}, '{word}')")
                print(f"For {seq}, inserted {word}")
            conn.commit()
            conn.execute("VACUUM")
            conn.commit()
            conn.close()
            cmd_refresh_cb()
            window.destroy()

        # Frames
        frm_inputs = ttk.Frame(window)
        frm_inputs.pack(side="top", padx=4, pady=4)
        frm_buttons = ttk.Frame(window)
        frm_buttons.pack(side="top", padx=4, pady=4)

        # Input Controls
        lbl_filepath = ttk.Label(frm_inputs, text="File")
        lbl_filepath.grid(row=0, column=0, padx=4, pady=4)
        txt_filepath = ttk.Entry(frm_inputs, width=25, textvariable=v_filepath)
        txt_filepath.grid(row=0, column=1, padx=4, pady=4)
        btn_browse = ttk.Button(frm_inputs, text="Browse", command=cmd_browse)
        btn_browse.grid(row=0, column=2, padx=4, pady=4)

        lbl_tablename = ttk.Label(frm_inputs, text="Name Table")
        lbl_tablename.grid(row=1, column=0, padx=4, pady=4)
        txt_tablename = ttk.Entry(frm_inputs, width=25, textvariable=v_tablename)
        txt_tablename.grid(row=1, column=1, padx=4, pady=4)

        # Button Controls
        btn_save = ttk.Button(frm_buttons, text="Save", command=cmd_save_table)
        btn_save.grid(row=0, column=0, padx=4, pady=4)
        btn_cancel = ttk.Button(frm_buttons, text="Cancel", bootstyle="secondary", command=cmd_close_window)
        btn_cancel.grid(row=0, column=1, padx=4, pady=4)

    def cmd_delete_table():
        conn, cur = create_conn()
        cur.execute(f"DELETE FROM 'tablelist' WHERE tablename = '{cb_tablename.get()}'")
        cur.execute(f"DROP TABLE IF EXISTS '{cb_tablename.get()}'")
        conn.commit()
        conn.execute("VACUUM")
        conn.commit()
        conn.close()
        cmd_refresh_cb()

    def cmd_lookup():
        conn, cur = create_conn()
        cur.execute(f"SELECT word FROM '{cb_tablename.get()}' WHERE seq = {v_txt_lookup.get()}")
        value = cur.fetchone()[0]
        conn.close()
        v_lookup.set(value)

    def cmd_random():
        conn, cur = create_conn()
        cur.execute(f"SELECT seq, word FROM '{cb_tablename.get()}' ORDER BY RANDOM() LIMIT 1")
        entry = cur.fetchone()
        conn.close()
        seq, word = entry[0], entry[1]
        v_txt_lookup.set(seq)
        v_lookup.set(word)

    def cmd_dicesim():
        window = ttk.Toplevel(title="Dice Simulator")

        # Variables
        v_nuofdice = ttk.IntVar(window)

        # Commands
        def cmd_rolldice():
            for control in frm_diceroll.winfo_children():
                control.destroy()
            for i in range(1, v_nuofdice.get()+1):
                frm_column = ttk.Frame(frm_diceroll)
                frm_column.pack(side="left", padx=4, pady=4)
                rnum = str(r.randint(1, 6))
                lbl_label = ttk.Label(frm_column, text=f"Dice #{i}:")
                lbl_label.pack(side="top", padx=4, pady=4)
                lbl_dice = ttk.Label(frm_column, text=rnum, font="16")
                lbl_dice.pack(side="top", padx=4, pady=4)
        
        # Frames
        frm_dicecontrols = ttk.Frame(window)
        frm_dicecontrols.pack(side="top", padx=4, pady=4)

        frm_diceroll = ttk.Frame(window)
        frm_diceroll.pack(side="top", padx=4, pady=4)

        # Dice Controls
        lbl_nuofdice = ttk.Label(frm_dicecontrols, text="Number of Dice: ")
        lbl_nuofdice.grid(row=0, column=0, padx=4, pady=4)

        txt_nuofdice = ttk.Entry(frm_dicecontrols, width=3, textvariable=v_nuofdice)
        txt_nuofdice.grid(row=0, column=1, padx=4, pady=4)

        btn_rolldice = ttk.Button(frm_dicecontrols, text="Roll Dice", command=cmd_rolldice)
        btn_rolldice.grid(row=0, column=2, padx=4, pady=4)

    def cmd_refresh_output():
        endstr = ""
        for w in v_wordlist:
            endstr += f" {w}"
        endstr = endstr.lstrip()
        v_output.set(endstr)

    def cmd_add_word():
        v_wordlist.append(v_lookup.get().title())
        cmd_refresh_output()

    def cmd_del_last_word():
        v_wordlist.pop()
        cmd_refresh_output()
    
    def cmd_add_random_number():
        endstr = ""
        for i in range(0, int(txt_randomdigits.get())):
            digit = str(r.randint(0, 9))
            endstr += digit
        v_wordlist.append(endstr)
        cmd_refresh_output()
    
    def cmd_clear_words():
        v_wordlist.clear()
        cmd_refresh_output()

    def cmd_copy():
        window.clipboard_clear()
        window.clipboard_append(v_output.get())
        
    # Frames
    frm_tableops = ttk.LabelFrame(window, text="Table Operations")
    frm_tableops.pack(side="top", padx=4, pady=4, fill="x")

    frm_tableselect = ttk.LabelFrame(window, text="Table Selection")
    frm_tableselect.pack(side="top", padx=4, pady=4, fill="x")

    frm_diceops = ttk.LabelFrame(window, text="Dice Operations")
    frm_diceops.pack(side="top", padx=4, pady=4, fill="x")

    frm_resultops = ttk.LabelFrame(window, text="Result Operations")
    frm_resultops.pack(side="top", padx=4, pady=4, fill="x")

    frm_output = ttk.LabelFrame(window, text="Output")
    frm_output.pack(side="top", padx=4, pady=4, fill="x")

    # Table Op Controls
    btn_importtable = ttk.Button(frm_tableops, text="Import Table", command=cmd_import_table)
    btn_importtable.grid(row=0, column=0, padx=4, pady=4)

    btn_deletetable = ttk.Button(frm_tableops, text="Delete Table", command=cmd_delete_table)
    btn_deletetable.grid(row=0, column=1, padx=4, pady=4)

    # Table Select Controls
    cb_tablename = ttk.Combobox(frm_tableselect, state="readonly")
    cb_tablename.grid(row=0, column=0, padx=4, pady=4)

    # Dice Op Controls
    txt_lookup = ttk.Entry(frm_diceops, width=8, textvariable=v_txt_lookup)
    txt_lookup.grid(row=0, column=0, padx=4, pady=4)

    btn_lookup = ttk.Button(frm_diceops, text="Lookup", command=cmd_lookup)
    btn_lookup.grid(row=0, column=1, padx=4, pady=4)

    btn_random = ttk.Button(frm_diceops, text="Random", command=cmd_random)
    btn_random.grid(row=0, column=2, padx=4, pady=4)

    lbl_lookup = ttk.Label(frm_diceops, textvariable=v_lookup, width=17)
    lbl_lookup.grid(row=0, column=3, padx=4, pady=4)

    btn_dicesim = ttk.Button(frm_diceops, text="Dice Sim", command=cmd_dicesim)
    btn_dicesim.grid(row=0, column=4, padx=4, pady=4)

    # Result Op Controls
    btn_addword = ttk.Button(frm_resultops, text="Add Current Word", command=cmd_add_word)
    btn_addword.grid(row=0, column=0, padx=4, pady=4)

    btn_dellastword = ttk.Button(frm_resultops, text="Delete Last Word", command=cmd_del_last_word)
    btn_dellastword.grid(row=0, column=1, padx=4, pady=4)

    txt_randomdigits = ttk.Entry(frm_resultops, width=4)
    txt_randomdigits.grid(row=0, column=2, padx=4, pady=4)

    btn_adddigits = ttk.Button(frm_resultops, text="Random Digits", command=cmd_add_random_number)
    btn_adddigits.grid(row=0, column=3, padx=4, pady=4)

    btn_clearresults = ttk.Button(frm_resultops, text="Clear Results", command=cmd_clear_words)
    btn_clearresults.grid(row=0, column=4, padx=4, pady=4)

    btn_copy = ttk.Button(frm_resultops, text="Copy Output", command=cmd_copy)
    btn_copy.grid(row=1, column=0, columnspan=5, padx=4, pady=4)

    # Output Controls
    lbl_output = ttk.Label(frm_output, textvariable=v_output)
    lbl_output.grid(row=0, column=0, padx=4, pady=4)

    cmd_refresh_cb()
    window.mainloop()

if __name__ == "__main__":
    main()