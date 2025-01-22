# dictionary with keys= names of columns in table, values function taking in matrics and returning the values
dataset_table = {"Total positives": lambda metrics: [v["total positives"] for v in metrics["single threshold"]]}
