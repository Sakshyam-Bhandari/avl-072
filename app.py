# app.py (Flask minimal)
from flask import Flask, request, render_template_string, jsonify
import os, openai

openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

FORM_HTML = """
<!doctype html>
<title>Apply Assistant - Demo</title>
<h2>Apply Assistant — preview</h2>
<form id="genForm">
  <label>Job description or link (paste):</label><br>
  <textarea id="job" name="job" rows="8" cols="80"></textarea><br>
  <label>Your 3-line profile (role / top skill / experience):</label><br>
  <input id="profile" name="profile" style="width:80%"><br><br>
  <button type="button" onclick="generate()">Generate proposals</button>
</form>
<pre id="out"></pre>
<script>
async function generate(){
  document.getElementById('out').textContent = 'Generating...';
  const job = document.getElementById('job').value;
  const profile = document.getElementById('profile').value;
  const resp = await fetch('/api/generate', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({job,profile})
  });
  const data = await resp.json();
  document.getElementById('out').textContent = data.text;
}
</script>
"""

PROMPT = """
You are a senior freelance proposal writer. Given JOB and PROFILE, produce:
HOOK (8-12 words)
PROPOSAL A (short 2-3 sentences)
PROPOSAL B (medium 4-6 sentences)
PROPOSAL C (detailed 6-10 sentences + first-step)
BID SUGGESTION (range + one-line reason)
FOLLOW-UPS (3 short templates)
Return as plain text sections.
Job: {job}
Profile: {profile}
"""

@app.route('/')
def index():
    return render_template_string(FORM_HTML)

@app.route('/api/generate', methods=['POST'])
def gen():
    data = request.json
    job = data.get('job','')
    profile = data.get('profile','')
    message = PROMPT.format(job=job, profile=profile)
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":message}],
        temperature=0.0,
        max_tokens=700
    )
    text = resp['choices'][0]['message']['content']
    return jsonify({'text': text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
