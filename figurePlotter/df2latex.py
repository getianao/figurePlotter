class LatexPrinter:
    def __init__(self, df):
        self.df = df
        self.bold_max = True
        self.letex_code = ""
        self.tex_table_start = r"\begin{tabular}"
        self.tex_table_end = r"\end{tabular}"
        self.tex_hline = r"\hline"
        self.new_line = r"\\"
        self.tex_table_header_position = None

    def add_line(self, line):
        self.letex_code += line + "\n"

    def escape(self, s):
        s = s.replace("_", r"\_")
        s = s.replace("#", r"\#")
        return s

    def bold(self, s):
        return r"\textbf{" + s + r"}"

    def gen_table_latex(self, tex_file_path=None):
        if self.tex_table_header_position is None:
            self.tex_table_header_position = r"{|c|" + "r|" * self.df.shape[1] + "}"
        self.add_line(self.tex_table_start + self.tex_table_header_position)
        self.add_line(self.tex_hline)
        # Column names
        columns = self.df.columns.tolist()
        columns = [self.bold(self.escape(col)) for col in columns]
        tex_columns = " & ".join(columns)
        self.add_line(tex_columns + self.new_line + self.tex_hline)

        # Data
        for i in range(self.df.shape[0]):
            row = self.df.iloc[i].tolist()
            print(row)

            max = -999
            max_id = -1
            for j in range(len(row)):
                if isinstance(row[j], (int, float)):
                    if row[j] > max:
                        max = row[j]
                        max_id = j
            if self.bold_max:
                row[max_id] = self.bold(str(row[max_id]))

            row = [self.escape(str(col)) for col in row]
            row_length = len(row)
            tex_row = " & ".join(row)
            tex_cline = r" \cline{1-" + str(row_length) + "}"
            self.add_line(tex_row + self.new_line + tex_cline)

        self.add_line(self.tex_table_end)
        print(self.letex_code)
        if tex_file_path is not None:
            with open(tex_file_path, "w") as f:
                f.write(self.letex_code)
            print(f"Table saved to {tex_file_path}")
