"""
Localhost web runner for the Interactive Calculator & Unit Converter.
Uses Python's standard library http.server module (no Flask/Django installation required).
"""

import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

from calculator import add, subtract, multiply, divide, modulus, power, clean_num
from converters import (
    UNIT_FACTORS,
    km_to_miles,
    miles_to_km,
    kg_to_lbs,
    lbs_to_kg,
    celsius_to_fahrenheit,
    fahrenheit_to_celsius,
)
from currency import (
    FOREX_RATES,
    FOREX_INFO,
    convert_fx,
    get_pair_rate,
)

PORT = 8000

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Calculator & Multi-Converter</title>
  <style>
    :root {
      --primary: #2563eb;
      --primary-hover: #1d4ed8;
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --text: #0f172a;
      --text-muted: #64748b;
      --border: #e2e8f0;
      --radius: 10px;
      --shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
    }
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: system-ui, -apple-system, sans-serif; }
    body { background: var(--bg); color: var(--text); padding: 30px 16px; display: flex; justify-content: center; }
    .wrap { width: 100%; max-width: 720px; }
    header { text-align: center; margin-bottom: 24px; }
    header h1 { font-size: 1.75rem; color: #1e293b; margin-bottom: 4px; }
    header p { color: var(--text-muted); font-size: 0.9rem; }
    .nav { display: flex; gap: 8px; background: #e2e8f0; padding: 6px; border-radius: var(--radius); margin-bottom: 20px; }
    .nav button { flex: 1; padding: 10px; border: none; background: transparent; border-radius: 6px; font-weight: 600; font-size: 0.9rem; color: var(--text-muted); cursor: pointer; }
    .nav button.active { background: var(--card-bg); color: var(--primary); box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    .card { display: none; background: var(--card-bg); padding: 24px; border-radius: var(--radius); box-shadow: var(--shadow); border: 1px solid var(--border); }
    .card.active { display: block; }
    .row { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-bottom: 14px; }
    .field { margin-bottom: 14px; }
    label { display: block; font-size: 0.85rem; font-weight: 600; color: #475569; margin-bottom: 5px; }
    input, select { width: 100%; padding: 10px 12px; border-radius: 6px; border: 1px solid var(--border); font-size: 0.95rem; }
    input:focus, select:focus { outline: none; border-color: var(--primary); }
    .btn { width: 100%; background: var(--primary); color: #fff; border: none; padding: 11px; border-radius: 6px; font-size: 0.95rem; font-weight: 600; cursor: pointer; }
    .btn:hover { background: var(--primary-hover); }
    .out { margin-top: 18px; padding: 14px; border-radius: 6px; background: #f1f5f9; border-left: 4px solid var(--primary); display: none; }
    .out.show { display: block; }
    .out.err { background: #fef2f2; border-left-color: #dc2626; color: #dc2626; }
    .out-main { font-size: 1.25rem; font-weight: 700; color: #0f172a; margin-bottom: 2px; }
    .out-sub { font-size: 0.82rem; color: var(--text-muted); }
    table { width: 100%; border-collapse: collapse; margin-top: 12px; font-size: 0.85rem; }
    th, td { padding: 8px 10px; text-align: left; border-bottom: 1px solid var(--border); }
    th { background: #f8fafc; font-weight: 600; color: #475569; }
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <h1>Interactive Calculator & Multi-Converter</h1>
      <p>Internship Project • Standard Library Python 3.10+ • Localhost:8000</p>
    </header>

    <div class="nav">
      <button class="active" onclick="showTab('calc')">Calculator</button>
      <button onclick="showTab('unit')">Unit Converter</button>
      <button onclick="showTab('curr')">Currency Converter</button>
    </div>

    <!-- Arithmetic Calculator -->
    <div id="tab-calc" class="card active">
      <div class="row">
        <div>
          <label for="n1">First Number</label>
          <input type="number" step="any" id="n1" value="24" />
        </div>
        <div>
          <label for="n2">Second Number</label>
          <input type="number" step="any" id="n2" value="6" />
        </div>
      </div>
      <div class="field">
        <label for="op">Operation</label>
        <select id="op">
          <option value="+">Addition (+)</option>
          <option value="-">Subtraction (-)</option>
          <option value="*">Multiplication (*)</option>
          <option value="/">Division (/)</option>
          <option value="%">Modulus (%)</option>
          <option value="^">Exponentiation (^)</option>
        </select>
      </div>
      <button class="btn" onclick="calc()">Calculate</button>

      <div id="calc-box" class="out">
        <div class="out-main" id="calc-main">--</div>
        <div class="out-sub" id="calc-sub"></div>
      </div>
    </div>

    <!-- Unit Converter -->
    <div id="tab-unit" class="card">
      <div class="field">
        <label for="u-type">Conversion Type</label>
        <select id="u-type" onchange="unitLabel()">
          <optgroup label="Length">
            <option value="km_to_miles">Kilometers to Miles (km → mi)</option>
            <option value="miles_to_km">Miles to Kilometers (mi → km)</option>
          </optgroup>
          <optgroup label="Weight">
            <option value="kg_to_lbs">Kilograms to Pounds (kg → lbs)</option>
            <option value="lbs_to_kg">Pounds to Kilograms (lbs → kg)</option>
          </optgroup>
          <optgroup label="Temperature">
            <option value="c_to_f">Celsius to Fahrenheit (°C → °F)</option>
            <option value="f_to_c">Fahrenheit to Celsius (°F → °C)</option>
          </optgroup>
        </select>
      </div>
      <div class="field">
        <label id="u-label" for="u-val">Value in Kilometers</label>
        <input type="number" step="any" id="u-val" value="10" />
      </div>
      <button class="btn" onclick="convertUnit()">Convert</button>

      <div id="u-box" class="out">
        <div class="out-main" id="u-main">--</div>
        <div class="out-sub" id="u-sub"></div>
      </div>
    </div>

    <!-- Currency Converter -->
    <div id="tab-curr" class="card">
      <div class="row">
        <div>
          <label for="c-from">From Currency</label>
          <select id="c-from"></select>
        </div>
        <div>
          <label for="c-to">To Currency</label>
          <select id="c-to"></select>
        </div>
      </div>
      <div class="field">
        <label for="c-amt">Amount</label>
        <input type="number" step="any" id="c-amt" value="100" />
      </div>
      <button class="btn" onclick="convertCurr()">Convert Currency</button>

      <div id="c-box" class="out">
        <div class="out-main" id="c-main">--</div>
        <div class="out-sub" id="c-sub"></div>
      </div>

      <div style="margin-top: 20px;">
        <label>Current Rates (Per 1 USD)</label>
        <table>
          <thead>
            <tr><th>Code</th><th>Symbol</th><th>Name</th><th>Rate</th></tr>
          </thead>
          <tbody id="rates-body"></tbody>
        </table>
      </div>
    </div>
  </div>

  <script>
    function showTab(id) {
      document.querySelectorAll('.nav button').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.card').forEach(c => c.classList.remove('active'));
      event.currentTarget.classList.add('active');
      document.getElementById('tab-' + id).classList.add('active');
    }

    async function calc() {
      const n1 = parseFloat(document.getElementById('n1').value);
      const n2 = parseFloat(document.getElementById('n2').value);
      const op = document.getElementById('op').value;
      const box = document.getElementById('calc-box');
      const main = document.getElementById('calc-main');
      const sub = document.getElementById('calc-sub');

      if (isNaN(n1) || isNaN(n2)) {
        box.className = 'out show err';
        main.textContent = 'Invalid Input';
        sub.textContent = 'Please enter valid numbers in both boxes.';
        return;
      }

      const res = await fetch('/api/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ num1: n1, num2: n2, operation: op })
      });
      const data = await res.json();
      if (data.ok) {
        box.className = 'out show';
        main.textContent = data.result_clean;
        sub.textContent = data.equation;
      } else {
        box.className = 'out show err';
        main.textContent = 'Error';
        sub.textContent = data.error;
      }
    }

    function unitLabel() {
      const t = document.getElementById('u-type').value;
      const lbl = document.getElementById('u-label');
      const m = {
        'km_to_miles': 'Value in Kilometers (km)',
        'miles_to_km': 'Value in Miles (mi)',
        'kg_to_lbs': 'Value in Kilograms (kg)',
        'lbs_to_kg': 'Value in Pounds (lbs)',
        'c_to_f': 'Value in Celsius (°C)',
        'f_to_c': 'Value in Fahrenheit (°F)'
      };
      lbl.textContent = m[t] || 'Enter Value';
    }

    async function convertUnit() {
      const type = document.getElementById('u-type').value;
      const val = parseFloat(document.getElementById('u-val').value);
      const box = document.getElementById('u-box');
      const main = document.getElementById('u-main');
      const sub = document.getElementById('u-sub');

      if (isNaN(val)) {
        box.className = 'out show err';
        main.textContent = 'Invalid Number';
        sub.textContent = 'Please type a valid numeric input.';
        return;
      }

      const res = await fetch('/api/unit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type, value: val })
      });
      const data = await res.json();
      if (data.ok) {
        box.className = 'out show';
        main.textContent = data.display;
        sub.textContent = 'Reference: ' + data.ref;
      } else {
        box.className = 'out show err';
        main.textContent = 'Conversion Error';
        sub.textContent = data.error;
      }
    }

    async function initForex() {
      const res = await fetch('/api/rates');
      const data = await res.json();
      const f = document.getElementById('c-from');
      const t = document.getElementById('c-to');
      const tbody = document.getElementById('rates-body');
      f.innerHTML = ''; t.innerHTML = ''; tbody.innerHTML = '';

      for (const [code, rate] of Object.entries(data.rates)) {
        const info = data.info[code] || [code, ''];
        f.add(new Option(`${code} - ${info[0]} (${info[1]})`, code));
        t.add(new Option(`${code} - ${info[0]} (${info[1]})`, code));
        tbody.innerHTML += `<tr><td><strong>${code}</strong></td><td>${info[1]}</td><td>${info[0]}</td><td>${rate.toFixed(2)}</td></tr>`;
      }
      f.value = 'USD';
      t.value = 'INR';
    }

    async function convertCurr() {
      const from = document.getElementById('c-from').value;
      const to = document.getElementById('c-to').value;
      const amt = parseFloat(document.getElementById('c-amt').value);
      const box = document.getElementById('c-box');
      const main = document.getElementById('c-main');
      const sub = document.getElementById('c-sub');

      if (isNaN(amt) || amt < 0) {
        box.className = 'out show err';
        main.textContent = 'Invalid Amount';
        sub.textContent = 'Please enter a non-negative number.';
        return;
      }

      const res = await fetch('/api/currency', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ from, to, amount: amt })
      });
      const data = await res.json();
      if (data.ok) {
        box.className = 'out show';
        main.textContent = data.result_str;
        sub.textContent = `1 ${from} = ${data.rate.toFixed(4)} ${to} (${data.source_str})`;
      } else {
        box.className = 'out show err';
        main.textContent = 'Forex Error';
        sub.textContent = data.error;
      }
    }

    initForex();
    unitLabel();
  </script>
</body>
</html>
"""


class AppServerHandler(BaseHTTPRequestHandler):
    """Handles GET and POST requests for the web UI."""

    def send_json_data(self, status: int, payload: dict) -> None:
        raw = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            raw = HTML_PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
        elif path == "/api/rates":
            self.send_json_data(200, {
                "rates": FOREX_RATES,
                "info": FOREX_INFO
            })
        else:
            self.send_error(404, "Page Not Found")

    def do_POST(self) -> None:
        path = urlparse(self.path).path

        try:
            length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(length) if length > 0 else b"{}"
            data = json.loads(raw_body.decode("utf-8"))
        except Exception as e:
            self.send_json_data(400, {"ok": False, "error": f"Bad request data: {e}"})
            return

        if path == "/api/calculate":
            try:
                n1 = float(data.get("num1", 0))
                n2 = float(data.get("num2", 0))
                op = str(data.get("operation", "+"))

                if op == "+":
                    ans = add(n1, n2)
                elif op == "-":
                    ans = subtract(n1, n2)
                elif op == "*":
                    ans = multiply(n1, n2)
                elif op == "/":
                    ans = divide(n1, n2)
                elif op == "%":
                    ans = modulus(n1, n2)
                elif op == "^":
                    ans = power(n1, n2)
                else:
                    self.send_json_data(400, {"ok": False, "error": "Unknown operation"})
                    return

                ans_clean = clean_num(ans)
                eq = f"{clean_num(n1)} {op} {clean_num(n2)} = {ans_clean}"
                self.send_json_data(200, {"ok": True, "result": ans, "result_clean": ans_clean, "equation": eq})
            except (ZeroDivisionError, ValueError, OverflowError) as err:
                self.send_json_data(200, {"ok": False, "error": str(err)})

        elif path == "/api/unit":
            try:
                kind = str(data.get("type", ""))
                val = float(data.get("value", 0))

                if kind == "km_to_miles":
                    out = km_to_miles(val)
                    disp = f"{val:,.3f} km = {out:,.3f} miles"
                    ref = f"1 km = {UNIT_FACTORS['km_to_miles']} mi"
                elif kind == "miles_to_km":
                    out = miles_to_km(val)
                    disp = f"{val:,.3f} miles = {out:,.3f} km"
                    ref = f"1 mi = {UNIT_FACTORS['miles_to_km']:.4f} km"
                elif kind == "kg_to_lbs":
                    out = kg_to_lbs(val)
                    disp = f"{val:,.3f} kg = {out:,.3f} lbs"
                    ref = f"1 kg = {UNIT_FACTORS['kg_to_lbs']} lbs"
                elif kind == "lbs_to_kg":
                    out = lbs_to_kg(val)
                    disp = f"{val:,.3f} lbs = {out:,.3f} kg"
                    ref = f"1 lb = {UNIT_FACTORS['lbs_to_kg']:.4f} kg"
                elif kind == "c_to_f":
                    out = celsius_to_fahrenheit(val)
                    disp = f"{val:,.2f} °C = {out:,.2f} °F"
                    ref = "F = C * 9/5 + 32"
                elif kind == "f_to_c":
                    out = fahrenheit_to_celsius(val)
                    disp = f"{val:,.2f} °F = {out:,.2f} °C"
                    ref = "C = (F - 32) * 5/9"
                else:
                    self.send_json_data(400, {"ok": False, "error": "Unknown unit type"})
                    return

                self.send_json_data(200, {"ok": True, "result": out, "display": disp, "ref": ref})
            except Exception as err:
                self.send_json_data(500, {"ok": False, "error": str(err)})

        elif path == "/api/currency":
            try:
                from_c = str(data.get("from", "USD"))
                to_c = str(data.get("to", "INR"))
                amt = float(data.get("amount", 0))

                converted = convert_fx(amt, from_c, to_c)
                rate = get_pair_rate(from_c, to_c)

                f_name, f_sym = FOREX_INFO.get(from_c, (from_c, ""))
                t_name, t_sym = FOREX_INFO.get(to_c, (to_c, ""))

                self.send_json_data(200, {
                    "ok": True,
                    "result": converted,
                    "rate": rate,
                    "source_str": f"{f_sym} {amt:,.2f} {from_c}",
                    "result_str": f"{t_sym} {converted:,.2f} {to_c}"
                })
            except (KeyError, ValueError) as err:
                self.send_json_data(400, {"ok": False, "error": str(err)})
            except Exception as err:
                self.send_json_data(500, {"ok": False, "error": str(err)})

        else:
            self.send_error(404, "Endpoint not found")

    def log_message(self, format, *args):
        # Keep console output quiet
        return


def main():
    server = HTTPServer(("127.0.0.1", PORT), AppServerHandler)
    print(f"Server is up at http://localhost:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        server.server_close()


if __name__ == "__main__":
    main()
