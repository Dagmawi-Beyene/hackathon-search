import asyncio
import time
import aiohttp
import json
from meilisearch import Client
import openai
from dotenv import load_dotenv
import os

load_dotenv()  

BUCKET_NAME = os.getenv("BUCKET_NAME")
URL = os.getenv("URL")
MEILISEARCH_KEY = os.getenv("MEILISEARCH_KEY")
openai.api_key = os.getenv("OPENAI_KEY")
MAX_CONCURRENT_REQUESTS = 10

KEYS = ['ADV700JU023.json', 'ADV700JU047.json', 'COL999MX036.json', 'COL285MX038.json', 'COL605MX039.json', 'COL999MX040.json', 'COL999MG053.json', 'COL385MU054.json', 'COL575MX055.json', 'COL999MX059.json', 'COL485MX069.json', 'COL425MX075.json', 'COL475MX082.json', 'COL140MX114.json', 'COL605MX132.json', 'COL200MX133.json', 'DEF500SF016.json', 'DEF420SF022.json', 'DEF270SF061.json', 'DEF305MX131.json', 'DIS475MU012.json', 'DIS175SU027.json', 'DIS280SU058.json', 'DIS175JU081.json', 'DIS115JU087.json', 'DIS315JU101.json', 'DIS195SU117.json', 'DIS495JU119.json', 'DIS150JU130.json', 'INT425JG001.json', 'INT425JG002.json', 'INT175SF003.json', 'LAB200JU018.json', 'LAB175SU026.json', 'LAB175SU032.json', 'LAB175SU033.json', 'LAB500SU044.json', 'LAB205SU045.json', 'LAB500SU089.json', 'LAB575JU095.json', 'LEL115SU005.json', 'LEL175MU014.json', 'LEL300SU020.json', 'LEL500JU034.json', 'LEL295JU035.json', 'LEL280JG051.json', 'LEL565SU064.json', 'LEL185SU066.json', 'LEL220JU071.json', 'LEL220SU073.json', 'LEL140SU074.json', 'LEL300SU076.json', 'LEL175JU086.json', 'LEL500SU088.json', 'LEL115JU090.json', 'LEL305JU092.json', 'LEL542SU096.json', 'LEL485JU097.json', 'LEL175SU098.json', 'LEL200JU105.json', 'LEL175SU106.json', 'LEL115SU107.json', 'LEL200MU110.json', 'LEL175JU112.json', 'LEL105SU113.json', 'LEL195SU120.json', 'LEL320JU143.json', 'LEL320JU147.json', 'LEL215SU150.json', 'LEL175JU154.json', 'LES485MG006.json', 'LES385SU007.json', 'LES355SU009.json', 'LES175SU025.json', 'LES175SU028.json', 'LES365JG029.json', 'LES175SU031.json', 'LES330JG052.json', 'LES215MU056.json', 'LES495JU063.json', 'LES335JG065.json', 'LES445SU067.json', 'LES425JG077.json', 'LES405JG078.json', 'LES175SU079.json', 'LES605SU080.json', 'LES320SU085.json', 'LES425SU093.json', 'LES235SU099.json', 'LES500SU102.json', 'LES300SU103.json', 'LES305MU108.json', 'LES165JG121.json', 'LES205JG124.json', 'LES315SU129.json', 'LES420MG134.json', 'LES500JU136.json', 'LES565SU137.json', 'LES280JG138.json', 'LES220SU140.json', 'LES115MU151.json', 'LES565MX152.json', 'MTG425JG004.json', 'MTG400MX008.json', 'MTG999ST015.json', 'MTG999SU043.json', 'MTG270SG049.json', 'MTG485SG142.json', 'OFC301MU021.json', 'OFC578SG037.json', 'OFC150MU042.json', 'OFC575MU046.json', 'OFC270MG048.json', 'OFC115SU060.json', 'OFC105SU068.json', 'OFC355SU094.json', 'OFC280SU109.json', 'OFC195SU116.json', 'OFC285SG135.json', 'OFC175JU145.json', 'OFC300JU149.json', 'OFC320SU153.json', 'SEM475MX041.json', 'SEM140JG070.json', 'SEM340JG072.json', 'SEM545MG083.json', 'SEM475JU084.json', 'SEM300MU100.json', 'SEM495SU111.json', 'SGR385SU057.json', 'SGR999MX115.json', 'SGR175SU123.json', 'SGR200JU125.json', 'SGR175MU126.json', 'SGR195SU127.json', 'SGR565SU144.json', 'SGR999SU146.json', 'STP355SU010.json', 'STP355MG011.json', 'STP285SU013.json', 'STP200JU019.json', 'STP125JG050.json', 'STP545JU091.json', 'STP560JG118.json', 'STP165JG122.json', 'STP450SG128.json', 'STP095SU139.json', 'STP175SU141.json', 'SVC999MX104.json', 'SVC999MX148.json', 'TOU999JU030.json', 'TOU999MX062.json']

client = Client(URL, MEILISEARCH_KEY)

openai.api_key = "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"

index = client.index("json_files")


async def get_embedding(text_to_embed):
    response = openai.Embedding.create(
        model="text-embedding-ada-002", input=[text_to_embed]
    )
    embedding = response["data"][0]["embedding"]

    return embedding


async def fetch(session, key):
    MAX_RETRIES = 5
    for i in range(MAX_RETRIES):
        try:
            async with session.get(
                f"https://{BUCKET_NAME}.s3.amazonaws.com/{key}"
            ) as response:
                data = await response.text()
                if data.strip() != "":  # check if response is not empty
                    return key, json.loads(data)
                else:
                    return None, None
        except Exception as e:
            print(f"Error on {key} attempt {i+1}: {e}")
            if i < MAX_RETRIES - 1:  # i is zero indexed
                await asyncio.sleep(2 ** (i + 1))  # Exponential back-off
            else:
                print("All attempts failed. Returning None, None.")
                return None, None


async def prepare_documents(session, key):
    try:
        key, data = await fetch(session, key)
        json_content = data["results"]
        segments = json_content.get("speaker_labels", {}).get("segments", [])
        indexed_data_list = []

        for i, segment in enumerate(segments):
            transcript = " ".join([item["content"] for item in segment["items"]])
            transcript_context = f"{segment['speaker_label']} from {segment['start_time']} to {segment['end_time']} said: {transcript}"
            retry = True
            while retry:
                try:
                    embedding = await get_embedding(transcript_context)
                    retry = False
                except:
                    print(f"Rate limit hit, waiting for 5 seconds before retrying...")
                    time.sleep(5)

            indexed_data = {
                "id": f"{key.replace('.json', '')}_{i}",
                "start_time": segment["start_time"],
                "end_time": segment["end_time"],
                "speakers": segment["speaker_label"],
                "transcripts": transcript,
                "_vectors": embedding,
            }
            indexed_data_list.append(indexed_data)
        print(f"Indexed {len(indexed_data_list)} documents for {key}")
        return indexed_data_list
    except Exception as e:
        print(f"Error on {key}: {e}")
        return []


async def main():
    all_keys = KEYS
    all_docs = []
    sem = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    MAX_RETRIES = 5

    CHUNK_SIZE = 1000  # Adjust this size if needed

    async def limited_wrapper(session, key):
        async with sem:  # semaphore limits num of simultaneous calls
            return await prepare_documents(session, key)

    async with aiohttp.ClientSession() as session:
        tasks = [limited_wrapper(session, key) for key in all_keys]
        responses = await asyncio.gather(*tasks)
    all_docs = [doc for sublist in responses for doc in sublist]

    if all_docs:
        print(f"Preparing to index {len(all_docs)} documents")
        # export documents to json
        with open('all_docs.json', 'w') as fp:
            json.dump(all_docs, fp)

        chunks = [all_docs[i:i + CHUNK_SIZE] for i in range(0, len(all_docs), CHUNK_SIZE)]  # Split all_docs into chunks

        for chunk in chunks:
            print(f"Indexing {len(chunk)} documents")

            for i in range(MAX_RETRIES):
                try:
                   index.add_documents_in_batches(chunk, len(chunk))
                   break  # Successful, so break out of the loop
                except Exception as e:
                   print("Error while adding documents to MeiliSearch index, attempt ", i+1, ":", str(e))
                   if i < MAX_RETRIES - 1:  # i is zero indexed
                      await asyncio.sleep(2**(i+1))  # Exponential back-off
                   else:
                      print("All attempts failed. Exiting.")
    else:
        print("No documents to index")





