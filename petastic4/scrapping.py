import requests
import pandas as pd

def rcsb_search(query:str, return_type:str = "entry", start:int = 0, rows:int = 200) -> pd.DataFrame:
  url = "https://search.rcsb.org/rcsbsearch/v2/query"
  data = {
    "query": {
      "type": "terminal",
      "service": "full_text",
      "parameters": {
        "value": query
      }
    },
    "return_type": return_type,
    "request_options": {
      "paginate": {
        "start": start,
        "rows": rows
      }
    },
  }

  res = requests.post(url, json=data, headers={"Content-Type": "application/json"})
  print('status code:', res.status_code)
  df = pd.DataFrame(res.json()['result_set'])
  return df

def get_fasta(pdb_id:str) -> pd.Series:
    url = f"https://www.rcsb.org/fasta/entry/{pdb_id}"
    res = requests.get(url)
    fasta = res.text
    lines = fasta.strip().split("\n")
    header = lines[0][1:]
    parts = header.split('|')
    file = pd.Series({
        "fasta_id" : parts[0],
        "chain" : parts[1],
        "sequence" : "".join(lines[1:]),
        "desc" : parts[2],
    })
    return file
