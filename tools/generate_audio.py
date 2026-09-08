import json
import time
import urllib.request
import urllib.parse
import os
import shutil

COMFY_URL = "http://127.0.0.1:8188"

prompt_workflow = {
    "1": {
        "inputs": {
            "model": "int8 text encoder only",
            "dtype": "auto",
            "device": "auto",
            "attention": "auto",
            "decode_mode": "eager",
            "download_if_missing": True
        },
        "class_type": "BreezeTTS2LoadModel"
    },
    "2": {
        "inputs": {
            "breeze_model": ["1", 0],
            "text": "The end of the world started on a Tuesday, and Arthur Vance was mostly annoyed that it interrupted his shelving.\n\nHe stood on the fourth rung of a rolling wooden ladder, deep in the chilly sub-basement of the Grand Municipal Library. In his hands was an old, battered guide on mine tunnels and furnace ventilation. It belonged on the top shelf, squeezed between an outdated metallurgy manual and a grease-stained book on steam boilers.",
            "instruction": "A deep, American male storyteller voice with a warm, commanding presence.",
            "cfg_scale": 4.0,
            "max_new_tokens": 1500,
            "temperature": 0.9,
            "top_k": 50,
            "top_p": 1.0,
            "repetition_penalty": 1.1,
            "depth_temperature": 0.9,
            "depth_top_k": 50,
            "depth_top_p": 1.0,
            "seed": 42
        },
        "class_type": "BreezeTTS2VoiceDesign"
    },
    "3": {
        "inputs": {
            "audio": ["2", 0],
            "filename_prefix": "breeze_storyteller"
        },
        "class_type": "SaveAudio"
    }
}

def queue_prompt(prompt):
    p = {"prompt": prompt}
    data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(f"{COMFY_URL}/prompt", data=data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

def get_history(prompt_id):
    with urllib.request.urlopen(f"{COMFY_URL}/history/{prompt_id}") as resp:
        return json.loads(resp.read().decode('utf-8'))

def main():
    print("Submitting prompt to ComfyUI...")
    res = queue_prompt(prompt_workflow)
    prompt_id = res.get("prompt_id")
    print(f"Prompt queued successfully with ID: {prompt_id}")

    print("Waiting for generation to finish...")
    start_time = time.time()
    last_print = 0
    while True:
        hist = get_history(prompt_id)
        if prompt_id in hist:
            print("\nPrompt finished processing!")
            outputs = hist[prompt_id].get("outputs", {})
            print("Outputs:", json.dumps(outputs, indent=2))
            
            # Find output files
            for node_id, node_output in outputs.items():
                if "audio" in node_output:
                    for audio_info in node_output["audio"]:
                        filename = audio_info.get("filename")
                        subfolder = audio_info.get("subfolder", "")
                        folder_type = audio_info.get("type", "output")
                        print(f"Audio output file: {filename} in {subfolder} ({folder_type})")
                        
                        base_output = r"C:\Users\Admin\AppData\Local\Comfy-Desktop\ComfyUI-Shared\output"
                        src_path = os.path.join(base_output, subfolder, filename)
                        if os.path.exists(src_path):
                            dest_path = os.path.join(r"d:\Antigravity Projects", filename)
                            shutil.copy2(src_path, dest_path)
                            print(f"Copied audio to: {dest_path}")
            break
        
        time.sleep(2)
        elapsed = int(time.time() - start_time)
        if elapsed - last_print >= 5:
            print(f"Still processing... ({elapsed}s elapsed)")
            last_print = elapsed

if __name__ == "__main__":
    main()
