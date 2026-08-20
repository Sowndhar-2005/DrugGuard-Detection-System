"""
test_system.py
DrugGuard — Integration & Inference Test Script

This script sends requests to the local running FastAPI server
to verify that DistilBERT, MobileNetV2, and OCR models are fully integrated and working.

Run:
    py -3 test_system.py
"""

import urllib.request
import json
import base64

SERVER_URL = "http://localhost:8000"

def test_endpoint(path, payload):
    url = f"{SERVER_URL}{path}"
    headers = {"Content-Type": "application/json"}
    data = json.dumps(payload).encode("utf-8")
    
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            res_data = response.read().decode("utf-8")
            return json.loads(res_data)
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        print(f"❌ Request to {path} failed: {e} | Detail: {err_body}")
        return None
    except Exception as e:
        print(f"❌ Request to {path} failed: {e}")
        return None

def test_health():
    url = f"{SERVER_URL}/health"
    try:
        with urllib.request.urlopen(url) as response:
            res_data = response.read().decode("utf-8")
            return json.loads(res_data)
    except Exception as e:
        print(f"❌ Health check failed (Is the server running?): {e}")
        return None

def main():
    print("="*60)
    print("🔬 DrugGuard System Integration Tests")
    print("="*60)
    
    # 1. Health Check
    health = test_health()
    if not health:
        print("Aborting tests because server is not running.")
        return
        
    print("\n[1] Server Health Status:")
    print(f"  - Status:      {health.get('status')}")
    print(f"  - Text Model:  {health.get('text_model')}")
    print(f"  - Image Model: {health.get('image_model')}")
    print(f"  - OCR Engine:  {health.get('ocr_engine')}")
    
    # 2. Text predictions
    print("\n[2] Testing Text Classifier (/predict):")
    
    # Safe text
    safe_res = test_endpoint("/predict", {"text": "I am feeling sick, so the doctor prescribed ibuprofen."})
    if safe_res:
        status = "✅ PASS" if safe_res["action"] == "safe" else "❌ FAIL"
        print(f"  - Safe Text Sample 1:  [{status}] Action: {safe_res['action']} (Score: {safe_res['risk_score']})")
        
    # FDA Safe text
    fda_res = test_endpoint("/predict", {"text": "The FDA approved a new medication to help treat patients suffering from chronic hypertension and migraines. Ensure you consult with your doctor before altering your dosage."})
    if fda_res:
        status = "✅ PASS" if fda_res["action"] == "safe" else "❌ FAIL"
        print(f"  - Safe Text Sample 2 (FDA): [{status}] Action: {fda_res['action']} (Score: {fda_res['risk_score']})")
        
    # Obfuscated drug text
    drug_res = test_endpoint("/predict", {"text": "🔌 got premium ❄️ and 🍃 ready for drop tonight, cash or btc."})
    if drug_res:
        status = "✅ PASS" if drug_res["action"] == "block" else "❌ FAIL"
        print(f"  - Drug Text Sample:  [{status}] Action: {drug_res['action']} (Score: {drug_res['risk_score']})")
        print(f"    Triggered words: {drug_res['triggered_words']}")

    # 3. Image predictions
    print("\n[3] Testing Image Classifier (/predict_image):")
    
    # Send a tiny blank image in base64 (simulate image transmission)
    tiny_img = (
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
    )
    
    img_res = test_endpoint("/predict_image", {"image": tiny_img})
    if img_res:
        print(f"  - Image Scan Sample: ✅ OK (Action: {img_res['action']}, Score: {img_res['risk_score']})")
        print(f"    Triggered words (OCR): {img_res['triggered_words']}")

    print("\n" + "="*60)
    print("🎉 Tests completed!")
    print("="*60)

if __name__ == "__main__":
    main()
