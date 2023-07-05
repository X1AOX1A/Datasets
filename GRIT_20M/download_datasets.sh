download_dir="$1"
file_url="https://conversationhub.blob.core.windows.net/beit-share-public/kosmos-2/data/grit_coyo.jsonl?sv=2021-10-04&st=2023-06-08T11%3A16%3A02Z&se=2033-06-09T11%3A16%3A00Z&sr=c&sp=r&sig=N4pfCVmSeq4L4tS8QbrFVsX6f6q844eft8xSuXdxU48%3D"

wget -O "${download_dir}" "$file_url"