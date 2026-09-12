# -*- coding: utf-8 -*-
"""
Pre-caches all scanning audio clips and career foretellings for Brahmasree Biju 2.0.
"""
import os
import asyncio
from voice import save_direct_audio, get_or_create_audio, AUDIO_CACHE_DIR
from predictions import CAREER_PREDICTIONS

SCAN_CLIPS = {
    "scan_step1.mp3": "ങ്ഹാ... ശിവ ശംഭോ... ക്യാമറയിലേക്ക് നേരെ നോക്ക് കുട്ടാ... കണ്ണടയുടെ മുകളിലൂടെ ഞാൻ നോക്കുകയാണ്... സാമുദ്രിക മുഖലക്ഷണം ഞാൻ പരിശോധിക്കട്ടെ...",
    "scan_smiling.mp3": "ഹും... ചുണ്ടിൽ ഒരു കള്ളച്ചിരി വിരിയുന്നുണ്ടല്ലോ! എന്തോ വലിയ അടവ് മനസ്സിൽ വെച്ചാണ് നിൽപ്പ്... നെറ്റിയിലെ രേഖകൾ വ്യക്തമായി!",
    "scan_tilted.mp3": "തലയൊന്ന് ചരിച്ചു നോക്കുന്നുണ്ട്... എന്തൊരു സംശയം! ഗ്രഹനിലയിലെ സംശയരോഗം ബിജു വ്യക്തമായി വായിച്ചെടുത്തിരിക്കുന്നു...",
    "scan_serious.mp3": "നെറ്റിയിലെ വരകൾ നോക്കട്ടെ... ശ്ശെടാ! ഇതെന്തൊരു ഗൗരവമാണിത്! രാഹുവും ശനിയും കൂടി തലയ്ക്ക് മീതെ കയറിയിരുന്ന് ചിന്തിക്കുകയാണല്ലോ!",
    "scan_step3.mp3": "അയ്യയ്യോ... കണ്ടോ കണ്ടോ! അഷ്ടമത്തിലെ വ്യാഴവും പത്താം ഭാവത്തിലെ ചൊവ്വയും! നിന്റെ സകല ജാതക രഹസ്യങ്ങളും ഞാൻ ഇതാ തുറക്കുകയാണ്... കേട്ടോ!",
    "scan_step4.mp3": "ഗ്രഹങ്ങളെല്ലാം ഒന്നിച്ചു നിരന്നു! നിന്റെ അന്തിമ വിധി ഇതാ വരുന്നു... കണ്ണു തുറന്നു കേട്ടോ കുട്ടാ!"
}

async def generate_scan_clips():
    print("Generating scanning & inferring audio clips...")
    for filename, text in SCAN_CLIPS.items():
        print(f" -> Generating {filename}...")
        await save_direct_audio(text, filename)
    print("Scanning clips generated successfully!")

async def generate_career_audios():
    print(f"Generating audio for {len(CAREER_PREDICTIONS)} careers...")
    sem = asyncio.Semaphore(3)

    async def gen(task_desc, text, prefix="biju"):
        async with sem:
            print(f" -> {task_desc}")
            await get_or_create_audio(text, filename_prefix=prefix)

    tasks = []
    for c in CAREER_PREDICTIONS:
        # Full speech
        tasks.append(gen(f"[{c['id']}] Full Speech", c["full_speech"], "biju"))
        # Individual sections
        tasks.append(gen(f"[{c['id']}] Career", c["speech_career"], "sec_career"))
        tasks.append(gen(f"[{c['id']}] Love", c["speech_love"], "sec_love"))
        tasks.append(gen(f"[{c['id']}] Wealth", c["speech_wealth"], "sec_wealth"))
        tasks.append(gen(f"[{c['id']}] Lifestyle", c["speech_lifestyle"], "sec_lifestyle"))
        tasks.append(gen(f"[{c['id']}] Pariharam", c["speech_pariharam"], "sec_pariharam"))

    await asyncio.gather(*tasks)
    print("All career audios generated successfully!")

async def main():
    await generate_scan_clips()
    await generate_career_audios()
    print("ALL AUDIO PRE-CACHING COMPLETE!")

if __name__ == "__main__":
    asyncio.run(main())
