import os
import pandas as pd
from pkg_resources import resource_filename

class vietnamese_conceptizer:
    def __init__(self):
        # Tải từ điển từ gói
        dictionary_path = resource_filename(
            __name__, "data/WORDS_WordNet_And_VCL_ALL_sorted.txt"
        )
        self.dictionary = self._load_dictionary(dictionary_path)

    def _load_dictionary(self, path):
        dic = {}
        with open(path, 'r', encoding="utf-8") as f:
            for i, line in enumerate(f):
                dic[line.strip()] = i
        return dic

    def process_file(self, input_path, output_path, log_path, columns_to_process):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

        # Read input file
        try:
            df = pd.read_csv(input_path, sep="\t", encoding="utf-8")
        except Exception as e:
            raise ValueError(f"Error reading file {input_path}: {e}")

        replated = []

        for col in columns_to_process:
            if col not in df.columns:
                raise ValueError(f"Column '{col}' does not exist in the input file.")
            
            original_data = df[col].dropna().tolist()
            result = []

            for sentence in original_data:
                ws = sentence.lower().split()
                n = len(ws)
                d = ""
                t = 0

                while t < n:
                    k = 1
                    tem = ws[t]
                    if t < n - 4 and "_".join(ws[t:t + 5]) in self.dictionary:
                        k = 5
                        tem = "_".join(ws[t:t + 5])
                    elif t < n - 3 and "_".join(ws[t:t + 4]) in self.dictionary:
                        k = 4
                        tem = "_".join(ws[t:t + 4])
                    elif t < n - 2 and "_".join(ws[t:t + 3]) in self.dictionary:
                        k = 3
                        tem = "_".join(ws[t:t + 3])
                    elif t < n - 1 and "_".join(ws[t:t + 2]) in self.dictionary:
                        k = 2
                        tem = "_".join(ws[t:t + 2])

                    if tem != ws[t] and tem not in replated:
                        replated.append(tem)

                    d = f"{d} {tem}".strip()
                    t += k

                result.append(d)

            df[col] = result

        # Save processed file
        df.to_csv(output_path, sep="\t", index=False, encoding="utf-8")

        # Save log file
        with open(log_path, 'w', encoding="utf-8") as log_file:
            for word in replated:
                log_file.write(f"{word}\n")
