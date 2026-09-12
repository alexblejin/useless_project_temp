# -*- coding: utf-8 -*-
"""
Builds the standalone, 100% static, GitHub Pages-compatible version of ജാതകംGPT.
Embeds all 16 satirical careers, multi-foretellings, and pre-computed audio URLs into app.js.
Ensures relative paths work seamlessly on GitHub Pages, local FastAPI, or raw file serving.
"""
import os
import json
import hashlib
import shutil
from predictions import CAREER_PREDICTIONS

BASE_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE_DIR, "static")
AUDIO_CACHE_DIR = os.path.join(STATIC_DIR, "audio_cache")

def build_client_predictions():
    client_data = []
    for c in CAREER_PREDICTIONS:
        full_h = hashlib.md5(c["full_speech"].strip().encode("utf-8")).hexdigest()
        full_audio = f"./static/audio_cache/biju_{full_h}.mp3"

        sections_map = {
            "career": ("sec_career", c.get("speech_career", c.get("stage3"))),
            "love": ("sec_love", c.get("speech_love", c.get("love_life"))),
            "wealth": ("sec_wealth", c.get("speech_wealth", c.get("wealth"))),
            "lifestyle": ("sec_lifestyle", c.get("speech_lifestyle", c.get("lifestyle"))),
            "pariharam": ("sec_pariharam", c.get("speech_pariharam", c.get("pariharam")))
        }

        sec_audios = {}
        for sec_key, (prefix, text) in sections_map.items():
            if text:
                h = hashlib.md5(text.strip().encode("utf-8")).hexdigest()
                sec_audios[sec_key] = f"./static/audio_cache/{prefix}_{h}.mp3"
            else:
                sec_audios[sec_key] = None

        client_data.append({
            "id": c["id"],
            "title": c["title"],
            "title_ml": c["title_ml"],
            "emoji": c["emoji"],
            "stage1": c["stage1"],
            "stage2": c["stage2"],
            "stage3": c["stage3"],
            "punchline": c["punchline"],
            "career_reading": c.get("career_reading", c.get("stage3")),
            "love_life": c.get("love_life"),
            "wealth": c.get("wealth"),
            "lifestyle": c.get("lifestyle"),
            "pariharam": c.get("pariharam"),
            "full_speech": c["full_speech"],
            "speech_career": c.get("speech_career"),
            "speech_love": c.get("speech_love"),
            "speech_wealth": c.get("speech_wealth"),
            "speech_lifestyle": c.get("speech_lifestyle"),
            "speech_pariharam": c.get("speech_pariharam"),
            "audio_url": full_audio,
            "section_audios": sec_audios
        })
    return client_data

def generate_static_app_js(client_careers):
    careers_json = json.dumps(client_careers, ensure_ascii=False, indent=2)

    js_template = f"""// ജാതകംGPT — Front-end Application Logic v2.5 (100% Static & GitHub Pages Compatible)
// Brahmasree Biju — AI ജ്യോത്സ്യൻ

let currentStream = null;
let faceDetector = null;
let cameraHelper = null;
let isScanning = false;
let faceDetected = false;
let scanStartTime = null;
let scanPhaseIndex = 0;
let currentPrediction = null;
let isMuted = false;
let currentFacingMode = 'user';
let lastDetectedSignal = 'neutral';
let activePlayingCard = null;

// Embedded Full 16 Careers Client Database
const ALL_CAREER_PREDICTIONS = {careers_json};

// Live Scanning Audio Clips
const SCAN_AUDIO_FILES = {{
  intro: {{
    url: "./static/audio_cache/scan_step1.mp3",
    text: "ങ്ഹാ... ശിവ ശംഭോ... ക്യാമറയിലേക്ക് നേരെ നോക്ക് കുട്ടാ... കണ്ണടയുടെ മുകളിലൂടെ ഞാൻ നോക്കുകയാണ്... സാമുദ്രിക മുഖലക്ഷണം ഞാൻ പരിശോധിക്കട്ടെ...",
    emoji: "🧙‍♂️"
  }},
  smiling: {{
    url: "./static/audio_cache/scan_smiling.mp3",
    text: "ഹും... ചുണ്ടിൽ ഒരു കള്ളച്ചിരി വിരിയുന്നുണ്ടല്ലോ! എന്തോ വലിയ അടവ് മനസ്സിൽ വെച്ചാണ് നിൽപ്പ്... നെറ്റിയിലെ രേഖകൾ വ്യക്തമായി!",
    emoji: "😏"
  }},
  tilted: {{
    url: "./static/audio_cache/scan_tilted.mp3",
    text: "തലയൊന്ന് ചരിച്ചു നോക്കുന്നുണ്ട്... എന്തൊരു സംശയം! ഗ്രഹനിലയിലെ സംശയരോഗം ബിജു വ്യക്തമായി വായിച്ചെടുത്തിരിക്കുന്നു...",
    emoji: "🧐"
  }},
  serious: {{
    url: "./static/audio_cache/scan_serious.mp3",
    text: "നെറ്റിയിലെ വരകൾ നോക്കട്ടെ... ശ്ശെടാ! ഇതെന്തൊരു ഗൗരവമാണിത്! രാഹുവും ശനിയും കൂടി തലയ്ക്ക് മീതെ കയറിയിരുന്ന് ചിന്തിക്കുകയാണല്ലോ!",
    emoji: "📐"
  }},
  math: {{
    url: "./static/audio_cache/scan_step3.mp3",
    text: "അയ്യയ്യോ... കണ്ടോ കണ്ടോ! അഷ്ടമത്തിലെ വ്യാഴവും പത്താം ഭാവത്തിലെ ചൊവ്വയും! നിന്റെ സകല ജാതക രഹസ്യങ്ങളും ഞാൻ ഇതാ തുറക്കുകയാണ്... കേട്ടോ!",
    emoji: "⚡"
  }},
  verdict: {{
    url: "./static/audio_cache/scan_step4.mp3",
    text: "ഗ്രഹങ്ങളെല്ലാം ഒന്നിച്ചു നിരന്നു! നിന്റെ അന്തിമ വിധി ഇതാ വരുന്നു... കണ്ണു തുറന്നു കേട്ടോ കുട്ടാ!",
    emoji: "🔥"
  }}
}};

// Audio Synth via Web Audio API for Retro Astrological Sound Effects
let audioCtx = null;
function getAudioContext() {{
  if (!audioCtx) {{
    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  }}
  return audioCtx;
}}

function playScanPulse() {{
  if (isMuted) return;
  try {{
    const ctx = getAudioContext();
    if (ctx.state === 'suspended') ctx.resume();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(540, ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(880, ctx.currentTime + 0.12);
    gain.gain.setValueAtTime(0.03, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.12);
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start();
    osc.stop(ctx.currentTime + 0.12);
  }} catch(e) {{}}
}}

function playRevealSound() {{
  if (isMuted) return;
  try {{
    const ctx = getAudioContext();
    if (ctx.state === 'suspended') ctx.resume();
    [523.25, 659.25, 783.99, 1046.50].forEach((freq, i) => {{
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(freq, ctx.currentTime + i * 0.08);
      gain.gain.setValueAtTime(0.08, ctx.currentTime + i * 0.08);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + i * 0.08 + 0.6);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start(ctx.currentTime + i * 0.08);
      osc.stop(ctx.currentTime + i * 0.08 + 0.6);
    }});
  }} catch(e) {{}}
}}

// DOM Elements
const screenLanding = document.getElementById('screenLanding');
const screenScanner = document.getElementById('screenScanner');
const screenResult = document.getElementById('screenResult');

const startBtn = document.getElementById('startBtn');
const cancelScanBtn = document.getElementById('cancelScanBtn');
const retryBtn = document.getElementById('retryBtn');
const newScanBtn = document.getElementById('newScanBtn');
const replayVoiceBtn = document.getElementById('replayVoiceBtn');
const soundToggleBtn = document.getElementById('soundToggleBtn');
const flipCamBtn = document.getElementById('flipCamBtn');
const shareBtn = document.getElementById('shareBtn');
const shareBtnText = document.getElementById('shareBtnText');

const videoElement = document.getElementById('webcam');
const canvasElement = document.getElementById('faceCanvas');
const canvasCtx = canvasElement.getContext('2d');

const camPlaceholder = document.getElementById('camPlaceholder');
const camStatusText = document.getElementById('camStatusText');
const scannerStatusMessage = document.getElementById('scannerStatusMessage');
const bijuEmoji = document.getElementById('bijuEmoji');
const voiceWaveIndicator = document.getElementById('voiceWaveIndicator');
const scannerLaser = document.getElementById('scannerLaser');
const scanSignalMeter = document.getElementById('scanSignalMeter');

const bijuAudio = document.getElementById('bijuAudio');
const bijuScanAudio = document.getElementById('bijuScanAudio');
const audioStatusBox = document.getElementById('audioStatusBox');
const audioStatusText = document.getElementById('audioStatusText');
const audioPlayingIcon = document.getElementById('audioPlayingIcon');

// Result Screen DOM Elements
const resultCareerTitle = document.getElementById('resultCareerTitle');
const resultPunchline = document.getElementById('resultPunchline');
const resultCareerReading = document.getElementById('resultCareerReading');
const resultLoveLife = document.getElementById('resultLoveLife');
const resultWealth = document.getElementById('resultWealth');
const resultLifestyle = document.getElementById('resultLifestyle');
const resultPariharam = document.getElementById('resultPariharam');

// Card DOM Mapping for Real-Time Highlighting
const FORETELLING_CARDS = {{
  career: document.getElementById('cardCareer'),
  love: document.getElementById('cardLove'),
  wealth: document.getElementById('cardWealth'),
  lifestyle: document.getElementById('cardLifestyle'),
  pariharam: document.getElementById('cardPariharam')
}};

// Screen Navigation
function showScreen(screen) {{
  screenLanding.classList.add('hidden');
  screenScanner.classList.add('hidden');
  screenResult.classList.add('hidden');

  if (screen === 'landing') {{
    stopCamera();
    stopAudio();
    screenLanding.classList.remove('hidden');
  }} else if (screen === 'scanner') {{
    stopAudio();
    screenScanner.classList.remove('hidden');
    initFaceScanner();
  }} else if (screen === 'result') {{
    stopCamera();
    stopScanAudio();
    screenResult.classList.remove('hidden');
    playRevealSound();
  }}
}}

// Camera & Scanner Initialization
async function initFaceScanner() {{
  resetScanState();
  camPlaceholder.classList.remove('hidden');
  camStatusText.textContent = "ക്യാമറ ആരംഭിക്കുന്നു...";
  scannerStatusMessage.textContent = "ക്യാമറയിലേക്ക് നോക്കൂ... ബിജു സംസാരിച്ചു തുടങ്ങും...";
  bijuEmoji.textContent = "🧙‍♂️";
  voiceWaveIndicator.classList.add('hidden');

  try {{
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {{
      throw new Error("ക്യാമറ ലഭ്യമല്ല.");
    }}

    const constraints = {{
      video: {{
        facingMode: currentFacingMode,
        width: {{ ideal: 640 }},
        height: {{ ideal: 480 }}
      }},
      audio: false
    }};

    const stream = await navigator.mediaDevices.getUserMedia(constraints);
    currentStream = stream;
    videoElement.srcObject = stream;

    if (currentFacingMode === 'user') {{
      videoElement.classList.add('scale-x-[-1]');
      canvasElement.classList.add('scale-x-[-1]');
    }} else {{
      videoElement.classList.remove('scale-x-[-1]');
      canvasElement.classList.remove('scale-x-[-1]');
    }}

    videoElement.onloadedmetadata = () => {{
      videoElement.play();
      canvasElement.width = videoElement.videoWidth || 640;
      canvasElement.height = videoElement.videoHeight || 480;
      camPlaceholder.classList.add('hidden');
      scannerLaser.classList.remove('hidden');
      setupMediaPipe();
    }};

  }} catch (err) {{
    console.warn("ക്യാമറ തകരാർ:", err);
    handleCameraError(err);
  }}
}}

// MediaPipe Setup
function setupMediaPipe() {{
  if (typeof FaceDetection !== 'undefined') {{
    try {{
      faceDetector = new FaceDetection({{
        locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/face_detection/${{file}}`
      }});

      faceDetector.setOptions({{
        model: 'short',
        minDetectionConfidence: 0.5
      }});

      faceDetector.onResults(onFaceDetectionResults);

      if (typeof Camera !== 'undefined') {{
        cameraHelper = new Camera(videoElement, {{
          onFrame: async () => {{
            if (isScanning && videoElement.videoWidth) {{
              await faceDetector.send({{ image: videoElement }});
            }}
          }},
          width: 640,
          height: 480
        }});
        cameraHelper.start();
        isScanning = true;
        return;
      }}
    }} catch (e) {{
      console.warn("MediaPipe load error:", e);
    }}
  }}

  startFallbackDetectionLoop();
}}

function onFaceDetectionResults(results) {{
  if (!isScanning) return;

  canvasCtx.save();
  canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);

  if (results.detections && results.detections.length > 0) {{
    const detection = results.detections[0];
    faceDetected = true;
    scanSignalMeter.textContent = "SIG: 99% (LOCKED)";
    scanSignalMeter.className = "text-green-400 font-mono text-xs";

    // Extract harmless facial cues from landmarks
    if (detection.landmarks && detection.landmarks.length >= 4) {{
      const leftEye = detection.landmarks[0];
      const rightEye = detection.landmarks[1];
      const noseTip = detection.landmarks[2];
      const mouthCenter = detection.landmarks[3];

      const dy = Math.abs(leftEye.y - rightEye.y);
      if (dy > 0.05) {{
        lastDetectedSignal = 'tilted';
      }} else if (mouthCenter.y - noseTip.y > 0.12) {{
        lastDetectedSignal = 'smiling';
      }} else {{
        lastDetectedSignal = 'serious';
      }}
    }}

    drawAstrologyHUD(detection);
    handleLiveVoiceScanningFlow();
  }} else {{
    faceDetected = false;
    scanSignalMeter.textContent = "SIG: SEARCHING...";
    scanSignalMeter.className = "text-brandYellow font-mono text-xs";
    if (!scanStartTime) {{
      scannerStatusMessage.textContent = "മുഖം കണ്ടെത്താനായില്ല... ക്യാമറയിലേക്ക് നേരെ നോക്കൂ...";
      bijuEmoji.textContent = "👀";
      voiceWaveIndicator.classList.add('hidden');
    }}
  }}

  canvasCtx.restore();
}}

function drawAstrologyHUD(detection) {{
  const box = detection.boundingBox;
  const w = canvasElement.width;
  const h = canvasElement.height;

  const x = box.xCenter * w - (box.width * w) / 2;
  const y = box.yCenter * h - (box.height * h) / 2;
  const width = box.width * w;
  const height = box.height * h;

  // Outer Reticle Box
  canvasCtx.strokeStyle = '#FFE600';
  canvasCtx.lineWidth = 3;
  canvasCtx.strokeRect(x, y, width, height);

  // Decorative Corner brackets
  const cornerSize = 18;
  canvasCtx.strokeStyle = '#FF5C00';
  canvasCtx.lineWidth = 4;

  canvasCtx.beginPath();
  canvasCtx.moveTo(x, y + cornerSize);
  canvasCtx.lineTo(x, y);
  canvasCtx.lineTo(x + cornerSize, y);
  canvasCtx.stroke();

  canvasCtx.beginPath();
  canvasCtx.moveTo(x + width - cornerSize, y);
  canvasCtx.lineTo(x + width, y);
  canvasCtx.lineTo(x + width, y + cornerSize);
  canvasCtx.stroke();

  canvasCtx.beginPath();
  canvasCtx.moveTo(x, y + height - cornerSize);
  canvasCtx.lineTo(x, y + height);
  canvasCtx.lineTo(x + cornerSize, y + height);
  canvasCtx.stroke();

  canvasCtx.beginPath();
  canvasCtx.moveTo(x + width - cornerSize, y + height);
  canvasCtx.lineTo(x + width, y + height);
  canvasCtx.lineTo(x + width, y + height - cornerSize);
  canvasCtx.stroke();

  // Forehead Chakra Point
  const foreheadX = x + width / 2;
  const foreheadY = y + height * 0.22;
  canvasCtx.beginPath();
  canvasCtx.arc(foreheadX, foreheadY, 6, 0, 2 * Math.PI);
  canvasCtx.fillStyle = '#FF5C00';
  canvasCtx.fill();
  canvasCtx.strokeStyle = '#FFFFFF';
  canvasCtx.lineWidth = 2;
  canvasCtx.stroke();

  // Chakra label
  canvasCtx.fillStyle = '#FFE600';
  canvasCtx.font = 'bold 12px "Space Grotesk", sans-serif';
  canvasCtx.fillText("CHAKRA // LOCK", foreheadX + 10, foreheadY + 4);
}}

// Audio Playback with Resilient Path Fallback (Supports GitHub Pages & Static Hosts)
function playAudioWithFallback(audioEl, primaryUrl, fallbackText, onEnded) {{
  if (isMuted) {{
    if (onEnded) onEnded();
    return;
  }}

  const cleanUrl = primaryUrl.replace(/^\\/+/, '');
  const attempts = [
    cleanUrl,
    './' + cleanUrl,
    './static/' + cleanUrl.replace(/^static\\//, ''),
    './audio_cache/' + cleanUrl.replace(/^.*?audio_cache\\//, '')
  ];

  let currentIdx = 0;

  function tryPlay() {{
    if (currentIdx < attempts.length) {{
      const candidateUrl = attempts[currentIdx++];
      audioEl.src = candidateUrl;
      audioEl.play().catch(e => {{
        tryPlay();
      }});
    }} else {{
      if (fallbackText) {{
        tryWebSpeech(fallbackText, onEnded);
      }} else if (onEnded) {{
        onEnded();
      }}
    }}
  }}

  audioEl.onended = () => {{
    if (onEnded) onEnded();
  }};

  tryPlay();
}}

// Live Voice Scanning Steps
function getScanSteps() {{
  let inferStep = SCAN_AUDIO_FILES.serious;
  if (lastDetectedSignal === 'smiling') {{
    inferStep = SCAN_AUDIO_FILES.smiling;
  }} else if (lastDetectedSignal === 'tilted') {{
    inferStep = SCAN_AUDIO_FILES.tilted;
  }}

  return [
    SCAN_AUDIO_FILES.intro,
    inferStep,
    SCAN_AUDIO_FILES.math,
    SCAN_AUDIO_FILES.verdict
  ];
}}

function handleLiveVoiceScanningFlow() {{
  if (!scanStartTime) {{
    scanStartTime = Date.now();
    scanPhaseIndex = 0;
    playNextScanningStepAudio();
  }}
}}

function playNextScanningStepAudio() {{
  const steps = getScanSteps();
  if (scanPhaseIndex >= steps.length) {{
    finishScanningAndFetchResult();
    return;
  }}

  const step = steps[scanPhaseIndex];
  scannerStatusMessage.textContent = step.text;
  bijuEmoji.textContent = step.emoji;
  voiceWaveIndicator.classList.remove('hidden');
  playScanPulse();

  playAudioWithFallback(bijuScanAudio, step.url, step.text, () => {{
    scanPhaseIndex++;
    playNextScanningStepAudio();
  }});
}}

function stopScanAudio() {{
  if (bijuScanAudio) {{
    bijuScanAudio.pause();
    bijuScanAudio.currentTime = 0;
  }}
  voiceWaveIndicator.classList.add('hidden');
}}

// Client-Side Astrological Selector (100% Offline / GitHub Pages Safe)
function getClientPrediction(signal) {{
  if (signal === 'smiling') {{
    const cands = ALL_CAREER_PREDICTIONS.filter(p => ['troll_admin', 'startup_ceo', 'software_engineer', 'food_vlogger', 'kalyana_broker'].includes(p.id));
    if (cands.length) return cands[Math.floor(Math.random() * cands.length)];
  }} else if (signal === 'tilted') {{
    const cands = ALL_CAREER_PREDICTIONS.filter(p => ['autorickshaw_pilot', 'lawyer', 'crypto_trader', 'uiux_designer'].includes(p.id));
    if (cands.length) return cands[Math.floor(Math.random() * cands.length)];
  }} else if (signal === 'serious') {{
    const cands = ALL_CAREER_PREDICTIONS.filter(p => ['govt_officer', 'doctor', 'gulf_uncle', 'psc_aspirant', 'master_chef'].includes(p.id));
    if (cands.length) return cands[Math.floor(Math.random() * cands.length)];
  }}
  return ALL_CAREER_PREDICTIONS[Math.floor(Math.random() * ALL_CAREER_PREDICTIONS.length)];
}}

// Finish scanning sequence and present prediction
async function finishScanningAndFetchResult() {{
  isScanning = false;
  stopScanAudio();
  scannerStatusMessage.textContent = "ഗ്രഹങ്ങൾ വെളിപ്പെട്ടു! വിധി വരുന്നു...";
  bijuEmoji.textContent = "⚡";

  // Try API first (works when running locally with FastAPI), fallback to client dataset (works on GitHub Pages!)
  try {{
    const res = await fetch('/api/predict', {{
      method: 'POST',
      headers: {{ 'Content-Type': 'application/json' }},
      body: JSON.stringify({{ harmless_signal: lastDetectedSignal }})
    }});
    if (!res.ok) throw new Error("API not available");
    currentPrediction = await res.json();
  }} catch (err) {{
    console.log("Using static client prediction engine (GitHub Pages mode)");
    currentPrediction = getClientPrediction(lastDetectedSignal);
  }}

  displayResult(currentPrediction);
}}

// Render Result Screen with All 5 Multi-Foretellings
function displayResult(pred) {{
  resultCareerTitle.textContent = `${{pred.emoji}} ${{pred.title}}`;
  resultPunchline.textContent = `“${{pred.punchline}}”`;
  resultCareerReading.textContent = pred.career_reading || pred.stage3 || "ഓഫീസിൽ ലാപ്ടോപ്പ് തുറന്നുവെച്ച് മീറ്റിംഗുകളിൽ ഒളിച്ചിരിക്കാനുള്ള ജന്മവാസന കാണുന്നുണ്ട്!";
  resultLoveLife.textContent = pred.love_life || "പ്രണയത്തിൽ വലിയ ദോഷങ്ങൾ കാണുന്നില്ല!";
  resultWealth.textContent = pred.wealth || "കയ്യിൽ കാശ് വന്ന വഴി അറിയില്ല!";
  resultLifestyle.textContent = pred.lifestyle || "ഉറക്കക്കുറവ് കട്ടക്ക് തുടരും!";
  resultPariharam.textContent = pred.pariharam || "പ്രത്യേകിച്ച് ഒരു പരിഹാരവുമില്ല. ദൈവം സഹായിക്കട്ടെ!";

  showScreen('result');
  playVoice(pred);
}}

// Play Final Satirical Reading Voice
function playVoice(pred) {{
  if (isMuted) return;

  clearActiveCardHighlight();
  audioStatusBox.classList.remove('hidden');
  audioStatusText.textContent = "ബിജു മുഴുവൻ ജാതകവും വായിക്കുന്നു...";
  audioPlayingIcon.classList.add('animate-pulse');

  playAudioWithFallback(bijuAudio, pred.audio_url, pred.full_speech, () => {{
    audioStatusText.textContent = "ജാതക വായന പൂർത്തിയായി. ഏത് ഭാഗവും വീണ്ടും കേൾക്കാം!";
    audioPlayingIcon.classList.remove('animate-pulse');
    clearActiveCardHighlight();
  }});
}}

// ON-DEMAND INDIVIDUAL SECTION AUDIO PLAYBACK
window.readSingleSection = function(sectionKey) {{
  if (isMuted) {{
    alert("ശബ്ദം മ്യൂട്ട് ചെയ്തിരിക്കുകയാണ്. മുകളിലെ സ്പീക്കർ ബട്ടൺ അമർത്തുക.");
    return;
  }}
  if (!currentPrediction) return;

  stopAudio();
  highlightActiveCard(sectionKey);

  audioStatusBox.classList.remove('hidden');
  audioPlayingIcon.classList.add('animate-pulse');

  const titlesMap = {{
    career: "കരിയർ ജാതകം",
    love: "പ്രണയ ജാതകം",
    wealth: "ധനയോഗം",
    lifestyle: "ജീവിതശൈലി",
    pariharam: "ബിജുവിന്റെ പരിഹാരം"
  }};
  audioStatusText.textContent = `ബിജു ${{titlesMap[sectionKey] || 'ഫലം'}} വായിക്കുന്നു...`;

  const audioUrl = currentPrediction.section_audios && currentPrediction.section_audios[sectionKey];
  const textMap = {{
    career: currentPrediction.speech_career || currentPrediction.career_reading,
    love: currentPrediction.speech_love || currentPrediction.love_life,
    wealth: currentPrediction.speech_wealth || currentPrediction.wealth,
    lifestyle: currentPrediction.speech_lifestyle || currentPrediction.lifestyle,
    pariharam: currentPrediction.speech_pariharam || currentPrediction.pariharam
  }};
  const textToSpeak = textMap[sectionKey] || currentPrediction.full_speech;

  playAudioWithFallback(bijuAudio, audioUrl || '', textToSpeak, () => {{
    audioStatusText.textContent = "വായന പൂർത്തിയായി.";
    audioPlayingIcon.classList.remove('animate-pulse');
    clearActiveCardHighlight();
  }});
}};

function highlightActiveCard(sectionKey) {{
  clearActiveCardHighlight();
  const card = FORETELLING_CARDS[sectionKey];
  if (card) {{
    card.classList.add('ring-4', 'ring-brandOrange', 'scale-[1.01]');
    activePlayingCard = card;
  }}
}}

function clearActiveCardHighlight() {{
  if (activePlayingCard) {{
    activePlayingCard.classList.remove('ring-4', 'ring-brandOrange', 'scale-[1.01]');
    activePlayingCard = null;
  }}
}}

function stopAudio() {{
  stopScanAudio();
  if (bijuAudio) {{
    bijuAudio.pause();
    bijuAudio.currentTime = 0;
  }}
  if ('speechSynthesis' in window) {{
    window.speechSynthesis.cancel();
  }}
  clearActiveCardHighlight();
}}

function tryWebSpeech(text, onEnded) {{
  if ('speechSynthesis' in window) {{
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'ml-IN';
    utterance.rate = 0.92;
    if (onEnded) {{
      utterance.onend = onEnded;
      utterance.onerror = onEnded;
    }}
    window.speechSynthesis.speak(utterance);
    audioStatusText.textContent = "ബിജു സംസാരിക്കുന്നു (Web Speech)...";
  }} else if (onEnded) {{
    onEnded();
  }}
}}

// Fallback Simulation Loop if camera is denied
function startFallbackDetectionLoop() {{
  isScanning = true;
  scanStartTime = Date.now();
  scanPhaseIndex = 0;
  playNextScanningStepAudio();
}}

function resetScanState() {{
  isScanning = true;
  faceDetected = false;
  scanStartTime = null;
  scanPhaseIndex = 0;
  lastDetectedSignal = 'neutral';
  stopScanAudio();
  clearActiveCardHighlight();
  if (canvasCtx) canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
}}

function stopCamera() {{
  isScanning = false;
  stopScanAudio();

  if (cameraHelper) {{
    try {{ cameraHelper.stop(); }} catch(e) {{}}
    cameraHelper = null;
  }}
  if (currentStream) {{
    currentStream.getTracks().forEach(track => track.stop());
    currentStream = null;
  }}
  if (videoElement) {{
    videoElement.srcObject = null;
  }}
  scannerLaser.classList.add('hidden');
}}

function handleCameraError(err) {{
  camPlaceholder.classList.remove('hidden');
  scannerLaser.classList.add('hidden');

  let errorMsg = "ക്യാമറ അനുമതി ലഭിച്ചില്ല. ദയവായി ക്യാമറ അനുമതി നൽകുക.";
  if (err.name === 'NotFoundError' || err.name === 'DevicesNotFoundError') {{
    errorMsg = "ക്യാമറ കണ്ടെത്താനായില്ല. ഒരു വെബ്‌ക്യാം ഘടിപ്പിച്ചിട്ടുണ്ടെന്ന് ഉറപ്പാക്കുക.";
  }} else if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {{
    errorMsg = "ക്യാമറ അനുമതി നിരസിക്കപ്പെട്ടു. ബ്രൗസറിന്റെ ക്രമീകരണങ്ങളിൽ അനുമതി നൽകുക.";
  }}

  camStatusText.innerHTML = `
    <span class="text-red-400 font-bold block mb-1">⚠️ ക്യാമറ പ്രവർത്തിക്കുന്നില്ല</span>
    <span class="text-xs text-gray-300 block mb-3">${{errorMsg}}</span>
    <button onclick="startSimulationMode()" class="px-3 py-1.5 bg-brandYellow text-black font-bold text-xs rounded-lg border border-black shadow-brutal-sm hover:bg-yellow-400 cursor-pointer">
      🔮 ക്യാമറ ഇല്ലാതെ ഡെമോ തുടരുക
    </button>
  `;
}}

window.startSimulationMode = function() {{
  camPlaceholder.classList.add('hidden');
  scannerLaser.classList.remove('hidden');
  resetScanState();
  startFallbackDetectionLoop();
}};

// UI Event Listeners
startBtn.addEventListener('click', () => showScreen('scanner'));
cancelScanBtn.addEventListener('click', () => showScreen('landing'));
retryBtn.addEventListener('click', () => showScreen('scanner'));
newScanBtn.addEventListener('click', () => showScreen('landing'));

flipCamBtn.addEventListener('click', () => {{
  currentFacingMode = (currentFacingMode === 'user') ? 'environment' : 'user';
  stopCamera();
  initFaceScanner();
}});

replayVoiceBtn.addEventListener('click', () => {{
  if (currentPrediction) {{
    playVoice(currentPrediction);
  }}
}});

shareBtn.addEventListener('click', () => {{
  if (!currentPrediction) return;
  const shareText = `🔮 ജാതകംGPT — ബ്രഹ്മശ്രീ ബിജുവിന്റെ ജാതകം!\\n` +
    `👨‍💻 തൊഴിൽ: ${{currentPrediction.emoji}} ${{currentPrediction.title}}\\n` +
    `💥 അന്തിമ വിധി: ${{currentPrediction.punchline}}\\n` +
    `💼 കരിയർ: ${{currentPrediction.career_reading || currentPrediction.stage3}}\\n` +
    `💘 പ്രണയം: ${{currentPrediction.love_life}}\\n` +
    `💰 ധനയോഗം: ${{currentPrediction.wealth}}\\n` +
    `🍕 ജീവിതശൈലി: ${{currentPrediction.lifestyle}}\\n` +
    `🧘‍♂️ പരിഹാരം: ${{currentPrediction.pariharam}}\\n` +
    `👉 നിങ്ങളും നോക്കൂ: ${{window.location.origin}}`;

  if (navigator.clipboard) {{
    navigator.clipboard.writeText(shareText).then(() => {{
      shareBtnText.textContent = "✓ കോപ്പി ചെയ്തു! (Copied!)";
      setTimeout(() => {{
        shareBtnText.textContent = "ജാതക ഫലം കോപ്പി ചെയ്യുക / Share";
      }}, 2500);
    }}).catch(() => {{
      prompt("നിങ്ങളുടെ ജാതകം കോപ്പി ചെയ്യുക:", shareText);
    }});
  }} else {{
    prompt("നിങ്ങളുടെ ജാതകം കോപ്പി ചെയ്യുക:", shareText);
  }}
}});

soundToggleBtn.addEventListener('click', () => {{
  isMuted = !isMuted;
  if (isMuted) {{
    soundToggleBtn.innerHTML = '<span>🔇</span>';
    soundToggleBtn.title = 'ശബ്ദം Off';
    stopAudio();
  }} else {{
    soundToggleBtn.innerHTML = '<span>🔊</span>';
    soundToggleBtn.title = 'ശബ്ദം On';
  }}
}});

console.log("ജാതകംGPT 2.5: GitHub Pages & Static Hosting Ready!");
"""
    return js_template

def main():
    print("Building client-side prediction dataset...")
    client_careers = build_client_predictions()
    print(f"Loaded {len(client_careers)} careers with full multi-foretellings & pre-rendered audio maps.")

    print("Generating standalone static app.js...")
    app_js_content = generate_static_app_js(client_careers)

    # Write app.js to root and static/
    root_app_js = os.path.join(BASE_DIR, "app.js")
    static_app_js = os.path.join(STATIC_DIR, "app.js")

    with open(root_app_js, "w", encoding="utf-8") as f:
        f.write(app_js_content)
    with open(static_app_js, "w", encoding="utf-8") as f:
        f.write(app_js_content)
    print("Saved app.js to project root and static/app.js")

    # Read static/index.html and update script tag
    static_index_path = os.path.join(STATIC_DIR, "index.html")
    with open(static_index_path, "r", encoding="utf-8") as f:
        index_html = f.read()

    # Replace absolute script with relative script
    index_html = index_html.replace('<script src="/static/app.js"></script>', '<script src="./app.js" onerror="this.onerror=null;this.src=\'./static/app.js\'"></script>')

    # Write index.html to root and static/
    root_index_path = os.path.join(BASE_DIR, "index.html")
    with open(root_index_path, "w", encoding="utf-8") as f:
        f.write(index_html)
    with open(static_index_path, "w", encoding="utf-8") as f:
        f.write(index_html)
    print("Saved index.html to project root and static/index.html")

    # Mirror audio_cache to root audio_cache if needed
    root_audio_cache = os.path.join(BASE_DIR, "audio_cache")
    if not os.path.exists(root_audio_cache):
        try:
            # On windows, copy or make directory
            os.makedirs(root_audio_cache, exist_ok=True)
            for item in os.listdir(AUDIO_CACHE_DIR):
                s = os.path.join(AUDIO_CACHE_DIR, item)
                d = os.path.join(root_audio_cache, item)
                if os.path.isfile(s):
                    shutil.copy2(s, d)
            print("Mirrored audio_cache to project root.")
        except Exception as e:
            print("Note on audio_cache copy:", e)

    print("\nSUCCESS! Static export build complete.")

if __name__ == "__main__":
    main()
