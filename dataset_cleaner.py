import pandas as pd


def duplicate_transcript_column(path, output_path):
    # Load data
    df = pd.read_csv(path, sep='|')
    df = pd.concat([df, df[df.columns[-1]]], axis=1)
    df.to_csv(output_path, sep='|', index=False)

def remove_white_spaces(path, output_path):
    df = pd.read_csv(path, sep='|')
    print(df.columns)
    df = df.map(lambda x: x.replace('\n', ' '))
    df.to_csv(output_path, sep='|', index=False)


# remove_white_spaces('data/pl_dataset.csv', 'data/pl_dataset_2.csv')
duplicate_transcript_column('data/pl_dataset.csv', 'data/metadata_pl.csv')
with open('data/metadata_pl.csv', "r", encoding="utf-8") as ttf:
    for line in ttf:
        cols = line.split("|")
        print(cols)  # Add this line to see the content of each line.
        # wav_file = os.path.join(root_path, "wavs", cols[0] + ".wav")
        text = cols[2]  # This is where the error occurs
